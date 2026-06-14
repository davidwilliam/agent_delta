"""Cost model per SPEC section 19.

Pricing is declared here with an explicit pricing date and source so reports can
cite it. Prices are USD per million tokens. UPDATE the date/source when prices
change; official runs must record the pricing basis in the reproducibility
manifest.
"""

from __future__ import annotations

PRICING_DATE = "2026-06-13"
PRICING_SOURCE = "https://docs.anthropic.com/en/docs/about-claude/pricing"
CURRENCY = "USD"

# USD per 1M tokens: (input, output, cache_write_5m, cache_read).
# NOTE: placeholder values for v0.1 scaffolding — verify against the live
# pricing page before any published run.
PRICING_PER_MTOK: dict[str, dict[str, float]] = {
    "claude-opus-4-8": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-opus-4-7": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-opus-4-6": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0, "cache_write": 3.75, "cache_read": 0.30},
}


def estimate_cost_usd(
    model_id: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_write_tokens: int = 0,
    cache_read_tokens: int = 0,
) -> float | None:
    """Estimate run cost in USD. Returns None if pricing for the model is unknown."""
    p = PRICING_PER_MTOK.get(model_id)
    if p is None:
        return None
    return (
        input_tokens * p["input"]
        + output_tokens * p["output"]
        + cache_write_tokens * p["cache_write"]
        + cache_read_tokens * p["cache_read"]
    ) / 1_000_000.0


def cost_efficiency(model_cost_per_success: float, best_cost_per_success: float) -> float:
    """SPEC 14.3 — normalized in [0, 1] against the best model in the set."""
    if model_cost_per_success <= 0:
        return 1.0
    return min(1.0, best_cost_per_success / model_cost_per_success)
