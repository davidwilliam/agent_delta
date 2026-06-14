"""Build SPEC section 16 run records from an Inspect EvalLog.

One JSON file per (sample, epoch) is written under
results/raw/<suite>/<run_id>/run.json, with the final diff saved alongside.
Set-relative scores (cost/time efficiency, full objective) are filled in later
during aggregation; per-run records carry the absolute components only.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from agent_delta import BENCHMARK_VERSION, config
from agent_delta.scoring.behavior import extract_agent_behavior
from agent_delta.scoring.cost import estimate_cost_usd
from agent_delta.scoring.failure import classify_failure
from agent_delta.scoring.validity import assess_validity

_SCORER_KEY = "agentdelta_scorer"
_SLUG = re.compile(r"[^a-zA-Z0-9]+")


def _slug(s: str) -> str:
    return _SLUG.sub("-", s).strip("-")


def _ts(dt: Any) -> str:
    if dt is None:
        return "unknown"
    return _slug(str(dt))


def _model_usage(sample) -> dict[str, Any]:
    """Flatten the first model's usage from an EvalSample."""
    usage = sample.model_usage or {}
    for _model, u in usage.items():
        d = u.model_dump() if hasattr(u, "model_dump") else dict(u)
        return d
    return {}


def build_run_record(
    log,
    sample,
    *,
    suite: str,
    agent: str,
    agent_version: str | None,
    mode: str = "default",
    epoch: int | None = None,
) -> dict[str, Any]:
    spec = log.eval
    model_id = (spec.model or "").split("/")[-1]
    # Effort lives on the task/plan config (what the model actually ran with),
    # not the eval-level config; fall back to the eval config if absent.
    plan_cfg = getattr(getattr(log, "plan", None), "config", None)
    reasoning_effort = getattr(plan_cfg, "reasoning_effort", None) or getattr(
        spec.model_generate_config, "reasoning_effort", None)
    mode = (sample.metadata or {}).get("mode", mode)
    epoch = sample.epoch if epoch is None else epoch
    score = (sample.scores or {}).get(_SCORER_KEY)
    smeta: dict[str, Any] = (score.metadata if score else {}) or {}
    components = smeta.get("components", {})

    usage = _model_usage(sample)
    cost = usage.get("total_cost") or estimate_cost_usd(
        model_id,
        input_tokens=usage.get("input_tokens", 0) or 0,
        output_tokens=usage.get("output_tokens", 0) or 0,
        cache_write_tokens=usage.get("input_tokens_cache_write", 0) or 0,
        cache_read_tokens=usage.get("input_tokens_cache_read", 0) or 0,
    )

    run_id = "_".join(
        [_ts(sample.started_at), f"task-{sample.id}", _slug(model_id), f"rep-{epoch:02d}"]
    )

    # Validity (SPEC 11.4 / 5.5): served-model fallback, broken baseline, crash.
    served = set((sample.model_usage or {}).keys())
    store = sample.store or {}
    baseline_pre_ok = store.get("baseline_pre_ok") if hasattr(store, "get") else None
    invalid, invalid_reason = assess_validity(
        requested_model=model_id,
        served_models=served,
        sample_error=str(sample.error) if sample.error else None,
        baseline_pre_ok=baseline_pre_ok,
    )

    verified = bool(components.get("verified_success"))
    timed_out = bool(getattr(sample, "limit", None) == "time")
    behavior = extract_agent_behavior(sample)
    # Failure taxonomy (SPEC 23): only for valid, non-successful runs.
    failure_labels = [] if invalid else classify_failure(
        verified=verified,
        public=smeta.get("public_tests"),
        hidden=smeta.get("hidden_tests"),
        regression_ok=smeta.get("regression_ok"),
        scope_violations=smeta.get("scope_violations"),
        modified_files=smeta.get("modified_files"),
        behavior=behavior,
        execution={"timeout": timed_out},
        language=(sample.metadata or {}).get("language", "python"),
    )

    return {
        "run_id": run_id,
        "benchmark_version": BENCHMARK_VERSION,
        "task_id": smeta.get("task_id", sample.id),
        "task_category": smeta.get("task_category"),
        "repo": (sample.metadata or {}).get("repo"),
        "agent": agent,
        "agent_version": agent_version,
        "provider": "anthropic",
        "model_id": model_id,
        "model_config": {"reasoning_effort": reasoning_effort},
        "mode": mode,
        "scaffolded": bool((sample.metadata or {}).get("scaffolded", False)),
        "epoch": epoch,
        "execution": {
            "started_at": str(sample.started_at) if sample.started_at else None,
            "completed_at": str(sample.completed_at) if sample.completed_at else None,
            "wall_clock_seconds": sample.total_time,
            "working_seconds": sample.working_time,
            "timeout": timed_out,
            "error": str(sample.error) if sample.error else None,
            "baseline_pre_ok": baseline_pre_ok,
            "invalid": invalid,
            "invalid_reason": invalid_reason,
        },
        "failure_labels": failure_labels,
        "usage": {
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "cache_read_tokens": usage.get("input_tokens_cache_read"),
            "cache_write_tokens": usage.get("input_tokens_cache_write"),
            "reasoning_tokens": usage.get("reasoning_tokens"),
            "estimated_cost_usd": cost,
        },
        "agent_behavior": {
            # Diff-derived (what changed on disk).
            "files_modified": len(smeta.get("modified_files", [])),
            "lines_added": smeta.get("lines_added"),
            "lines_removed": smeta.get("lines_removed"),
            "modified_files": smeta.get("modified_files", []),
            # Transcript-derived (how much work the agent did).
            **behavior,
        },
        "diff_metrics": smeta.get("diff_metrics"),
        "scoring": {
            "verified_success": bool(components.get("verified_success")),
            "hidden_test_score": components.get("hidden_test_score"),
            "regression_avoidance": components.get("regression_avoidance"),
            "scope_control": components.get("scope_control"),
            "public_tests": smeta.get("public_tests"),
            "hidden_tests": smeta.get("hidden_tests"),
            "scope_violations": smeta.get("scope_violations", []),
            # Authoritative objective/full scores are computed at aggregation.
            "partial_objective_score": smeta.get("partial_objective_score"),
        },
    }


def write_run_records(
    logs,
    *,
    suite: str,
    agent: str = "claude_code",
    agent_version: str | None = None,
    mode: str = "default",
    epoch: int | None = None,
    out_root: Path | None = None,
) -> list[Path]:
    """Write one run.json (+ final.diff) per sample/epoch. Returns the paths.

    `mode` is a fallback; each record prefers the mode recorded in sample metadata.
    `epoch` overrides the sample epoch so a matrix can label repetitions distinctly.
    """
    out_root = out_root or (config.RAW_RESULTS_DIR / suite)
    out_root.mkdir(parents=True, exist_ok=True)
    if not isinstance(logs, list):
        logs = [logs]

    written: list[Path] = []
    for log in logs:
        for sample in log.samples or []:
            record = build_run_record(
                log, sample, suite=suite, agent=agent, agent_version=agent_version,
                mode=mode, epoch=epoch,
            )
            run_dir = out_root / record["run_id"]
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "run.json").write_text(json.dumps(record, indent=2, default=str))

            score = (sample.scores or {}).get(_SCORER_KEY)
            diff = (score.metadata or {}).get("diff", "") if score else ""
            (run_dir / "final.diff").write_text(diff or "")
            written.append(run_dir / "run.json")
    return written
