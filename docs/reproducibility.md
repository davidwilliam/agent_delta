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

## Known gaps to close before an official run (Phase 1)

1. **Network lockdown.** The v0.1 compose leaves the default network up so the
   Claude Code CLI and any first-run download work without friction. The SPEC
   target is `network: disabled`. Hardening path: bake/inject the agent binary on
   the host, route model calls through the Inspect proxy, then set
   `network_mode: none` in `sandboxes/claude-code/compose.yaml`.
2. **Pinned CLI version.** The image installs the latest `@anthropic-ai/claude-code`.
   Pin an exact version and record it.
3. **Pinned dependency lockfiles** for each fixture.
4. **`reproducibility.json`** emitted per report (schema in SPEC §27): Inspect /
   inspect-swe versions, image digests, tasks hash, scoring hash, run-order seed.

## Fallback detection (SPEC §5.5)

Silent model fallback invalidates a run. inspect_swe proxies the agent's model
calls through Inspect, so the actual model served is observable in the eval log.
`agent_delta/scoring/validity.py` compares the served model (from the sample's
model usage) against the requested pinned ID and marks any mismatch invalid with
reason `model_fallback`. Invalid runs are reported separately and excluded from
rankings (see `docs/methodology.md`).
