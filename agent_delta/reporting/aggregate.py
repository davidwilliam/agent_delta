"""Aggregate run records into a structured report (SPEC section 17 + ADDENDUM).

Loads the per-run JSON written by reporting.result, groups by evaluation mode and
model, computes the authoritative set-relative objective scores (SPEC 14), the
statistical summaries (SPEC 15), and the Agentic Amplification metrics
(ADDENDUM 6 to 8), and returns a report dict ready to render.
"""

from __future__ import annotations

import json
import re
import statistics
from pathlib import Path
from typing import Any

from agent_delta import BENCHMARK_VERSION, config
from agent_delta.scoring import amplification as amp
from agent_delta.scoring import stats as st
from agent_delta.scoring.cost import cost_efficiency
from agent_delta.scoring.latency import time_efficiency
from agent_delta.reporting.charts import cost_success_frontier, latency_success_frontier
from agent_delta.scoring.objective import ObjectiveComponents, full_score, objective_score
from agent_delta.scoring.review import load_review_score
from agent_delta.scoring.synthesis import synthesize_cross_mode


def _mean(vals: list[float | None]) -> float | None:
    clean = [v for v in vals if isinstance(v, (int, float))]
    return sum(clean) / len(clean) if clean else None


def load_run_records(results_dir: Path) -> list[dict[str, Any]]:
    """Load every run.json under a results directory, attaching any review score."""
    records = []
    for p in sorted(Path(results_dir).rglob("run.json")):
        rec = json.loads(p.read_text())
        rs = load_review_score(p.parent)
        if rs is not None:
            rec["review_score"] = rs
        records.append(rec)
    return records


def _version_key(model_id: str) -> tuple:
    m = re.search(r"(\d+)[-.](\d+)", model_id)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def _work_components(records: list[dict]) -> dict[str, float | None]:
    """Mean per-run work signals used by the Agentic Work Index."""
    def mean_of(path: tuple[str, str]) -> float | None:
        return _mean([(r.get(path[0]) or {}).get(path[1]) for r in records])

    # file_edits prefers the transcript edit-tool count; falls back to the
    # number of distinct files changed on disk when transcript counts are absent.
    file_edits = mean_of(("agent_behavior", "file_edits"))
    if file_edits is None:
        file_edits = mean_of(("agent_behavior", "files_modified"))
    return {
        "input_tokens": mean_of(("usage", "input_tokens")),
        "output_tokens": mean_of(("usage", "output_tokens")),
        "wall_clock_seconds": mean_of(("execution", "wall_clock_seconds")),
        "api_calls": mean_of(("agent_behavior", "api_calls")),
        "tool_calls": mean_of(("agent_behavior", "tool_calls")),
        "shell_commands": mean_of(("agent_behavior", "shell_commands")),
        "test_runs": mean_of(("agent_behavior", "test_runs")),
        "file_reads": mean_of(("agent_behavior", "files_read")),
        "file_edits": file_edits,
        "retry_count": mean_of(("agent_behavior", "retry_count")),
        "review_passes": mean_of(("agent_behavior", "review_passes")),
    }


def _aggregate_model(model_id: str, records: list[dict]) -> dict[str, Any]:
    valid = [r for r in records if not r.get("execution", {}).get("invalid")]
    invalid = [r for r in records if r.get("execution", {}).get("invalid")]
    n = len(valid)
    succ = [bool(r["scoring"]["verified_success"]) for r in valid]
    n_succ = sum(succ)
    success_rate = n_succ / n if n else 0.0

    hidden = _mean([r["scoring"].get("hidden_test_score") for r in valid]) or 0.0
    regression_avoidance = _mean([r["scoring"].get("regression_avoidance") for r in valid]) or 0.0
    scope = _mean([r["scoring"].get("scope_control") for r in valid]) or 0.0
    partial = _mean([r["scoring"].get("partial_objective_score") for r in valid])

    costs = [(r.get("usage") or {}).get("estimated_cost_usd") for r in valid]
    cost_total = sum(c for c in costs if isinstance(c, (int, float)))
    cost_per_success = (cost_total / n_succ) if n_succ and cost_total else None

    succ_times = [
        (r.get("execution") or {}).get("wall_clock_seconds")
        for r, s in zip(valid, succ) if s
    ]
    succ_times = [t for t in succ_times if isinstance(t, (int, float))]
    median_time_to_success = statistics.median(succ_times) if succ_times else None
    all_times = [t for t in ((r.get("execution") or {}).get("wall_clock_seconds") for r in valid)
                 if isinstance(t, (int, float))]

    fail_counter: dict[str, int] = {}
    for r in valid:
        for lbl in r.get("failure_labels", []):
            fail_counter[lbl] = fail_counter.get(lbl, 0) + 1
    invalid_by_reason: dict[str, int] = {}
    for r in invalid:
        reason = (r.get("execution", {}).get("invalid_reason") or "unknown").split(":")[0]
        invalid_by_reason[reason] = invalid_by_reason.get(reason, 0) + 1

    return {
        "model_id": model_id,
        "n_runs": n,
        "n_invalid": len(records) - n,
        "failure_labels": dict(sorted(fail_counter.items(), key=lambda kv: -kv[1])),
        "invalid_by_reason": invalid_by_reason,
        "category_success": _category_success(valid),
        "diagnostics": _diagnostics(valid),
        "n_success": n_succ,
        "success_rate": success_rate,
        "success_ci95": list(st.wilson_ci(n_succ, n)),
        "hidden_test_rate": hidden,
        "regression_rate": 1.0 - regression_avoidance,
        "scope_control": scope,
        "partial_objective_mean": partial,
        "review_mean": _mean([r.get("review_score") for r in valid]),
        "cost_total_usd": cost_total or None,
        "cost_mean_usd": (cost_total / n) if (n and cost_total) else None,
        "cost_per_success_usd": cost_per_success,
        "median_time_to_success_s": median_time_to_success,
        "wall_clock_percentiles": st.percentiles(all_times),
        "tokens_total_mean": _mean([(r.get("usage") or {}).get("total_tokens") for r in valid]),
        "components": ObjectiveComponents(
            verified_success=success_rate,
            hidden_test_score=hidden,
            regression_avoidance=regression_avoidance,
            scope_control=scope,
        ),
        "work": _work_components(valid),
        "_success_by_key": {
            (r["task_id"], r.get("epoch")): s for r, s in zip(valid, succ)
        },
        "_cost_by_key": {
            (r["task_id"], r.get("epoch")): (r.get("usage") or {}).get("estimated_cost_usd")
            for r in valid
        },
        "_time_by_key": {
            (r["task_id"], r.get("epoch")): (r.get("execution") or {}).get("wall_clock_seconds")
            for r in valid
        },
    }


def _category_success(valid: list[dict]) -> dict[str, float]:
    """Success rate per task category (SPEC 17.2)."""
    by_cat: dict[str, list[bool]] = {}
    for r in valid:
        cat = r.get("task_category") or "uncategorized"
        by_cat.setdefault(cat, []).append(bool(r["scoring"]["verified_success"]))
    return {cat: sum(v) / len(v) for cat, v in by_cat.items() if v}


def _diagnostics(valid: list[dict]) -> dict[str, float | None]:
    """Diagnostic ratios and timings (SPEC 13.3, 20), averaged over valid runs."""
    def ratios(num_key, den_key, section="agent_behavior"):
        out = []
        for r in valid:
            d = (r.get(section) or {}).get(den_key)
            nval = (r.get(section) or {}).get(num_key)
            if isinstance(d, (int, float)) and d > 0 and isinstance(nval, (int, float)):
                out.append(nval / d)
        return _mean(out)

    timeouts = [1.0 if (r.get("execution") or {}).get("timeout") else 0.0 for r in valid]
    return {
        "failed_command_ratio": ratios("failed_shell_commands", "shell_commands"),
        "exploration_edit_ratio": ratios("files_read", "file_edits"),
        "timeout_rate": (sum(timeouts) / len(timeouts)) if timeouts else None,
        "mean_time_to_first_edit_s": _mean(
            [(r.get("agent_behavior") or {}).get("time_to_first_edit") for r in valid]),
        "mean_time_to_first_test_s": _mean(
            [(r.get("agent_behavior") or {}).get("time_to_first_test") for r in valid]),
        "mean_diff_locality": _mean([(r.get("diff_metrics") or {}).get("diff_locality") for r in valid]),
        "mean_patch_entropy": _mean([(r.get("diff_metrics") or {}).get("patch_entropy") for r in valid]),
        "mean_test_to_code_ratio": _mean(
            [(r.get("diff_metrics") or {}).get("test_to_code_ratio") for r in valid]),
    }


def aggregate_mode(records: list[dict], baseline: str | None = None) -> dict[str, Any]:
    """Aggregate the records for a single evaluation mode."""
    by_model: dict[str, list[dict]] = {}
    for r in records:
        by_model.setdefault(r["model_id"], []).append(r)

    models = {mid: _aggregate_model(mid, recs) for mid, recs in by_model.items()}

    # Set-relative efficiency (SPEC 14.3 / 14.4) -> authoritative objective score.
    cps = [m["cost_per_success_usd"] for m in models.values() if m["cost_per_success_usd"]]
    best_cps = min(cps) if cps else None
    mtts = [m["median_time_to_success_s"] for m in models.values() if m["median_time_to_success_s"]]
    best_time = min(mtts) if mtts else None

    amp_cfg = amp.load_amplification_config()
    work_by_model = {mid: m["work"] for mid, m in models.items()}
    awi, awi_components = amp.agentic_work_index(work_by_model, amp_cfg["agentic_work_index"]["weights"])

    for mid, m in models.items():
        ce = cost_efficiency(m["cost_per_success_usd"], best_cps) if (m["cost_per_success_usd"] and best_cps) else 1.0
        te = time_efficiency(m["median_time_to_success_s"], best_time) if (m["median_time_to_success_s"] and best_time) else 1.0
        obj = objective_score(m["components"], ce, te)
        m["cost_efficiency"] = ce
        m["time_efficiency"] = te
        m["objective_score"] = obj
        m["review_score"] = m.get("review_mean")
        m["full_score"] = full_score(obj, m.get("review_mean"))
        m["work_index"] = awi.get(mid)
        # Quality-per-resource uses raw per-task spend (ADDENDUM 6.3/6.4), not
        # per-success cost (which drives the SPEC efficiency components above).
        mins_mean = (m["work"].get("wall_clock_seconds") / 60.0) if m["work"].get("wall_clock_seconds") else None
        m.update(amp.quality_efficiency(obj, m["cost_mean_usd"], mins_mean, m["work_index"]))

    # Ranking by objective score.
    ranking = sorted(models.values(), key=lambda m: m["objective_score"], reverse=True)
    for i, m in enumerate(ranking, 1):
        m["rank"] = i

    # Baseline = explicit, else the oldest model version present.
    if baseline is None or baseline not in models:
        baseline = sorted(models, key=lambda mid: (_version_key(mid), mid))[0] if models else None

    level1 = _level1_assessment(models, ranking, baseline)
    level2 = _level2_assessment(models, baseline, level1["improvements"], amp_cfg, awi_components)
    cost_frontier = cost_success_frontier(models)
    latency_frontier = latency_success_frontier(models)

    # Strip non-serializable helpers.
    for m in models.values():
        for k in ("_success_by_key", "_cost_by_key", "_time_by_key"):
            m.pop(k, None)
        m["components"] = m["components"].as_dict()

    return {
        "models": models,
        "baseline": baseline,
        "best_cost_per_success_usd": best_cps,
        "best_median_time_to_success_s": best_time,
        "level1": level1,
        "level2": level2,
        "cost_frontier": cost_frontier,
        "latency_frontier": latency_frontier,
    }


def _level1_assessment(models: dict, ranking: list, baseline: str | None) -> dict:
    """Level 1 (SPEC.md): ranking and which Model B over Model A gains are material.

    Materiality (SPEC 14.6 / 15.4): success improvement >= threshold percentage
    points AND statistically supported (paired McNemar p < 0.05). This is what
    Level 2 narrows down to.
    """
    materiality = config.load_scoring_config()["materiality"]
    thresh_pp = materiality["task_success_delta_pp"]
    improvements = []
    raw_p: dict[str, float] = {}
    if baseline:
        a = models[baseline]
        for mid, b in models.items():
            if mid == baseline:
                continue
            paired = _paired(a, b)
            p = paired.p_value if paired else 1.0
            raw_p[mid] = p
            improvements.append({
                "model_b": mid,
                "model_a": baseline,
                "success_delta_pp": (b["success_rate"] - a["success_rate"]) * 100.0,
                "objective_delta": b["objective_score"] - a["objective_score"],
                "paired": paired.__dict__ if paired else None,
                "raw_p_value": p,
            })
        # Holm correction across the family of pairwise comparisons (SPEC 15.3);
        # materiality uses the corrected p-value.
        corrected = st.holm_correction(raw_p) if raw_p else {}
        for imp in improvements:
            cp = corrected.get(imp["model_b"], imp["raw_p_value"])
            imp["holm_p_value"] = cp
            delta_pp = imp["success_delta_pp"]
            significant = cp < 0.05
            imp["material"] = delta_pp >= thresh_pp and significant
            if delta_pp < thresh_pp:
                imp["materiality_reason"] = (
                    f"success delta {delta_pp:+.1f} pp is below the {thresh_pp} pp threshold")
            elif not significant:
                imp["materiality_reason"] = (
                    f"success delta {delta_pp:+.1f} pp but Holm-corrected McNemar p = {cp:.3f} (>= 0.05)")
            else:
                imp["materiality_reason"] = (
                    f"success delta {delta_pp:+.1f} pp with Holm-corrected McNemar p = {cp:.3f}")
    return {
        "ranking": [m["model_id"] for m in ranking],
        "baseline": baseline,
        "improvements": improvements,
    }


def _level2_assessment(
    models: dict, baseline: str | None, improvements: list, amp_cfg: dict, awi_components: list
) -> dict:
    """Level 2 (SPEC-ADDENDUM): amplification analysis of ONLY the material gains.

    For each materially-better Model B from Level 1, decide whether the gain is
    intrinsic or driven by agentic amplification. Non-material gains are recorded
    as excluded (not escalated to Level 2).
    """
    assessments, excluded = [], []
    for imp in improvements:
        if not imp["material"]:
            excluded.append({
                "model_b": imp["model_b"],
                "model_a": imp["model_a"],
                "reason": imp["materiality_reason"],
            })
            continue
        a, b = models[imp["model_a"]], models[imp["model_b"]]
        a_metrics, b_metrics = _amp_metrics(a), _amp_metrics(b)
        ratios = amp.amplification_ratios(a_metrics, b_metrics)
        cls = amp.classify_improvement(
            a_metrics, b_metrics, ratios, amp_cfg,
            success_material=True, success_delta_pp=imp["success_delta_pp"],
        )
        assessments.append({
            "model_b": imp["model_b"],
            "model_a": imp["model_a"],
            "success_delta_pp": imp["success_delta_pp"],
            "objective_delta": imp["objective_delta"],
            "ratios": ratios,
            "cost_wilcoxon": _paired_continuous(a, b, "_cost_by_key"),
            "time_wilcoxon": _paired_continuous(a, b, "_time_by_key"),
            "quality_delta_per_extra_dollar": amp.quality_delta_per_extra(
                a["objective_score"], b["objective_score"], a["cost_mean_usd"], b["cost_mean_usd"]),
            "quality_delta_per_extra_minute": amp.quality_delta_per_extra(
                a["objective_score"], b["objective_score"], _minutes(a), _minutes(b)),
            "classification": {
                "category": cls.category,
                "rationale": cls.rationale,
                "red_flags": cls.red_flags,
                "modes_missing": cls.modes_missing,
            },
        })
    return {
        "baseline": baseline,
        "work_index_components": awi_components,
        "assessments": assessments,
        "excluded": excluded,
    }


def _amp_metrics(m: dict) -> dict[str, float | None]:
    w = m["work"]
    return {
        "total_tokens": m["tokens_total_mean"],
        "cost": m["cost_mean_usd"],
        "wall_clock_seconds": w.get("wall_clock_seconds"),
        "tool_calls": w.get("tool_calls"),
        "retry_count": w.get("retry_count"),
        "test_runs": w.get("test_runs"),
        "api_calls": w.get("api_calls"),
        "work_index": m["work_index"],
    }


def _minutes(m: dict) -> float | None:
    """Mean per-task wall-clock minutes (raw spend, for extra-minute deltas)."""
    t = (m.get("work") or {}).get("wall_clock_seconds")
    return (t / 60.0) if t else None


def _paired(a: dict, b: dict):
    keys = sorted(set(a["_success_by_key"]) & set(b["_success_by_key"]))
    if not keys:
        return None
    return st.mcnemar([a["_success_by_key"][k] for k in keys],
                      [b["_success_by_key"][k] for k in keys])


def _paired_continuous(a: dict, b: dict, attr: str):
    """Wilcoxon signed-rank on a paired continuous metric (B vs A)."""
    am, bm = a.get(attr, {}), b.get(attr, {})
    xs, ys = [], []
    for k in sorted(set(am) & set(bm)):
        av, bv = am[k], bm[k]
        if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
            xs.append(bv)
            ys.append(av)
    return st.wilcoxon_signed_rank(xs, ys) if xs else None


def build_report(results_dir: Path, suite: str, baseline: str | None = None) -> dict[str, Any]:
    """Build the full report dict from a results directory."""
    records = load_run_records(results_dir)
    by_mode: dict[str, list[dict]] = {}
    for r in records:
        by_mode.setdefault(r.get("mode", "default"), []).append(r)

    per_mode = {mode: aggregate_mode(recs, baseline) for mode, recs in by_mode.items()}
    tasks = {r["task_id"] for r in records}
    invalid = [
        {"run_id": r["run_id"], "model_id": r["model_id"],
         "reason": r.get("execution", {}).get("invalid_reason")}
        for r in records if r.get("execution", {}).get("invalid")
    ]

    materiality_pp = config.load_scoring_config()["materiality"]["task_success_delta_pp"]
    default_baseline = per_mode.get("default", {}).get("baseline")
    cross_mode = None
    if default_baseline and len(by_mode) > 1:
        cross_mode = synthesize_cross_mode(per_mode, default_baseline, materiality_pp)

    return {
        "benchmark_version": BENCHMARK_VERSION,
        "suite": suite,
        "agent": records[0]["agent"] if records else None,
        "n_tasks": len(tasks),
        "n_runs": len(records),
        "n_invalid": len(invalid),
        "invalid_runs": invalid,
        "models": sorted({r["model_id"] for r in records}),
        "modes": sorted(by_mode),
        "scoring_formula": config.load_scoring_config(),
        "per_mode": per_mode,
        "cross_mode": cross_mode,
        "limitations": _limitations(by_mode, per_mode),
    }


def _limitations(by_mode: dict, per_mode: dict) -> list[str]:
    out = []
    if list(by_mode) == ["default"]:
        out.append(
            "Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be "
            "distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes."
        )
    present = set()
    for mode in per_mode.values():
        present.update(mode["level2"].get("work_index_components") or [])
    missing = [c for c in amp.WORK_COMPONENTS if c not in present]
    if missing:
        out.append(
            "Agentic Work Index components with no captured data in this run: "
            + ", ".join(missing) + " (the index uses the remaining components)."
        )
    return out


def write_report_json(report: dict, suite: str, out_root: Path | None = None) -> Path:
    out_root = out_root or (config.RESULTS_DIR / "reports" / suite)
    out_root.mkdir(parents=True, exist_ok=True)
    path = out_root / "report.json"
    path.write_text(json.dumps(report, indent=2, default=str))
    return path
