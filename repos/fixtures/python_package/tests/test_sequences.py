"""Baseline tests for mathkit.sequences (must keep passing).

These cover only behavior that is already correct at the fixture base. The
intentional `chunk` remainder bug is exercised by task_002's injected tests, not
here, so the baseline stays green.
"""

import pytest

from mathkit.sequences import chunk, dedupe


def test_chunk_evenly_divisible():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_size_one():
    assert chunk([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_invalid_size_raises():
    with pytest.raises(ValueError):
        chunk([1, 2, 3], 0)


def test_dedupe_preserves_order():
    assert dedupe([1, 1, 2, 3, 2, 1]) == [1, 2, 3]


def test_dedupe_empty():
    assert dedupe([]) == []
