"""Tests for the Gemini CLI provider/agent wiring (no API, no Docker)."""

import pytest

from agent_delta import config
from agent_delta.scoring.cost import PRICING_PER_MTOK, estimate_cost_usd


def test_provider_for_agent():
    assert config.provider_for_agent("gemini_cli") == "google"


def test_google_model_config_loads_priced_cohort():
    inc = config.included_models("google")
    assert "gemini-2.5-pro" in inc
    assert "gemini-3.5-flash" in inc
    # preview pros are present but excluded (no published price).
    assert "gemini-3.1-pro-preview" not in inc


def test_gemini_agent_config_loads():
    cfg = config.load_agent_config("gemini_cli")
    assert cfg["inspect_swe_agent"] == "gemini_cli"


def test_build_gemini_agent_constructs():
    from agent_delta.eval import _build_agent
    from agent_delta.runners.gemini_cli import build_gemini_cli_agent
    cfg = config.load_agent_config("gemini_cli")
    assert build_gemini_cli_agent(cfg) is not None
    assert build_gemini_cli_agent(cfg, "gemini-2.5-pro") is not None  # model_id -> gemini_model
    assert _build_agent("gemini_cli", "gemini-3.5-flash") is not None  # dispatch path


def test_google_pricing_present_and_priced():
    for m in ["gemini-2.5-pro", "gemini-3.5-flash", "gemini-2.5-flash", "gemini-3.1-flash-lite"]:
        assert m in PRICING_PER_MTOK
    assert estimate_cost_usd("gemini-2.5-pro", input_tokens=1_000_000) == pytest.approx(1.25)
    assert estimate_cost_usd("gemini-3.5-flash", output_tokens=1_000_000) == pytest.approx(9.0)


def test_preview_pros_have_no_pricing():
    # Excluded models carry no pricing entry (we will not run an unpriced model).
    assert "gemini-3.1-pro-preview" not in PRICING_PER_MTOK
