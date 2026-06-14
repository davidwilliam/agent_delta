"""Basic statistics functions (reference solution for task_001).

Used only by AgentDelta's --dry-run mode to exercise the scoring pipeline
without calling a model. It is never shown to a real agent.
"""

from collections.abc import Sequence


def mean(values: Sequence[float]) -> float:
    """Return the arithmetic mean of a non-empty sequence of numbers."""
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def variance(values: Sequence[float]) -> float:
    """Return the population variance of a non-empty sequence of numbers."""
    if not values:
        raise ValueError("variance() requires at least one value")
    mu = mean(values)
    return sum((x - mu) ** 2 for x in values) / len(values)


def median(values: Sequence[float]) -> float:
    """Return the median; averages the two middle values for even length."""
    if not values:
        raise ValueError("median() requires at least one value")
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2
