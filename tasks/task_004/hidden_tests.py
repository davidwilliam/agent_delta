"""Hidden tests for task_004 (extract require_nonempty).

Includes a structural check that stats.py actually *uses* the helper, so a
solution that merely creates the module without refactoring fails.
"""

import inspect

import pytest

import mathkit.stats
from mathkit.validation import require_nonempty


def test_stats_uses_helper():
    src = inspect.getsource(mathkit.stats)
    assert "require_nonempty" in src


def test_require_nonempty_on_empty_tuple():
    with pytest.raises(ValueError):
        require_nonempty(())


def test_require_nonempty_on_empty_string():
    with pytest.raises(ValueError):
        require_nonempty("")


def test_require_nonempty_returns_none_for_nonempty_string():
    assert require_nonempty("a") is None


def test_variance_value_unchanged():
    assert mathkit.stats.variance([1, 2, 3, 4]) == pytest.approx(1.25, rel=1e-9)
