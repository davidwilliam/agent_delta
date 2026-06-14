"""Author-time task validation.

For a task, spin up one sandbox container from the fixture image and verify:

  * BEFORE (clean base): the public/hidden tests FAIL — proving the task is
    non-trivial (the tests actually detect the missing/buggy behavior).
  * AFTER (reference solution applied): the baseline, public, and hidden tests
    all PASS — proving the task is solvable and the tests/reference agree.

This is the objective quality gate for task authoring (SPEC docs/task_authoring).
It uses docker run/exec/cp directly (no model, no Inspect) so it is fast and free.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from agent_delta.registry import Task, load_fixture, load_task
from agent_delta.scoring.sandbox_scorer import parse_pytest_summary


@dataclass
class Phase:
    passed: int
    failed: int
    error: int
    total: int

    @property
    def all_passed(self) -> bool:
        return self.total > 0 and self.failed == 0 and self.error == 0

    @property
    def any_failed(self) -> bool:
        return self.failed > 0 or self.error > 0


@dataclass
class TaskCheck:
    task_id: str
    base_public: Phase
    base_hidden: Phase
    after_baseline_ok: bool
    after_public: Phase
    after_hidden: Phase

    @property
    def non_trivial(self) -> bool:
        return self.base_public.any_failed or self.base_hidden.any_failed

    @property
    def solvable(self) -> bool:
        return self.after_baseline_ok and self.after_public.all_passed and self.after_hidden.all_passed

    @property
    def ok(self) -> bool:
        return self.non_trivial and self.solvable


def _exec(container: str, workdir: str, cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", "-w", workdir, container, *cmd],
        capture_output=True, text=True,
    )


def _run_test_files(container: str, workdir: str, files: list[Path]) -> Phase:
    """Copy host test files into the container and run them with pytest."""
    if not files:
        return Phase(0, 0, 0, 0)
    paths = []
    for f in files:
        dest = f"/tmp/check_{f.name}"
        subprocess.run(["docker", "cp", str(f), f"{container}:{dest}"], capture_output=True)
        paths.append(dest)
    res = _exec(container, workdir, ["python", "-m", "pytest", "-q", "--tb=no", *paths])
    c = parse_pytest_summary(res.stdout + res.stderr)
    return Phase(c["passed"], c["failed"], c["error"], c["total"])


def _apply_reference(container: str, workdir: str, task: Task) -> None:
    ref_dir = task.dir / "reference_solution"
    for path in sorted(ref_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(ref_dir).as_posix()
            subprocess.run(["docker", "exec", container, "mkdir", "-p",
                            f"{workdir}/{Path(rel).parent.as_posix()}"], capture_output=True)
            subprocess.run(["docker", "cp", str(path), f"{container}:{workdir}/{rel}"],
                           capture_output=True)


def check_task(task_id: str) -> TaskCheck:
    task = load_task(task_id)
    fixture = load_fixture(task.repo)
    workdir = fixture.workdir
    container = f"agentdelta-check-{task_id}"

    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
    subprocess.run(
        ["docker", "run", "-d", "--name", container, fixture.image_tag, "sleep", "infinity"],
        capture_output=True, check=True,
    )
    try:
        base_public = _run_test_files(container, workdir, task.public_test_files)
        base_hidden = _run_test_files(container, workdir, task.hidden_test_files)

        _apply_reference(container, workdir, task)

        baseline_ok = True
        for cmd in task.baseline_cmds:
            r = _exec(container, workdir, ["bash", "-lc", cmd])
            baseline_ok = baseline_ok and r.returncode == 0
        after_public = _run_test_files(container, workdir, task.public_test_files)
        after_hidden = _run_test_files(container, workdir, task.hidden_test_files)
    finally:
        subprocess.run(["docker", "rm", "-f", container], capture_output=True)

    return TaskCheck(
        task_id=task_id,
        base_public=base_public,
        base_hidden=base_hidden,
        after_baseline_ok=baseline_ok,
        after_public=after_public,
        after_hidden=after_hidden,
    )
