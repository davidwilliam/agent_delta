"""Baseline test suite for mathkit.

These tests cover existing behavior (mean, variance) and MUST keep passing.
They form the regression surface for AgentDelta tasks on this fixture.
"""

import pytest

from mathkit.stats import mean, variance


def test_mean_basic():
    assert mean([1, 2, 3]) == 2.0


def test_mean_single():
    assert mean([42]) == 42.0


def test_mean_empty_raises():
    with pytest.raises(ValueError):
        mean([])


def test_variance_basic():
    assert variance([2, 4, 6]) == pytest.approx(2.6666666, rel=1e-5)


def test_variance_empty_raises():
    with pytest.raises(ValueError):
        variance([])
