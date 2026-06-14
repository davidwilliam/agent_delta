# Reproducibility

AgentDelta aims for reproducible-or-auditable runs (SPEC §5.1, §27).

## What is pinned today (v0.1 slice)

- **Model ID** - full ID only, never an alias (SPEC §5.2). Passed to
  `inspect_ai.eval()` as `anthropic/<model-id>`; the agent inherits it.
- **Fixture base commit** - the sandbox image runs `git init && commit` on the
  pristine fixture, so every run starts from an identical clean worktree.
- **Sandbox image** - built from `sandboxes/claude-code/Dockerfile`, tagged
  `agentdelta/<fixture>:v0.1`. Capture the image digest for official runs.
- **Scoring** - `configs/scoring/default.yaml`, frozen (see `docs/scoring.md`).
- **Tasks** - `tasks/<id>/` with `task.yaml`, prompt, and public/hidden tests.

## Reproducibility manifest (SPEC §27)

`agentdelta run-matrix` writes `results/reports/<suite>/reproducibility.json`
(`agent_delta/reproducibility.py`): agentdelta / Inspect / inspect-swe / Python /
Docker versions, host OS, sandbox image digests, the agent-settings hash, the
model and task lists, the `tasks_hash`, `scoring_hash`, `hidden_tests_hash`, the
run-order seed, and the realized run order. The hidden-test hash is a commitment
(SPEC §8.5): publish it before evaluation so the hidden tests cannot change after
seeing results. `agentdelta validate-reproducibility --suite <s>` recomputes the
content hashes and flags any drift.

## Run order (SPEC §12.2)

`run-matrix` blocked-randomizes the model order per task and repetition from the
seed (`agent_delta/matrix.py`), so no model runs all its repetitions before the
next. Each repetition is recorded as a distinct epoch so paired comparisons line
up across models.

## Network lockdown (SPEC §22)

The sandbox network defaults to `none` (`network_mode: ${AGENTDELTA_NETWORK:-none}`
in `sandboxes/claude-code/compose.yaml`). The runner sets it from each task's
`execution.network` (disabled -> `none`, enabled -> `bridge`); every task is
disabled today. Fixture dependencies are baked into the image and the scoring
tools run fully offline (verified: external egress is blocked while pytest, git,
and `go test` still work; the Go image bakes `GOPROXY=off`). A real model run that
needs the inspect_swe model proxy is the one case that may require a restricted
network; enable it per task and record it.

## Dependency pinning (SPEC §5.2)

- **Python fixture**: `repos/fixtures/python_package/requirements.lock` pins the
  exact deps (captured from the image); the build installs from it then the
  package with `--no-deps`.
- **Go fixture**: `go.mod` pins the Go version; with no external modules there is
  no `go.sum`.
- **Agent CLI**: `configs/agents/claude_code.yaml` `version` (a pinned channel by
  default; set an exact version for an official run). Recorded in the manifest as
  `agent_cli_version`.
- The manifest's `fixtures_hash` covers the fixture manifests and lockfiles.

## Known gaps to close before an official run

1. **Exact agent CLI version.** `version: stable` is a pinned channel; resolve it
   to an exact version string once a live run reports it.

## Fallback detection (SPEC §5.5)

Silent model fallback invalidates a run. inspect_swe proxies the agent's model
calls through Inspect, so the actual model served is observable in the eval log.
`agent_delta/scoring/validity.py` compares the served model (from the sample's
model usage) against the requested pinned ID and marks any mismatch invalid with
reason `model_fallback`. Invalid runs are reported separately and excluded from
rankings (see `docs/methodology.md`).
