"""Evaluation modes (SPEC-ADDENDUM section 5).

A mode transforms a run's conditions without changing the task, fixture, base
commit, or scoring: it may rewrite the prompt (Matched-Workflow, Strong-Spec) and
or impose resource limits (Equal-Budget, Cost-Matched, Time-Matched). Running the
same task across modes is what lets cross-mode synthesis tell intrinsic capability
apart from agentic amplification.
"""

from __future__ import annotations

from functools import lru_cache

import yaml

from agent_delta import config


@lru_cache(maxsize=1)
def _modes_config() -> dict:
    with (config.CONFIGS_DIR / "modes.yaml").open() as f:
        return yaml.safe_load(f)


def available_modes() -> list[str]:
    return list(_modes_config()["modes"])


def mode_spec(mode: str) -> dict:
    modes = _modes_config()["modes"]
    if mode not in modes:
        raise KeyError(f"Unknown mode {mode!r}; available: {', '.join(modes)}")
    return modes[mode]


def _strong_spec_block(task) -> str:
    lines = ["## Acceptance criteria (definition of done)"]
    for c in task.spec.get("acceptance_criteria", []):
        lines.append(f"- {c}")
    if task.forbidden_paths:
        lines.append("")
        lines.append("## Do not modify these paths")
        for f in task.forbidden_paths:
            lines.append(f"- {f}")
    lines.append("")
    lines.append("## Before finishing")
    lines.append("- Confirm the existing test suite still passes.")
    lines.append("- Review your diff against each acceptance criterion above.")
    return "\n".join(lines)


def build_prompt(task, mode: str) -> str:
    """Return the task prompt transformed for `mode`."""
    spec = mode_spec(mode)
    body = task.prompt
    if spec.get("strong_spec"):
        body = f"{body}\n\n{_strong_spec_block(task)}"
    if spec.get("workflow"):
        steps = _modes_config()["workflow_steps"]
        body = f"{steps}\n\n{body}"
    return body


def mode_limits(task, mode: str) -> dict:
    """Resource limits for the Inspect task: mode caps override the task defaults."""
    limits = {
        "time_limit": task.timeout_seconds,
        "cost_limit": task.max_cost_usd,
        "token_limit": None,
        "message_limit": None,
    }
    limits.update(mode_spec(mode).get("limits", {}))
    return limits
