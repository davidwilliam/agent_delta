"""Machine-readable JSON export of the cross-suite report (docs/website_json_export.md).

The HTML report is one rendering of this data; this JSON is the source of truth the
AI Unmasked website reads to build its AgentDelta page. It is the exact same
`bundle` that render_html consumes (one entry per suite: report, records, repro),
wrapped with a stable, versioned envelope. Anything visible in the HTML must be
derivable from here.

Strict JSON only: no NaN/Infinity, UTF-8, deterministic ordering, indent 2.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from agent_delta.reporting.html import PROVIDER_LABELS, REPORT_SECTIONS, model_provider

# Bump only on a BREAKING change (rename/remove/move/retype a key a consumer
# relies on). Additive changes (new optional key, new appended section) do not bump.
# v1: single agentdelta-report.json. v2: sharded export/ (index.json + suite shards).
SCHEMA_VERSION = 1
EXPORT_SCHEMA_VERSION = 2


def build_report_json(bundle: list[dict], *, generated_at: str, baseline: str) -> dict[str, Any]:
    """Wrap the render_html bundle in the stable export envelope.

    `bundle` is `[{"report": ..., "records": [...], "repro": ... | None}, ...]`,
    the same structure render_html consumes. `report` per suite is the exact
    build_report() output (identical to results/reports/<suite>/report.json).
    """
    versions = {b["report"].get("benchmark_version") for b in bundle}
    versions.discard(None)
    if len(versions) == 1:
        benchmark_version: Any = next(iter(versions))
    else:
        benchmark_version = sorted(versions)

    suites = sorted(bundle, key=lambda b: b["report"].get("suite") or "")
    return {
        "schema_version": SCHEMA_VERSION,
        "benchmark_version": benchmark_version,
        "generated_at": generated_at,
        "baseline": baseline,
        "sections": [{"id": sid, "label": label} for sid, label in REPORT_SECTIONS],
        "suites": [
            {
                "suite": b["report"].get("suite"),
                "report": b["report"],
                "records": b["records"],
                "repro": b["repro"],
            }
            for b in suites
        ],
    }


def dump_report_json(data: dict) -> str:
    """Serialize to strict, JS-parseable JSON. Fails loudly on any non-finite float."""
    safe = _strip_non_finite(data)
    return json.dumps(safe, indent=2, ensure_ascii=False, sort_keys=False, allow_nan=False)


# ---------------------------------------------------------------------------
# Sharded export (schema v2): a small index.json + one shard per suite.
# Sustainable as providers/experiments/tasks grow: adding a suite = adding one
# shard + one index entry; no single file grows unbounded. Consumers read the
# index, then lazy-load only the shards they need (e.g. one provider).
# ---------------------------------------------------------------------------
def _suite_provider(entry: dict) -> str:
    """The provider of a suite: the single provider of its runs, else 'mixed'."""
    provs = set()
    for r in entry.get("records") or []:
        provs.add(r.get("provider") or model_provider(r.get("model_id", "")))
    for mid in (entry["report"].get("models") or []):
        provs.add(model_provider(mid))
    provs.discard("unknown")
    if len(provs) == 1:
        return next(iter(provs))
    return "mixed" if provs else "unknown"


def _shard_filename(suite: str) -> str:
    return f"suites/{suite}.json"


def build_sharded_export(bundle: list[dict], *, generated_at: str, baseline: str) -> tuple[dict, dict]:
    """Return (index, shards). `shards` maps suite name to its shard dict.

    Each shard carries the same per-suite report/records/repro as the single-file
    export; the index is a small manifest the consumer reads first.
    """
    suites = sorted(bundle, key=lambda b: b["report"].get("suite") or "")
    versions = {b["report"].get("benchmark_version") for b in bundle}
    versions.discard(None)
    benchmark_version: Any = next(iter(versions)) if len(versions) == 1 else sorted(versions)

    shards: dict[str, dict] = {}
    suite_index: list[dict] = []
    model_provider_map: dict[str, str] = {}
    provider_suites: dict[str, list[str]] = {}

    for b in suites:
        name = b["report"].get("suite")
        prov = _suite_provider(b)
        models = sorted(b["report"].get("models") or [])
        for mid in models:
            model_provider_map[mid] = model_provider(mid)
        provider_suites.setdefault(prov, []).append(name)
        shards[name] = {
            "schema_version": EXPORT_SCHEMA_VERSION,
            "suite": name,
            "provider": prov,
            "report": b["report"],
            "records": b["records"],
            "repro": b["repro"],
        }
        suite_index.append({
            "suite": name,
            "provider": prov,
            "n_runs": len(b["records"]),
            "n_models": len(models),
            "models": models,
            "file": _shard_filename(name),
        })

    providers = []
    for pid in sorted(provider_suites):
        providers.append({
            "id": pid,
            "label": PROVIDER_LABELS.get(pid, pid),
            "suites": sorted(provider_suites[pid]),
            "models": sorted(m for m, p in model_provider_map.items() if p == pid),
        })

    index = {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "benchmark_version": benchmark_version,
        "generated_at": generated_at,
        "baseline": baseline,
        "sections": [{"id": sid, "label": label} for sid, label in REPORT_SECTIONS],
        "providers": providers,
        "models": [{"id": m, "provider": p} for m, p in sorted(model_provider_map.items())],
        "suites": suite_index,
    }
    return index, shards


def write_sharded_export(index: dict, shards: dict, out_dir: str | Path) -> Path:
    """Write index.json + suites/<suite>.json under out_dir (strict JSON). Returns out_dir."""
    out_dir = Path(out_dir)
    (out_dir / "suites").mkdir(parents=True, exist_ok=True)
    (out_dir / "index.json").write_text(dump_report_json(index))
    for name, shard in shards.items():
        (out_dir / "suites" / f"{name}.json").write_text(dump_report_json(shard))
    return out_dir


def _strip_non_finite(obj: Any) -> Any:
    """Recursively make a value JSON-safe.

    NaN/Infinity become None; numpy scalars (and other objects exposing .item())
    are coerced to native Python numbers so json.dumps does not need a default=
    fallback. Tuples become lists.
    """
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, int):
        return obj
    if isinstance(obj, dict):
        return {k: _strip_non_finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_strip_non_finite(v) for v in obj]
    if obj is None or isinstance(obj, str):
        return obj
    # numpy scalars and similar single-value objects expose .item().
    item = getattr(obj, "item", None)
    if callable(item):
        try:
            return _strip_non_finite(item())
        except (ValueError, TypeError):
            pass
    return obj
