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
from typing import Any

from agent_delta.reporting.html import REPORT_SECTIONS

# Bump only on a BREAKING change (rename/remove/move/retype a key the website
# relies on). Additive changes (new optional key, new appended section) do not bump.
SCHEMA_VERSION = 1


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
