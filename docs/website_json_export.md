# Machine-readable JSON export for the website

## Context and goal

The **AI Unmasked** website (a separate Next.js project) renders an "AgentDelta"
page in its own editorial design system. It must **not** scrape
`agentdelta-report.html` (72 tables of themed markup with no embedded data is
brittle and breaks on every layout change). Instead, AgentDelta must publish a
**stable, versioned JSON file that contains everything the HTML report shows**,
written automatically on every report generation.

This document is the implementation spec. Implement it exactly. Do not change
scoring, task definitions, or the HTML report's appearance. This is an
**additive export only**.

The contract in one line: **`agentdelta-report.json` is the source of truth;
`agentdelta-report.html` is one rendering of it. Anything visible in the HTML
must be derivable from the JSON.**

## What to build

1. On **every** `report-html` run, also write
   `results/reports/agentdelta-report.json` next to the HTML. No separate manual
   step — the JSON must never drift from the HTML.
2. Add a standalone `report-json` command (same options as `report-html`) for
   JSON-only generation. It must reuse the same data-building code path so the
   two never diverge.
3. The JSON must be **strict, valid JSON** (parseable by JavaScript
   `JSON.parse`): no `NaN`, no `Infinity`, no Python `repr` strings, UTF-8,
   deterministic ordering, `indent=2`.

## Exact code change

The data is **already structured before it becomes HTML**. In
`agent_delta/cli.py`, the `report-html` command (`report_html_cmd`) builds:

```python
bundle.append({"report": report, "records": records, "repro": repro})
...
doc = render_html(bundle, generated_at=generated)
out.write_text(doc)
```

`bundle` is a `list[dict]` — one entry per suite — and is the same structure
`render_html` consumes. Persist that bundle as JSON.

### Step 1 — factor the section list into a shared constant (sidebar sync)

`render_html` (in `agent_delta/reporting/html.py`) hardcodes the sidebar/tab
list:

```python
tabs = [
    ("overview", "Results"),
    ("models", "Per-model"),
    ("suites", "Per-suite"),
    ("stats", "Statistics"),
    ("raw", "Raw runs"),
    ("methodology", "Methodology"),
    ("stack", "Stack &amp; requirements"),
    ("repro", "Reproducibility"),
    ("about", "About"),
]
```

Move this to a module-level constant and use it in **both** the HTML renderer
and the JSON export:

```python
# agent_delta/reporting/html.py  (or a small shared module)
REPORT_SECTIONS: list[tuple[str, str]] = [
    ("overview", "Results"),
    ("models", "Per-model"),
    ("suites", "Per-suite"),
    ("stats", "Statistics"),
    ("raw", "Raw runs"),
    ("methodology", "Methodology"),
    ("stack", "Stack & requirements"),   # plain text label, NOT HTML-escaped, in the JSON
    ("repro", "Reproducibility"),
    ("about", "About"),
]
```

`render_html` keeps using it (HTML-escape the label there as today). The JSON
export emits the **un-escaped** labels. This single source means: **when you add
or rename a section in the future, you change one list, and both the HTML and the
website's sidebar update automatically.**

### Step 2 — build a serializable export structure

Add a function in the reporting package, e.g.
`agent_delta/reporting/json_export.py`:

```python
import json, math
from agent_delta.reporting.html import REPORT_SECTIONS

SCHEMA_VERSION = 1

def build_report_json(bundle: list[dict], *, generated_at: str, baseline: str) -> dict:
    # benchmark_version is per-suite in report.json; surface it at top level
    # and assert the suites agree.
    versions = {b["report"].get("benchmark_version") for b in bundle}
    benchmark_version = next(iter(versions)) if len(versions) == 1 else sorted(v for v in versions if v)

    return {
        "schema_version": SCHEMA_VERSION,
        "benchmark_version": benchmark_version,
        "generated_at": generated_at,
        "baseline": baseline,
        "sections": [{"id": sid, "label": label} for sid, label in REPORT_SECTIONS],
        "suites": [
            {
                "suite": b["report"].get("suite"),
                "report": b["report"],     # identical to results/reports/<suite>/report.json
                "records": b["records"],   # the run records the HTML "Raw runs" tab uses
                "repro": b["repro"],       # reproducibility.json or null
            }
            for b in bundle
        ],
    }

def dump_report_json(data: dict) -> str:
    safe = _strip_non_finite(data)            # NaN/Infinity -> None
    return json.dumps(safe, indent=2, ensure_ascii=False, sort_keys=False, allow_nan=False)

def _strip_non_finite(obj):
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    if isinstance(obj, dict):
        return {k: _strip_non_finite(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_strip_non_finite(v) for v in obj]
    return obj
```

Notes:
- **Serializability.** `report` and `repro` are already JSON (they are written to
  `report.json` / `reproducibility.json`). For `records`: if `load_run_records`
  returns dataclasses or objects, convert them to plain dicts using the **same
  serializer that already writes `run.json`** (reuse `write_run_records` / the
  run-record `to_dict`/`asdict`). Do not hand-roll a second serializer. If a
  field is genuinely non-serializable, fix it at the serializer, not with
  `default=str` hacks.
- Use `allow_nan=False` so the dump **fails loudly** if any non-finite slips
  through after `_strip_non_finite` — that guarantees valid JS-parseable JSON.

### Step 3 — write it on every report run

In `report_html_cmd`, after writing the HTML:

```python
from agent_delta.reporting.json_export import build_report_json, dump_report_json

json_out = out.with_suffix(".json")  # results/reports/agentdelta-report.json
data = build_report_json(bundle, generated_at=generated, baseline=baseline)
json_out.write_text(dump_report_json(data))
click.secho(f"Wrote {json_out} ({len(json_out.read_text()) // 1024} KB)", fg="green")
```

Add a sibling `report-json` command with the **same** `--suites / --baseline /
--output / --min-runs` options that builds `bundle` the same way (extract the
bundle-building loop into a shared helper so `report-html` and `report-json`
share it) and writes only the JSON.

## The data contract (what the website depends on)

Top-level shape (stable):

```jsonc
{
  "schema_version": 1,
  "benchmark_version": "…",      // string, or array if suites disagree
  "generated_at": "2026-06-15 07:19 UTC",
  "baseline": "claude-opus-4-6",
  "sections": [                  // drives the website sidebar; mirrors HTML tabs
    { "id": "overview", "label": "Results" },
    { "id": "models",   "label": "Per-model" },
    … one per REPORT_SECTIONS entry …
  ],
  "suites": [
    {
      "suite": "anthropic-v0.1-frontier",
      "report": { … exact build_report() output: models, modes, per_mode,
                   cross_mode, scoring_formula, n_tasks, limitations, … },
      "records": [ { … one run record, same fields the HTML "Raw runs" tab uses … } ],
      "repro": { … reproducibility.json … } | null
    }
  ]
}
```

- `report` per suite is **byte-for-byte the same object** as
  `results/reports/<suite>/report.json`. Keep it that way (reuse `build_report`).
- `suites` is sorted by suite name (deterministic).
- Unknown/extra keys are allowed and expected to grow; the website is written to
  ignore keys it does not recognize.

## Forward-compatibility rules (this is the important part)

AgentDelta will keep evolving: new sections, new sidebar items, new metrics, new
modes, new models. To keep the website working without becoming a maintenance
treadmill:

1. **Single section list.** The sidebar/sections come from `REPORT_SECTIONS`
   only. Adding/renaming/reordering a section = edit that one list. Both HTML and
   the website's nav follow automatically.
2. **JSON is a superset of the HTML.** Whenever you add a new `_tab_*` section or
   new metric/table to `render_html`, ensure the data behind it is present in the
   JSON (inside `report` / `records` / `repro`, or a new top-level key). A
   reviewer rule: *if a number appears in the HTML, it must be reachable in the
   JSON.* Add a test that fails if a section id in `REPORT_SECTIONS` has no
   corresponding data path documented here.
3. **Schema versioning.**
   - `schema_version` starts at `1`.
   - **Additive** change (new optional key, new section appended, new metric on
     an existing object): do **not** bump; just append a line to the changelog
     below. The website tolerates unknown keys.
   - **Breaking** change (rename, remove, move, or change the type of an existing
     key the website relies on): **bump `schema_version`** and add a changelog
     entry describing the migration. Avoid breaking changes; prefer adding a new
     key and deprecating the old one for a release.
4. **Stability of identifiers.** Treat `sections[].id`, suite names, model IDs,
   mode names, and metric keys as a public API. Do not silently rename them.

## JSON-safety and determinism checklist

- [ ] Valid JSON: `json.dumps(..., allow_nan=False)` succeeds (no NaN/Infinity).
- [ ] UTF-8, `ensure_ascii=False`, `indent=2`.
- [ ] Suites sorted by name; section order = `REPORT_SECTIONS` order.
- [ ] No Python objects leak through (dataclasses converted via the real
      run-record serializer; no `default=str` masking).

## Acceptance criteria (run these before considering it done)

1. `.venv/bin/agentdelta report-html` writes **both**
   `results/reports/agentdelta-report.html` **and**
   `results/reports/agentdelta-report.json`.
2. `.venv/bin/agentdelta report-json` writes the JSON alone, identical content.
3. Strict-parse + sanity:
   ```bash
   python3 -c "import json; d=json.load(open('results/reports/agentdelta-report.json')); \
   assert d['schema_version']==1; \
   assert d['sections'] and all('id' in s and 'label' in s for s in d['sections']); \
   assert d['suites'] and all({'suite','report','records'} <= set(s) for s in d['suites']); \
   print('ok', d['benchmark_version'], len(d['suites']), [s['id'] for s in d['sections']])"
   ```
4. Re-dump round-trips with `allow_nan=False` (no non-finite floats).
5. A unit test in `tests/` that: builds a small bundle (or uses an existing
   fixture/suite), calls `build_report_json`, asserts the top-level keys, asserts
   `sections` equals `REPORT_SECTIONS`, asserts each suite carries `report` ==
   the suite's `report.json`, and asserts `json.dumps(..., allow_nan=False)`
   succeeds.
6. Update the **Reporting** section of `README.md` to mention the JSON artifact
   and the `report-json` command, and note that `report-html` also emits it.

## Schema changelog

- **v1** (initial): `schema_version`, `benchmark_version`, `generated_at`,
  `baseline`, `sections[]`, `suites[]` ({ suite, report, records, repro }).

## Out of scope

- No changes to scoring, modes, task definitions, fixtures, or the HTML report's
  visual output.
- No new runtime dependencies.
