"""Basic statistics functions.

NOTE (fixture): `median` is intentionally not yet implemented. The AgentDelta
task asks the agent to add it. `mean` and `variance` are the baseline behavior
that must keep working (regression surface).
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
