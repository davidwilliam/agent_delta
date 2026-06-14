"""Agentic Amplification Assessment (SPEC-ADDENDUM sections 6 to 8).

Computes the Agentic Work Index, amplification ratios, quality-per-resource
efficiency, and a classification of each Model B over Model A improvement, so a
report can answer "is the gain intrinsic, or did the newer model just do more
work by default?".
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agent_delta import config

# Components that may feed the Agentic Work Index, in the order reported.
WORK_COMPONENTS = [
    "input_tokens", "output_tokens", "wall_clock_seconds", "api_calls",
    "tool_calls", "shell_commands", "test_runs", "file_reads",
    "file_edits", "retry_count", "review_passes",
]


def load_amplification_config() -> dict:
    return config.load_scoring_config("amplification")


def agentic_work_index(
    work_by_model: dict[str, dict[str, float | None]],
    weights: dict[str, float],
) -> tuple[dict[str, float], list[str]]:
    """Return ({model: AWI in [0,100]}, present_components).

    Each present component is normalized by the set maximum, weighted (weights
    renormalized over present components), summed, and scaled so the
    heaviest-working system is 100. A component is "present" only if some model
    reports a positive value for it; missing values count as 0.
    """
    models = list(work_by_model)
    maxima: dict[str, float] = {}
    for comp in WORK_COMPONENTS:
        vals = [
            work_by_model[m].get(comp) or 0.0
            for m in models
            if isinstance(work_by_model[m].get(comp), (int, float))
        ]
        mx = max(vals) if vals else 0.0
        if mx > 0:
            maxima[comp] = mx

    present = list(maxima)
    if not present:
        return ({m: 0.0 for m in models}, [])

    wsum = sum(weights.get(c, 0.0) for c in present) or 1.0
    raw: dict[str, float] = {}
    for m in models:
        raw[m] = sum(
            (weights.get(c, 0.0) / wsum) * ((work_by_model[m].get(c) or 0.0) / maxima[c])
            for c in present
        )
    top = max(raw.values()) or 1.0
    return ({m: 100.0 * raw[m] / top for m in models}, present)


def _ratio(b: float | None, a: float | None) -> float | None:
    if a in (None, 0) or b is None:
        return None
    return b / a


def amplification_ratios(a: dict[str, float | None], b: dict[str, float | None]) -> dict[str, float | None]:
    """Model B over Model A ratios (SPEC-ADDENDUM 6.5 to 6.10, plus api/work)."""
    return {
        "token_amplification": _ratio(b.get("total_tokens"), a.get("total_tokens")),
        "cost_amplification": _ratio(b.get("cost"), a.get("cost")),
        "time_amplification": _ratio(b.get("wall_clock_seconds"), a.get("wall_clock_seconds")),
        "tool_amplification": _ratio(b.get("tool_calls"), a.get("tool_calls")),
        "retry_amplification": _ratio(b.get("retry_count"), a.get("retry_count")),
        "test_amplification": _ratio(b.get("test_runs"), a.get("test_runs")),
        "api_amplification": _ratio(b.get("api_calls"), a.get("api_calls")),
        "work_index_amplification": _ratio(b.get("work_index"), a.get("work_index")),
    }


def quality_efficiency(objective: float, cost: float | None, minutes: float | None, awi: float | None) -> dict:
    """Quality per dollar / minute / work unit (SPEC-ADDENDUM 6.2 to 6.4)."""
    return {
        "quality_per_dollar": (objective / cost) if cost else None,
        "quality_per_minute": (objective / minutes) if minutes else None,
        "quality_per_work_unit": (objective / awi) if awi else None,
    }


def quality_delta_per_extra(obj_a: float, obj_b: float, res_a: float | None, res_b: float | None) -> float | None:
    """(Objective_B - Objective_A) / (Resource_B - Resource_A) (6.11 / 6.12)."""
    if res_a is None or res_b is None:
        return None
    denom = res_b - res_a
    if denom == 0:
        return None
    return (obj_b - obj_a) / denom


@dataclass
class Classification:
    category: str
    rationale: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)
    modes_missing: list[str] = field(default_factory=list)


def classify_improvement(
    a: dict, b: dict, ratios: dict[str, float | None], cfg: dict,
    success_material: bool, success_delta_pp: float,
) -> Classification:
    """Classify a Model B over Model A change (SPEC-ADDENDUM section 8).

    With only Default Mode data we can detect Agentic-Amplification, Cost/Time-
    Inefficient, and No-Material-Gain, and we mark the modes still needed to
    distinguish Intrinsic vs Workflow-Equivalent.
    """
    thresholds = cfg["red_flags"]
    flags = [name for name, ratio in ratios.items()
             if ratio is not None and ratio >= thresholds.get(name, 1e9)]
    modest = cfg.get("modest_quality_gain_pp", 5)
    rationale: list[str] = []

    if not success_material:
        return Classification(
            "No Material Gain",
            ["Success difference is below the materiality threshold or not statistically supported."],
            flags,
        )

    cost_amp = ratios.get("cost_amplification")
    time_amp = ratios.get("time_amplification")

    if success_delta_pp < modest and cost_amp is not None and cost_amp >= thresholds["cost_amplification"]:
        rationale.append(
            f"Quality gain is modest ({success_delta_pp:.1f} pp) but cost is "
            f"{cost_amp:.1f}x higher."
        )
        return Classification("Cost-Inefficient Gain", rationale, flags,
                              modes_missing=["Equal-Budget", "Cost-Matched"])

    if success_delta_pp < modest and time_amp is not None and time_amp >= thresholds["time_amplification"]:
        rationale.append(
            f"Quality gain is modest ({success_delta_pp:.1f} pp) but wall-clock time "
            f"is {time_amp:.1f}x higher."
        )
        return Classification("Time-Inefficient Gain", rationale, flags,
                              modes_missing=["Time-Matched"])

    if flags:
        rationale.append(
            "Higher quality but with large resource amplification ("
            + ", ".join(flags) + ")."
        )
        return Classification("Agentic Amplification Gain (provisional)", rationale, flags,
                              modes_missing=["Equal-Budget", "Matched-Workflow"])

    rationale.append("Higher quality with comparable resource use in Default Mode.")
    return Classification(
        "Intrinsic Capability Gain (provisional)", rationale, flags,
        modes_missing=["Equal-Budget", "Matched-Workflow"],
    )
