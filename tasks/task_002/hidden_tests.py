"""Hidden tests for task_002 (fix chunk remainder). Edge cases."""

from mathkit.sequences import chunk


def test_chunk_size_larger_than_seq():
    assert chunk([1, 2], 5) == [[1, 2]]


def test_chunk_remainder_of_one():
    assert chunk([1, 2, 3], 2) == [[1, 2], [3]]


def test_chunk_empty_sequence():
    assert chunk([], 3) == []


def test_chunk_exact_multiple_three():
    assert chunk([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]
