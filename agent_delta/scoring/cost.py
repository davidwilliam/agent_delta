"""Cost model per SPEC section 19.

Pricing is declared here with an explicit pricing date and source so reports can
cite it. Prices are USD per million tokens. UPDATE the date/source when prices
change; official runs must record the pricing basis in the reproducibility
manifest.
"""

from __future__ import annotations

PRICING_DATE = "2026-06-15"
PRICING_SOURCE = {
    "anthropic": "https://docs.anthropic.com/en/docs/about-claude/pricing",
    "openai": "https://developers.openai.com/api/docs/pricing",
}
CURRENCY = "USD"

# USD per 1M tokens: (input, output, cache_write, cache_read). Keyed by model ID
# (unique across providers). OpenAI bills no separate cache-write charge, so
# cache_write mirrors input and cache_read is the reduced cached-input rate; dated
# snapshots inherit their family's rate. OpenAI rates verified from the developers
# pricing docs on PRICING_DATE; Anthropic rates from the Anthropic pricing page.
PRICING_PER_MTOK: dict[str, dict[str, float]] = {
    # Anthropic (Claude Code agent).
    "claude-opus-4-8": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-opus-4-7": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-opus-4-6": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0, "cache_write": 3.75, "cache_read": 0.30},
    # OpenAI (Codex CLI agent). Verified from developers.openai.com on PRICING_DATE.
    "gpt-5.4": {"input": 2.50, "output": 15.0, "cache_write": 2.50, "cache_read": 0.25},
    "gpt-5.1-2025-11-13": {"input": 1.25, "output": 10.0, "cache_write": 1.25, "cache_read": 0.125},
    "gpt-5": {"input": 1.25, "output": 10.0, "cache_write": 1.25, "cache_read": 0.125},
    "gpt-5-mini-2025-08-07": {"input": 0.25, "output": 2.0, "cache_write": 0.25, "cache_read": 0.025},
    # gpt-5.4-pro publishes no cached-input rate; cache_read mirrors input.
    "gpt-5.4-pro-2026-03-05": {"input": 30.0, "output": 180.0, "cache_write": 30.0, "cache_read": 30.0},
    "gpt-4o-2024-11-20": {"input": 2.50, "output": 10.0, "cache_write": 2.50, "cache_read": 1.25},
    "gpt-5-nano-2025-08-07": {"input": 0.05, "output": 0.40, "cache_write": 0.05, "cache_read": 0.005},
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
    """SPEC 14.3 - normalized in [0, 1] against the best model in the set."""
    if model_cost_per_success <= 0:
        return 1.0
    return min(1.0, best_cost_per_success / model_cost_per_success)
