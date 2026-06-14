"""Public tests for task_004 (extract require_nonempty). Injected at score time."""

import pytest

from mathkit.stats import mean, variance
from mathkit.validation import require_nonempty


def test_require_nonempty_raises_on_empty():
    with pytest.raises(ValueError):
        require_nonempty([])


def test_require_nonempty_passes_on_nonempty():
    assert require_nonempty([1]) is None


def test_mean_behavior_preserved():
    assert mean([1, 2, 3]) == 2.0
    with pytest.raises(ValueError):
        mean([])


def test_variance_behavior_preserved():
    assert variance([2, 4, 6]) == pytest.approx(2.6666666, rel=1e-5)
    with pytest.raises(ValueError):
        variance([])
