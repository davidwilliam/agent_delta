"""Tests for the Codex CLI provider/agent wiring (no API, no Docker)."""

import pytest

from agent_delta import config
from agent_delta.scoring.cost import PRICING_PER_MTOK, estimate_cost_usd


def test_provider_for_agent():
    assert config.provider_for_agent("claude_code") == "anthropic"
    assert config.provider_for_agent("codex_cli") == "openai"
    assert config.provider_for_agent("unknown") == "anthropic"


def test_openai_model_config_loads_included_cohort():
    inc = config.included_models("openai")
    assert "gpt-5.4" in inc
    assert "gpt-5-mini-2025-08-07" in inc
    assert "gpt-4o-2024-11-20" not in inc  # present but include: false


def test_codex_agent_config_loads():
    cfg = config.load_agent_config("codex_cli")
    assert cfg["inspect_swe_agent"] == "codex_cli"
    assert cfg["web_search"] == "disabled"


def test_build_codex_agent_constructs():
    from agent_delta.eval import _build_agent
    from agent_delta.runners.codex_cli import build_codex_cli_agent
    assert build_codex_cli_agent(config.load_agent_config("codex_cli")) is not None
    assert _build_agent("codex_cli") is not None        # dispatch path
    assert _build_agent("claude_code") is not None


def test_openai_pricing_present_and_priced():
    for m in ["gpt-5.4", "gpt-5.1-2025-11-13", "gpt-5", "gpt-5-mini-2025-08-07"]:
        assert m in PRICING_PER_MTOK
    # 1M input tokens at the gpt-5.4 placeholder input rate.
    assert estimate_cost_usd("gpt-5.4", input_tokens=1_000_000) == pytest.approx(1.25)


def test_ensure_provider_key_missing_raises(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        config.ensure_provider_key("google")
