"""Claude Code agent adapter via inspect_swe.

Wraps `inspect_swe.claude_code()` with AgentDelta's benchmark-safe defaults:
no web search, no MCP servers, no skills, and a pinned CLI version for official
runs. The model is supplied at the eval level (full pinned ID, never an alias);
the agent inherits it.
"""

from __future__ import annotations

from typing import Any

from inspect_ai.agent import Agent
from inspect_swe import claude_code

# Tools disabled for a hermetic benchmark run unless a task explicitly needs them.
_DEFAULT_DISALLOWED = ["WebSearch", "WebFetch"]


def build_claude_code_agent(agent_cfg: dict[str, Any] | None = None) -> Agent:
    """Construct a benchmark-configured Claude Code agent.

    The model is intentionally NOT set here; it is passed to `inspect_ai.eval()`
    as a full pinned model ID so the agent inherits it (SPEC 5.2: no aliases).
    """
    agent_cfg = agent_cfg or {}
    settings = agent_cfg.get("settings", {})

    disallowed = list(_DEFAULT_DISALLOWED)
    if agent_cfg.get("web_search") == "enabled":
        disallowed = [t for t in disallowed if t != "WebSearch"]

    version = agent_cfg.get("version", "auto")
    # "pinned" is a placeholder in the config; resolve to "sandbox" so the CLI
    # baked into the image (a known version) is used rather than a fresh download.
    if version == "pinned":
        version = "sandbox"

    return claude_code(
        skills=agent_cfg.get("skills") or [],
        mcp_servers=agent_cfg.get("mcp_servers") or [],
        disallowed_tools=disallowed,
        version=version,
        # Benchmark integrity: do not silently retry refusals as successes.
        retry_refusals=None if settings.get("retry_refusals") is False else 3,
    )
