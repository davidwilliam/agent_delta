"""Configuration, paths, and environment handling for AgentDelta.

Loads `.env`, normalizes the Anthropic API key (tolerating the common
`ANTHORPIC_API_KEY` misspelling), and exposes repo-root-relative paths plus
helpers for loading the YAML model/agent/scoring configs.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# Paths (anchored to the repository root, two levels up from this file).
ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tasks"
REPOS_DIR = ROOT / "repos"
FIXTURES_DIR = REPOS_DIR / "fixtures"
MANIFESTS_DIR = REPOS_DIR / "manifests"
CONFIGS_DIR = ROOT / "configs"
SANDBOXES_DIR = ROOT / "sandboxes"
RESULTS_DIR = ROOT / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"
SCHEMAS_DIR = ROOT / "agent_delta" / "schemas"


def load_dotenv(path: Path | None = None) -> None:
    """Minimal .env loader (no external dependency). Does not overwrite existing env."""
    path = path or (ROOT / ".env")
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def ensure_anthropic_key() -> str:
    """Return the Anthropic API key, tolerating the ANTHORPIC misspelling.

    Sets a normalized ANTHROPIC_API_KEY in the environment so the Anthropic SDK
    (used by Inspect) can find it. Raises if no key is present.
    """
    load_dotenv()
    key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHORPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY in your environment or .env."
        )
    os.environ["ANTHROPIC_API_KEY"] = key
    return key


# Which provider (and thus which API key) each agent CLI talks to.
AGENT_PROVIDER = {
    "claude_code": "anthropic",
    "codex_cli": "openai",
    "gemini_cli": "google",
}
_PROVIDER_KEY_ENV = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GEMINI_API_KEY",
}


def provider_for_agent(agent: str) -> str:
    """The model provider an agent CLI uses (default anthropic)."""
    return AGENT_PROVIDER.get(agent, "anthropic")


def ensure_provider_key(provider: str) -> str:
    """Ensure the API key for `provider` is present (loading .env). Raises if missing."""
    if provider == "anthropic":
        return ensure_anthropic_key()
    load_dotenv()
    env = _PROVIDER_KEY_ENV.get(provider)
    key = os.environ.get(env) if env else None
    if not key:
        raise RuntimeError(
            f"No API key for provider {provider!r}. Set {env} in your environment or .env."
        )
    return key


# YAML config loading.
def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=None)
def load_models_config(provider: str = "anthropic") -> dict[str, Any]:
    return _load_yaml(CONFIGS_DIR / "models" / f"{provider}.yaml")


@lru_cache(maxsize=None)
def load_agent_config(agent: str = "claude_code") -> dict[str, Any]:
    return _load_yaml(CONFIGS_DIR / "agents" / f"{agent}.yaml")


@lru_cache(maxsize=None)
def load_scoring_config(name: str = "default") -> dict[str, Any]:
    return _load_yaml(CONFIGS_DIR / "scoring" / f"{name}.yaml")


def included_models(provider: str = "anthropic") -> dict[str, dict[str, Any]]:
    """Return the {model_id: spec} mapping for models flagged include: true."""
    cfg = load_models_config(provider)
    models = cfg.get("models", {})
    return {mid: spec for mid, spec in models.items() if spec.get("include")}


def model_spec(model_id: str, provider: str = "anthropic") -> dict[str, Any]:
    cfg = load_models_config(provider)
    spec = cfg.get("models", {}).get(model_id)
    if spec is None:
        raise KeyError(f"Model {model_id!r} not found in {provider} model config")
    return spec
