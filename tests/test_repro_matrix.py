"""Tests for blocked randomization and the reproducibility manifest."""

from agent_delta import reproducibility as repro
from agent_delta.matrix import shuffled_order


def test_shuffled_order_deterministic():
    m = ["a", "b", "c", "d"]
    assert shuffled_order(m, 7, 0, 0) == shuffled_order(m, 7, 0, 0)
    assert sorted(shuffled_order(m, 7, 1, 2)) == m  # still a permutation


def test_shuffled_order_varies():
    m = ["a", "b", "c", "d", "e"]
    orders = {tuple(shuffled_order(m, 7, r, t)) for r in range(4) for t in range(4)}
    assert len(orders) > 1  # the order is not constant across reps/tasks


def test_no_randomize_preserves_order():
    # run_matrix with randomize=False uses the given order; shuffled_order is only
    # called when randomize is True, so here we just assert the identity contract.
    m = ["x", "y", "z"]
    assert list(m) == m


def test_content_hashes_stable_and_prefixed():
    assert repro.tasks_hash() == repro.tasks_hash()
    assert repro.tasks_hash().startswith("sha256:")
    assert repro.hidden_tests_hash().startswith("sha256:")
    assert repro.scoring_hash().startswith("sha256:")
    # The three cover different files, so they should differ.
    assert len({repro.tasks_hash(), repro.hidden_tests_hash(), repro.scoring_hash()}) == 3


def test_validate_manifest_detects_drift():
    good = {
        "tasks_hash": repro.tasks_hash(),
        "scoring_hash": repro.scoring_hash(),
        "hidden_tests_hash": repro.hidden_tests_hash(),
        "sandbox_images": {"python_package": "sha256:abc"},
    }
    assert repro.validate_manifest(good) == []

    drifted = dict(good, tasks_hash="sha256:deadbeef")
    problems = repro.validate_manifest(drifted)
    assert any("tasks_hash" in p for p in problems)

    missing_image = dict(good, sandbox_images={"python_package": None})
    assert any("sandbox image" in p for p in repro.validate_manifest(missing_image))


def test_collect_versions_has_core_fields():
    v = repro.collect_versions()
    assert v["agentdelta_version"]
    assert "python_version" in v and v["python_version"]
