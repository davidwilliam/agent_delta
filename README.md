# AgentDelta

Reproducible, objective evaluation of frontier coding agents and model-upgrade deltas.

AgentDelta measures the **delta** between agentic coding systems under controlled,
repeatable, auditable conditions. It does not ask whether a new model "feels"
better; it asks whether a claimed improvement holds up on real coding-agent
workloads, graded by hidden tests, and whether any gain is genuine capability or
just a newer model doing more work by default.

Source: https://github.com/davidwilliam/agent_delta

The full methodology is in [`SPEC.md`](SPEC.md), the amplification framework in
[`SPEC-ADDENDUM.md`](SPEC-ADDENDUM.md), and the hard-task design rules in
[`HARD-TASKS-SPEC.md`](HARD-TASKS-SPEC.md). Shorter topic docs live in
[`docs/`](docs/) (methodology, scoring, modes, amplification, reproducibility,
task authoring, limitations).

## What it does

Every run is a real coding agent ([Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
driven by [inspect_swe](https://pypi.org/project/inspect-swe/) on top of
[Inspect AI](https://inspect.aisi.org.uk/)) acting inside a per-fixture
[Docker](https://www.docker.com/) sandbox on a seeded git repository, graded by
tests the agent never sees.

Scoring is two levels:

- **Level 1 (primary):** rank systems by objective success (verified pass +
  hidden-test score + regression avoidance + scope control + set-relative
  cost/time efficiency), and decide which Model-B-over-Model-A gains are
  *material*: a success delta above threshold that also survives a Holm-corrected
  paired McNemar test.
- **Level 2 (Agentic Amplification):** for material gains only, decide whether the
  newer model is intrinsically better or merely does more work by default (more
  tokens, time, tool calls, retries, self-review), by re-running under normalized
  modes (equal budget, matched workflow, strong spec).

When models are statistically tied, AgentDelta reports the tie rather than
manufacturing a ranking from noise.

## Status

A **50-task suite** across **6 fixtures** in **3 languages**, evaluated across the
four 1M-context Anthropic models (`claude-opus-4-8`, `claude-opus-4-7`,
`claude-opus-4-6`, `claude-sonnet-4-6`). The harness is provider-pluggable: the
**Anthropic (Claude Code)** and **OpenAI (Codex CLI)** agents are both implemented,
selectable per run with `--agent`. Each provider declares its own pinned model
cohort under `configs/models/`.

| Fixture | Language | Runner | What it is |
| --- | --- | --- | --- |
| `python_package` | Python | pytest | `mathkit` utility toolkit (stats, sequences, text, io) |
| `saas` | Python | pytest | Layered multi-tenant service (models/storage/policy/service/api/ownership/lifecycle) |
| `payments` | Python | pytest | Webhook/invoice/refund service with simulated write latency |
| `long_context` | Python | pytest | 220-file multi-schema ledger (~228k tokens) for long-context tasks |
| `pricing_ts` | TypeScript | `node --test` | Money/cart/discount/tax library compiled with `tsc` |
| `go_cli` | Go | `go test` | `textkit` text-processing module |

Task mix: 14 categories spanning the HARD-TASKS-SPEC families (multi-file
localization, hidden-invariant preservation, security/authorization,
state-machine correctness, cross-file contract consistency, long-context
retrieval, concurrency/idempotency, minimal-diff repair, test-writing, dependency
migration). The graded **core** suite is 39 multi-file/repo-level tasks (100%
multi-file); 11 single-file algorithmic tasks are tagged `tier: supplementary`.
Hardness spans H1 to H5; over half the tasks carry author-written minimal / strong
/ workflow prompt variants. See [`tasks/SUITE_PLAN.md`](tasks/SUITE_PLAN.md).

## Requirements

- **Python 3.11+** for the harness.
- **Docker** (daemon running). Fixture images bundle their own toolchains
  (Python 3.12, Node 20 + TypeScript, Go 1.22), so no host install of Node or Go
  is needed.
- An **Anthropic API key** for real model runs (task authoring and verification
  need only Docker, no API). Set `ANTHROPIC_API_KEY` in your environment or `.env`.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"      # drop [dev] to skip pytest/ruff
cp .env.example .env                   # then put your real key in .env (ANTHROPIC_API_KEY)
```

Build the sandbox image for each fixture once (run-commit avoids BuildKit issues):

```bash
for f in python_package saas payments long_context pricing_ts go_cli; do
  .venv/bin/agentdelta build-sandbox --fixture "$f" --method run-commit
done
```

## Quick start

```bash
# Verify every task fails at base and passes with its reference (Docker only, no API, no cost)
.venv/bin/agentdelta check-task --all

# Prove the scoring pipeline on one task with no API calls (applies the reference solution)
.venv/bin/agentdelta run --task task_001 --dry-run

# Real run of one task against a pinned model
.venv/bin/agentdelta run --task hard_task_004 --model claude-opus-4-8 --network enabled --effort high

# Run a matrix: all 4 models x 5 reps over chosen tasks
.venv/bin/agentdelta run-matrix --suite my-suite \
  --tasks hard_task_004,pay_concurrency_01 --repetitions 5 --network enabled --effort high

# Generate the comprehensive HTML report across every suite
.venv/bin/agentdelta report-html
```

Run records land in `results/raw/<suite>/<run_id>/run.json` (with the final diff);
per-suite reports in `results/reports/<suite>/` (`report.json`, `report.md`,
`reproducibility.json`); the cross-suite HTML at
`results/reports/agentdelta-report.html`, with the machine-readable
`agentdelta-report.json` beside it.

## Command reference

All commands are subcommands of `agentdelta` (installed entry point; or
`.venv/bin/agentdelta`).

### Authoring and validation (no API, no cost)

`list-tasks` lists available tasks.

`validate-task TASK_ID` checks a task's definition and that its referenced files
(prompt, tests, fixture) exist.

`check-task [TASK_ID] [--all]` spins up the fixture container and verifies the task
is non-trivial (public/hidden tests fail at base) and solvable (baseline + public +
hidden pass after applying `reference_solution/`). Uses Docker only.

`build-sandbox --fixture NAME [--method auto|dockerfile|run-commit]` builds the
Docker image for a fixture. `run-commit` (recommended) builds without BuildKit.

### Running

`run --task TASK_ID [options]` runs one task for one model in one mode and writes a
run record.

| Option | Meaning |
| --- | --- |
| `--task` | Task ID (required), e.g. `hard_task_004` |
| `--agent` | `claude_code` (Anthropic, default) or `codex_cli` (OpenAI) |
| `--model` | Pinned model ID (default: the first included model for the agent's provider) |
| `--repetitions` | Repeated runs (epochs) |
| `--suite` | Results suite name |
| `--mode` | Evaluation mode (see Modes below) |
| `--scaffold-model` | Model that receives the scaffold under `older_plus_scaffold` |
| `--network` | `disabled` (default) or `enabled`; a real model run needs `enabled` |
| `--effort` | Reasoning effort: `low`/`medium`/`high`/`xhigh`/`max` |
| `--dry-run` | Apply the reference solution instead of calling the model (no API cost) |

`run-matrix --suite NAME [options]` runs the task x model x repetition grid with
blocked randomization of model order.

| Option | Meaning |
| --- | --- |
| `--suite` | Results suite name (required) |
| `--agent` | `claude_code` (default) or `codex_cli`; sets the provider for every run |
| `--tasks` | Comma-separated task IDs (default: all) |
| `--models` | Comma-separated model IDs (default: the agent's provider's included cohort) |
| `--repetitions` | Repetitions per task per model |
| `--mode` | Evaluation mode |
| `--seed` | Run-order randomization seed |
| `--randomize / --no-randomize` | Blocked-randomize model order (default on) |
| `--network`, `--effort`, `--dry-run` | As for `run` |

### Reporting

`aggregate --results DIR --suite NAME [--baseline MODEL]` turns raw run records into
`report.json` (scores, confidence intervals, paired comparisons, amplification).

`report --suite NAME [--baseline MODEL] [--level 1|2|both] [--output PATH]` writes a
Markdown report (and `report.json`). `--results` defaults from the suite name.

`report-html [--suites a,b,c] [--baseline MODEL] [--output PATH] [--min-runs N]`
generates one self-contained HTML report across all suites (results-first overview,
per-model, per-suite, statistics, raw runs, methodology, stack, reproducibility,
about). Multiple providers (Claude Code, Codex CLI) appear side by side, with a
sidebar **provider filter** (All / Anthropic / OpenAI / ...). Suites named `*smoke*`
are excluded unless listed explicitly in `--suites`. On every run it also writes the
machine-readable exports below, so they never drift from the rendered report.

`report-export [--suites a,b,c] [--baseline MODEL] [--output DIR] [--min-runs N]`
writes the **sharded JSON export** (schema v2), the sustainable source of truth for
downstream consumers (for example the AI Unmasked website):

```
results/reports/export/
  index.json              # manifest: schema_version, providers[], models[], sections[], suites[]
  suites/<suite>.json     # one shard per suite: {suite, provider, report, records, repro}
```

A consumer reads `index.json` (small), then lazy-loads only the suite shards (or one
provider) it needs. Adding an experiment/model/task adds one shard plus one index
entry, so no single file grows unbounded. Everything is provider-tagged for filtering.

`report-json [--suites ...]` writes the legacy single-file `agentdelta-report.json`
(schema v1; the same data in one document). Kept during transition; prefer the
sharded export. All exports are strict, JS-parseable JSON (no NaN/Infinity). See
[`docs/website_json_export.md`](docs/website_json_export.md).

### Review and reproducibility

`review-packets --suite NAME` writes blinded `packet.json` files next to each run
for optional human review (fill each packet's rubric into a `review.json`, then
re-run `report`).

`validate-reproducibility --suite NAME` recomputes content hashes (tasks, scoring,
fixtures, hidden tests, sandbox image digests) and checks them against the recorded
manifest, detecting drift.

## Evaluation modes

A mode normalizes a run without changing the task, fixture, base commit, or scoring.
Set with `--mode`.

| Mode | Effect |
| --- | --- |
| `default` | Each model as a normal user would run it |
| `minimal_spec` | The terse, weak-user prompt (author `minimal` variant if present) |
| `strong_spec` | Full requirements (author `strong` variant, else synthesized from acceptance criteria) |
| `matched_workflow` | The same explicit step-by-step workflow forced on every model |
| `equal_budget` | Comparable token/message/time/cost caps for all models |
| `cost_matched` | Same dollar budget per task |
| `time_matched` | Same wall-clock budget per task |
| `older_plus_scaffold` | The older baseline model gets structured support; newer models run default |

Running the same task across modes is what lets the Cross-Mode Synthesis tell
intrinsic capability apart from agentic amplification. See [`docs/modes.md`](docs/modes.md).

## How scoring works

A run is **verified** only if the public tests pass, the pre-existing suite still
passes (no regression), and no hard scope or forbidden-shortcut violation occurred.
Hidden tests measure how completely the fix generalizes; scope control measures edit
discipline (forbidden paths, forbidden patterns such as skipped tests, and
max-files/lines budgets). Test-writing tasks are graded by mutation kill rate
against planted mutants. Details in [`docs/scoring.md`](docs/scoring.md) and
[`docs/amplification.md`](docs/amplification.md).

## Layout

| Path | What |
| --- | --- |
| `agent_delta/` | Python package: config, registry, modes, eval/matrix runners, scoring, reporting |
| `agent_delta/scoring/` | Objective/cost/latency/stats/amplification/diff/testrunner/review subsystems |
| `agent_delta/reporting/` | Run-record builder, aggregation, Markdown and HTML report generators |
| `evals/` | Inspect AI task entry point (`anthropic_claude_code.py`) |
| `tasks/` | Task definitions (prompt + variants, public/hidden tests, reference solution, acceptance), plus `SUITE_PLAN.md` |
| `repos/fixtures/`, `repos/manifests/` | Fixture repositories and their build manifests |
| `sandboxes/` | Dockerfile for the agent sandboxes |
| `configs/` | Pinned model / agent / scoring / mode configs |
| `results/raw/`, `results/reports/` | Raw run records and generated reports |
| `docs/` | Topic docs (methodology, scoring, modes, amplification, reproducibility, task authoring, limitations) |
| `tests/` | Unit tests for the harness |

## Principles

Pinned model IDs only (no aliases); the same task from the same clean,
digest-pinned repository state; objective scoring first; no silent model fallback
(served-model mismatch quarantines a run); predeclared scoring and modes; and raw
results published alongside rankings with confidence intervals and materiality
tests. A result you cannot reproduce is an anecdote.

## Roadmap

AgentDelta supports the Claude Code (Anthropic) and Codex CLI (OpenAI) agents
today, selectable with `--agent`, so the same tasks and the same objective scoring
compare coding agents across providers on a level field. The Gemini CLI is next
(`inspect_swe` already exposes it). OpenAI model pricing in
`agent_delta/scoring/cost.py` is verified against the OpenAI developer pricing docs.

## Contributing

Questions, feedback, or ideas for improving AgentDelta are very welcome. If you have
a suggestion, a new task idea, or want to add a fixture or a provider adapter, please
get in touch at the contact email below, or open an issue or pull request on the
repository.

To contribute code:

- Fork the repository and work on a feature branch.
- Before opening a pull request, run `.venv/bin/agentdelta check-task --all` and
  `.venv/bin/python -m pytest -q`, and make sure both are green.
- For new tasks, follow [`docs/task_authoring.md`](docs/task_authoring.md): every
  task must fail at base and pass with its reference solution, and must ship public
  and hidden tests plus an explicit forbidden-shortcut check.
- Open an issue to discuss larger changes (new fixtures, new providers, scoring
  changes) before building them, so we can agree on the approach first.

## Author

**David William Silva**
Contact: contact@davidwsilva.com

AgentDelta exists because the narrative and culture around AI models lean blindly
toward the latest and greatest, with little discernment, no pragmatics, and rarely
any justification for upgrading, least of all a justification for the additional
cost. When a model is called "better", that judgment usually rests on a subjective,
biased, and ungrounded personal perception that some task was handled better by the
newer model, rather than on objective metrics. It is often not even clear whether
the latest model is genuinely more capable or is simply doing more agentic work:
more tool calls, longer workflows, more retries, more self-review. AgentDelta aims
to answer those questions and to provide a clear, evidence-based understanding of
model capability, alongside the cost, latency, and amplification metrics that should
actually drive an upgrade decision.
