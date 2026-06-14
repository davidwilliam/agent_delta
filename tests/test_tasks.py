"""Tests for task metadata: types, mutants, and category coverage."""

from agent_delta.registry import list_tasks, load_task


def test_test_writing_task_type_and_mutants():
    t = load_task("task_006")
    assert t.task_type == "test_writing"
    assert t.test_writing["target_path"] == "src/mathkit/textnorm.py"
    mutants = t.load_mutants()
    names = {n for n, _ in mutants}
    assert names == {"strip_only", "noop", "wrong_sep"}
    # Each mutant overwrites the target source file.
    for _name, files in mutants:
        assert "src/mathkit/textnorm.py" in files


def test_implement_tasks_have_no_mutants():
    t = load_task("task_001")
    assert t.task_type == "implement"
    assert t.load_mutants() == []


def test_tasks_default_to_network_disabled():
    # Network is disabled by default (SPEC 22); no task opts into network for now.
    for tid in list_tasks():
        assert load_task(tid).network == "disabled"


def test_all_seven_categories_present():
    cats = {load_task(tid).category for tid in list_tasks()}
    expected = {
        "small_bug_fix", "medium_feature", "multi_file_refactor", "security_fix",
        "test_writing", "long_horizon", "dependency_migration",
    }
    assert expected <= cats
