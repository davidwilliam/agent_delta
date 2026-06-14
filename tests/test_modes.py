"""Tests for evaluation-mode prompt transforms and resource limits."""

from agent_delta.modes import (
    available_modes,
    build_prompt,
    is_scaffolded,
    mode_limits,
    mode_spec,
    oldest_included_model,
)
from agent_delta.registry import load_task


def test_available_modes():
    modes = available_modes()
    for m in ("default", "equal_budget", "matched_workflow", "strong_spec",
              "cost_matched", "time_matched", "older_plus_scaffold"):
        assert m in modes


def test_default_mode_leaves_prompt_unchanged():
    task = load_task("task_001")
    assert build_prompt(task, "default") == task.prompt


def test_matched_workflow_prepends_steps():
    task = load_task("task_001")
    p = build_prompt(task, "matched_workflow")
    assert "Follow this process" in p
    assert p.endswith(task.prompt)
    assert "implementation plan" in p.lower()


def test_strong_spec_appends_acceptance_criteria():
    task = load_task("task_001")
    p = build_prompt(task, "strong_spec")
    assert task.prompt in p
    assert "Acceptance criteria" in p
    # A real acceptance criterion from task_001 should appear.
    assert "median" in p.lower()


def test_equal_budget_limits_override_task():
    task = load_task("task_001")
    limits = mode_limits(task, "equal_budget")
    assert limits["token_limit"] == 400000
    assert limits["message_limit"] == 80
    assert limits["cost_limit"] == 2.00


def test_default_limits_come_from_task():
    task = load_task("task_001")
    limits = mode_limits(task, "default")
    assert limits["time_limit"] == task.timeout_seconds
    assert limits["token_limit"] is None


def test_cost_matched_only_caps_cost():
    task = load_task("task_001")
    limits = mode_limits(task, "cost_matched")
    assert limits["cost_limit"] == 1.00
    # Time still defaults to the task value.
    assert limits["time_limit"] == task.timeout_seconds


def test_unknown_mode_raises():
    try:
        mode_spec("nope")
        assert False, "expected KeyError"
    except KeyError:
        pass


def test_oldest_included_model_is_baseline():
    # The Anthropic cohort's oldest included model is opus-4-6.
    assert oldest_included_model() == "claude-opus-4-6"


def test_scaffold_targets_only_the_older_model():
    assert is_scaffolded("older_plus_scaffold", "claude-opus-4-6") is True
    assert is_scaffolded("older_plus_scaffold", "claude-opus-4-8") is False
    # Explicit override.
    assert is_scaffolded("older_plus_scaffold", "claude-opus-4-7",
                         scaffold_model="claude-opus-4-7") is True
    # Other modes never scaffold.
    assert is_scaffolded("matched_workflow", "claude-opus-4-6") is False


def test_scaffold_prompt_asymmetric():
    task = load_task("task_001")
    # Scaffolded (older) model gets the full scaffold plus acceptance criteria.
    scaffolded = build_prompt(task, "older_plus_scaffold", scaffolded=True)
    assert "extra structure" in scaffolded
    assert "test-first" in scaffolded.lower()
    assert "Acceptance criteria" in scaffolded
    # Non-scaffolded (newer) model runs the plain prompt.
    assert build_prompt(task, "older_plus_scaffold", scaffolded=False) == task.prompt
