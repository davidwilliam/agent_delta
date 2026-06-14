# AgentDelta

Reproducible evaluation of frontier coding agents and model-upgrade deltas.

AgentDelta measures the **delta** between agentic coding systems under controlled,
repeatable, auditable conditions — not whether a new model "feels" better, but
whether a claimed improvement holds up on real coding-agent workloads. See
[`SPEC.md`](SPEC.md) for the full methodology.

## Status

**v0.1 — vertical slice.** One pilot task (`task_001`) runs end-to-end through
Inspect AI + Claude Code (via `inspect_swe`) inside a Docker sandbox, with
objective scoring (baseline/public/hidden tests, scope control) and SPEC §16 run
records. The architecture is wired for the full 50-task / 4-model benchmark and
for future Codex CLI / Gemini CLI adapters.

What works today:
- `agentdelta list-tasks` / `validate-task`
- `agentdelta build-sandbox` — builds the fixture Docker image
- `agentdelta run --task task_001 --dry-run` — full pipeline, no API cost
- `agentdelta run --task task_001 --model claude-opus-4-8` — real run

Not yet built: aggregation/statistics, report generation, additional tasks &
fixtures, network-locked sandbox, the Codex/Gemini adapters.

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
```

Run records land in `results/raw/<suite>/<run_id>/run.json` with the final diff.

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
