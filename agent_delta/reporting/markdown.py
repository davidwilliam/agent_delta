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
        qd = a.get("quality_delta_per_extra_dollar")
        if qd is not None:
            L.append(f"- Quality delta per extra dollar: {qd:.1f}")
        if cls["modes_missing"]:
            L.append(f"- To confirm intrinsic vs workflow-equivalent, run: "
                     f"{', '.join(cls['modes_missing'])} mode(s).")
        L.append("")
    _render_excluded(L, excluded)


def _render_excluded(L: list[str], excluded: list) -> None:
    if not excluded:
        return
    L.append("#### Not escalated to Level 2 (non-material)")
    L.append("")
    for e in excluded:
        L.append(f"- {e['model_b']} vs {e['model_a']}: {e['reason']}.")
    L.append("")
