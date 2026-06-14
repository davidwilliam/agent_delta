"""Render an aggregated report dict as Markdown (SPEC 17 + ADDENDUM 9, 10)."""

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


def render(report: dict) -> str:
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
        _render_mode(L, mode, data)

    if report.get("limitations"):
        L.append("## Limitations")
        L.append("")
        for lim in report["limitations"]:
            L.append(f"- {lim}")
        L.append("")

    return "\n".join(L)


def _ordered(data: dict) -> list[dict]:
    return [data["models"][mid] for mid in data["ranking"]]


def _render_mode(L: list[str], mode: str, data: dict) -> None:
    models = _ordered(data)
    L.append(f"## Mode: {mode}")
    L.append("")

    # Primary ranking table (SPEC 17.1).
    L.append("### Primary ranking")
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

    # Resource amplification table (ADDENDUM 10.2).
    L.append("### Resource use and Agentic Work Index")
    L.append("")
    comps = data.get("work_index_components") or []
    L.append(f"Agentic Work Index components in use: {', '.join(comps) if comps else 'none'}.")
    L.append("")
    L.append("| Model | Mean tokens | Cost/Success | Median Time | Files edited | Work Index |")
    L.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for m in models:
        L.append(
            f"| {m['model_id']} | {_n(m['tokens_total_mean'], '{:,.0f}')} | "
            f"{_cost(m['cost_per_success_usd'])} | {_time(m['median_time_to_success_s'])} | "
            f"{_n((m['work'] or {}).get('file_edits'), '{:.1f}')} | {_n(m.get('work_index'))} |"
        )
    L.append("")

    # Efficiency table (ADDENDUM 10.3).
    L.append("### Efficiency")
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

    _render_amplification(L, data)


def _render_amplification(L: list[str], data: dict) -> None:
    L.append("### Agentic Amplification Analysis")
    L.append("")
    baseline = data.get("baseline")
    comparisons = data.get("comparisons") or []
    if not comparisons:
        L.append("Only one model present; no amplification comparison.")
        L.append("")
        return
    L.append(f"Baseline (Model A): `{baseline}`. Each row compares a newer model B "
             f"against this baseline.")
    L.append("")
    L.append("| Model B | Success delta | Objective delta | Token amp | Cost amp | Time amp | Classification |")
    L.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for c in comparisons:
        r = c["ratios"]
        L.append(
            f"| {c['model_b']} | {c['success_delta_pp']:+.1f} pp | {c['objective_delta']:+.1f} | "
            f"{_ratio(r.get('token_amplification'))} | {_ratio(r.get('cost_amplification'))} | "
            f"{_ratio(r.get('time_amplification'))} | {c['classification']['category']} |"
        )
    L.append("")
    for c in comparisons:
        cls = c["classification"]
        L.append(f"**{c['model_b']} vs {baseline}: {cls['category']}**")
        L.append("")
        for reason in cls["rationale"]:
            L.append(f"- {reason}")
        if cls["red_flags"]:
            L.append(f"- Red flags (ratio >= 2.0): {', '.join(cls['red_flags'])}")
        qd = c.get("quality_delta_per_extra_dollar")
        if qd is not None:
            L.append(f"- Quality delta per extra dollar: {qd:.1f}")
        if cls["modes_missing"]:
            L.append(f"- To confirm, run: {', '.join(cls['modes_missing'])} mode(s).")
        paired = c.get("paired")
        if paired:
            L.append(f"- Paired McNemar over {paired['n_pairs']} pairs: "
                     f"p = {paired['p_value']:.3f} (B-only wins {paired['b_only']}, "
                     f"A-only wins {paired['a_only']}).")
        L.append("")
