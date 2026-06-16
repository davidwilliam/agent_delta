"""Render a comprehensive, self-contained HTML report across every suite.

Unlike the per-suite Markdown report, this combines all evaluated suites into a
single tabbed document: a results-first overview, per-model and per-suite detail,
the full statistical apparatus, every raw run with all metrics, the methodology,
and the reproducibility manifest. The output is one standalone .html file with
inline CSS, inline SVG charts, and a few lines of vanilla JS for the tabs (no
external assets, no network), so it opens anywhere and can be archived as-is.
"""

from __future__ import annotations

import html
import math
import statistics
from collections import defaultdict
from typing import Any

ACCENT = "#c75b39"
GOOD = "#2f7d5b"
WARN = "#b58900"
BAD = "#b3322c"

REPO_URL = "https://github.com/davidwilliam/agent_delta"

# The report's sections, in order. Single source of truth for both the HTML
# sidebar and the website JSON export (agent_delta/reporting/json_export.py).
# Labels are PLAIN text here; the HTML renderer escapes them, the JSON emits them
# as-is. Add, rename, or reorder a section by editing this one list.
REPORT_SECTIONS: list[tuple[str, str]] = [
    ("overview", "Results"),
    ("models", "Per-model"),
    ("crossprovider", "Cross-provider"),
    ("suites", "Per-suite"),
    ("stats", "Statistics"),
    ("raw", "Raw runs"),
    ("methodology", "Methodology"),
    ("stack", "Stack & requirements"),
    ("repro", "Reproducibility"),
    ("about", "About"),
]

# Provider identity, used for the JSON export's provider index and the report's
# provider filter. Treated as a stable public vocabulary.
PROVIDER_LABELS = {
    "anthropic": "Anthropic (Claude Code)",
    "openai": "OpenAI (Codex CLI)",
    "google": "Google (Gemini CLI)",
}


def model_provider(model_id: str) -> str:
    """Infer the provider from a model id (claude-* / gpt-* / gemini-*)."""
    m = (model_id or "").lower()
    if m.startswith("claude"):
        return "anthropic"
    if m.startswith(("gpt", "o1", "o3", "o4")):
        return "openai"
    if m.startswith("gemini"):
        return "google"
    return "unknown"


# Third-party components AgentDelta builds on. Cited with a link and a one-line
# explanation wherever they appear in the report (the user should never hit an
# unexplained tool name).
TOOLS = {
    "Inspect AI": ("https://inspect.aisi.org.uk/",
        "The UK AI Safety Institute's open-source LLM evaluation framework. It drives each "
        "task: provisioning the sandbox, invoking the solver, scoring, and writing the eval log."),
    "inspect_swe": ("https://pypi.org/project/inspect-swe/",
        "An Inspect AI extension that runs real software-engineering agents as the solver. "
        "AgentDelta uses it to run the Claude Code and Codex CLI agents inside the sandbox."),
    "Claude Code": ("https://docs.claude.com/en/docs/claude-code/overview",
        "Anthropic's agentic coding CLI (one of the agents under test). It reads files, runs "
        "shell commands, edits code, and iterates on test feedback autonomously."),
    "Codex CLI": ("https://developers.openai.com/codex/cli/",
        "OpenAI's agentic coding CLI (the second agent under test), driven the same way as "
        "Claude Code and graded by the same hidden tests, selectable per run with --agent."),
    "Anthropic API": ("https://docs.claude.com/en/api/overview",
        "Serves the pinned Claude models (opus-4-8 / 4-7 / 4-6 and sonnet-4-6) the Claude Code agent calls."),
    "OpenAI API": ("https://developers.openai.com/api/docs/",
        "Serves the pinned GPT-5 models (gpt-5.4 / 5.1 / 5 / 5-mini) the Codex CLI agent calls."),
    "Gemini CLI": ("https://github.com/google-gemini/gemini-cli",
        "Google's agentic coding CLI, available via inspect_swe and planned as a third provider."),
    "Docker": ("https://www.docker.com/",
        "Provides one isolated sandbox container per fixture, pinned by image digest so every "
        "run starts from a byte-identical repository state."),
    "pytest": ("https://docs.pytest.org/",
        "Runs the baseline, public, and hidden Python test suites that grade a run."),
    "Node.js test runner": ("https://nodejs.org/api/test.html",
        "The built-in <code>node --test</code> runner executes the TypeScript fixture's tests "
        "against the compiled output."),
    "TypeScript": ("https://www.typescriptlang.org/",
        "One fixture is a TypeScript library compiled with <code>tsc</code>, giving cross-language coverage."),
    "Go": ("https://go.dev/",
        "<code>go test</code> runs the Go fixture's tests; a third language alongside Python and TypeScript."),
    "Python": ("https://www.python.org/",
        "The harness language and three of the fixtures (the package toolkit, the multi-tenant "
        "service, the payments service, and the long-context ledger)."),
}


def _tool(name: str) -> str:
    """A linked tool name (falls back to plain text if unknown)."""
    t = TOOLS.get(name)
    if not t:
        return _esc(name)
    return f'<a href="{t[0]}" target="_blank" rel="noopener">{_esc(name)}</a>'


def _tools_table() -> str:
    rows = [[_tool(n), blurb] for n, (_url, blurb) in TOOLS.items()]
    return _table(["Component", "What it is, and why AgentDelta uses it"], rows, scroll=False)


# ---------------------------------------------------------------------------
# value formatting
# ---------------------------------------------------------------------------
def _esc(x: Any) -> str:
    return html.escape("" if x is None else str(x))


def _n(x: Any, fmt: str = "{:.1f}", dash: str = "n/a") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return dash
    try:
        return fmt.format(x)
    except (ValueError, TypeError):
        return _esc(x)


def _pct(x: Any, dash: str = "n/a") -> str:
    return dash if x is None else f"{x * 100:.1f}%"


def _cost(x: Any, fmt: str = "${:.3f}") -> str:
    return "n/a" if x is None else fmt.format(x)


def _time(x: Any) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x / 60:.1f}m" if x >= 60 else f"{x:.0f}s"


def _ratio(x: Any) -> str:
    return "n/a" if x is None else f"{x:.2f}&times;"


def _mean(vals: list) -> float | None:
    clean = [v for v in vals if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v))]
    return sum(clean) / len(clean) if clean else None


def _sum(vals: list) -> float:
    return sum(v for v in vals if isinstance(v, (int, float)))


# ---------------------------------------------------------------------------
# small HTML builders
# ---------------------------------------------------------------------------
def _table(headers: list[str], rows: list[list[str]], *, cls: str = "", scroll: bool = True,
           aligns: list[str] | None = None, row_attrs: list[str] | None = None) -> str:
    aligns = aligns or []
    head = "".join(
        f'<th class="{aligns[i] if i < len(aligns) else ""}">{h}</th>'
        for i, h in enumerate(headers)
    )
    body = []
    for ri, r in enumerate(rows):
        cells = "".join(
            f'<td class="{aligns[i] if i < len(aligns) else ""}">{c}</td>'
            for i, c in enumerate(r)
        )
        attr = f" {row_attrs[ri]}" if row_attrs and ri < len(row_attrs) and row_attrs[ri] else ""
        body.append(f"<tr{attr}>{cells}</tr>")
    tbl = f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'
    return f'<div class="scroll">{tbl}</div>' if scroll else tbl


def _badge(text: str, kind: str) -> str:
    return f'<span class="badge {kind}">{text}</span>'


def _yn(flag: bool) -> str:
    return _badge("yes", "ok") if flag else _badge("no", "muted")


def _verified_cell(flag: bool) -> str:
    return _badge("verified", "ok") if flag else _badge("failed", "bad")


def _kpi(value: str, label: str, sub: str = "") -> str:
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f'<div class="kpi"><div class="kpi-val">{value}</div><div class="kpi-label">{label}</div>{sub_html}</div>'


# ---------------------------------------------------------------------------
# inline SVG charts
# ---------------------------------------------------------------------------
def _hbar_chart(items: list[tuple[str, float | None]], unit_fmt, *, title: str = "",
                accent: str = ACCENT, height_per: int = 30) -> str:
    """Horizontal bar chart. items = [(label, value)]. value None -> 'n/a'."""
    rows = [(lbl, v) for lbl, v in items]
    vals = [v for _, v in rows if isinstance(v, (int, float))]
    vmax = max(vals) if vals else 1.0
    vmax = vmax or 1.0
    label_w, bar_w, pad = 150, 360, 8
    width = label_w + bar_w + 70
    height = pad * 2 + height_per * len(rows)
    parts = [f'<svg viewBox="0 0 {width} {height}" class="chart" role="img">']
    if title:
        parts.append(f'<text x="0" y="0" class="chart-title">{title}</text>')
    for i, (lbl, v) in enumerate(rows):
        y = pad + i * height_per
        cy = y + height_per / 2
        parts.append(f'<text x="0" y="{cy + 4:.0f}" class="chart-lbl">{_esc(lbl)}</text>')
        if isinstance(v, (int, float)):
            w = max(2, (v / vmax) * bar_w)
            parts.append(
                f'<rect x="{label_w}" y="{y + 5:.0f}" width="{w:.1f}" height="{height_per - 12}" '
                f'rx="2" fill="{accent}" />'
            )
            parts.append(f'<text x="{label_w + w + 6:.0f}" y="{cy + 4:.0f}" class="chart-val">{unit_fmt(v)}</text>')
        else:
            parts.append(f'<text x="{label_w}" y="{cy + 4:.0f}" class="chart-val muted">n/a</text>')
    parts.append("</svg>")
    return "".join(parts)


def _heat_cell(rate: float | None) -> str:
    if rate is None:
        return '<td class="heat na">n/a</td>'
    # green for high, fading to red for low
    g = int(125 + 0 * rate)
    if rate >= 0.999:
        bg = "#d6ecdf"
    elif rate >= 0.75:
        bg = "#e8f0d6"
    elif rate >= 0.5:
        bg = "#faf0cf"
    else:
        bg = "#f6dcd6"
    return f'<td class="heat" style="background:{bg}">{rate * 100:.0f}%</td>'


# ---------------------------------------------------------------------------
# cross-suite aggregation (per model, over all suites)
# ---------------------------------------------------------------------------
def _model_global(records: list[dict]) -> dict[str, dict]:
    by_model: dict[str, list[dict]] = {}
    for r in records:
        by_model.setdefault(r["model_id"], []).append(r)
    out: dict[str, dict] = {}
    for mid, recs in by_model.items():
        valid = [r for r in recs if not r.get("execution", {}).get("invalid")]
        n = len(valid)
        verified = sum(1 for r in valid if r["scoring"]["verified_success"])
        out[mid] = {
            "model_id": mid,
            "n_total": len(recs),
            "n_valid": n,
            "n_invalid": len(recs) - n,
            "n_verified": verified,
            "success_rate": (verified / n) if n else None,
            "cost_total": _sum([(r.get("usage") or {}).get("estimated_cost_usd") for r in valid]),
            "cost_mean": _mean([(r.get("usage") or {}).get("estimated_cost_usd") for r in valid]),
            "time_mean": _mean([(r.get("execution") or {}).get("wall_clock_seconds") for r in valid]),
            "tokens_mean": _mean([(r.get("usage") or {}).get("total_tokens") for r in valid]),
            "output_mean": _mean([(r.get("usage") or {}).get("output_tokens") for r in valid]),
            "cache_read_mean": _mean([(r.get("usage") or {}).get("cache_read_tokens") for r in valid]),
            "reasoning_mean": _mean([(r.get("usage") or {}).get("reasoning_tokens") for r in valid]),
            "tool_calls_mean": _mean([(r.get("agent_behavior") or {}).get("tool_calls") for r in valid]),
            "test_runs_mean": _mean([(r.get("agent_behavior") or {}).get("test_runs") for r in valid]),
            "edits_mean": _mean([(r.get("agent_behavior") or {}).get("file_edits") for r in valid]),
            "reads_mean": _mean([(r.get("agent_behavior") or {}).get("files_read") for r in valid]),
            "lines_mean": _mean([
                ((r.get("agent_behavior") or {}).get("lines_added") or 0)
                + ((r.get("agent_behavior") or {}).get("lines_removed") or 0) for r in valid]),
            "scope_mean": _mean([r["scoring"].get("scope_control") for r in valid]),
        }
    return out


def _version_key(mid: str):
    import re
    m = re.search(r"(\d+)[-.](\d+)", mid)
    fam = 0 if "opus" in mid else (1 if "sonnet" in mid else 2)
    ver = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return (fam, ver[0], ver[1])


def _sorted_models(model_ids) -> list[str]:
    return sorted(model_ids, key=_version_key)


# ---------------------------------------------------------------------------
# tab: overview
# ---------------------------------------------------------------------------
def _tab_overview(suites: list[dict], all_records: list[dict], gmodels: dict) -> str:
    n_runs = len(all_records)
    valid = [r for r in all_records if not r.get("execution", {}).get("invalid")]
    n_valid = len(valid)
    n_invalid = n_runs - n_valid
    n_verified = sum(1 for r in valid if r["scoring"]["verified_success"])
    spend = _sum([(r.get("usage") or {}).get("estimated_cost_usd") for r in all_records])
    models = _sorted_models({r["model_id"] for r in all_records})
    tasks = {r["task_id"] for r in all_records}
    overall_sr = (n_verified / n_valid) if n_valid else 0.0

    # material gains across every suite/mode
    total_cmp = material_cmp = 0
    for s in suites:
        for mode in s["report"]["per_mode"].values():
            for imp in mode["level1"]["improvements"]:
                total_cmp += 1
                if imp["material"]:
                    material_cmp += 1

    # efficiency leaders
    cheapest = min((m for m in gmodels.values() if m["cost_mean"]),
                   key=lambda m: m["cost_mean"], default=None)
    fastest = min((m for m in gmodels.values() if m["time_mean"]),
                  key=lambda m: m["time_mean"], default=None)

    kpis = "".join([
        _kpi(f"{n_verified}/{n_valid}", "verified runs", f"{overall_sr * 100:.1f}% of valid runs"),
        _kpi(f"{material_cmp}/{total_cmp}", "material capability gains", "Holm-corrected, paired"),
        _kpi(str(len(models)), "models compared", "1M-context, single agent"),
        _kpi(str(len(tasks)), "distinct tasks", f"{len(suites)} suites"),
        _kpi(f"${spend:.2f}", "total API spend", f"{n_runs} runs"),
        _kpi(f"{n_invalid}", "invalid runs", "excluded from ranking"),
    ])

    # headline finding callout
    leaders = ""
    if cheapest and fastest:
        leaders = (
            f"<p>Where the models <em>do</em> separate is efficiency. "
            f"Cheapest per run: <strong>{_esc(cheapest['model_id'])}</strong> "
            f"({_cost(cheapest['cost_mean'])}/run). "
            f"Fastest per run: <strong>{_esc(fastest['model_id'])}</strong> "
            f"({_time(fastest['time_mean'])}/run).</p>"
        )

    finding = f"""
    <div class="callout">
      <h3>Headline finding</h3>
      <p>Across <strong>{len(suites)} suites</strong> spanning every difficulty tier we have built, from easy fixes and harder multi-step work to
      frontier tasks, hard H2 to H5 tasks (multi-tenant authorization, state machines, multi-file
      root-cause), and a real widened-window concurrency race, all {len(models)} 1M-context Claude
      models verified <strong>{overall_sr * 100:.1f}%</strong>
      of valid runs. <strong>{material_cmp} of {total_cmp}</strong> pairwise model comparisons cleared the
      materiality bar (success delta above threshold <em>and</em> a significant Holm-corrected paired
      McNemar test). At single-repository scale, capability is not differentiable among these models.</p>
      {leaders}
      <p class="muted">This is an honest negative result on capability and a positive result on efficiency.
      It does not say newer models are equivalent in general; it says these tasks do not separate them.
      See <a href="#" data-jump="interpretation">Interpretation</a> for what that means and where a gap
      is likely to appear.</p>
    </div>
    """

    # five-tier / per-suite summary table
    rows = []
    for s in suites:
        rep = s["report"]
        recs = s["records"]
        sv = [r for r in recs if not r.get("execution", {}).get("invalid")]
        ver = sum(1 for r in sv if r["scoring"]["verified_success"])
        sr = (ver / len(sv)) if sv else 0.0
        hard = sorted({r.get("hardness_level") for r in recs if r.get("hardness_level")})
        scost = _sum([(r.get("usage") or {}).get("estimated_cost_usd") for r in recs])
        rows.append([
            f'<strong>{_esc(rep["suite"])}</strong>',
            _esc(", ".join(rep["modes"])),
            ", ".join(hard) if hard else "n/a",
            str(rep["n_tasks"]),
            str(len(rep["models"])),
            str(rep["n_runs"]),
            _badge(f"{ver}/{len(sv)}", "ok" if sr > 0.999 else "warn"),
            _pct(sr),
            str(rep["n_invalid"]),
            _cost(scost, "${:.2f}"),
        ])
    suite_table = _table(
        ["Suite", "Mode(s)", "Hardness", "Tasks", "Models", "Runs", "Verified", "Success", "Invalid", "Spend"],
        rows, cls="lead",
        aligns=["", "", "", "num", "num", "num", "center", "num", "num", "num"],
    )

    # model x suite success heatmap
    heat_head = "<th>Model</th>" + "".join(
        f'<th class="rot">{_esc(s["report"]["suite"].replace("anthropic-v0.1-", ""))}</th>'
        for s in suites
    ) + "<th>Overall</th>"
    heat_rows = []
    for mid in models:
        cells = [f'<td class="rowlab">{_esc(mid)}</td>']
        for s in suites:
            recs = [r for r in s["records"] if r["model_id"] == mid
                    and not r.get("execution", {}).get("invalid")]
            if recs:
                rate = sum(1 for r in recs if r["scoring"]["verified_success"]) / len(recs)
                cells.append(_heat_cell(rate))
            else:
                cells.append(_heat_cell(None))
        gm = gmodels.get(mid, {})
        cells.append(_heat_cell(gm.get("success_rate")))
        heat_rows.append(f'<tr data-provider="{model_provider(mid)}">' + "".join(cells) + "</tr>")
    heatmap = (
        '<div class="scroll"><table class="heatmap"><thead><tr>'
        + heat_head + "</tr></thead><tbody>" + "".join(heat_rows) + "</tbody></table></div>"
    )

    # efficiency charts
    chart_cost = _hbar_chart(
        [(m["model_id"], m["cost_mean"]) for m in
         sorted(gmodels.values(), key=lambda m: m["cost_mean"] or 9e9)],
        lambda v: _cost(v), title="Mean cost per run (USD)")
    chart_time = _hbar_chart(
        [(m["model_id"], m["time_mean"]) for m in
         sorted(gmodels.values(), key=lambda m: m["time_mean"] or 9e9)],
        lambda v: _time(v), title="Mean wall-clock per run", accent="#5b7fb3")

    interp = """
    <h2 id="interpretation">Interpretation: what this does and does not mean</h2>
    <div class="grid2">
      <div class="card">
        <h4>What the data supports</h4>
        <ul>
          <li>On objective, hidden-test-graded tasks at single-repository scale, these four
          1M-context models are <strong>capability-equivalent</strong>: none has a material,
          statistically supported success advantage over the oldest baseline.</li>
          <li>The benchmark <strong>refuses to manufacture a gap</strong>: the materiality gate
          (delta threshold + Holm-corrected McNemar) correctly reports "no difference" rather than
          promoting noise to a finding.</li>
          <li>The real, consistent separator is <strong>efficiency</strong>: cost and latency
          per verified task, which is exactly the axis a buyer optimizes once correctness is saturated.</li>
        </ul>
      </div>
      <div class="card">
        <h4>What it does not claim</h4>
        <ul>
          <li>It does not claim newer models are pointless. It claims <em>these tasks</em> do not
          discriminate them. The plausible discriminators, namely multi-service changes, large ambiguous
          specs, and long-horizon planning across the full 1M context, are not yet in the suite.</li>
          <li>Saturation is itself the signal: when a tier hits 100% for everyone, the next version must
          raise difficulty along the dimension that actually taxes a frontier model (scope and ambiguity,
          not just algorithmic trickiness).</li>
          <li>The efficiency ranking is real but workload-specific; it should be re-measured per task family.</li>
        </ul>
      </div>
    </div>
    """

    return f"""
    <section id="overview" class="tab active">
      <h1>AgentDelta: cross-suite evaluation report</h1>
      <p class="lede">A reproducible, objective-first benchmark for frontier coding agents. This report
      consolidates every suite run to date into one view: results first, then the full apparatus behind them.</p>
      <div class="kpis">{kpis}</div>
      {finding}
      <h2>Suites at a glance</h2>
      {suite_table}
      <h2>Verified-success by model and suite</h2>
      <p class="muted">Each cell is the verified-success rate for that model on that suite (valid runs only).</p>
      {heatmap}
      <h2>The separator is efficiency, not capability</h2>
      <div class="grid2">
        <div class="card chart-card">{chart_cost}</div>
        <div class="card chart-card">{chart_time}</div>
      </div>
      {interp}
    </section>
    """


# ---------------------------------------------------------------------------
# tab: per-model
# ---------------------------------------------------------------------------
def _tab_models(gmodels: dict, suites: list[dict]) -> str:
    models = _sorted_models(gmodels.keys())
    rows = []
    for mid in models:
        m = gmodels[mid]
        rows.append([
            f'<strong>{_esc(mid)}</strong>',
            str(m["n_valid"]),
            _badge(f'{m["n_verified"]}/{m["n_valid"]}', "ok" if (m["success_rate"] or 0) > 0.999 else "warn"),
            _pct(m["success_rate"]),
            _cost(m["cost_mean"]),
            _cost(m["cost_total"], "${:.2f}"),
            _time(m["time_mean"]),
            _n(m["tokens_mean"], "{:,.0f}"),
            _n(m["output_mean"], "{:,.0f}"),
            _n(m["cache_read_mean"], "{:,.0f}"),
            _n(m["reasoning_mean"], "{:,.0f}"),
            _n(m["tool_calls_mean"], "{:.1f}"),
            _n(m["test_runs_mean"], "{:.1f}"),
            _n(m["reads_mean"], "{:.1f}"),
            _n(m["edits_mean"], "{:.1f}"),
            _n(m["lines_mean"], "{:.0f}"),
            _n(m["scope_mean"], "{:.2f}"),
            str(m["n_invalid"]),
        ])
    table = _table(
        ["Model", "Valid runs", "Verified", "Success", "Cost/run", "Cost total", "Time/run",
         "Tokens/run", "Output tok", "Cache-read", "Reasoning tok", "Tools/run", "Test runs",
         "Reads/run", "Edits/run", "Lines/run", "Scope ctrl", "Invalid"],
        rows,
        aligns=["", "num", "center", "num", "num", "num", "num", "num", "num", "num", "num",
                "num", "num", "num", "num", "num", "num", "num"],
        row_attrs=[f'data-provider="{model_provider(mid)}"' for mid in models],
    )

    # per-model x per-suite cost + time matrices
    def matrix(metric_fn, fmt):
        head = "<th>Model</th>" + "".join(
            f'<th class="rot num">{_esc(s["report"]["suite"].replace("anthropic-v0.1-", ""))}</th>'
            for s in suites)
        body = []
        for mid in models:
            cells = [f'<td class="rowlab">{_esc(mid)}</td>']
            for s in suites:
                recs = [r for r in s["records"] if r["model_id"] == mid
                        and not r.get("execution", {}).get("invalid")]
                cells.append(f'<td class="num">{fmt(metric_fn(recs))}</td>' if recs
                             else '<td class="num muted">n/a</td>')
            body.append("<tr>" + "".join(cells) + "</tr>")
        return ('<div class="scroll"><table><thead><tr>' + head
                + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")

    cost_matrix = matrix(
        lambda recs: _mean([(r.get("usage") or {}).get("estimated_cost_usd") for r in recs]),
        lambda v: _cost(v))
    time_matrix = matrix(
        lambda recs: _mean([(r.get("execution") or {}).get("wall_clock_seconds") for r in recs]),
        lambda v: _time(v))

    return f"""
    <section id="models" class="tab">
      <h1>Per-model comparison</h1>
      <p class="lede">Every metric is a mean over that model's valid runs across all suites.
      Work signals (tokens, tools, reads, edits) are the basis of the agentic-amplification analysis:
      a newer model that wins only by doing more work is amplified, not intrinsically better.</p>
      <h2>Aggregate metrics (all suites)</h2>
      {table}
      <h2>Mean cost per run, by suite</h2>
      {cost_matrix}
      <h2>Mean wall-clock per run, by suite</h2>
      {time_matrix}
    </section>
    """


# ---------------------------------------------------------------------------
# tab: per-suite detail
# ---------------------------------------------------------------------------
def _suite_block(s: dict) -> str:
    rep = s["report"]
    blocks = [f'<h2 id="suite-{_esc(rep["suite"])}">{_esc(rep["suite"])}</h2>']
    blocks.append(
        f'<p class="muted">{rep["n_tasks"]} task(s) &middot; {rep["n_runs"]} runs &middot; '
        f'{rep["n_invalid"]} invalid &middot; modes: {_esc(", ".join(rep["modes"]))} &middot; '
        f'agent: {_esc(rep.get("agent"))}</p>'
    )
    for mode, data in rep["per_mode"].items():
        ranking = [data["models"][mid] for mid in data["level1"]["ranking"]]
        blocks.append(f'<h3>Mode: {_esc(mode)} / Level 1 ranking</h3>')
        rows = []
        for m in ranking:
            lo, hi = m["success_ci95"]
            rows.append([
                str(m["rank"]),
                f'<strong>{_esc(m["model_id"])}</strong>',
                _n(m["objective_score"]),
                f'{_pct(m["success_rate"])} <span class="muted">({_pct(lo)} to {_pct(hi)})</span>',
                _pct(m["hidden_test_rate"]),
                _pct(1.0 - (m["regression_rate"] or 0)),
                _n(m["scope_control"], "{:.2f}"),
                _cost(m["cost_per_success_usd"]),
                _time(m["median_time_to_success_s"]),
                _n(m.get("work_index")),
            ])
        blocks.append(_table(
            ["Rank", "Model", "Objective", "Success (95% CI)", "Hidden", "Regr-avoid",
             "Scope", "Cost/succ", "Med time", "Work idx"],
            rows,
            aligns=["num", "", "num", "", "num", "num", "num", "num", "num", "num"]))

        # category breakdown
        cats = sorted({c for m in ranking for c in (m.get("category_success") or {})})
        if cats:
            crows = []
            for m in ranking:
                cs = m.get("category_success") or {}
                crows.append([f'<strong>{_esc(m["model_id"])}</strong>']
                             + [_pct(cs.get(c)) if c in cs else "n/a" for c in cats])
            blocks.append("<h4>Category success</h4>")
            blocks.append(_table(["Model"] + [_esc(c) for c in cats], crows,
                                 aligns=[""] + ["num"] * len(cats)))

        # failure taxonomy
        if any(m.get("failure_labels") for m in ranking):
            frows = []
            for m in ranking:
                labels = m.get("failure_labels") or {}
                cell = ", ".join(f"{_esc(k)} ({v})" for k, v in labels.items()) if labels else \
                    _badge("none", "ok")
                frows.append([f'<strong>{_esc(m["model_id"])}</strong>', cell])
            blocks.append("<h4>Failure taxonomy (valid failed runs)</h4>")
            blocks.append(_table(["Model", "Labels"], frows, scroll=False))

        # diagnostics
        if any(m.get("diagnostics") for m in ranking):
            drows = []
            for m in ranking:
                d = m.get("diagnostics") or {}
                drows.append([
                    f'<strong>{_esc(m["model_id"])}</strong>',
                    _n(d.get("failed_command_ratio"), "{:.2f}"),
                    _n(d.get("exploration_edit_ratio"), "{:.2f}"),
                    _pct(d.get("timeout_rate")),
                    _n(d.get("mean_diff_locality"), "{:.2f}"),
                    _n(d.get("mean_patch_entropy"), "{:.2f}"),
                    _n(d.get("mean_test_to_code_ratio"), "{:.2f}"),
                ])
            blocks.append("<h4>Diagnostics</h4>")
            blocks.append(_table(
                ["Model", "Failed-cmd ratio", "Explore/edit", "Timeout rate",
                 "Diff locality", "Patch entropy", "Test/code"],
                drows, aligns=["", "num", "num", "num", "num", "num", "num"]))

        # frontiers
        for title, key, fmt in [("Cost-success frontier", "cost_frontier", _cost),
                                ("Latency-success frontier", "latency_frontier", _time)]:
            pts = data.get(key) or []
            if any(p.get("x") is not None for p in pts):
                prows = [[
                    f'<strong>{_esc(p["model_id"])}</strong>', fmt(p["x"]), _pct(p["y"]),
                    _yn(bool(p.get("on_frontier")))]
                    for p in sorted(pts, key=lambda q: (q["x"] is None, q["x"] or 0))]
                blocks.append(f"<h4>{title}</h4>")
                blocks.append(_table(["Model", "Axis", "Success", "On frontier"], prows,
                                     aligns=["", "num", "num", "center"]))
    return "".join(blocks)


def build_cross_provider(all_records: list[dict]) -> dict | None:
    """Computed cross-provider comparison: a like-for-like head-to-head on the tasks
    that at least two providers each ran with a full (>=4 model) cohort.

    Returns a serializable dict (the single source of truth for both the HTML panel
    and the JSON export's `cross_provider` block), or None when there are fewer than
    two providers or no shared full-cohort tasks.
    """
    valid = [r for r in all_records if not (r.get("execution") or {}).get("invalid")]
    ptm: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for r in valid:
        ptm[model_provider(r["model_id"])][r["task_id"]].add(r["model_id"])
    providers = [p for p in sorted(ptm) if p != "unknown"]
    if len(providers) < 2:
        return None
    taskcount: dict[str, int] = defaultdict(int)
    for p in providers:
        for t, ms in ptm[p].items():
            if len(ms) >= 4:
                taskcount[t] += 1
    shared = sorted(t for t, c in taskcount.items() if c >= 2)
    if not shared:
        return None

    sset = set(shared)
    sv = [r for r in valid if r["task_id"] in sset]
    perprov = defaultdict(lambda: {"runs": 0, "ver": 0, "cost": [], "time": [], "models": set()})
    permodel = defaultdict(lambda: {"runs": 0, "ver": 0, "cost": [], "time": []})
    ptask = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    hardness = {}
    for r in sv:
        p = model_provider(r["model_id"]); m = r["model_id"]
        v = int(r["scoring"]["verified_success"])
        c = (r.get("usage") or {}).get("estimated_cost_usd") or 0
        t = (r.get("execution") or {}).get("wall_clock_seconds") or 0
        a = perprov[p]; a["runs"] += 1; a["ver"] += v; a["cost"].append(c); a["time"].append(t); a["models"].add(m)
        b = permodel[m]; b["runs"] += 1; b["ver"] += v; b["cost"].append(c); b["time"].append(t)
        ptask[r["task_id"]][p][0] += 1; ptask[r["task_id"]][p][1] += v
        hardness[r["task_id"]] = r.get("hardness_level") or "?"

    def _med(xs):
        return statistics.median(xs) if xs else None

    def _rate(ver, runs):
        return (ver / runs) if runs else None

    return {
        "shared_task_count": len(shared),
        "shared_tasks": shared,
        "providers": [
            {"id": p, "label": PROVIDER_LABELS.get(p, p), "models": sorted(perprov[p]["models"]),
             "runs": perprov[p]["runs"], "verified": perprov[p]["ver"],
             "verified_rate": _rate(perprov[p]["ver"], perprov[p]["runs"]),
             "mean_cost_usd": _mean(perprov[p]["cost"]), "median_time_s": _med(perprov[p]["time"])}
            for p in providers],
        "models": [
            {"model_id": m, "provider": model_provider(m), "runs": permodel[m]["runs"],
             "verified": permodel[m]["ver"], "verified_rate": _rate(permodel[m]["ver"], permodel[m]["runs"]),
             "mean_cost_usd": _mean(permodel[m]["cost"]), "median_time_s": _med(permodel[m]["time"])}
            for m in sorted(permodel, key=lambda x: (model_provider(x), x))],
        "per_task": [
            {"task_id": t, "hardness_level": hardness.get(t, "?"),
             "providers": {p: {"runs": ptask[t][p][0], "verified": ptask[t][p][1],
                               "verified_rate": _rate(ptask[t][p][1], ptask[t][p][0])}
                           for p in providers}}
            for t in shared],
    }


def _tab_crossprovider(all_records: list[dict]) -> str:
    """Render the cross-provider panel from build_cross_provider (same source the
    JSON export uses, so the HTML and JSON can never diverge)."""
    head = '<section id="crossprovider" class="tab"><h1>Cross-provider comparison</h1>'
    cp = build_cross_provider(all_records)
    if cp is None:
        present = sorted({model_provider(r["model_id"]) for r in all_records
                          if not (r.get("execution") or {}).get("invalid")} - {"unknown"})
        msg = ("A second provider is needed for a cross-provider comparison. Run a suite with "
               "another agent (for example <code>--agent codex_cli</code>) and regenerate."
               if len(present) < 2 else
               "No tasks yet have a full model cohort on two providers. The comparison appears once "
               "both providers have run the same tasks with their full cohort.")
        return f'{head}<p class="muted">{msg}</p></section>'

    providers = [p["id"] for p in cp["providers"]]
    plabel = {p["id"]: p["label"].split(" (")[0] for p in cp["providers"]}

    summary = _table(
        ["Provider", "Models", "Runs", "Verified", "Mean $/run", "Median time"],
        [[f'<strong>{_esc(p["label"])}</strong>', str(len(p["models"])), str(p["runs"]),
          _pct(p["verified_rate"]), _cost(p["mean_cost_usd"]), _time(p["median_time_s"])]
         for p in cp["providers"]],
        aligns=["", "num", "num", "num", "num", "num"],
        row_attrs=[f'data-provider="{p["id"]}"' for p in cp["providers"]])

    permodel_tbl = _table(
        ["Model", "Provider", "Verified", "Success", "Mean $/run", "Median time"],
        [[f'<strong>{_esc(m["model_id"])}</strong>', _esc(plabel.get(m["provider"], m["provider"])),
          f'{m["verified"]}/{m["runs"]}', _pct(m["verified_rate"]),
          _cost(m["mean_cost_usd"]), _time(m["median_time_s"])] for m in cp["models"]],
        aligns=["", "", "num", "num", "num", "num"],
        row_attrs=[f'data-provider="{m["provider"]}"' for m in cp["models"]])

    pertask_tbl = _table(
        ["Task", "H"] + [plabel[p] for p in providers],
        [[f'<strong>{_esc(row["task_id"])}</strong>', _esc(row["hardness_level"]),
          *[_pct(row["providers"][p]["verified_rate"]) for p in providers]]
         for row in cp["per_task"]],
        aligns=["", "", *["num"] * len(providers)])

    return f"""{head}
      <p class="lede">A like-for-like comparison on the <strong>{cp["shared_task_count"]} tasks</strong>
      that both providers ran with a full model cohort. Equal high rates mean the tier does not separate
      the providers on capability (read the per-model mean cost for the efficiency difference); where
      rates diverge, notably long-context retrieval, capability does separate them.</p>
      <h2>By provider</h2>
      {summary}
      <h2>By model</h2>
      {permodel_tbl}
      <h2>Per task (verified rate, each provider's full cohort)</h2>
      {pertask_tbl}
      <p class="muted">Verified rate is over all of a provider's runs (models x repetitions) on each
      task. This same comparison is in the JSON export under the top-level <code>cross_provider</code>
      key.</p>
    </section>"""


def _suite_provider(s: dict) -> str:
    provs = {r.get("provider") or model_provider(r.get("model_id", "")) for r in s["records"]}
    provs.discard("unknown")
    return next(iter(provs)) if len(provs) == 1 else ("mixed" if provs else "unknown")


def _tab_suites(suites: list[dict]) -> str:
    nav = " &middot; ".join(
        f'<a href="#" data-jump="suite-{_esc(s["report"]["suite"])}">'
        f'{_esc(s["report"]["suite"].replace("anthropic-v0.1-", ""))}</a>'
        for s in suites)
    body = "".join(f'<div data-provider="{_suite_provider(s)}">{_suite_block(s)}</div>'
                   for s in suites)
    return f"""
    <section id="suites" class="tab">
      <h1>Per-suite detail</h1>
      <p class="lede">Full Level 1 assessment for every suite: ranking with Wilson confidence
      intervals, category success, failure taxonomy, behavioral diagnostics, and Pareto frontiers.</p>
      <p class="muted">Jump to: {nav}</p>
      {body}
    </section>
    """


# ---------------------------------------------------------------------------
# tab: statistics
# ---------------------------------------------------------------------------
def _tab_stats(suites: list[dict]) -> str:
    blocks = ["""
    <section id="stats" class="tab">
      <h1>Statistical assessment</h1>
      <p class="lede">A gain is promoted to "material" only if it clears both gates: a success
      improvement of at least the configured threshold (in percentage points) <em>and</em> a significant
      paired McNemar test after Holm correction across the comparison family. Material gains are then
      escalated to the Level 2 amplification analysis. This is where the benchmark earns the right to
      say "no difference."</p>
    """]
    for s in suites:
        rep = s["report"]
        for mode, data in rep["per_mode"].items():
            imps = data["level1"]["improvements"]
            if not imps:
                continue
            blocks.append(
                f'<h2>{_esc(rep["suite"])} <span class="muted">/ {_esc(mode)} '
                f'&middot; baseline {_esc(data["level1"]["baseline"])}</span></h2>')
            rows = []
            for imp in imps:
                paired = imp.get("paired") or {}
                rows.append([
                    f'<strong>{_esc(imp["model_b"])}</strong>',
                    f'{imp["success_delta_pp"]:+.1f} pp',
                    f'{imp["objective_delta"]:+.1f}',
                    _n(imp.get("raw_p_value"), "{:.3f}"),
                    _n(imp.get("holm_p_value"), "{:.3f}"),
                    str(paired.get("n", "n/a")),
                    (_badge("material", "warn") if imp["material"] else _badge("not material", "muted")),
                    f'<span class="muted">{_esc(imp.get("materiality_reason"))}</span>',
                ])
            blocks.append(_table(
                ["Model B vs baseline", "Success delta", "Objective delta", "McNemar p",
                 "Holm p", "Pairs", "Verdict", "Reason"],
                rows,
                aligns=["", "num", "num", "num", "num", "num", "center", ""]))

            # amplification (level 2) if any
            assessments = data["level2"].get("assessments") or []
            if assessments:
                arows = []
                for a in assessments:
                    r = a["ratios"]
                    arows.append([
                        f'<strong>{_esc(a["model_b"])}</strong>',
                        f'{a["success_delta_pp"]:+.1f} pp',
                        _ratio(r.get("token_amplification")),
                        _ratio(r.get("cost_amplification")),
                        _ratio(r.get("time_amplification")),
                        _ratio(r.get("work_index_amplification")),
                        _esc(a["classification"]["category"]),
                    ])
                blocks.append("<h4>Level 2: amplification of material gains</h4>")
                blocks.append(_table(
                    ["Model B", "Success delta", "Token amp", "Cost amp", "Time amp",
                     "Work amp", "Classification"], arows,
                    aligns=["", "num", "num", "num", "num", "num", ""]))
    blocks.append("</section>")
    return "".join(blocks)


# ---------------------------------------------------------------------------
# tab: raw runs (every metric, scroll right)
# ---------------------------------------------------------------------------
RAW_COLS = [
    ("Suite", "suite"), ("Task", "task_id"), ("H", "hardness_level"),
    ("Category", "task_category"), ("Model", "model_id"), ("Effort", "effort"),
    ("Mode", "mode"), ("Rep", "epoch"), ("Verified", "verified"), ("Hidden", "hidden"),
    ("Regr-avoid", "regr"), ("Scope", "scope"), ("Partial obj", "partial"),
    ("Public", "public"), ("Hidden tests", "hiddent"),
    ("Input tok", "input"), ("Output tok", "output"), ("Total tok", "total"),
    ("Cache-read", "cread"), ("Cache-write", "cwrite"), ("Reasoning", "reason"),
    ("Cost", "cost"), ("Wall (s)", "wall"), ("Working (s)", "work"),
    ("Files", "files"), ("+", "ladd"), ("-", "lrem"), ("Tools", "tools"),
    ("Shell", "shell"), ("Failed cmd", "failed"), ("Tests", "tests"),
    ("Reads", "reads"), ("Edits", "edits"), ("Retries", "retries"),
    ("Diff loc", "dloc"), ("Entropy", "entropy"), ("Failure labels", "labels"),
    ("Invalid", "invalid"),
]


def _raw_row(r: dict) -> list[str]:
    ab = r.get("agent_behavior") or {}
    u = r.get("usage") or {}
    sc = r.get("scoring") or {}
    ex = r.get("execution") or {}
    dm = r.get("diff_metrics") or {}
    pub = sc.get("public_tests") or {}
    hid = sc.get("hidden_tests") or {}
    invalid = bool(ex.get("invalid"))
    labels = ", ".join(r.get("failure_labels") or []) or ("n/a")
    return [
        _esc(r.get("suite", "").replace("anthropic-v0.1-", "")),
        _esc(r.get("task_id")),
        _esc(r.get("hardness_level") or "n/a"),
        _esc(r.get("task_category") or "n/a"),
        _esc(r.get("model_id")),
        _esc((r.get("model_config") or {}).get("reasoning_effort") or "n/a"),
        _esc(r.get("mode")),
        _esc(r.get("epoch")),
        (_badge("inv", "muted") if invalid else _verified_cell(bool(sc.get("verified_success")))),
        _n(sc.get("hidden_test_score"), "{:.2f}"),
        _n(sc.get("regression_avoidance"), "{:.0f}"),
        _n(sc.get("scope_control"), "{:.2f}"),
        _n(sc.get("partial_objective_score"), "{:.1f}"),
        f'{pub.get("passed", 0)}/{pub.get("total", 0)}',
        f'{hid.get("passed", 0)}/{hid.get("total", 0)}',
        _n(u.get("input_tokens"), "{:,.0f}"),
        _n(u.get("output_tokens"), "{:,.0f}"),
        _n(u.get("total_tokens"), "{:,.0f}"),
        _n(u.get("cache_read_tokens"), "{:,.0f}"),
        _n(u.get("cache_write_tokens"), "{:,.0f}"),
        _n(u.get("reasoning_tokens"), "{:,.0f}"),
        _cost(u.get("estimated_cost_usd")),
        _n(ex.get("wall_clock_seconds"), "{:.0f}"),
        _n(ex.get("working_seconds"), "{:.0f}"),
        _n(ab.get("files_modified"), "{:.0f}"),
        _n(ab.get("lines_added"), "{:.0f}"),
        _n(ab.get("lines_removed"), "{:.0f}"),
        _n(ab.get("tool_calls"), "{:.0f}"),
        _n(ab.get("shell_commands"), "{:.0f}"),
        _n(ab.get("failed_shell_commands"), "{:.0f}"),
        _n(ab.get("test_runs"), "{:.0f}"),
        _n(ab.get("files_read"), "{:.0f}"),
        _n(ab.get("file_edits"), "{:.0f}"),
        _n(ab.get("retry_count"), "{:.0f}"),
        _n(dm.get("diff_locality"), "{:.2f}"),
        _n(dm.get("patch_entropy"), "{:.2f}"),
        f'<span class="muted">{labels}</span>',
        _yn(invalid) if invalid else _badge("ok", "ok"),
    ]


def _tab_raw(all_records: list[dict]) -> str:
    recs = sorted(all_records, key=lambda r: (
        r.get("suite", ""), r.get("task_id", ""), _version_key(r["model_id"]), r.get("epoch") or 0))
    headers = [h for h, _ in RAW_COLS]
    rows = [_raw_row(r) for r in recs]
    num_cols = {"Rep", "Hidden", "Regr-avoid", "Scope", "Partial obj", "Input tok", "Output tok",
                "Total tok", "Cache-read", "Cache-write", "Reasoning", "Cost", "Wall (s)",
                "Working (s)", "Files", "+", "-", "Tools", "Shell", "Failed cmd", "Tests",
                "Reads", "Edits", "Retries", "Diff loc", "Entropy"}
    aligns = ["num" if h in num_cols else "" for h in headers]
    row_attrs = [f'data-provider="{r.get("provider") or model_provider(r.get("model_id", ""))}"'
                 for r in recs]
    table = _table(headers, rows, cls="raw", aligns=aligns, row_attrs=row_attrs)
    return f"""
    <section id="raw" class="tab">
      <h1>Raw runs: every metric</h1>
      <p class="lede">One row per run, every captured field. Scroll horizontally to see all
      {len(headers)} columns. This is the ground truth behind every aggregate in this report:
      not "all models passed" but the exact tokens, cost, time, and edit footprint each run produced.</p>
      <p class="muted">{len(rows)} runs.</p>
      {table}
    </section>
    """


# ---------------------------------------------------------------------------
# tab: methodology
# ---------------------------------------------------------------------------
def _flatten(d, prefix="") -> list[tuple[str, str]]:
    out = []
    for k, v in (d or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.extend(_flatten(v, key + "."))
        else:
            out.append((key, str(v)))
    return out


def _tab_methodology(suites: list[dict]) -> str:
    formula = suites[0]["report"].get("scoring_formula") if suites else {}
    frows = [[f'<code>{_esc(k)}</code>', _esc(v)] for k, v in _flatten(formula)]
    formula_table = _table(["Parameter", "Value"], frows, scroll=False) if frows else ""
    return f"""
    <section id="methodology" class="tab">
      <h1>Methodology</h1>
      <p class="lede">AgentDelta evaluates a model-plus-agent system, not a model in isolation. Every
      run is a real coding agent ({_tool("Claude Code")} or {_tool("Codex CLI")}, via
      {_tool("inspect_swe")}) acting inside a pinned {_tool("Docker")} sandbox on a seeded git repository,
      graded by tests the agent never sees. The agent is chosen per run with <code>--agent</code>; the
      full tech stack is under <a href="#" data-jump="stack-top">Stack &amp; requirements</a>.</p>

      <h2>Execution</h2>
      <ul>
        <li><strong>Harness:</strong> {_tool("Inspect AI")} drives the task; {_tool("inspect_swe")} runs
        the selected agent CLI ({_tool("Claude Code")} or {_tool("Codex CLI")}) inside a per-fixture
        {_tool("Docker")} image. The model edits files; nothing else is scripted.</li>
        <li><strong>Sandbox:</strong> one image per fixture, pinned by digest. Network is disabled by
        default and only enabled for real model runs that need {_tool("Anthropic API")} or
        {_tool("OpenAI API")} access.</li>
        <li><strong>Reasoning effort</strong> is a recorded, controllable dimension (low to max) so the
        same model can be compared across effort settings.</li>
        <li><strong>Repetitions</strong> per (task, model) with blocked randomization of run order, so
        provider-side variance and ordering effects do not bias one model.</li>
      </ul>

      <h2>Scoring (objective-first)</h2>
      <p>A run is <strong>verified</strong> only if the public tests pass, the pre-existing suite still
      passes (no regression), and no hard scope or forbidden-shortcut violation occurred. Hidden tests
      measure how completely the fix generalizes; scope control measures edit discipline. The objective
      score combines verified success, hidden-test score, regression avoidance, scope control, and
      set-relative cost/time efficiency.</p>
      <ul>
        <li><strong>Hard scope violation</strong> (touching a forbidden file, or matching a forbidden
        pattern such as deleting/skipping tests) fails the run.</li>
        <li><strong>Soft over-budget</strong> (too many files or lines) lowers the scope-control
        component but does not by itself fail a correct fix.</li>
        <li><strong>Test-writing tasks</strong> are graded by mutation kill rate against planted mutants.</li>
      </ul>
      {formula_table}

      <h2>Two levels of assessment</h2>
      <div class="grid2">
        <div class="card">
          <h4>Level 1: primary ranking</h4>
          <p>Who performs best on objective evidence, and which Model-B-over-Model-A gains are
          <em>material</em>: success delta above threshold <em>and</em> a significant Holm-corrected
          paired McNemar test. Non-material gains are reported and excluded from escalation.</p>
        </div>
        <div class="card">
          <h4>Level 2: agentic amplification</h4>
          <p>For material gains only: is the improvement intrinsic capability, or does the newer model
          simply do more work by default (more tokens, time, tool calls, retries, self-review)? The
          Agentic Work Index and amplification ratios separate "better" from "busier."</p>
        </div>
      </div>

      <h2>Hardness levels</h2>
      <ul>
        <li><strong>H1 to H2:</strong> localized fixes and small multi-step changes.</li>
        <li><strong>H3:</strong> hidden-invariant tasks (e.g. multi-tenant authorization where the
        naive fix leaks across tenants).</li>
        <li><strong>H5:</strong> state machines and concurrency, e.g. a webhook idempotency race
        with a deliberately widened window where check-then-act and unlocked guards both fail.</li>
      </ul>

      <h2>Validity</h2>
      <p>Runs are quarantined (not counted in ranking) when the served model differs from the requested
      one (fallback), the baseline suite was broken before the agent started, the run timed out, or the
      infrastructure crashed (billing, rate limit, provider error). Invalid runs are reported separately
      with their reason.</p>
    </section>
    """


# ---------------------------------------------------------------------------
# tab: reproducibility
# ---------------------------------------------------------------------------
def _tab_repro(suites: list[dict]) -> str:
    blocks = ["""
    <section id="repro" class="tab">
      <h1>Reproducibility</h1>
      <p class="lede">Each suite carries a manifest: tool versions, host, agent CLI version, content
      hashes of tasks/scoring/fixtures/hidden-tests, sandbox image digests, and the seeded run order.
      Drift in any hash is detectable with <code>agentdelta validate-reproducibility</code>.</p>
    """]
    common_keys = ["agentdelta_version", "inspect_version", "inspect_swe_version", "python_version",
                   "docker_version", "host_os", "agent", "agent_cli_version"]
    for s in suites:
        repro = s.get("repro")
        if not repro:
            continue
        blocks.append(f'<h2>{_esc(s["report"]["suite"])}</h2>')
        env_rows = [[f'<code>{_esc(k)}</code>', _esc(repro.get(k))] for k in common_keys if k in repro]
        env_rows += [
            ["<code>run_order_seed</code>", _esc(repro.get("run_order_seed"))],
            ["<code>models</code>", _esc(", ".join(repro.get("models", [])))],
            ["<code>tasks</code>", _esc(", ".join(repro.get("tasks", [])))],
        ]
        blocks.append(_table(["Field", "Value"], env_rows, scroll=False))
        hash_rows = []
        for k, v in repro.items():
            if isinstance(v, str) and v.startswith("sha256:"):
                hash_rows.append([f'<code>{_esc(k)}</code>', f'<code class="hash">{_esc(v)}</code>'])
        for img, dig in (repro.get("sandbox_images") or {}).items():
            hash_rows.append([f'<code>sandbox_image:{_esc(img)}</code>', f'<code class="hash">{_esc(dig)}</code>'])
        if hash_rows:
            blocks.append("<h4>Content hashes</h4>")
            blocks.append(_table(["Artifact", "Digest"], hash_rows))
    blocks.append("</section>")
    return "".join(blocks)


# ---------------------------------------------------------------------------
# tab: stack & requirements
# ---------------------------------------------------------------------------
def _tab_stack(suites: list[dict]) -> str:
    repro = next((s.get("repro") for s in suites if s.get("repro")), {}) or {}
    ver_keys = [
        ("agentdelta_version", "AgentDelta"),
        ("python_version", "Python (harness)"),
        ("inspect_version", "Inspect AI (inspect_ai)"),
        ("inspect_swe_version", "inspect_swe"),
        ("docker_version", "Docker"),
        ("agent", "Agent"),
        ("agent_cli_version", "Agent CLI"),
        ("host_os", "Host OS (this report)"),
    ]
    vrows = [[_esc(label), f'<code>{_esc(repro.get(key))}</code>']
             for key, label in ver_keys if repro.get(key) is not None]
    versions = _table(["Component", "Pinned version"], vrows, scroll=False) if vrows else \
        "<p class='muted'>No reproducibility manifest available yet.</p>"

    return f"""
    <section id="stack" class="tab">
      <h1 id="stack-top">Stack &amp; requirements</h1>
      <p class="lede">AgentDelta is a thin, reproducible harness over established, open tools. Nothing
      about the agent's behavior is simulated: a real coding-agent CLI runs against real repositories in
      real containers, and every external component is pinned by version or image digest.</p>

      <h2>What it is built on</h2>
      {_tools_table()}

      <h2>Agents and providers</h2>
      <p>AgentDelta runs the same tasks through interchangeable agent CLIs, selected per run with
      <code>--agent</code>. Each agent talks to its own provider and a pinned model cohort:</p>
      <ul>
        <li><strong>{_tool("Claude Code")}</strong> (<code>--agent claude_code</code>) on the
        {_tool("Anthropic API")}: <code>claude-opus-4-8</code>, <code>claude-opus-4-7</code>,
        <code>claude-opus-4-6</code>, <code>claude-sonnet-4-6</code>.</li>
        <li><strong>{_tool("Codex CLI")}</strong> (<code>--agent codex_cli</code>) on the
        {_tool("OpenAI API")}: <code>gpt-5.4</code>, <code>gpt-5.1</code>, <code>gpt-5</code>,
        <code>gpt-5-mini</code>.</li>
        <li><strong>{_tool("Gemini CLI")}</strong>: planned as a third provider (already exposed by
        inspect_swe).</li>
      </ul>
      <p class="muted">Cohorts and pinned IDs live in <code>configs/models/</code>; pricing (per provider,
      with source and date) in <code>agent_delta/scoring/cost.py</code>.</p>

      <h2>Pinned versions</h2>
      <p class="muted">Captured in each suite's reproducibility manifest; drift is detected by
      <code>agentdelta validate-reproducibility</code>.</p>
      {versions}

      <h2>Fixtures and language toolchains</h2>
      <p>Tasks live in small but realistic repositories ("fixtures"), each built into its own Docker image
      pinned by digest:</p>
      <ul>
        <li><strong>{_tool("Python")} (4 fixtures)</strong> on <code>python:3.12-slim</code>, graded with
        {_tool("pytest")}: a utility toolkit, a layered multi-tenant SaaS service, a payments/webhook
        service, and a 220-file long-context ledger.</li>
        <li><strong>{_tool("TypeScript")} (1 fixture)</strong> on <code>node:20-bookworm-slim</code>,
        compiled with <code>tsc</code> and graded with the {_tool("Node.js test runner")}: a pricing library.</li>
        <li><strong>{_tool("Go")} (1 fixture)</strong> on <code>golang:1.22</code>, graded with
        <code>go test</code>: a text-processing toolkit.</li>
      </ul>

      <h2>Requirements to reproduce</h2>
      <ul>
        <li>A running {_tool("Docker")} daemon (the sandbox images are built and run locally; task
        verification via <code>agentdelta check-task</code> uses Docker only, no model calls, no cost).</li>
        <li>A provider API key for real runs: <code>ANTHROPIC_API_KEY</code> for {_tool("Claude Code")},
        <code>OPENAI_API_KEY</code> for {_tool("Codex CLI")}. The agent reaches its provider from inside
        the sandbox.</li>
        <li>Python 3.12+ in a virtual environment with {_tool("Inspect AI")}, {_tool("inspect_swe")}, and
        the Anthropic and OpenAI SDKs installed; the chosen agent CLI is provisioned by inspect_swe.</li>
        <li>Build the per-fixture images once with <code>agentdelta build-sandbox</code>, then
        <code>agentdelta run-matrix</code> drives the task x model x repetition grid with blocked
        randomization, and <code>agentdelta report-html</code> renders this document.</li>
      </ul>
      <p>Source, fixtures, tasks, and the harness are open at
      <a href="{REPO_URL}" target="_blank" rel="noopener">{_esc(REPO_URL.replace("https://", ""))}</a>.</p>
    </section>
    """


# ---------------------------------------------------------------------------
# tab: about (what and why)
# ---------------------------------------------------------------------------
def _tab_about() -> str:
    return f"""
    <section id="about" class="tab">
      <h1>About AgentDelta</h1>
      <p class="lede">AgentDelta measures the <em>delta</em> between coding-agent systems with objective,
      reproducible evidence, and refuses to report a difference it cannot defend statistically.</p>

      <h2>What it is</h2>
      <p>A benchmark that evaluates a <strong>model-plus-agent system</strong> end to end. Each task is a
      real repository with a planted bug or a missing feature; a coding agent ({_tool("Claude Code")} on
      Anthropic or {_tool("Codex CLI")} on OpenAI) works autonomously inside a pinned {_tool("Docker")}
      sandbox, and the result is graded by hidden tests the agent never sees, alongside a regression suite
      and an edit-scope check. The same tasks run across providers, so agents are compared on a level
      field. Every run records the full resource footprint: tokens, cost, wall-clock time, tool calls,
      retries, and diff size.</p>
      <p>Scoring is <strong>two-level</strong>. Level 1 ranks systems on objective success and asks which
      gains are <em>material</em> (a meaningful success delta that also survives a Holm-corrected paired
      McNemar test). Level 2, the Agentic Amplification Assessment, takes only the material gains and asks
      whether a newer model is genuinely better or merely <em>does more work by default</em>, by comparing
      it under normalized conditions (equal budget, matched workflow, strong spec).</p>

      <h2>Why it exists</h2>
      <p>Coding-agent capability is usually communicated through demos and single-number leaderboards.
      Those answer "can the model produce a plausible answer?" AgentDelta is built to answer a harder,
      more useful question:</p>
      <blockquote class="quote">Can the model make the correct change, in the correct place, with the
      correct scope, preserving hidden invariants, passing hidden tests, avoiding shortcuts, and doing so
      at an acceptable cost in time, tokens, and money?</blockquote>
      <p>Four convictions shape the design:</p>
      <ul>
        <li><strong>Objective over impressionistic.</strong> A beautiful patch that fails a hidden edge
        case, weakens a test, or leaks across tenants should fail. Grading is by tests and diffs, not taste.</li>
        <li><strong>Capability is not the same as more work.</strong> A model that wins only by spending
        5x the tokens and 4x the tool calls is <em>amplified</em>, not necessarily more capable. Separating
        the two is the whole point of the Level 2 assessment, and it changes what you should pay for.</li>
        <li><strong>"No difference" is a real, valuable result.</strong> When models are statistically tied,
        the benchmark says so rather than manufacturing a ranking from noise. The materiality gate exists to
        earn the right to make, or withhold, a claim.</li>
        <li><strong>Reproducibility is non-negotiable.</strong> Pinned models, pinned images by digest,
        content-hashed tasks and tests, seeded run order. A result you cannot reproduce is an anecdote.</li>
      </ul>
      <p>The practical payoff is an honest, cost-and-latency-aware comparison: not just "which model is
      best" but "which is best for a weak-spec user, a budget-constrained user, or a long-horizon task,"
      and whether paying for a newer model buys capability or just buys more tokens.</p>

      <h2>How to read this report</h2>
      <ul>
        <li><strong>Results</strong> leads with the headline and the honest interpretation.</li>
        <li><strong>Per-model</strong> and <strong>Per-suite</strong> hold the detailed tables.</li>
        <li><strong>Statistics</strong> shows the materiality gates (McNemar / Holm) behind every claim.</li>
        <li><strong>Raw runs</strong> is the ground truth: every run, every metric.</li>
        <li><strong>Methodology</strong> and <strong>Stack &amp; requirements</strong> document how it works
        and what it runs on; <strong>Reproducibility</strong> carries the manifests.</li>
      </ul>

      <h2>Source</h2>
      <p>AgentDelta is open source at
      <a href="{REPO_URL}" target="_blank" rel="noopener">{_esc(REPO_URL.replace("https://", ""))}</a>.
      The repository contains the harness, all fixtures, the task suite, the scoring subsystem, and the
      report generator that produced this page.</p>
    </section>
    """


# ---------------------------------------------------------------------------
# document shell
# ---------------------------------------------------------------------------
_CSS = """
:root{--accent:#c75b39;--bg:#faf9f7;--card:#fff;--ink:#1b1a18;--muted:#74706a;
--border:#e7e2d9;--head:#f3efe8;--good:#2f7d5b;--warn:#9a7a16;--bad:#b3322c;}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
h1,h2,h3,h4{font-family:Georgia,"Times New Roman",serif;font-weight:600;line-height:1.2;color:#16150f;}
h1{font-size:30px;margin:.2em 0 .4em;} h2{font-size:22px;margin:1.6em 0 .5em;
padding-bottom:.25em;border-bottom:1px solid var(--border);} h3{font-size:18px;margin:1.3em 0 .4em;}
h4{font-size:15px;margin:1.2em 0 .35em;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);}
a{color:var(--accent);text-decoration:none;} a:hover{text-decoration:underline;}
p{margin:.5em 0;} ul{margin:.4em 0 .8em;padding-left:1.2em;} li{margin:.25em 0;}
code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.86em;
background:#f1ece3;padding:.08em .35em;border-radius:3px;}
code.hash{background:none;padding:0;color:var(--muted);font-size:.8em;}
.layout{display:flex;min-height:100vh;}
.sidebar{width:248px;flex:0 0 248px;background:#1b1a18;color:#cfc9be;position:fixed;top:0;bottom:0;left:0;
display:flex;flex-direction:column;overflow-y:auto;z-index:30;}
.sidebar .brand{font-family:Georgia,serif;font-size:22px;font-weight:600;color:#f7f4ee;padding:22px 22px 6px;}
.sidebar .tagline{font-size:11.5px;color:#8d877c;padding:0 22px 14px;letter-spacing:.02em;}
.sidebar .nav{display:flex;flex-direction:column;padding:6px 10px;gap:2px;}
.sidebar .nav-item{font:inherit;font-size:14px;font-weight:500;text-align:left;color:#cfc9be;background:none;
border:none;border-left:3px solid transparent;padding:9px 14px;border-radius:0 6px 6px 0;cursor:pointer;}
.sidebar .nav-item:hover{background:#2a2824;color:#fff;}
.sidebar .nav-item.active{background:#2a2824;color:#fff;border-left-color:var(--accent);}
.sidebar .side-bottom{margin-top:auto;}
.sidebar .provfilter{padding:14px 16px 8px;border-top:1px solid #2f2c27;}
.sidebar .pf-label{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:#8d877c;padding:0 6px 6px;}
.sidebar .pf{font:inherit;font-size:12.5px;color:#cfc9be;background:none;border:1px solid #3a3630;
border-radius:20px;padding:4px 11px;margin:2px;cursor:pointer;}
.sidebar .pf:hover{background:#2a2824;color:#fff;}
.sidebar .pf.active{background:var(--accent);color:#fff;border-color:var(--accent);}
.sidebar .side-foot{padding:14px 22px 16px;font-size:12px;color:#8d877c;border-top:1px solid #2f2c27;}
.sidebar .side-foot a{color:#cfc9be;word-break:break-all;}
.sidebar .side-foot .meta{margin-top:8px;line-height:1.55;}
main{flex:1 1 auto;margin-left:248px;max-width:1080px;padding:32px 38px 90px;}
.tab{display:none;} .tab.active{display:block;}
@media(max-width:880px){
  .layout{flex-direction:column;}
  .sidebar{position:static;width:auto;flex:none;}
  .sidebar .nav{flex-direction:row;flex-wrap:wrap;}
  .sidebar .nav-item{border-left:none;border-radius:6px;}
  .sidebar .side-foot{margin-top:0;}
  main{margin-left:0;padding:24px 18px 70px;}
}
.lede{font-size:17px;color:#3a382f;max-width:75ch;}
.muted{color:var(--muted);}
blockquote.quote{margin:14px 0;padding:12px 20px;border-left:4px solid var(--accent);
background:var(--card);border-radius:0 8px 8px 0;font-size:17px;font-style:italic;color:#3a382f;max-width:78ch;}
section p{max-width:82ch;}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:12px;margin:22px 0;}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 16px;}
.kpi-val{font-size:26px;font-weight:700;font-family:Georgia,serif;color:#16150f;}
.kpi-label{font-size:12.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-top:2px;}
.kpi-sub{font-size:12px;color:var(--accent);margin-top:3px;}
.callout{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--accent);
border-radius:10px;padding:6px 22px 16px;margin:18px 0;}
.callout h3{margin-top:.7em;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:14px 0;}
@media(max-width:780px){.grid2{grid-template-columns:1fr;}}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:4px 18px 14px;}
.card h4{margin-top:1em;color:#16150f;}
.chart-card{padding:16px 18px;}
.scroll{overflow-x:auto;border:1px solid var(--border);border-radius:10px;margin:12px 0;
background:var(--card);}
.scroll::-webkit-scrollbar{height:10px;} .scroll::-webkit-scrollbar-thumb{background:#d8d1c4;border-radius:6px;}
table{border-collapse:collapse;width:100%;font-size:13px;}
table.lead,table.raw{font-size:12.5px;}
th,td{padding:7px 11px;text-align:left;white-space:nowrap;border-bottom:1px solid var(--border);}
thead th{position:sticky;top:0;background:var(--head);font-weight:600;font-size:11.5px;
text-transform:uppercase;letter-spacing:.03em;color:#5a564d;z-index:1;}
tbody tr:hover{background:#fbf8f2;}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;
font-family:"SF Mono",Menlo,Consolas,monospace;font-size:12px;}
td.center,th.center{text-align:center;}
td.rowlab{font-weight:600;background:var(--head);position:sticky;left:0;}
th.rot{font-size:11px;}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;
text-transform:uppercase;letter-spacing:.03em;}
.badge.ok{background:#dcefe3;color:var(--good);} .badge.bad{background:#f5dcd9;color:var(--bad);}
.badge.warn{background:#f5eccf;color:var(--warn);} .badge.muted{background:#ece8e0;color:var(--muted);}
table.heatmap td.heat{text-align:center;font-variant-numeric:tabular-nums;font-weight:600;font-size:12px;}
table.heatmap td.heat.na{background:#f4f1ea;color:var(--muted);font-weight:400;}
.chart{width:100%;height:auto;overflow:visible;font-family:inherit;}
.chart-title{font-size:13px;font-weight:600;fill:#16150f;}
.chart-lbl{font-size:12px;fill:var(--ink);}
.chart-val{font-size:11px;fill:var(--muted);font-variant-numeric:tabular-nums;}
.chart-val.muted{fill:#bbb;}
footer{margin-top:48px;padding-top:20px;color:var(--muted);font-size:12.5px;
border-top:1px solid var(--border);}
"""

_JS = """
(function(){
  function show(id){
    document.querySelectorAll('.tab').forEach(function(s){s.classList.toggle('active',s.id===id);});
    document.querySelectorAll('.sidebar .nav-item').forEach(function(b){
      b.classList.toggle('active',b.dataset.tab===id);});
    window.scrollTo(0,0);
  }
  document.querySelectorAll('.sidebar .nav-item').forEach(function(b){
    b.addEventListener('click',function(){show(b.dataset.tab);});
  });
  document.querySelectorAll('[data-jump]').forEach(function(a){
    a.addEventListener('click',function(e){
      e.preventDefault();
      var t=a.dataset.jump;
      var el=document.getElementById(t);
      if(el){var sec=el.closest('.tab');if(sec){show(sec.id);}
        setTimeout(function(){el.scrollIntoView({behavior:'smooth',block:'start'});},60);}
    });
  });
  function setProvider(p){
    document.querySelectorAll('.provfilter .pf').forEach(function(b){
      b.classList.toggle('active', b.dataset.prov===p);});
    document.querySelectorAll('[data-provider]').forEach(function(el){
      el.style.display=(p==='all'||el.getAttribute('data-provider')===p||el.getAttribute('data-provider')==='mixed')?'':'none';
    });
  }
  document.querySelectorAll('.provfilter .pf').forEach(function(b){
    b.addEventListener('click',function(){setProvider(b.dataset.prov);});
  });
})();
"""


def render_html(suites: list[dict], *, generated_at: str = "") -> str:
    """suites = [{report, records, repro}], one per suite. Returns a full HTML doc."""
    suites = [s for s in suites if s["records"]]
    # difficulty-ordered: by max hardness then run count
    def order_key(s):
        hards = [r.get("hardness_level") for r in s["records"] if r.get("hardness_level")]
        rank = max((int(h[1:]) for h in hards if h and h[1:].isdigit()), default=0)
        return (rank, len(s["records"]))
    suites = sorted(suites, key=order_key)

    all_records: list[dict] = []
    for s in suites:
        for r in s["records"]:
            r = dict(r)
            r["suite"] = s["report"]["suite"]
            all_records.append(r)
    gmodels = _model_global(all_records)

    models = _sorted_models({r["model_id"] for r in all_records})
    bench = suites[0]["report"]["benchmark_version"] if suites else "?"
    meta = (f"benchmark v{bench} &middot; {len(suites)} suites &middot; {len(all_records)} runs "
            f"&middot; {len(models)} models &middot; agent: "
            f"{_esc(suites[0]['report'].get('agent')) if suites else '?'}")
    if generated_at:
        meta += f" &middot; generated {_esc(generated_at)}"

    # Provider filter (only when more than one provider is present).
    provs_present = sorted({model_provider(r["model_id"]) for r in all_records} - {"unknown"})
    if len(provs_present) > 1:
        btns = '<button class="pf active" data-prov="all">All</button>' + "".join(
            f'<button class="pf" data-prov="{p}">{_esc(PROVIDER_LABELS.get(p, p).split(" (")[0])}</button>'
            for p in provs_present)
        provider_filter = f'<div class="provfilter"><div class="pf-label">Provider</div>{btns}</div>'
    else:
        provider_filter = ""

    tabs = REPORT_SECTIONS
    nav = "".join(
        f'<button class="nav-item{" active" if i == 0 else ""}" data-tab="{tid}">{_esc(label)}</button>'
        for i, (tid, label) in enumerate(tabs))

    body = "".join([
        _tab_overview(suites, all_records, gmodels),
        _tab_models(gmodels, suites),
        _tab_crossprovider(all_records),
        _tab_suites(suites),
        _tab_stats(suites),
        _tab_raw(all_records),
        _tab_methodology(suites),
        _tab_stack(suites),
        _tab_repro(suites),
        _tab_about(),
    ])

    repo_label = _esc(REPO_URL.replace("https://", ""))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AgentDelta: cross-suite report</title>
<style>{_CSS}</style>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <div class="brand">Agent<b>Delta</b></div>
    <div class="tagline">Reproducible coding-agent evaluation</div>
    <nav class="nav">{nav}</nav>
    <div class="side-bottom">
      {provider_filter}
      <div class="side-foot">
        <a href="{REPO_URL}" target="_blank" rel="noopener">{repo_label}</a>
        <div class="meta">{meta}</div>
      </div>
    </div>
  </aside>
  <main>{body}
    <footer>
      Generated by <code>agentdelta report-html</code>. Self-contained: no external assets, no network.
      Objective scores are hidden-test-graded; statistical materiality uses Holm-corrected paired McNemar.
      Source: <a href="{REPO_URL}" target="_blank" rel="noopener">{repo_label}</a>.
    </footer>
  </main>
</div>
<script>{_JS}</script>
</body>
</html>"""
