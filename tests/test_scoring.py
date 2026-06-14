"""Unit tests for objective scoring, statistics, and amplification classification."""

import math

from agent_delta.scoring import amplification as amp
from agent_delta.scoring import stats as st
from agent_delta.scoring.objective import (
    ObjectiveComponents,
    objective_score,
    partial_objective_score,
)

CFG = {
    "red_flags": {
        "token_amplification": 2.0, "cost_amplification": 2.0, "time_amplification": 2.0,
        "tool_amplification": 2.0, "retry_amplification": 2.0, "test_amplification": 2.0,
        "api_amplification": 2.0, "work_index_amplification": 2.0,
    },
    "modest_quality_gain_pp": 5,
}


def test_partial_objective_perfect():
    c = ObjectiveComponents(1.0, 1.0, 1.0, 1.0)
    assert partial_objective_score(c) == 100.0


def test_partial_objective_only_success():
    # success weight 0.60 of the 0.90 absolute mass -> 66.67.
    c = ObjectiveComponents(1.0, 0.0, 0.0, 0.0)
    assert round(partial_objective_score(c), 2) == 66.67


def test_objective_score_full_with_efficiency():
    c = ObjectiveComponents(1.0, 1.0, 1.0, 1.0)
    assert objective_score(c, cost_efficiency=1.0, time_efficiency=1.0) == 100.0
    # Worst cost/time efficiency removes the 0.10 cost+time mass.
    assert objective_score(c, 0.0, 0.0) == 90.0


def test_wilson_ci_bounds():
    lo, hi = st.wilson_ci(8, 10)
    assert 0.0 <= lo < 0.8 < hi <= 1.0


def test_mcnemar_significant_when_one_sided():
    a = [True] * 2 + [False] * 8
    b = [True] * 10  # B wins the 8 discordant pairs, A wins none
    r = st.mcnemar(a, b)
    assert r.b_only == 8 and r.a_only == 0
    assert r.p_value < 0.05


def test_classify_no_material_gain():
    cls = amp.classify_improvement(
        {}, {}, {"cost_amplification": 1.1}, CFG,
        success_material=False, success_delta_pp=2.0,
    )
    assert cls.category == "No Material Gain"


def test_classify_cost_inefficient():
    # Small (3pp) gain but 3x cost -> cost-inefficient.
    ratios = {"cost_amplification": 3.0, "time_amplification": 1.2}
    cls = amp.classify_improvement(
        {}, {}, ratios, CFG, success_material=True, success_delta_pp=3.0,
    )
    assert cls.category == "Cost-Inefficient Gain"


def test_classify_intrinsic_when_no_amplification():
    ratios = {k: 1.1 for k in CFG["red_flags"]}
    cls = amp.classify_improvement(
        {}, {}, ratios, CFG, success_material=True, success_delta_pp=12.0,
    )
    assert cls.category.startswith("Intrinsic")
    assert not cls.red_flags


def test_wilcoxon_detects_consistent_difference():
    # B consistently higher than A -> small p-value.
    b = [10, 11, 12, 13, 14, 15, 16, 17]
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    r = st.wilcoxon_signed_rank(b, a)
    assert r["n"] == 8
    assert r["p_value"] < 0.05


def test_wilcoxon_no_difference():
    r = st.wilcoxon_signed_rank([1, 2, 3], [1, 2, 3])
    assert r["n"] == 0 and r["p_value"] == 1.0


def test_holm_correction_monotone_and_scaled():
    corrected = st.holm_correction({"a": 0.01, "b": 0.04, "c": 0.04})
    # Smallest gets multiplied by m (3); order preserved and non-decreasing.
    assert corrected["a"] == 0.03
    assert corrected["b"] >= corrected["a"] and corrected["c"] >= corrected["a"]
    assert all(0 <= v <= 1 for v in corrected.values())


def test_agentic_work_index_scales_to_100():
    work = {
        "A": {"input_tokens": 100, "output_tokens": 10, "wall_clock_seconds": 100},
        "B": {"input_tokens": 500, "output_tokens": 50, "wall_clock_seconds": 500},
    }
    weights = {"input_tokens": 0.15, "output_tokens": 0.15, "wall_clock_seconds": 0.15}
    awi, present = amp.agentic_work_index(work, weights)
    assert awi["B"] == 100.0
    assert math.isclose(awi["A"], 20.0)
    assert set(present) == {"input_tokens", "output_tokens", "wall_clock_seconds"}
