"""Public tests for task_007 (summary module). Injected at score time."""

import pytest

from mathkit.summary import describe, summarize, top_n


def test_summarize_basic():
    assert summarize([1, 2, 3]) == {
        "count": 3, "mean": 2.0, "minimum": 1, "maximum": 3, "span": 2,
    }


def test_describe_format():
    assert describe([1, 2, 3]) == "count=3 mean=2.00 min=1 max=3 span=2"


def test_top_n_basic():
    assert top_n([3, 1, 2, 5, 4], 2) == [5, 4]


def test_summarize_empty_raises():
    with pytest.raises(ValueError):
        summarize([])
