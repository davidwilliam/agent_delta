"""Tests for the Node/TypeScript test runner and author-written prompt variants."""

from agent_delta.modes import available_modes, build_prompt
from agent_delta.registry import load_task
from agent_delta.scoring.testrunner import parse, parse_node_test, plan


def test_parse_node_counts_pass_fail():
    c = parse_node_test("# tests 4\n# pass 3\n# fail 1\n")
    assert c["passed"] == 3 and c["failed"] == 1 and c["total"] == 4


def test_parse_node_compile_error_is_error():
    c = parse_node_test("src/discount.ts(8,10): error TS2322: Type 'x'.\n")
    assert c["error"] == 1 and c["total"] == 1 and c["passed"] == 0


def test_parse_node_no_tests_no_error_is_empty():
    c = parse_node_test("some unrelated chatter\n")
    assert c["total"] == 0 and c["error"] == 0


def test_plan_typescript_builds_then_runs_node_test():
    targets, cmd = plan("typescript", "hidden", ["hidden_tests.mjs"], "/repo")
    assert targets["hidden_tests.mjs"] == "/repo/agentdelta_eval/hidden/hidden_tests.mjs"
    assert "npm run --silent build" in cmd[-1]
    assert "node --test agentdelta_eval/hidden/hidden_tests.mjs" in cmd[-1]


def test_parse_dispatches_to_node():
    c = parse("node", "# tests 2\n# pass 2\n# fail 0\n")
    assert c["passed"] == 2 and c["total"] == 2


def test_minimal_spec_mode_available():
    assert "minimal_spec" in available_modes()


def test_author_prompt_variants_are_used():
    task = load_task("ts_task_001")
    # The author files differ from the default prompt and from each other.
    minimal = build_prompt(task, "minimal_spec")
    strong = build_prompt(task, "strong_spec")
    workflow = build_prompt(task, "matched_workflow")
    assert task.prompt_variant("minimal") is not None
    assert "Fix it." in minimal
    assert "Requirements:" in strong          # author strong file, not synthesis
    assert "Acceptance criteria" not in strong  # synthesis header absent
    assert "Follow this process" in workflow


def test_missing_variant_falls_back_to_synthesis():
    # task_001 declares no author variants, so strong_spec synthesizes one.
    task = load_task("task_001")
    assert task.prompt_variant("strong") is None
    assert "Acceptance criteria" in build_prompt(task, "strong_spec")
