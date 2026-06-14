"""Run validity and model-fallback detection (SPEC sections 11.4, 5.5).

A run is invalid (not a fair measure of the model on the task) when the baseline
was broken before the agent ran, the served model was not the requested pinned
model (silent fallback), or the agent crashed for infrastructure reasons. Invalid
runs are reported separately and excluded from rankings, never silently dropped.
"""

from __future__ import annotations


def normalize_model(name: str | None) -> str:
    """Strip the provider prefix: 'anthropic/claude-opus-4-8' -> 'claude-opus-4-8'."""
    return (name or "").split("/")[-1]


def assess_validity(
    *,
    requested_model: str,
    served_models: set[str],
    sample_error: str | None,
    baseline_pre_ok: bool | None,
) -> tuple[bool, str | None]:
    """Return (invalid, reason). reason is None when the run is valid.

    served_models is the set of models actually billed in the transcript
    (normalized). Empty (for example in dry-run) disables fallback detection.
    """
    if baseline_pre_ok is False:
        return True, "baseline_failed_pre_run"

    served = {normalize_model(m) for m in served_models if m}
    if served and requested_model and requested_model not in served:
        return True, f"model_fallback: requested {requested_model}, served {sorted(served)}"

    if sample_error:
        return True, f"{_error_category(sample_error)}: {sample_error[:200]}"

    return False, None


def _error_category(err: str) -> str:
    """Classify a sample error into a SPEC 11.4 invalid reason."""
    low = err.lower()
    if "credit balance" in low or "billing" in low or "quota" in low:
        return "provider_error_billing"
    if "rate_limit" in low or "rate limit" in low or "429" in low:
        return "rate_limited"
    if "overloaded" in low or "529" in low:
        return "provider_overloaded"
    if "authentication" in low or "401" in low or "invalid x-api-key" in low:
        return "provider_auth_error"
    if "model proxy" in low or "proxy" in low:
        return "model_proxy_error"
    return "agent_crash"
