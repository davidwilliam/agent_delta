"""Tests for cross-mode synthesis classification (SPEC-ADDENDUM 8)."""

from agent_delta.scoring.synthesis import synthesize_cross_mode

M = 5.0  # materiality threshold in percentage points


def _per_mode(success_by_mode: dict[str, tuple[float, float]], b="B", a="A") -> dict:
    """Minimal per_mode dict: {mode: (a_success_rate, b_success_rate)}."""
    pm = {}
    for mode, (a_sr, b_sr) in success_by_mode.items():
        pm[mode] = {"models": {a: {"success_rate": a_sr}, b: {"success_rate": b_sr}}}
    pm["default"]["level1"] = {"improvements": [{"model_b": b, "material": True}]}
    return pm


def _classify(success_by_mode):
    out = synthesize_cross_mode(_per_mode(success_by_mode), "A", M)
    return out["assessments"][0]


def test_amplification_when_equal_budget_shrinks():
    a = _classify({"default": (0.80, 1.00), "equal_budget": (0.80, 0.84)})
    assert a["category"] == "Agentic Amplification Gain"
    assert a["confidence"] == "confirmed"


def test_intrinsic_when_equal_budget_persists():
    a = _classify({
        "default": (0.80, 1.00),
        "equal_budget": (0.80, 0.98),
        "matched_workflow": (0.80, 0.97),
    })
    assert a["category"] == "Intrinsic Capability Gain"


def test_workflow_equivalent_when_matched_workflow_shrinks():
    a = _classify({"default": (0.80, 1.00), "matched_workflow": (0.80, 0.83)})
    assert a["category"] == "Workflow-Equivalent Gain"


def test_provisional_when_only_default():
    a = _classify({"default": (0.80, 1.00)})
    assert a["category"].startswith("Provisional")
    assert a["confidence"] == "provisional"


def test_cost_matched_note_added():
    a = _classify({
        "default": (0.80, 1.00),
        "equal_budget": (0.80, 0.98),
        "cost_matched": (0.80, 0.79),
    })
    assert any("Cost-Matched" in e for e in a["evidence"])


def test_only_material_default_gains_synthesized():
    pm = _per_mode({"default": (0.80, 0.82), "equal_budget": (0.80, 0.81)})
    pm["default"]["level1"]["improvements"][0]["material"] = False
    out = synthesize_cross_mode(pm, "A", M)
    assert out["assessments"] == []
