"""Statistical helpers for aggregation (SPEC section 15).

Binary outcomes get a Wilson score interval and a paired McNemar comparison;
continuous outcomes (time, cost, tokens) get percentiles and a bootstrap CI.
All randomness is seeded so reports are reproducible.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

Z95 = 1.959963984540054


def wilson_ci(successes: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion, returned in [0, 1]."""
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def bootstrap_ci(
    values: list[float], statistic=np.median, n_boot: int = 2000, z: float = Z95, seed: int = 12345
) -> tuple[float, float]:
    """Percentile bootstrap CI for a statistic of `values`. Empty -> (nan, nan)."""
    if not values:
        return (math.nan, math.nan)
    if len(values) == 1:
        return (values[0], values[0])
    rng = np.random.default_rng(seed)
    arr = np.asarray(values, dtype=float)
    boots = [statistic(rng.choice(arr, size=arr.size, replace=True)) for _ in range(n_boot)]
    return (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))


@dataclass
class PairedResult:
    """McNemar paired comparison of two models over aligned binary outcomes."""

    n_pairs: int
    a_only: int  # A success, B failure (discordant b)
    b_only: int  # B success, A failure (discordant c)
    both: int
    neither: int
    p_value: float


def mcnemar(a_success: list[bool], b_success: list[bool]) -> PairedResult:
    """Exact McNemar test (binomial on discordant pairs) for paired outcomes."""
    both = sum(1 for a, b in zip(a_success, b_success) if a and b)
    neither = sum(1 for a, b in zip(a_success, b_success) if not a and not b)
    a_only = sum(1 for a, b in zip(a_success, b_success) if a and not b)
    b_only = sum(1 for a, b in zip(a_success, b_success) if b and not a)
    n_disc = a_only + b_only
    # Two-sided exact binomial p-value on the discordant pairs (p = 0.5).
    if n_disc == 0:
        p = 1.0
    else:
        k = min(a_only, b_only)
        tail = sum(math.comb(n_disc, i) for i in range(0, k + 1)) * (0.5 ** n_disc)
        p = min(1.0, 2.0 * tail)
    return PairedResult(len(a_success), a_only, b_only, both, neither, p)


def _phi(z: float) -> float:
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _average_ranks(values: list[float]) -> list[float]:
    """1-based ranks with ties averaged."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(values):
        j = i
        while j + 1 < len(values) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def wilcoxon_signed_rank(x: list[float], y: list[float]) -> dict[str, float]:
    """Paired Wilcoxon signed-rank test (normal approximation, SPEC 15.2).

    Returns the W statistic, z, two-sided p-value, and the non-zero pair count.
    """
    diffs = [a - b for a, b in zip(x, y)]
    nz = [d for d in diffs if d != 0]
    n = len(nz)
    if n == 0:
        return {"statistic": 0.0, "z": 0.0, "p_value": 1.0, "n": 0}
    ranks = _average_ranks([abs(d) for d in nz])
    w_plus = sum(r for r, d in zip(ranks, nz) if d > 0)
    w_minus = sum(r for r, d in zip(ranks, nz) if d < 0)
    w = min(w_plus, w_minus)
    mean_w = n * (n + 1) / 4.0
    sd_w = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    if sd_w == 0:
        return {"statistic": w, "z": 0.0, "p_value": 1.0, "n": n}
    z = max(0.0, abs(w - mean_w) - 0.5) / sd_w  # continuity-corrected
    p = 2.0 * (1.0 - _phi(z))
    return {"statistic": w, "z": z, "p_value": min(1.0, p), "n": n}


def holm_correction(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm step-down correction for a family of comparisons (SPEC 15.3)."""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    corrected: dict[str, float] = {}
    prev = 0.0
    for i, (key, p) in enumerate(items):
        c = max(prev, min(1.0, (m - i) * p))  # monotone non-decreasing
        corrected[key] = c
        prev = c
    return corrected


def percentiles(values: list[float]) -> dict[str, float]:
    """Median, mean, p25, p75, p90 for a list of values (nan-safe on empty)."""
    if not values:
        return {k: math.nan for k in ("median", "mean", "p25", "p75", "p90")}
    arr = np.asarray(values, dtype=float)
    return {
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "p25": float(np.percentile(arr, 25)),
        "p75": float(np.percentile(arr, 75)),
        "p90": float(np.percentile(arr, 90)),
    }
