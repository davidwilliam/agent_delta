"""Basic statistics functions (reference solution for task_004)."""

from collections.abc import Sequence

from mathkit.validation import require_nonempty


def mean(values: Sequence[float]) -> float:
    """Return the arithmetic mean of a non-empty sequence of numbers."""
    require_nonempty(values, "mean()")
    return sum(values) / len(values)


def variance(values: Sequence[float]) -> float:
    """Return the population variance of a non-empty sequence of numbers."""
    require_nonempty(values, "variance()")
    mu = mean(values)
    return sum((x - mu) ** 2 for x in values) / len(values)
