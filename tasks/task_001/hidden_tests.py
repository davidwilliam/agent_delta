"""Hidden tests for task_001 (add median).

These measure generalization and edge-case handling beyond the public criteria.
They are kept out of the agent's view and injected only at score time.
A solution that mishandles unsorted even-length input or negatives fails here.
"""

import pytest

from mathkit.stats import median


def test_median_single():
    assert median([7]) == 7


def test_median_unsorted_even():
    # Must sort: middle two of sorted [1,2,8,9] -> 5.0
    assert median([9, 1, 8, 2]) == 5.0


def test_median_negatives():
    assert median([-5, -1, -3]) == -3


def test_median_floats():
    assert median([1.5, 2.5, 0.5]) == 1.5


def test_median_does_not_mutate_input():
    data = [3, 1, 2]
    _ = median(data)
    assert data == [3, 1, 2]
