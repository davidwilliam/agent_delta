"""Tests for failure taxonomy and validity assessment."""

from agent_delta.scoring.failure import classify_failure
from agent_delta.scoring.validity import assess_validity, normalize_model


def _classify(**kw):
    base = dict(
        verified=False, public=None, hidden=None, regression_ok=True,
        scope_violations=None, modified_files=["src/x.py"], behavior=None,
        execution=None, language="python",
    )
    base.update(kw)
    return classify_failure(**base)


def test_verified_has_no_labels():
    assert _classify(verified=True) == []


def test_public_and_hidden_failures():
    labels = _classify(
        public={"passed": 1, "failed": 2, "error": 0, "total": 3},
        hidden={"passed": 0, "failed": 3, "error": 0, "total": 3},
    )
    assert "public_tests_failed" in labels
    assert "hidden_tests_failed" in labels


def test_regression_and_scope():
    labels = _classify(
        regression_ok=False,
        scope_violations=["forbidden_path_modified:go.mod", "too_many_files:9>4"],
    )
    assert "regression_introduced" in labels
    assert "forbidden_file_modified" in labels
    assert "overbroad_edit" in labels


def test_incomplete_when_no_diff():
    assert "incomplete_implementation" in _classify(modified_files=[])


def test_did_not_run_tests():
    assert "did_not_run_tests" in _classify(behavior={"test_runs": 0})


def test_go_build_failure():
    labels = _classify(
        language="go",
        public={"passed": 0, "failed": 0, "error": 1, "total": 1},
    )
    assert "build_failed" in labels


def test_hardcoded_suspected():
    labels = _classify(
        public={"passed": 3, "failed": 0, "error": 0, "total": 3},
        hidden={"passed": 1, "failed": 4, "error": 0, "total": 5},
    )
    assert "hardcoded_solution" in labels


def test_modified_baseline_test():
    labels = _classify(modified_files=["tests/test_stats.py"])
    assert "test_removed_or_weakened" in labels


def test_wrong_behavior_fallback_label():
    # A non-verified run with no specific signal still gets a label.
    assert _classify() == ["wrong_behavior"]


def test_validity_baseline_broken():
    invalid, reason = assess_validity(
        requested_model="claude-opus-4-8", served_models=set(),
        sample_error=None, baseline_pre_ok=False)
    assert invalid and reason == "baseline_failed_pre_run"


def test_validity_fallback_detected():
    invalid, reason = assess_validity(
        requested_model="claude-opus-4-8",
        served_models={"anthropic/claude-opus-4-7"},
        sample_error=None, baseline_pre_ok=True)
    assert invalid and reason.startswith("model_fallback")


def test_validity_match_is_valid():
    invalid, reason = assess_validity(
        requested_model="claude-opus-4-8",
        served_models={"anthropic/claude-opus-4-8"},
        sample_error=None, baseline_pre_ok=True)
    assert not invalid and reason is None


def test_validity_empty_served_skips_fallback():
    # Dry-run: no served models -> fallback detection disabled.
    invalid, _ = assess_validity(
        requested_model="model", served_models=set(),
        sample_error=None, baseline_pre_ok=True)
    assert not invalid


def test_validity_crash():
    invalid, reason = assess_validity(
        requested_model="m", served_models={"m"},
        sample_error="boom", baseline_pre_ok=True)
    assert invalid and reason.startswith("agent_crash")


def test_validity_categorizes_provider_errors():
    cases = {
        "Your credit balance is too low": "provider_error_billing",
        "Error code: 429 rate_limit_error": "rate_limited",
        "overloaded_error 529": "provider_overloaded",
        "authentication_error invalid x-api-key": "provider_auth_error",
        "Model proxy process exited unexpectedly": "model_proxy_error",
    }
    for err, expected in cases.items():
        _, reason = assess_validity(requested_model="m", served_models={"m"},
                                    sample_error=err, baseline_pre_ok=True)
        assert reason.startswith(expected), (err, reason)


def test_normalize_model():
    assert normalize_model("anthropic/claude-opus-4-8") == "claude-opus-4-8"


def test_aggregate_surfaces_failures_and_invalid(tmp_path):
    """build_report should report per-model failure labels and invalid runs."""
    import json
    from agent_delta.reporting.aggregate import build_report

    root = tmp_path / "raw" / "s"

    def rec(rid, model, verified, labels, invalid, reason):
        return {
            "run_id": rid, "benchmark_version": "v", "task_id": "task_001",
            "agent": "claude_code", "model_id": model, "mode": "default", "epoch": 0,
            "execution": {"wall_clock_seconds": 100, "invalid": invalid,
                          "invalid_reason": reason, "timeout": False},
            "usage": {"total_tokens": 1000, "estimated_cost_usd": 0.1},
            "agent_behavior": {"files_modified": 1},
            "failure_labels": labels,
            "scoring": {"verified_success": verified, "hidden_test_score": 1.0 if verified else 0.0,
                        "regression_avoidance": 1.0, "scope_control": 1.0,
                        "partial_objective_score": 100.0 if verified else 40.0},
        }

    records = [
        rec("r1", "claude-opus-4-8", True, [], False, None),
        rec("r2", "claude-opus-4-8", False, ["public_tests_failed", "hidden_tests_failed"], False, None),
        rec("r3", "claude-opus-4-8", False, ["regression_introduced"], False, None),
        rec("r4", "claude-opus-4-8", False, [], True, "model_fallback: served opus-4-7"),
    ]
    for r in records:
        d = root / r["run_id"]
        d.mkdir(parents=True)
        (d / "run.json").write_text(json.dumps(r))

    report = build_report(root, suite="s")
    assert report["n_invalid"] == 1
    assert report["invalid_runs"][0]["reason"].startswith("model_fallback")

    m = report["per_mode"]["default"]["models"]["claude-opus-4-8"]
    # The invalid run is excluded from the 3 valid runs.
    assert m["n_runs"] == 3 and m["n_invalid"] == 1
    assert m["failure_labels"]["public_tests_failed"] == 1
    assert m["failure_labels"]["regression_introduced"] == 1
    assert m["invalid_by_reason"]["model_fallback"] == 1
