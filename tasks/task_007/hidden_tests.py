"""Hidden tests for task_007 (summary module). Edge cases."""

import pytest

from mathkit.summary import describe, summarize, top_n


def test_summarize_single():
    assert summarize([7]) == {
        "count": 1, "mean": 7.0, "minimum": 7, "maximum": 7, "span": 0,
    }


def test_describe_two_decimals():
    assert describe([1, 2]) == "count=2 mean=1.50 min=1 max=2 span=1"


def test_top_n_over_length():
    assert top_n([2, 1], 5) == [2, 1]


def test_top_n_zero():
    assert top_n([3, 1, 2], 0) == []


def test_top_n_negative_raises():
    with pytest.raises(ValueError):
        top_n([1, 2, 3], -1)


def test_describe_empty_raises():
    with pytest.raises(ValueError):
        describe([])
