"""Latency scoring helpers (SPEC section 14.4 / section 20)."""

from __future__ import annotations


def time_efficiency(model_median_time: float, best_median_time: float) -> float:
    """SPEC 14.4 - normalized in [0, 1] against the fastest model in the set."""
    if model_median_time <= 0:
        return 1.0
    return min(1.0, best_median_time / model_median_time)
