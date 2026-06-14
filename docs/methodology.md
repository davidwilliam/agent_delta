# Methodology

AgentDelta evaluates coding *systems* (model + scaffold + tools + sandbox), not
abstract models. See SPEC §2 for the full thesis and §11 for the run lifecycle.

## Evaluation modes (SPEC §2)

1. **Model-upgrade mode** — same scaffold (Claude Code), different model versions.
   *This is the v0.1 focus.*
2. **Agent-product mode** — different agent products, each with its native model.
3. **Controlled-model mode** — different models through a common Inspect solver.

Cross-agent results (mode 2) must never be reported as pure model comparisons.

## Run lifecycle (SPEC §11)

1. Fresh sandbox container from the pinned fixture image (clean base commit).
2. Baseline test suite must pass before the agent runs — else the run is invalid.
3. Agent runs from the task prompt with standardized, hermetic tooling.
4. Post-run: capture diff + modified files; run baseline (regression), public, and
   hidden suites; compute scope control; assemble objective components.
5. Archive the run record and diff; container is torn down.

## Repetition & randomization (SPEC §12)

Frontier models are non-deterministic, so tasks are repeated (`--repetitions`,
Inspect epochs). For multi-model matrices, use blocked randomization of model
order per task/repetition; full-matrix orchestration lands in Phase 2.

## Validity (SPEC §11.4)

A run is invalid if baseline tests fail first, the wrong/fallback model is served,
the agent crashes for infrastructure reasons, the sandbox cannot initialize, or
state is contaminated. Invalid runs are reported separately, never silently
dropped.
