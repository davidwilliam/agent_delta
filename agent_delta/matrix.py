"""Run-matrix orchestration with blocked randomization (SPEC sections 12.2, 25).

Runs the (task x model x repetition) matrix. For each repetition and task the
model order is shuffled with a seeded RNG, then each model runs once, so no model
runs all its repetitions before the next (which would bias results by transient
provider load or time-of-day). The seed and the realized order are recorded for
reproducibility.
"""

from __future__ import annotations

import random
from typing import Any


def shuffled_order(models: list[str], seed: int, rep: int, task_index: int) -> list[str]:
    """Deterministic per (seed, rep, task) shuffle of the model order."""
    rng = random.Random(seed * 1_000_000 + rep * 1_000 + task_index)
    order = list(models)
    rng.shuffle(order)
    return order


def run_matrix(
    suite: str,
    task_ids: list[str],
    model_ids: list[str],
    *,
    repetitions: int = 1,
    mode: str = "default",
    seed: int = 12345,
    randomize: bool = True,
    dry_run: bool = False,
    scaffold_model: str | None = None,
    network: str | None = None,
    effort: str | None = None,
    agent: str = "claude_code",
    on_run=None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Execute the matrix. Returns (run_order_log, fixtures_used)."""
    from agent_delta.eval import run_task
    from agent_delta.registry import load_task
    from agent_delta.reporting import write_run_records

    order_log: list[dict[str, Any]] = []
    for rep in range(repetitions):
        for ti, task_id in enumerate(task_ids):
            order = shuffled_order(model_ids, seed, rep, ti) if randomize else list(model_ids)
            order_log.append({"rep": rep, "task": task_id, "order": order})
            for model_id in order:
                if on_run:
                    on_run(rep, task_id, model_id)
                logs = run_task(task_id, model_id, repetitions=1, mode=mode,
                                dry_run=dry_run, scaffold_model=scaffold_model,
                                network=network, effort=effort, agent_name=agent)
                write_run_records(logs, suite=suite, mode=mode, epoch=rep, agent=agent)

    fixtures = sorted({load_task(t).repo for t in task_ids})
    return order_log, fixtures
