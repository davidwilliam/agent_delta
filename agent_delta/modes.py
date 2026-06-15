"""Evaluation modes (SPEC-ADDENDUM section 5).

A mode transforms a run's conditions without changing the task, fixture, base
commit, or scoring: it may rewrite the prompt (Matched-Workflow, Strong-Spec) and
or impose resource limits (Equal-Budget, Cost-Matched, Time-Matched). Running the
same task across modes is what lets cross-mode synthesis tell intrinsic capability
apart from agentic amplification.
"""

from __future__ import annotations

import re
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


def _forbidden_block(task) -> str:
    if not task.forbidden_changes:
        return ""
    lines = ["", "## Do not (forbidden changes)"]
    lines += [f"- {c}" for c in task.forbidden_changes]
    return "\n".join(lines)


def build_prompt(task, mode: str, *, scaffolded: bool = False) -> str:
    """Return the task prompt transformed for `mode`.

    `scaffolded` only matters for the asymmetric older_plus_scaffold mode: the
    designated older model gets the scaffold; every other model runs default.
    Forbidden-change constraints (HARD-TASKS-SPEC) are appended in every mode.
    """
    spec = mode_spec(mode)
    forbidden = _forbidden_block(task)
    if spec.get("scaffold"):
        if not scaffolded:
            return task.prompt + forbidden
        steps = _modes_config()["scaffold_steps"]
        return f"{steps}\n\n{task.prompt}\n\n{_strong_spec_block(task)}{forbidden}"
    body = task.prompt
    if spec.get("strong_spec"):
        body = f"{body}\n\n{_strong_spec_block(task)}"
    if spec.get("workflow"):
        steps = _modes_config()["workflow_steps"]
        body = f"{steps}\n\n{body}"
    return body + forbidden


def _version_key(model_id: str) -> tuple:
    m = re.search(r"(\d+)[-.](\d+)", model_id)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def oldest_included_model(provider: str = "anthropic") -> str | None:
    """The oldest included model in the cohort (default scaffold target)."""
    models = config.included_models(provider)
    return min(models, key=lambda mid: (_version_key(mid), mid)) if models else None


def is_scaffolded(mode: str, model_id: str, scaffold_model: str | None = None) -> bool:
    """Whether this model receives the scaffold under older_plus_scaffold mode.

    The scaffold goes to `scaffold_model` if given, else the oldest included model.
    """
    if not mode_spec(mode).get("scaffold"):
        return False
    target = scaffold_model or oldest_included_model()
    return model_id == target


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
