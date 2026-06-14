"""Inspect scorer that grades a finished agent run inside the sandbox.

It runs the baseline (regression), public, and hidden test suites in the
container, captures the final git diff, computes scope control, and assembles
the absolute objective components. Set-relative cost/time efficiency are added
later during aggregation.
"""

from __future__ import annotations

import re
from typing import Any

from inspect_ai.scorer import Score, Target, accuracy, scorer, stderr
from inspect_ai.solver import TaskState
from inspect_ai.util import sandbox

from agent_delta.registry import load_task
from agent_delta.scoring.objective import ObjectiveComponents, partial_objective_score

_SUMMARY_RE = re.compile(r"(\d+) (passed|failed|error|errors|skipped)")


def parse_pytest_summary(output: str) -> dict[str, int]:
    """Parse pytest's summary line into counts. Robust to ordering/wording."""
    counts = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    for n, kind in _SUMMARY_RE.findall(output):
        key = "error" if kind.startswith("error") else kind
        counts[key] += int(n)
    counts["total"] = counts["passed"] + counts["failed"] + counts["error"]
    return counts


async def _exec(cmd: list[str], cwd: str, timeout: int = 300):
    return await sandbox().exec(cmd, cwd=cwd, timeout=timeout)


async def _run_pytest_files(files: dict[str, str], workdir: str) -> dict[str, int]:
    """Write test files into the sandbox (outside the repo) and run them.

    files: {filename: contents}. Tests import the installed package, so they can
    live in /tmp and need not be inside the repo working tree.
    """
    if not files:
        return {"passed": 0, "failed": 0, "error": 0, "skipped": 0, "total": 0}
    paths = []
    for name, contents in files.items():
        path = f"/tmp/agentdelta_{name}"
        await sandbox().write_file(path, contents)
        paths.append(path)
    result = await _exec(["python", "-m", "pytest", "-q", "--tb=line", *paths], cwd=workdir)
    return parse_pytest_summary(result.stdout + result.stderr)


def _compute_scope_control(
    modified_files: list[str], forbidden: list[str], max_files: int | None
) -> tuple[float, list[str]]:
    """Return (scope_control_score in [0,1], list of violations)."""
    violations: list[str] = []
    score = 1.0
    for f in modified_files:
        for fp in forbidden:
            # forbidden entry may be a file or a directory prefix
            if f == fp or f.startswith(fp.rstrip("/") + "/"):
                violations.append(f"forbidden_path_modified:{f}")
    if violations:
        return 0.0, violations
    if max_files is not None and len(modified_files) > max_files:
        violations.append(f"too_many_files:{len(modified_files)}>{max_files}")
        score = 0.5
    return score, violations


@scorer(metrics=[accuracy(), stderr()])
def agentdelta_scorer():
    """Score a run: returns verified_success as value, full detail in metadata."""

    async def score(state: TaskState, target: Target) -> Score:
        meta: dict[str, Any] = state.metadata or {}
        task = load_task(meta["task_id"])
        workdir = meta.get("workdir", "/repo")

        # --- final diff + modified file list (numstat for line counts) ---
        diff_res = await _exec(["git", "-C", workdir, "diff", "HEAD"], workdir)
        names_res = await _exec(
            ["git", "-C", workdir, "diff", "--name-only", "HEAD"], workdir
        )
        numstat_res = await _exec(
            ["git", "-C", workdir, "diff", "--numstat", "HEAD"], workdir
        )
        modified_files = [f for f in names_res.stdout.splitlines() if f.strip()]
        lines_added = lines_removed = 0
        for row in numstat_res.stdout.splitlines():
            parts = row.split("\t")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                lines_added += int(parts[0])
                lines_removed += int(parts[1])

        # --- regression: baseline suite must still pass ---
        regression_ok = True
        for cmd in task.baseline_cmds:
            res = await _exec(["bash", "-lc", cmd], workdir)
            if res.returncode != 0:
                regression_ok = False
        regression_avoidance = 1.0 if regression_ok else 0.0

        # --- public + hidden tests (injected, not in the repo) ---
        public_files = {p.name: p.read_text() for p in task.public_test_files}
        hidden_files = {p.name: p.read_text() for p in task.hidden_test_files}
        public = await _run_pytest_files(public_files, workdir)
        hidden = await _run_pytest_files(hidden_files, workdir)

        public_ok = public["total"] > 0 and public["failed"] == 0 and public["error"] == 0
        hidden_score = (hidden["passed"] / hidden["total"]) if hidden["total"] else 0.0

        # --- scope control ---
        scope_score, violations = _compute_scope_control(
            modified_files, task.forbidden_paths, task.max_files_modified
        )

        # --- verified success: public passes + no regression + in scope ---
        verified = public_ok and regression_ok and not violations
        components = ObjectiveComponents(
            verified_success=1.0 if verified else 0.0,
            hidden_test_score=hidden_score,
            regression_avoidance=regression_avoidance,
            scope_control=scope_score,
        )
        partial = partial_objective_score(components)

        # --- usage from Inspect's tracked state ---
        usage = _extract_usage(state)

        return Score(
            value=1.0 if verified else 0.0,
            answer="verified" if verified else "not_verified",
            explanation=(
                f"public {public['passed']}/{public['total']} | "
                f"hidden {hidden['passed']}/{hidden['total']} | "
                f"regression={'ok' if regression_ok else 'FAIL'} | "
                f"scope={scope_score} | files={len(modified_files)}"
            ),
            metadata={
                "task_id": task.id,
                "task_category": task.category,
                "components": components.as_dict(),
                "partial_objective_score": partial,
                "public_tests": public,
                "hidden_tests": hidden,
                "regression_ok": regression_ok,
                "scope_violations": violations,
                "modified_files": modified_files,
                "lines_added": lines_added,
                "lines_removed": lines_removed,
                "diff": diff_res.stdout,
                "usage": usage,
            },
        )

    return score


def _extract_usage(state: TaskState) -> dict[str, Any]:
    """Best-effort extraction of token usage from the Inspect TaskState."""
    out: dict[str, Any] = {}
    try:
        tu = state.token_usage
        if isinstance(tu, int):
            out["total_tokens"] = tu
    except Exception:
        pass
    try:
        # state.model.api / usage may carry per-model breakdown; capture cost too
        out["cost_usage"] = getattr(state, "cost_usage", None)
    except Exception:
        pass
    return out
