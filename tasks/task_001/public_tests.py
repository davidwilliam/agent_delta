"""Public tests for task_001 (add median).

These encode the stated acceptance criteria. They are injected into the sandbox
at score time and are NOT present in the repository the agent edits.
"""

import pytest

from mathkit import median as median_pkg
from mathkit.stats import median


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_empty_raises():
    with pytest.raises(ValueError):
        median([])


def test_median_exported_from_package():
    assert median_pkg([5, 1, 3]) == 3
