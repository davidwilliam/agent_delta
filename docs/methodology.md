# Methodology

AgentDelta evaluates coding *systems* (model + scaffold + tools + sandbox), not
abstract models. See SPEC §2 for the full thesis and §11 for the run lifecycle.

## Evaluation modes (SPEC §2)

1. **Model-upgrade mode** - same scaffold (Claude Code), different model versions.
   *This is the v0.1 focus.*
2. **Agent-product mode** - different agent products, each with its native model.
3. **Controlled-model mode** - different models through a common Inspect solver.

Cross-agent results (mode 2) must never be reported as pure model comparisons.

## Run lifecycle (SPEC §11)

1. Fresh sandbox container from the pinned fixture image (clean base commit).
2. Baseline test suite must pass before the agent runs - else the run is invalid.
3. Agent runs from the task prompt with standardized, hermetic tooling.
4. Post-run: capture diff + modified files; run baseline (regression), public, and
   hidden suites; compute scope control; assemble objective components.
5. Archive the run record and diff; container is torn down.

## Repetition & randomization (SPEC §12)

Frontier models are non-deterministic, so tasks are repeated (`--repetitions`,
Inspect epochs). For multi-model matrices, use blocked randomization of model
order per task/repetition; full-matrix orchestration lands in Phase 2.

## Validity (SPEC §11.4, §5.5, §11.1)

A run is invalid if baseline tests fail first, the wrong/fallback model is served,
the agent crashes for infrastructure reasons, the sandbox cannot initialize, or
state is contaminated. Invalid runs are reported separately, never silently
dropped.

This is enforced in `agent_delta/scoring/validity.py`. Every run runs the baseline
suite once before the agent (a setup solver records `baseline_pre_ok`); a broken
baseline marks the run invalid (`baseline_failed_pre_run`). The served model is
compared against the requested pinned ID and any mismatch is `model_fallback`. A
sample-level exception is `agent_crash`. Invalid runs are excluded from rankings
and listed in their own report section with reasons.

## Failure taxonomy (SPEC §23)

Every valid run that did not verify gets one or more failure labels
(`agent_delta/scoring/failure.py`): public/hidden test failures, regression,
build failure, scope violations (forbidden file, overbroad edit), incomplete
implementation, did-not-run-tests, and the heuristics `hardcoded_solution`
(public passes but hidden largely fails) and `looping_or_thrashing`. The report
shows failure-label frequencies per model. Labels needing signals not yet
captured (lint, typecheck, refusal) remain in the taxonomy for manual use.
