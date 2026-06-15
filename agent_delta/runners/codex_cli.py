"""Codex CLI agent adapter via inspect_swe.

Wraps `inspect_swe.codex_cli()` with AgentDelta's benchmark-safe defaults: no web
search, no MCP servers, no skills, and a pinned CLI version for official runs. The
OpenAI model is supplied at the eval level (full pinned ID, never an alias); the
agent inherits it. This mirrors runners/claude_code.py so the two providers are
treated identically by the harness.
"""

from __future__ import annotations

from typing import Any

from inspect_ai.agent import Agent
from inspect_swe import codex_cli


def build_codex_cli_agent(agent_cfg: dict[str, Any] | None = None) -> Agent:
    """Construct a benchmark-configured Codex CLI agent.

    The model is intentionally NOT set here; it is passed to `inspect_ai.eval()` as
    a full pinned model ID so the agent inherits it (SPEC 5.2: no aliases).
    """
    agent_cfg = agent_cfg or {}
    settings = agent_cfg.get("settings", {})

    # codex_cli uses a web_search literal (live|cached|disabled), not a tool list.
    web_search = "live" if agent_cfg.get("web_search") == "enabled" else "disabled"

    version = agent_cfg.get("version", "auto")
    # "pinned" is a placeholder in the config; resolve to "sandbox" so the CLI
    # baked into / provisioned in the image is used rather than a fresh download.
    if version == "pinned":
        version = "sandbox"

    return codex_cli(
        skills=agent_cfg.get("skills") or [],
        mcp_servers=agent_cfg.get("mcp_servers") or [],
        web_search=web_search,
        version=version,
        # Benchmark integrity: do not silently retry refusals as successes.
        retry_refusals=None if settings.get("retry_refusals") is False else 3,
    )
