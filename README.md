# AgentDelta

Reproducible evaluation of frontier coding agents and model-upgrade deltas.

AgentDelta measures the **delta** between agentic coding systems under controlled,
repeatable, auditable conditions - not whether a new model "feels" better, but
whether a claimed improvement holds up on real coding-agent workloads. See
[`SPEC.md`](SPEC.md) for the full methodology.

## Status

**v0.1 - vertical slice + initial task suite.** Five tasks across four
categories run end-to-end through Inspect AI + Claude Code (via `inspect_swe`)
inside a Docker sandbox, with objective scoring (baseline/public/hidden tests,
scope control) and SPEC §16 run records. The architecture is wired for the full
50-task / 4-model benchmark and for future Codex CLI / Gemini CLI adapters.

Fixtures span two languages: `python_package` (the `mathkit` library, pytest) and
`go_cli` (the `textkit` Go module, `go test`). The scorer, builder, and task
checker are language-aware.

| Task | Fixture | Category | What |
| --- | --- | --- | --- |
| `task_001` | python_package | small_bug_fix | Add a `median` function |
| `task_002` | python_package | small_bug_fix | Fix `chunk()` dropping the final partial chunk |
| `task_003` | python_package | medium_feature | Add a `slugify` function |
| `task_004` | python_package | multi_file_refactor | Extract a shared `require_nonempty` helper |
| `task_005` | python_package | security_fix | Fix path traversal in `read_fixture` |
| `go_task_001` | go_cli | small_bug_fix | Fix `Truncate` past the string length |
| `go_task_002` | go_cli | medium_feature | Add a `Capitalize` function |

What works today:
- `agentdelta list-tasks` / `validate-task`
- `agentdelta build-sandbox` - builds the fixture Docker image
- `agentdelta check-task --all` - verifies each task fails at base and passes
  with its reference solution (no model, no API)
- `agentdelta run --task <id> --dry-run` - full scoring pipeline, no API cost
- `agentdelta run --task <id> --model claude-opus-4-8` - real run
- `agentdelta run --mode <mode>` - run a task under a normalized mode
  (equal_budget, matched_workflow, strong_spec, cost_matched, time_matched,
  older_plus_scaffold; see `docs/modes.md`)
- `agentdelta aggregate` / `agentdelta report` - turn run records into rankings,
  confidence intervals, paired comparisons, the Agentic Amplification Analysis,
  and a Cross-Mode Synthesis that confirms whether a gain is intrinsic, amplified,
  or workflow-equivalent (see SPEC-ADDENDUM.md, `docs/amplification.md`)

Not yet built: review-pass capture, a second-language fixture, network-locked
sandbox, the Codex/Gemini adapters.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
# Put your key in .env as ANTHROPIC_API_KEY=sk-ant-...
```

Requirements: Python 3.11+, Docker.

## Quick start

```bash
# 1. Build the sandbox image for the python_package fixture
.venv/bin/agentdelta build-sandbox --fixture python_package

# 2. Prove the pipeline with no API calls (applies the reference solution)
.venv/bin/agentdelta run --task task_001 --dry-run

# 3. Real run against a pinned model
.venv/bin/agentdelta run --task task_001 --model claude-opus-4-8 --repetitions 1

# 4. Aggregate run records into a Markdown report
.venv/bin/agentdelta report --suite anthropic-claude-code-v0.1
```

Run records land in `results/raw/<suite>/<run_id>/run.json` with the final diff;
reports land in `results/reports/<suite>/` as `report.json` and `report.md`.

## Layout

| Path | What |
| --- | --- |
| `agent_delta/` | Python package: config, registry, scoring, runners, reporting |
| `evals/` | Inspect task entry points |
| `tasks/` | Task definitions (prompt, public/hidden tests, acceptance) |
| `repos/` | Fixture repositories and manifests |
| `sandboxes/` | Dockerfiles + compose for agent sandboxes |
| `configs/` | Pinned model / agent / scoring configs |
| `results/` | Raw run records, normalized data, reports |

## Principles (from the SPEC)

Pinned model IDs only (no aliases), same task from the same clean repo state,
objective scoring first, no silent model fallback, predeclared scoring, and raw
results published alongside rankings with confidence intervals.
