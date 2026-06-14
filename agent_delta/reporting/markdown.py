"""Render an aggregated report dict as Markdown.

The report is presented as two levels of assessment:
  Level 1 (SPEC.md): the primary ranking and which gains are real and material.
  Level 2 (SPEC-ADDENDUM.md): for ONLY those material gains, whether the gain is
  intrinsic capability or agentic amplification.
"""

from __future__ import annotations

import math
from typing import Any


def _n(x: Any, fmt: str = "{:.1f}", dash: str = "n/a") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return dash
    try:
        return fmt.format(x)
    except (ValueError, TypeError):
        return str(x)


def _pct(x: Any) -> str:
    return "n/a" if x is None else f"{x * 100:.0f}%"


def _cost(x: Any) -> str:
    return "n/a" if x is None else f"${x:.2f}"


def _time(x: Any) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x / 60:.1f}m" if x >= 60 else f"{x:.0f}s"


def _ratio(x: Any) -> str:
    return "n/a" if x is None else f"{x:.2f}x"


def render(report: dict, levels: tuple[int, ...] = (1, 2)) -> str:
    L: list[str] = []
    L.append(f"# AgentDelta report: {report['suite']}")
    L.append("")
    L.append(f"Benchmark version: {report['benchmark_version']}  ")
    L.append(f"Agent: {report.get('agent')}  ")
    L.append(f"Tasks: {report['n_tasks']} | Runs: {report['n_runs']} "
             f"(invalid: {report['n_invalid']})  ")
    L.append(f"Models: {', '.join(report['models'])}  ")
    L.append(f"Modes: {', '.join(report['modes'])}")
    L.append("")

    for mode, data in report["per_mode"].items():
        L.append(f"## Mode: {mode}")
        L.append("")
        if 1 in levels:
            _render_level1(L, data)
        if 2 in levels:
            _render_level2(L, data)

    if 2 in levels and report.get("cross_mode"):
        _render_cross_mode(L, report["cross_mode"])

    invalid = report.get("invalid_runs") or []
    if invalid:
        L.append("## Invalid runs (reported separately, excluded from ranking)")
        L.append("")
        L.append(f"{len(invalid)} run(s) were invalid (SPEC 11.4): broken baseline, "
                 "model fallback, or infrastructure crash.")
        L.append("")
        L.append("| Run | Model | Reason |")
        L.append("| --- | --- | --- |")
        for r in invalid:
            L.append(f"| {r['run_id']} | {r['model_id']} | {r.get('reason') or 'unknown'} |")
        L.append("")

    if report.get("limitations"):
        L.append("## Limitations")
        L.append("")
        for lim in report["limitations"]:
            L.append(f"- {lim}")
        L.append("")

    return "\n".join(L)


def _ordered(data: dict) -> list[dict]:
    return [data["models"][mid] for mid in data["level1"]["ranking"]]


def _render_level1(L: list[str], data: dict) -> None:
    models = _ordered(data)
    L.append("### Level 1: Primary Assessment (SPEC.md)")
    L.append("")
    L.append("Which model-agent system performs best, by objective evidence.")
    L.append("")

    L.append("#### Primary ranking")
    L.append("")
    L.append("| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |")
    L.append("| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for m in models:
        lo, hi = m["success_ci95"]
        L.append(
            f"| {m['rank']} | {m['model_id']} | {_n(m['objective_score'])} | "
            f"{_pct(m['success_rate'])} ({_pct(lo)}-{_pct(hi)}) | {_pct(m['hidden_test_rate'])} | "
            f"{_pct(m['regression_rate'])} | {_cost(m['cost_per_success_usd'])} | "
            f"{_time(m['median_time_to_success_s'])} |"
        )
    L.append("")

    # Failure taxonomy per model (SPEC 23).
    rows = [(m["model_id"], m.get("failure_labels") or {}) for m in models]
    if any(labels for _, labels in rows):
        L.append("#### Failure taxonomy (valid failed runs)")
        L.append("")
        L.append("| Model | Failure labels (count) |")
        L.append("| --- | --- |")
        for mid, labels in rows:
            cell = ", ".join(f"{k} ({v})" for k, v in labels.items()) if labels else "none"
            L.append(f"| {mid} | {cell} |")
        L.append("")

    improvements = data["level1"]["improvements"]
    if improvements:
        baseline = data["level1"]["baseline"]
        L.append(f"#### Material improvements over baseline (`{baseline}`)")
        L.append("")
        L.append("A gain is material only if success improves by at least the configured "
                 "threshold and the paired McNemar test is significant. Only material gains "
                 "are escalated to Level 2.")
        L.append("")
        L.append("| Model B | Success delta | Objective delta | Material? | Reason |")
        L.append("| --- | ---: | ---: | :---: | --- |")
        for imp in improvements:
            mark = "yes" if imp["material"] else "no"
            L.append(
                f"| {imp['model_b']} | {imp['success_delta_pp']:+.1f} pp | "
                f"{imp['objective_delta']:+.1f} | {mark} | {imp['materiality_reason']} |"
            )
        L.append("")

    _render_category(L, models)
    _render_frontiers(L, data)
    _render_diagnostics(L, models)
    _render_full_score(L, models)


def _render_category(L: list[str], models: list[dict]) -> None:
    cats = sorted({c for m in models for c in (m.get("category_success") or {})})
    if not cats:
        return
    L.append("#### Category breakdown (success rate)")
    L.append("")
    L.append("| Model | " + " | ".join(cats) + " |")
    L.append("| --- |" + " ---: |" * len(cats))
    for m in models:
        cs = m.get("category_success") or {}
        cells = " | ".join(_pct(cs.get(c)) if c in cs else "-" for c in cats)
        L.append(f"| {m['model_id']} | {cells} |")
    L.append("")


def _render_frontiers(L: list[str], data: dict) -> None:
    for title, key in [("Cost-success frontier", "cost_frontier"),
                       ("Latency-success frontier", "latency_frontier")]:
        points = data.get(key) or []
        if not any(p.get("x") is not None for p in points):
            continue
        axis = "Cost/success" if key == "cost_frontier" else "Median time"
        fmt = _cost if key == "cost_frontier" else _time
        L.append(f"#### {title}")
        L.append("")
        L.append(f"| Model | {axis} | Success | On frontier |")
        L.append("| --- | ---: | ---: | :---: |")
        for p in sorted(points, key=lambda q: (q["x"] is None, q["x"] or 0)):
            L.append(f"| {p['model_id']} | {fmt(p['x'])} | {_pct(p['y'])} | "
                     f"{'yes' if p.get('on_frontier') else 'no'} |")
        L.append("")


def _render_diagnostics(L: list[str], models: list[dict]) -> None:
    if not any(m.get("diagnostics") for m in models):
        return
    L.append("#### Diagnostics")
    L.append("")
    L.append("| Model | Failed-cmd ratio | Explore/edit | Timeout rate | "
             "First edit (s) | First test (s) | Diff locality | Patch entropy |")
    L.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for m in models:
        d = m.get("diagnostics") or {}
        L.append(
            f"| {m['model_id']} | {_n(d.get('failed_command_ratio'), '{:.2f}')} | "
            f"{_n(d.get('exploration_edit_ratio'), '{:.2f}')} | {_pct(d.get('timeout_rate'))} | "
            f"{_n(d.get('mean_time_to_first_edit_s'), '{:.0f}')} | "
            f"{_n(d.get('mean_time_to_first_test_s'), '{:.0f}')} | "
            f"{_n(d.get('mean_diff_locality'), '{:.2f}')} | "
            f"{_n(d.get('mean_patch_entropy'), '{:.2f}')} |"
        )
    L.append("")


def _render_full_score(L: list[str], models: list[dict]) -> None:
    if not any(m.get("review_score") is not None for m in models):
        return
    L.append("#### Full score (with blinded review, SPEC 14.2)")
    L.append("")
    L.append("| Model | Objective | Review (0-100) | Full (95/5) |")
    L.append("| --- | ---: | ---: | ---: |")
    for m in models:
        L.append(f"| {m['model_id']} | {_n(m['objective_score'])} | "
                 f"{_n(m.get('review_score'))} | {_n(m.get('full_score'))} |")
    L.append("")


def _render_level2(L: list[str], data: dict) -> None:
    models = _ordered(data)
    level2 = data["level2"]
    L.append("### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)")
    L.append("")
    L.append("For the material Level 1 gains only: is the improvement intrinsic model "
             "capability, or does the newer model mainly do more work by default "
             "(more tokens, time, tool calls, retries, self-review)?")
    L.append("")

    comps = level2.get("work_index_components") or []
    L.append(f"Agentic Work Index components in use: {', '.join(comps) if comps else 'none'}.")
    L.append("")
    L.append("#### Resource use and Agentic Work Index")
    L.append("")
    L.append("| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |")
    L.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for m in models:
        L.append(
            f"| {m['model_id']} | {_n(m['tokens_total_mean'], '{:,.0f}')} | "
            f"{_cost(m['cost_mean_usd'])} | {_time(m['median_time_to_success_s'])} | "
            f"{_n((m['work'] or {}).get('file_edits'), '{:.1f}')} | {_n(m.get('work_index'))} |"
        )
    L.append("")

    L.append("#### Efficiency")
    L.append("")
    L.append("| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |")
    L.append("| --- | ---: | ---: | ---: | ---: |")
    for m in models:
        L.append(
            f"| {m['model_id']} | {_n(m['objective_score'])} | "
            f"{_n(m.get('quality_per_dollar'))} | {_n(m.get('quality_per_minute'))} | "
            f"{_n(m.get('quality_per_work_unit'), '{:.2f}')} |"
        )
    L.append("")

    assessments = level2.get("assessments") or []
    excluded = level2.get("excluded") or []
    if not assessments:
        L.append("No material Level 1 gains were escalated to amplification analysis"
                 + (f" ({len(excluded)} comparison(s) excluded as non-material)." if excluded else "."))
        L.append("")
        _render_excluded(L, excluded)
        return

    baseline = level2.get("baseline")
    L.append(f"#### Amplification of material gains (baseline `{baseline}`)")
    L.append("")
    L.append("| Model B | Success delta | Token amp | Cost amp | Time amp | Work amp | Classification |")
    L.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for a in assessments:
        r = a["ratios"]
        L.append(
            f"| {a['model_b']} | {a['success_delta_pp']:+.1f} pp | "
            f"{_ratio(r.get('token_amplification'))} | {_ratio(r.get('cost_amplification'))} | "
            f"{_ratio(r.get('time_amplification'))} | {_ratio(r.get('work_index_amplification'))} | "
            f"{a['classification']['category']} |"
        )
    L.append("")
    for a in assessments:
        cls = a["classification"]
        L.append(f"**{a['model_b']} vs {a['model_a']}: {cls['category']}**")
        L.append("")
        for reason in cls["rationale"]:
            L.append(f"- {reason}")
        if cls["red_flags"]:
            L.append(f"- Red flags (ratio >= 2.0): {', '.join(cls['red_flags'])}")
        cw = a.get("cost_wilcoxon")
        if cw and cw.get("n"):
            L.append(f"- Paired cost difference (Wilcoxon over {cw['n']} pairs): "
                     f"p = {cw['p_value']:.3f}.")
        tw = a.get("time_wilcoxon")
        if tw and tw.get("n"):
            L.append(f"- Paired time difference (Wilcoxon over {tw['n']} pairs): "
                     f"p = {tw['p_value']:.3f}.")
        qd = a.get("quality_delta_per_extra_dollar")
        if qd is not None:
            L.append(f"- Quality delta per extra dollar: {qd:.1f}")
        if cls["modes_missing"]:
            L.append(f"- To confirm intrinsic vs workflow-equivalent, run: "
                     f"{', '.join(cls['modes_missing'])} mode(s).")
        L.append("")
    _render_excluded(L, excluded)


def _render_cross_mode(L: list[str], cross: dict) -> None:
    assessments = cross.get("assessments") or []
    L.append("## Cross-Mode Synthesis (Level 2 definitive)")
    L.append("")
    L.append(f"Modes available: {', '.join(cross.get('modes_present') or [])}. "
             "Each material Default-Mode gain is re-checked across the normalized modes "
             "to decide whether it is intrinsic, amplified, or workflow-equivalent.")
    L.append("")
    if not assessments:
        L.append("No material Default-Mode gains to synthesize.")
        L.append("")
        return
    for a in assessments:
        L.append(f"### {a['model_b']} vs {a['model_a']}: {a['category']} ({a['confidence']})")
        L.append("")
        L.append("| Mode | A success | B success | Gap | Material? |")
        L.append("| --- | ---: | ---: | ---: | :---: |")
        for row in a["by_mode"]:
            L.append(
                f"| {row['mode']} | {_pct(row['a_success_rate'])} | {_pct(row['b_success_rate'])} | "
                f"{row['delta_pp']:+.1f} pp | {'yes' if row['material'] else 'no'} |"
            )
        L.append("")
        for ev in a["evidence"]:
            L.append(f"- {ev}")
        L.append("")


def _render_excluded(L: list[str], excluded: list) -> None:
    if not excluded:
        return
    L.append("#### Not escalated to Level 2 (non-material)")
    L.append("")
    for e in excluded:
        L.append(f"- {e['model_b']} vs {e['model_a']}: {e['reason']}.")
    L.append("")
