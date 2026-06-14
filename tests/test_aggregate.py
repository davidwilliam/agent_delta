"""Validate aggregation + reporting with synthetic run records (no Docker, no API)."""

import json

from agent_delta.reporting.aggregate import build_report
from agent_delta.reporting.markdown import render


def _record(model, task, epoch, *, success, cost, time_s, tokens, tools=10, tests=2):
    """Build a SPEC-16-shaped run record dict."""
    return {
        "run_id": f"{model}_{task}_rep{epoch}",
        "benchmark_version": "agentdelta-v0.1",
        "task_id": task,
        "task_category": "small_bug_fix",
        "repo": "python_package",
        "agent": "claude_code",
        "agent_version": "test",
        "provider": "anthropic",
        "model_id": model,
        "mode": "default",
        "epoch": epoch,
        "execution": {"wall_clock_seconds": time_s, "invalid": False, "error": None},
        "usage": {
            "input_tokens": int(tokens * 0.9),
            "output_tokens": int(tokens * 0.1),
            "total_tokens": tokens,
            "estimated_cost_usd": cost,
        },
        "agent_behavior": {
            "files_modified": 2, "lines_added": 20, "lines_removed": 5,
            "tool_calls": tools, "shell_commands": tools // 2, "test_runs": tests,
            "files_read": tools // 2, "file_edits": 4, "api_calls": tools // 2,
            "retry_count": 0,
        },
        "scoring": {
            "verified_success": success,
            "hidden_test_score": 1.0 if success else 0.4,
            "regression_avoidance": 1.0,
            "scope_control": 1.0,
            "partial_objective_score": 100.0 if success else 40.0,
        },
    }


def _write_suite(tmp_path):
    """Two models, 5 tasks x 10 reps. opus-4-8 strictly dominates 4-6 and costs 4x."""
    tasks = [f"task_{i:03d}" for i in range(1, 6)]
    root = tmp_path / "raw" / "suite"
    n = 0
    for ti, task in enumerate(tasks):
        for rep in range(10):
            # opus-4-6: succeeds unless (task index 0 and rep < 8) -> 42/50 successes pattern
            a_success = not (ti == 0)  # fails all reps of task_001 -> 40/50 = 80%
            # opus-4-8: also succeeds on task_001 reps -> strictly dominates -> 50/50 = 100%
            b_success = True
            for model, succ, cost, time_s, tok, tools, tests in [
                ("claude-opus-4-6", a_success, 0.40, 300, 200_000, 12, 2),
                ("claude-opus-4-8", b_success, 1.60, 900, 1_000_000, 48, 8),
            ]:
                rec = _record(model, task, rep, success=succ, cost=cost, time_s=time_s,
                              tokens=tok, tools=tools, tests=tests)
                d = root / rec["run_id"]
                d.mkdir(parents=True)
                (d / "run.json").write_text(json.dumps(rec))
                n += 1
    return root


def test_build_report_and_render(tmp_path):
    root = _write_suite(tmp_path)
    report = build_report(root, suite="synthetic")

    assert report["n_runs"] == 100
    assert report["n_tasks"] == 5
    assert set(report["models"]) == {"claude-opus-4-6", "claude-opus-4-8"}

    mode = report["per_mode"]["default"]
    # Level 1: opus-4-8 has higher success so it should rank first by objective score.
    assert mode["level1"]["ranking"][0] == "claude-opus-4-8"
    assert mode["baseline"] == "claude-opus-4-6"

    m8 = mode["models"]["claude-opus-4-8"]
    m6 = mode["models"]["claude-opus-4-6"]
    assert m8["success_rate"] == 1.0
    assert m6["success_rate"] == 0.8
    # opus-4-6 is cheaper/faster, so it should be the cost/time efficiency reference (1.0).
    assert m6["cost_efficiency"] == 1.0
    assert m6["time_efficiency"] == 1.0
    assert 0 < m8["cost_efficiency"] < 1.0

    # Level 1 flags the opus-4-8 gain as material (20pp, McNemar p<0.05).
    imp = {i["model_b"]: i for i in mode["level1"]["improvements"]}["claude-opus-4-8"]
    assert imp["material"] is True
    assert imp["paired"]["b_only"] == 10 and imp["paired"]["a_only"] == 0

    # Level 2 narrows down: only the material gain is assessed.
    assessed = {a["model_b"]: a for a in mode["level2"]["assessments"]}
    assert "claude-opus-4-8" in assessed
    a8 = assessed["claude-opus-4-8"]
    assert a8["ratios"]["cost_amplification"] == 4.0
    assert a8["ratios"]["token_amplification"] == 5.0
    # Transcript-derived ratios are now real (48 vs 12 tools, 8 vs 2 test runs).
    assert a8["ratios"]["tool_amplification"] == 4.0
    assert a8["ratios"]["test_amplification"] == 4.0
    assert a8["ratios"]["work_index_amplification"] is not None
    # The Work Index now uses the full set of captured signals.
    assert "tool_calls" in mode["level2"]["work_index_components"]
    assert "test_runs" in mode["level2"]["work_index_components"]
    assert "Amplification" in a8["classification"]["category"]

    md = render(report)
    assert "Level 1: Primary Assessment" in md
    assert "Level 2: Agentic Amplification Assessment" in md
    assert "Primary ranking" in md
    assert "claude-opus-4-8" in md
