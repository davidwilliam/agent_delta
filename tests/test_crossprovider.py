"""Tests for the cross-provider comparison panel and its computed JSON block."""

from agent_delta.reporting.html import _tab_crossprovider, build_cross_provider

AN = ["claude-opus-4-8", "claude-opus-4-7", "claude-opus-4-6", "claude-sonnet-4-6"]
OA = ["gpt-5.4", "gpt-5.1-2025-11-13", "gpt-5", "gpt-5-mini-2025-08-07"]


def _rec(model, task, v=True, invalid=False):
    return {
        "model_id": model, "task_id": task, "hardness_level": "H5",
        "scoring": {"verified_success": v},
        "usage": {"estimated_cost_usd": 0.1},
        "execution": {"wall_clock_seconds": 60, "invalid": invalid},
    }


def test_needs_two_providers():
    out = _tab_crossprovider([_rec(m, "t1") for m in AN])
    assert 'id="crossprovider"' in out
    assert "second provider" in out.lower()


def test_shared_tasks_only_when_both_have_full_cohort():
    recs = []
    for t in ["t1", "t2"]:                       # both providers, 4 models each -> shared
        recs += [_rec(m, t) for m in AN + OA]
    recs += [_rec(m, "t3") for m in AN]          # anthropic only -> NOT shared
    out = _tab_crossprovider(recs)
    assert 'id="crossprovider"' in out
    assert "<strong>2 tasks</strong>" in out     # t1, t2
    assert "Anthropic" in out and "OpenAI" in out


def test_invalid_runs_excluded():
    recs = []
    for t in ["t1"]:
        recs += [_rec(m, t) for m in AN + OA]
    recs.append(_rec("gpt-5.4", "t1", invalid=True))  # ignored
    out = _tab_crossprovider(recs)
    assert "<strong>1 tasks</strong>" in out


def test_build_cross_provider_returns_serializable_dict():
    import json
    recs = []
    for t in ["t1", "t2"]:
        recs += [_rec(m, t) for m in AN + OA]
    cp = build_cross_provider(recs)
    assert cp["shared_task_count"] == 2
    assert {p["id"] for p in cp["providers"]} == {"anthropic", "openai"}
    assert len(cp["models"]) == 8
    pt = cp["per_task"][0]["providers"]
    assert pt["anthropic"]["verified_rate"] == 1.0 and pt["openai"]["verified_rate"] == 1.0
    json.dumps(cp)  # serializable for the export


def test_build_cross_provider_none_without_two_providers():
    assert build_cross_provider([_rec(m, "t1") for m in AN]) is None


def test_html_panel_and_json_block_share_the_computation():
    # The HTML panel reflects the same shared-task count the dict reports.
    recs = []
    for t in ["t1", "t2", "t3"]:
        recs += [_rec(m, t) for m in AN + OA]
    cp = build_cross_provider(recs)
    out = _tab_crossprovider(recs)
    assert f'<strong>{cp["shared_task_count"]} tasks</strong>' in out
