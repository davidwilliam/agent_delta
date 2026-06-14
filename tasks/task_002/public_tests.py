"""Public tests for task_002 (fix chunk remainder). Injected at score time."""

import pytest

from mathkit.sequences import chunk


def test_chunk_includes_remainder():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_even_still_works():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_invalid_size_raises():
    with pytest.raises(ValueError):
        chunk([1, 2, 3], 0)
