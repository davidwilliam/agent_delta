"""Summary helpers (reference solution for task_007)."""

from mathkit.stats import mean


def summarize(values):
    """Return count, mean, minimum, maximum, and span of a non-empty sequence."""
    if not values:
        raise ValueError("summarize() requires at least one value")
    return {
        "count": len(values),
        "mean": mean(values),
        "minimum": min(values),
        "maximum": max(values),
        "span": max(values) - min(values),
    }


def describe(values):
    """Return a one-line summary string."""
    s = summarize(values)
    return (f"count={s['count']} mean={s['mean']:.2f} "
            f"min={s['minimum']} max={s['maximum']} span={s['span']}")


def top_n(values, n):
    """Return the n largest values in descending order."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return sorted(values, reverse=True)[:n]
