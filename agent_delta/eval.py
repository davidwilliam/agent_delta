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
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.util import sandbox

from inspect_ai.model import ModelCost, set_model_cost

from agent_delta import config
from agent_delta.modes import build_prompt, is_scaffolded, mode_limits
from agent_delta.scoring.cost import PRICING_PER_MTOK
from agent_delta.registry import Fixture, Task as ADTask, load_fixture, load_task
from agent_delta.runners.claude_code import build_claude_code_agent
from agent_delta.scoring.sandbox_scorer import agentdelta_scorer

COMPOSE_PATH = config.SANDBOXES_DIR / "claude-code" / "compose.yaml"


def _register_model_costs() -> None:
    """Register AgentDelta's pricing with Inspect so cost limits and cost tracking
    work for the pinned model IDs of every provider (Inspect has no built-in
    pricing for them). Each model is registered under its provider prefix."""
    for provider in ("anthropic", "openai", "google"):
        try:
            models = config.load_models_config(provider).get("models", {})
        except FileNotFoundError:
            continue
        for mid in models:
            p = PRICING_PER_MTOK.get(mid)
            if not p:
                continue
            set_model_cost(f"{provider}/{mid}", ModelCost(
                input=p["input"], output=p["output"],
                input_cache_write=p["cache_write"], input_cache_read=p["cache_read"],
            ))


def _build_agent(agent_name: str):
    """Construct the real agent solver for the given agent CLI."""
    cfg = config.load_agent_config(agent_name)
    if agent_name == "codex_cli":
        from agent_delta.runners.codex_cli import build_codex_cli_agent
        return build_codex_cli_agent(cfg)
    return build_claude_code_agent(cfg)


@solver
def baseline_precheck_solver() -> Solver:
    """Run the baseline suite before the agent (SPEC 11.1). Stores pass/fail.

    If the baseline does not pass on the clean checkout, the run is invalid
    (the image is broken) and must not be scored as a model failure.
    """

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        meta = state.metadata or {}
        task = load_task(meta["task_id"])
        workdir = meta.get("workdir", "/repo")
        ok = True
        for cmd in task.baseline_cmds:
            res = await sandbox().exec(["bash", "-c", cmd], cwd=workdir)
            ok = ok and res.returncode == 0
        state.store.set("baseline_pre_ok", ok)
        return state

    return solve


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
    scaffolded: bool = False,
    effort: str | None = None,
) -> Task:
    limits = mode_limits(task, mode)
    gen_config = GenerateConfig(reasoning_effort=effort) if effort else GenerateConfig()
    sample = Sample(
        id=task.id,
        input=build_prompt(task, mode, scaffolded=scaffolded),
        metadata={
            "task_id": task.id,
            "repo": task.repo,
            "category": task.category,
            "workdir": fixture.workdir,
            "language": fixture.language,
            "mode": mode,
            "scaffolded": scaffolded,
        },
        sandbox=("docker", str(COMPOSE_PATH)),
    )

    if dry_run:
        agent = reference_solution_solver()
    else:
        agent = _build_agent(agent_name)

    return Task(
        dataset=[sample],
        setup=baseline_precheck_solver(),
        solver=agent,
        scorer=agentdelta_scorer(),
        epochs=epochs,
        config=gen_config,
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
    scaffold_model: str | None = None,
    network: str | None = None,
    effort: str | None = None,
    log_dir: str | Path | None = None,
):
    """Run one AgentDelta task for one model in one mode. Returns the EvalLogs."""
    task = load_task(task_id)
    fixture = load_fixture(task.repo)
    provider = config.provider_for_agent(agent_name)
    # Effort: explicit override, else the model's configured effort, else high.
    if effort is None and not dry_run:
        try:
            effort = config.model_spec(model_id, provider).get("effort")
        except KeyError:
            effort = None
    effort = effort or "high"
    os.environ["AGENTDELTA_IMAGE"] = fixture.image_tag
    # Network disabled by default (SPEC 22); a task opts in with network: enabled,
    # or the caller overrides (a real model run needs the inspect_swe proxy).
    net = network if network is not None else task.network
    os.environ["AGENTDELTA_NETWORK"] = "bridge" if net == "enabled" else "none"

    if not dry_run:
        config.ensure_provider_key(provider)
        _register_model_costs()

    scaffolded = is_scaffolded(mode, model_id, scaffold_model)
    log_dir = str(log_dir) if log_dir else str(config.RESULTS_DIR / "logs")
    eval_task = build_task(
        task, fixture, epochs=repetitions, dry_run=dry_run, agent_name=agent_name,
        mode=mode, scaffolded=scaffolded, effort=None if dry_run else effort,
    )

    # In dry-run there is no model; pass a placeholder Inspect accepts via the
    # mockllm provider so eval() has a model role even though the solver is mocked.
    model = "mockllm/model" if dry_run else f"{provider}/{model_id}"

    return inspect_eval(
        eval_task,
        model=model,
        log_dir=log_dir,
        sandbox_cleanup=True,
        fail_on_error=False,
    )
