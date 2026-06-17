"""Gemini CLI agent adapter via inspect_swe.

Wraps `inspect_swe.gemini_cli()` with AgentDelta's benchmark-safe defaults: no MCP
servers, no skills, a pinned CLI version for official runs, and the model set
explicitly (`gemini_model`) so the CLI runs the pinned model id rather than its
built-in default. Mirrors runners/claude_code.py and runners/codex_cli.py so all
three providers are treated identically by the harness. The Gemini CLI exposes no
web-search toggle, so there is nothing to disable there.
"""

from __future__ import annotations

from typing import Any

from inspect_ai.agent import Agent
from inspect_swe import gemini_cli


def build_gemini_cli_agent(agent_cfg: dict[str, Any] | None = None,
                           model_id: str | None = None) -> Agent:
    """Construct a benchmark-configured Gemini CLI agent.

    `model_id` is the bare pinned model id (e.g. "gemini-2.5-pro"); it is passed as
    `gemini_model` so the CLI runs exactly that model. The eval-level model
    ("google/<id>") still drives Inspect's tracking and cost (SPEC 5.2: no aliases).
    """
    agent_cfg = agent_cfg or {}
    settings = agent_cfg.get("settings", {})

    version = agent_cfg.get("version", "auto")
    if version == "pinned":
        version = "sandbox"

    kwargs: dict[str, Any] = {
        "skills": agent_cfg.get("skills") or [],
        "mcp_servers": agent_cfg.get("mcp_servers") or [],
        "version": version,
        # Benchmark integrity: do not silently retry refusals as successes.
        "retry_refusals": None if settings.get("retry_refusals") is False else 3,
    }
    if model_id:
        kwargs["gemini_model"] = model_id
    return gemini_cli(**kwargs)
