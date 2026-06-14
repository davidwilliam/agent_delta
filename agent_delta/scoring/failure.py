"""Failure taxonomy (SPEC section 23).

Assigns one or more failure labels to a valid-but-failed run from the observable
scoring and behavior signals, so the report can show failure frequencies per
model. Invalid runs (infrastructure, fallback, baseline-broken) are handled
separately by `validity`, not here.

Some labels are derivable from hard signals (test results, scope, diff); a few
are heuristics flagged as "suspected" in the docs (hardcoded_solution,
looping_or_thrashing). Labels that need signals we do not yet capture (lint,
typecheck, refusal) stay in the canonical list for manual use but are not
auto-assigned.
"""

from __future__ import annotations

# Canonical taxonomy (SPEC section 23).
FAILURE_LABELS = [
    "wrong_behavior", "incomplete_implementation", "public_tests_failed",
    "hidden_tests_failed", "regression_introduced", "build_failed", "lint_failed",
    "typecheck_failed", "timeout", "agent_crash", "provider_error", "rate_limited",
    "model_refusal", "overbroad_edit", "forbidden_file_modified",
    "test_removed_or_weakened", "hardcoded_solution", "unnecessary_rewrite",
    "dependency_breakage", "security_regression", "hallucinated_api",
    "did_not_run_tests", "looping_or_thrashing",
]


def _modified_a_baseline_test(modified_files: list[str], language: str) -> bool:
    for f in modified_files or []:
        if language == "go" and f.endswith("_test.go"):
            return True
        if language == "python" and (f.startswith("tests/") or "/tests/" in f) and f.endswith(".py"):
            return True
    return False


def classify_failure(
    *,
    verified: bool,
    public: dict | None,
    hidden: dict | None,
    regression_ok: bool | None,
    scope_violations: list[str] | None,
    modified_files: list[str] | None,
    behavior: dict | None,
    execution: dict | None,
    language: str = "python",
) -> list[str]:
    """Return the sorted failure labels for a run. Empty for a verified success."""
    if verified:
        return []

    labels: set[str] = set()
    public = public or {}
    hidden = hidden or {}
    behavior = behavior or {}
    execution = execution or {}

    if execution.get("timeout"):
        labels.add("timeout")

    pub_fail = public.get("failed", 0) + public.get("error", 0)
    hid_fail = hidden.get("failed", 0) + hidden.get("error", 0)
    if pub_fail > 0:
        labels.add("public_tests_failed")
    if hid_fail > 0:
        labels.add("hidden_tests_failed")
    if language == "go" and (public.get("error", 0) or hidden.get("error", 0)):
        labels.add("build_failed")
    if regression_ok is False:
        labels.add("regression_introduced")

    for v in scope_violations or []:
        if v.startswith("forbidden_path_modified"):
            labels.add("forbidden_file_modified")
        if v.startswith("too_many_files"):
            labels.add("overbroad_edit")

    if not modified_files:
        labels.add("incomplete_implementation")
    elif _modified_a_baseline_test(modified_files, language):
        labels.add("test_removed_or_weakened")

    test_runs = behavior.get("test_runs")
    if test_runs == 0:
        labels.add("did_not_run_tests")
    if (behavior.get("failed_shell_commands") or 0) >= 5:
        labels.add("looping_or_thrashing")

    # Suspected hardcoding: public criteria pass but hidden generalization fails.
    public_ok = public.get("total", 0) > 0 and pub_fail == 0
    if public_ok and hidden.get("total", 0) > 0 and (hidden["passed"] / hidden["total"]) < 0.5:
        labels.add("hardcoded_solution")

    if not labels:
        labels.add("wrong_behavior")
    return sorted(labels)
