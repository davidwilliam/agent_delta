# AI Unmasked: how to consume the AgentDelta export

This is the integration guide for the AI Unmasked "AgentDelta" page. It explains how
to read the machine-readable export and build the page in your own design system.

Do NOT scrape `agentdelta-report.html`. It is one rendering of the data, themed and
subject to layout change. The JSON export below is the source of truth: anything the
HTML report shows is derivable from it.

## What you receive

A small **index** plus one **shard per suite** (schema v2):

```
export/
  index.json              # the manifest you read first (a few KB)
  suites/<suite>.json      # one file per suite (KB to ~1 MB each)
```

Read `index.json` once, then lazy-load only the shards you actually need (for
example only one provider's suites). Adding experiments/models/tasks over time adds
new shards and new index entries; existing files do not grow unbounded, so the page
stays fast.

(There is also a single-file `agentdelta-report.json`, schema v1, with the same data
in one document. It is kept only during transition. Prefer the sharded export.)

## Hosting

AgentDelta writes the export to `results/reports/export/`. Serve those files at a
stable base URL of your choosing (copy into your app's `public/` at build time, push
to a CDN, or fetch from the repository). The only contract is that, relative to a
base URL, `index.json` and `suites/<file>` resolve, where `<file>` is exactly the
`file` value the index gives for each suite.

## index.json

```jsonc
{
  "schema_version": 2,
  "benchmark_version": "agentdelta-v0.1",   // string, or array if suites disagree
  "generated_at": "2026-06-16 02:42 UTC",
  "baseline": "claude-opus-4-6",
  "sections": [                              // drives your page navigation, in order
    { "id": "overview", "label": "Results" },
    { "id": "models",   "label": "Per-model" },
    // ... methodology, stack, reproducibility, about, etc.
  ],
  "providers": [                             // use this to build the provider filter
    {
      "id": "anthropic",
      "label": "Anthropic (Claude Code)",
      "suites": ["anthropic-hardest5-4x5", "..."],
      "models": ["claude-opus-4-8", "..."]
    },
    { "id": "openai", "label": "OpenAI (Codex CLI)", "suites": ["openai-hardest5-4x5"], "models": ["gpt-5.4", "..."] }
  ],
  "models": [ { "id": "claude-opus-4-8", "provider": "anthropic" }, { "id": "gpt-5.4", "provider": "openai" } ],
  "suites": [
    {
      "suite": "openai-hardest5-4x5",
      "provider": "openai",
      "n_runs": 100,
      "n_models": 4,
      "models": ["gpt-5.4", "gpt-5.1-2025-11-13", "gpt-5", "gpt-5-mini-2025-08-07"],
      "file": "suites/openai-hardest5-4x5.json"
    }
    // ... one entry per suite
  ]
}
```

## suites/<suite>.json (a shard)

```jsonc
{
  "schema_version": 2,
  "suite": "openai-hardest5-4x5",
  "provider": "openai",
  "report": { /* the aggregated report for this suite, see below */ },
  "records": [ /* one object per run, the raw-runs ground truth */ ],
  "repro": { /* reproducibility manifest, or null */ }
}
```

`report` is the aggregated view used by the report's tabs:

- `report.models`: list of model ids in the suite.
- `report.per_mode.default`: the default-mode results, containing:
  - `models[modelId]`: per-model metrics, including `success_rate`, `success_ci95`
    (Wilson 95% CI), `hidden_test_rate`, `regression_rate`, `scope_control`,
    `cost_mean_usd`, `cost_per_success_usd`, `median_time_to_success_s`,
    `tokens_total_mean`, `objective_score`, `failure_labels`, `category_success`,
    `diagnostics`, `work` (resource footprint), `wall_clock_percentiles`.
  - `level1`: `{ ranking: [modelId...], baseline, improvements: [{ model_b, model_a,
    success_delta_pp, raw_p_value, holm_p_value, material, materiality_reason }] }`.
    Materiality = a meaningful success delta that also survives a Holm-corrected
    paired McNemar test; render `material: false` honestly as "no significant
    difference".
  - `level2`: the agentic-amplification analysis (only for material gains).
  - `cost_frontier`, `latency_frontier`: Pareto points for cost/latency-vs-success.
- `report.n_tasks`, `report.n_runs`, `report.n_invalid`, `report.scoring_formula`,
  `report.limitations`.

`records` is the per-run detail (the "Raw runs" table). Each record has `task_id`,
`hardness_level`, `task_category`, `model_id`, `provider`, `mode`, `epoch`,
`scoring` (`verified_success`, `hidden_test_score`, `regression_avoidance`,
`scope_control`, `public_tests`, `hidden_tests`), `usage` (tokens, cost), `execution`
(wall_clock_seconds, invalid, invalid_reason), `agent_behavior`, `diff_metrics`, and
`failure_labels`.

## Building the page

1. Fetch `index.json`. Build the nav from `sections` and the provider filter from
   `providers`.
2. For the selected view (default: everything), fetch the relevant shards from
   `suites[].file`. For "just Claude" / "just OpenAI", fetch only the suites whose
   `provider` matches (or use `providers[].suites`).
3. Render per-suite tables from `shard.report.per_mode.default`, raw runs from
   `shard.records`, and reproducibility from `shard.repro`.
4. For cross-suite views (a global per-model table, a model x suite heatmap), merge
   across the shards you loaded.

### Example (Next.js / fetch)

```ts
const BASE = process.env.AGENTDELTA_EXPORT_BASE; // e.g. https://.../export

async function loadIndex() {
  return (await fetch(`${BASE}/index.json`)).json();
}

async function loadSuite(file: string) {
  return (await fetch(`${BASE}/${file}`)).json(); // file is "suites/<name>.json"
}

// Provider filter: load only the shards for one provider (or all).
async function loadForProvider(index, providerId /* or null for all */) {
  const suites = index.suites.filter(s => !providerId || s.provider === providerId);
  return Promise.all(suites.map(s => loadSuite(s.file)));
}
```

## Filtering by provider

Everything is provider-tagged: `index.providers[]`, each `suites[].provider`, and each
`models[].provider`, plus `provider` inside every shard and every record. Default to
showing all providers; to filter, restrict to the matching shards/models. No
recomputation server-side is required: you already have all the data per shard.

## Versioning and stability

- `schema_version` is `2` for this sharded export. A breaking change (rename, remove,
  retype, or move a key you rely on) will bump it and be noted in
  `docs/website_json_export.md`. Additive changes (new optional keys, new sections,
  new suites/providers/models) will NOT bump it.
- Treat these as a stable public API: `sections[].id`, suite names, model ids,
  provider ids, and the metric keys above.
- Be tolerant of unknown keys: the export will grow new fields over time. Ignore what
  you do not recognize rather than failing.

## Updates

The export is regenerated on every report run (`agentdelta report-export`, and
automatically by `agentdelta report-html`). To refresh the page, re-fetch
`index.json` and the shards; `generated_at` tells you when it was produced. New
experiments appear as new entries in `index.suites` and new files under `suites/`.

## Reference

- Implementation spec (what produced this): `docs/website_json_export.md`.
- Source: https://github.com/davidwilliam/agent_delta
