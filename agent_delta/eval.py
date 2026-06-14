"""Eval orchestration: build an Inspect Task for an AgentDelta task and run it.

Supports two solver paths:
  * real     -> the Claude Code agent via inspect_swe (calls the model).
  * dry-run  -> a mock solver that applies the task's reference solution inside
               the sandbox, exercising the full Docker + scoring pipeline with
               no API cost.
"""

from __future__ import annotations

import os
from pathlib import Path

from inspect_ai import Task, eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.util import sandbox

from agent_delta import config
from agent_delta.modes import build_prompt, mode_limits
from agent_delta.registry import Fixture, Task as ADTask, load_fixture, load_task
from agent_delta.runners.claude_code import build_claude_code_agent
from agent_delta.scoring.sandbox_scorer import agentdelta_scorer

COMPOSE_PATH = config.SANDBOXES_DIR / "claude-code" / "compose.yaml"


@solver
def reference_solution_solver() -> Solver:
    """Dry-run solver: copy tasks/<id>/reference_solution/* into the sandbox repo."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        meta = state.metadata or {}
        task = load_task(meta["task_id"])
        workdir = meta.get("workdir", "/repo")
        ref_dir = task.dir / "reference_solution"
        if not ref_dir.is_dir():
            return state
        for path in sorted(ref_dir.rglob("*")):
            if path.is_file():
                rel = path.relative_to(ref_dir).as_posix()
                await sandbox().write_file(f"{workdir}/{rel}", path.read_text())
        return state

    return solve


def build_task(
    task: ADTask,
    fixture: Fixture,
    *,
    epochs: int,
    dry_run: bool,
    agent_name: str = "claude_code",
    mode: str = "default",
) -> Task:
    limits = mode_limits(task, mode)
    sample = Sample(
        id=task.id,
        input=build_prompt(task, mode),
        metadata={
            "task_id": task.id,
            "repo": task.repo,
            "category": task.category,
            "workdir": fixture.workdir,
            "mode": mode,
        },
        sandbox=("docker", str(COMPOSE_PATH)),
    )

    if dry_run:
        agent = reference_solution_solver()
    else:
        agent = build_claude_code_agent(config.load_agent_config(agent_name))

    return Task(
        dataset=[sample],
        solver=agent,
        scorer=agentdelta_scorer(),
        epochs=epochs,
        time_limit=limits["time_limit"],
        cost_limit=limits["cost_limit"] if not dry_run else None,
        token_limit=limits["token_limit"],
        message_limit=limits["message_limit"],
        name=f"agentdelta_{task.id}_{mode}",
    )


def run_task(
    task_id: str,
    model_id: str,
    *,
    repetitions: int = 1,
    agent_name: str = "claude_code",
    dry_run: bool = False,
    mode: str = "default",
    log_dir: str | Path | None = None,
):
    """Run one AgentDelta task for one model in one mode. Returns the EvalLogs."""
    task = load_task(task_id)
    fixture = load_fixture(task.repo)
    os.environ["AGENTDELTA_IMAGE"] = fixture.image_tag

    if not dry_run:
        config.ensure_anthropic_key()

    log_dir = str(log_dir) if log_dir else str(config.RESULTS_DIR / "logs")
    eval_task = build_task(
        task, fixture, epochs=repetitions, dry_run=dry_run, agent_name=agent_name, mode=mode
    )

    # In dry-run there is no model; pass a placeholder Inspect accepts via the
    # mockllm provider so eval() has a model role even though the solver is mocked.
    model = "mockllm/model" if dry_run else f"anthropic/{model_id}"

    return inspect_eval(
        eval_task,
        model=model,
        log_dir=log_dir,
        sandbox_cleanup=True,
        fail_on_error=False,
    )
