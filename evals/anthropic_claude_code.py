"""Inspect entry point for the Anthropic / Claude Code suite.

Usable directly with the Inspect CLI, e.g.:

    inspect eval evals/anthropic_claude_code.py -T task_id=task_001 \
        --model anthropic/claude-opus-4-8 --epochs 5

or via the AgentDelta CLI (`agentdelta run`), which also writes SPEC §16 records.
"""

from __future__ import annotations

from inspect_ai import Task, task

from agent_delta.eval import build_task
from agent_delta.registry import load_fixture, load_task


@task
def agentdelta(
    task_id: str = "task_001",
    repetitions: int = 1,
    dry_run: bool = False,
    mode: str = "default",
) -> Task:
    import os

    t = load_task(task_id)
    fixture = load_fixture(t.repo)
    os.environ["AGENTDELTA_IMAGE"] = fixture.image_tag
    return build_task(t, fixture, epochs=repetitions, dry_run=dry_run, mode=mode)
