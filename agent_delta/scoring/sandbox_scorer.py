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
from agent_delta.scoring.diff import parse_diff
from agent_delta.scoring.objective import ObjectiveComponents, partial_objective_score
from agent_delta.scoring.testrunner import injection, parse


async def _exec(cmd: list[str], cwd: str, timeout: int = 300):
    return await sandbox().exec(cmd, cwd=cwd, timeout=timeout)


async def _run_injected(language: str, label: str, files: dict[str, str], workdir: str) -> dict[str, int]:
    """Inject public/hidden test files into the sandbox and run them."""
    if not files:
        return {"passed": 0, "failed": 0, "error": 0, "skipped": 0, "total": 0}
    writes, cmd = injection(language, label, files, workdir)
    for path, contents in writes:
        await sandbox().write_file(path, contents)
    result = await _exec(cmd, cwd=workdir)
    return parse(language, result.stdout + result.stderr)


async def _score_test_writing(task, workdir: str):
    """Mutation scoring (SPEC 13 test quality): the agent's tests should pass on
    the correct code and fail on each planted mutant.

    Returns (public, hidden, regression_ok) where public encodes test validity and
    hidden encodes the mutation kill rate.
    """
    baseline_cmd = task.baseline_cmds[0] if task.baseline_cmds else "true"
    # Tests must pass on the correct code (and not break the existing suite).
    res = await _exec(["bash", "-c", baseline_cmd], workdir)
    tests_valid = res.returncode == 0

    mutants = task.load_mutants()
    killed = 0
    for _name, files in mutants:
        for rel_path, contents in files.items():
            await sandbox().write_file(f"{workdir}/{rel_path}", contents)
        res = await _exec(["bash", "-c", baseline_cmd], workdir)
        if res.returncode != 0:
            killed += 1
        # Restore the correct sources (the agent only edits test files).
        for rel_path in files:
            await _exec(["git", "-C", workdir, "checkout", "--", rel_path], workdir)

    total = len(mutants)
    public = {"passed": 1 if tests_valid else 0, "failed": 0 if tests_valid else 1,
              "error": 0, "skipped": 0, "total": 1}
    hidden = {"passed": killed, "failed": total - killed, "error": 0,
              "skipped": 0, "total": total}
    return public, hidden, tests_valid


def _added_lines(diff_text: str) -> str:
    """The added lines of a unified diff (for forbidden-pattern scanning)."""
    return "\n".join(ln[1:] for ln in (diff_text or "").splitlines()
                     if ln.startswith("+") and not ln.startswith("+++"))


def _compute_scope_control(
    modified_files: list[str], forbidden: list[str], max_files: int | None,
    *, lines_changed: int | None = None, max_lines: int | None = None,
    diff_text: str = "", forbidden_patterns: list[dict] | None = None,
) -> tuple[float, list[str]]:
    """Return (scope_control_score in [0,1], list of violations).

    Hard violations (forbidden path or forbidden shortcut pattern) zero the score;
    over-budget edits (too many files/lines) halve it (HARD-TASKS-SPEC 8, 11.4).
    """
    hard: list[str] = []
    soft: list[str] = []
    for f in modified_files:
        for fp in forbidden:
            if f == fp or f.startswith(fp.rstrip("/") + "/"):
                hard.append(f"forbidden_path_modified:{f}")

    added = _added_lines(diff_text)
    for spec in forbidden_patterns or []:
        pattern = spec.get("pattern") if isinstance(spec, dict) else spec
        label = spec.get("label", "forbidden_pattern") if isinstance(spec, dict) else "forbidden_pattern"
        if pattern and re.search(pattern, added):
            hard.append(f"forbidden_pattern:{label}")

    if max_files is not None and len(modified_files) > max_files:
        soft.append(f"too_many_files:{len(modified_files)}>{max_files}")
    if max_lines is not None and lines_changed is not None and lines_changed > max_lines:
        soft.append(f"too_many_lines:{lines_changed}>{max_lines}")

    violations = hard + soft
    if hard:
        return 0.0, violations
    if soft:
        return 0.5, violations
    return 1.0, violations


@scorer(metrics=[accuracy(), stderr()])
def agentdelta_scorer():
    """Score a run: returns verified_success as value, full detail in metadata."""

    async def score(state: TaskState, target: Target) -> Score:
        meta: dict[str, Any] = state.metadata or {}
        task = load_task(meta["task_id"])
        workdir = meta.get("workdir", "/repo")
        language = meta.get("language", "python")

        # final diff + modified file list (numstat for line counts)
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

        if task.task_type == "test_writing":
            # The agent wrote tests; score by mutation (do the tests catch bugs?).
            public, hidden, regression_ok = await _score_test_writing(task, workdir)
        else:
            # regression: baseline suite must still pass
            regression_ok = True
            for cmd in task.baseline_cmds:
                res = await _exec(["bash", "-c", cmd], workdir)
                if res.returncode != 0:
                    regression_ok = False
            # public + hidden tests (injected, not in the repo)
            public_files = {p.name: p.read_text() for p in task.public_test_files}
            hidden_files = {p.name: p.read_text() for p in task.hidden_test_files}
            public = await _run_injected(language, "public", public_files, workdir)
            hidden = await _run_injected(language, "hidden", hidden_files, workdir)

        regression_avoidance = 1.0 if regression_ok else 0.0
        public_ok = public["total"] > 0 and public["failed"] == 0 and public["error"] == 0
        hidden_score = (hidden["passed"] / hidden["total"]) if hidden["total"] else 0.0

        # scope control + forbidden-shortcut detection (HARD-TASKS-SPEC 8)
        scope_score, violations = _compute_scope_control(
            modified_files, task.forbidden_paths, task.max_files_modified,
            lines_changed=lines_added + lines_removed, max_lines=task.max_lines_changed,
            diff_text=diff_res.stdout, forbidden_patterns=task.forbidden_patterns,
        )

        # verified success: public passes + no regression + in scope. For
        # test_writing, also require the mutation kill rate to meet the threshold.
        mutation_ok = True
        if task.task_type == "test_writing":
            threshold = task.test_writing.get("mutation_threshold", 1.0)
            mutation_ok = hidden_score >= threshold
        verified = public_ok and regression_ok and not violations and mutation_ok
        components = ObjectiveComponents(
            verified_success=1.0 if verified else 0.0,
            hidden_test_score=hidden_score,
            regression_avoidance=regression_avoidance,
            scope_control=scope_score,
        )
        partial = partial_objective_score(components)

        # usage from Inspect's tracked state
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
                "hardness_level": task.hardness_level,
                "known_llm_failure_mode": task.known_llm_failure_mode,
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
                "diff_metrics": parse_diff(diff_res.stdout, language),
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
