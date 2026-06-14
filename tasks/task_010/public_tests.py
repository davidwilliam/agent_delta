"""Public tests for task_010 (merge_intervals). Injected at score time."""

from mathkit.intervals import merge_intervals


def test_basic_overlap():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_touching_merges():
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]


def test_empty():
    assert merge_intervals([]) == []
