"""Cross-mode synthesis (SPEC-ADDENDUM sections 5, 8, 10.5).

Default Mode alone can only label a gain "provisional". This compares the same
Model B over Model A gain across the normalized modes to reach a definitive
classification:

  * Equal-Budget shrinks the gain  -> Agentic Amplification (it was extra budget).
  * Matched-Workflow / Strong-Spec shrinks it -> Workflow-Equivalent (the older
    model catches up given the process or spec the newer one applies by default).
  * Equal-Budget keeps the gain     -> Intrinsic Capability.

Only gains that Level 1 found material in Default Mode are synthesized, preserving
the narrowing of the two-level design.
"""

from __future__ import annotations


def _success(per_mode: dict, mode: str, model: str) -> float | None:
    m = per_mode.get(mode, {}).get("models", {}).get(model)
    return m["success_rate"] if m else None


def synthesize_cross_mode(per_mode: dict, baseline: str, materiality_pp: float) -> dict:
    """Definitive classification of material Default-Mode gains across modes."""
    modes = list(per_mode)
    default = per_mode.get("default")
    if not default or not baseline:
        return {"baseline": baseline, "modes_present": modes, "assessments": []}

    material_b = {
        imp["model_b"] for imp in default["level1"]["improvements"] if imp["material"]
    }

    assessments = []
    for b_model in sorted(material_b):
        by_mode = []
        deltas: dict[str, float] = {}
        for mode in modes:
            a_sr = _success(per_mode, mode, baseline)
            b_sr = _success(per_mode, mode, b_model)
            if a_sr is None or b_sr is None:
                continue
            delta = (b_sr - a_sr) * 100.0
            deltas[mode] = delta
            by_mode.append({
                "mode": mode,
                "a_success_rate": a_sr,
                "b_success_rate": b_sr,
                "delta_pp": delta,
                "material": delta >= materiality_pp,
            })
        category, evidence, confidence = _classify(deltas, materiality_pp)
        # Cost-matched practical note.
        cm = deltas.get("cost_matched")
        if cm is not None and cm < materiality_pp:
            evidence.append(
                f"Under Cost-Matched Mode the gap is {cm:+.1f} pp, so `{baseline}` is "
                "competitive or better at equal cost."
            )
        assessments.append({
            "model_b": b_model,
            "model_a": baseline,
            "by_mode": by_mode,
            "category": category,
            "evidence": evidence,
            "confidence": confidence,
        })
    return {"baseline": baseline, "modes_present": modes, "assessments": assessments}


_WORKFLOW_MODES = [
    ("matched_workflow", "Matched-Workflow Mode"),
    ("strong_spec", "Strong-Spec Mode"),
    ("older_plus_scaffold", "Older-Model-Plus-Scaffold Mode"),
]


def _classify(deltas: dict[str, float], m: float) -> tuple[str, list[str], str]:
    default_d = deltas.get("default")
    eq = deltas.get("equal_budget")
    evidence: list[str] = []

    def line(mode_name: str, d: float) -> str:
        return f"{mode_name}: gap {d:+.1f} pp ({'persists' if d >= m else 'shrinks below ' + str(m) + ' pp'})."

    if default_d is not None:
        evidence.append(f"Default Mode: gap {default_d:+.1f} pp.")

    if eq is not None and eq < m:
        evidence.append(line("Equal-Budget Mode", eq))
        return ("Agentic Amplification Gain", evidence, "confirmed")

    # Workflow-equivalent: the older model closes the gap given process or spec
    # (Matched-Workflow, Strong-Spec, or an explicit scaffold).
    wf_shrinks = [(name, deltas[key]) for key, name in _WORKFLOW_MODES
                  if key in deltas and deltas[key] < m]
    if wf_shrinks:
        for name, d in wf_shrinks:
            evidence.append(line(name, d))
        return ("Workflow-Equivalent Gain", evidence, "confirmed")

    if eq is not None and eq >= m:
        evidence.append(line("Equal-Budget Mode", eq))
        for key, name in _WORKFLOW_MODES:
            if key in deltas:
                evidence.append(line(name, deltas[key]))
        return ("Intrinsic Capability Gain", evidence, "confirmed")

    evidence.append("No normalized mode (Equal-Budget, Matched-Workflow, Strong-Spec, "
                    "Older-Model-Plus-Scaffold) available; classification stays provisional.")
    return ("Provisional (run normalized modes)", evidence, "provisional")
