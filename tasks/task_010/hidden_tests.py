"""Hidden tests for task_010 (merge_intervals). Subtle edge cases."""

from mathkit.intervals import merge_intervals


def test_unsorted_input():
    assert merge_intervals([[8, 10], [1, 3], [2, 6], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_nested_interval():
    assert merge_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]


def test_disjoint_stay_separate():
    assert merge_intervals([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]


def test_negative_numbers():
    assert merge_intervals([[-5, -1], [-3, 2]]) == [[-5, 2]]


def test_duplicates():
    assert merge_intervals([[1, 4], [1, 4]]) == [[1, 4]]


def test_single():
    assert merge_intervals([[5, 7]]) == [[5, 7]]
