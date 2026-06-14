# Scoring (frozen for v0.1)

This document is the authoritative description of how AgentDelta scores runs. It
implements SPEC §14 and must not change after an official run begins. The machine
-readable form lives in `configs/scoring/default.yaml`.

## Per-run components (absolute)

Each computed by `agent_delta.scoring.sandbox_scorer` inside the sandbox after the
agent stops. Each is in `[0, 1]`.

| Component | How it is measured |
| --- | --- |
| `verified_success` | 1.0 iff all public tests pass **and** baseline (regression) tests still pass **and** there are no scope violations; else 0.0 |
| `hidden_test_score` | fraction of hidden tests passed |
| `regression_avoidance` | 1.0 iff the baseline suite still passes |
| `scope_control` | 1.0 normally; 0.0 if a forbidden path was modified; 0.5 if `max_files_modified` was exceeded |

Public and hidden tests are **injected at score time** from the task directory and
run in the sandbox. They are never present in the repository the agent edits, so a
solution cannot be hardcoded to a specific test file.

## Objective score (SPEC §14.1)

```
Objective = 0.60·verified_success + 0.15·hidden_test_score
          + 0.10·regression_avoidance + 0.05·scope_control
          + 0.05·cost_efficiency + 0.05·time_efficiency      (×100)
```

`cost_efficiency` and `time_efficiency` are **set-relative** (normalized against
the best model in the evaluation set, SPEC §14.3-14.4), so they are unknown at
single-run time. Therefore:

- Each run record stores `partial_objective_score`: the four absolute components
  renormalized over their `0.90` weight to a 0-100 scale.
- The authoritative `objective_score` and `full_score` are computed during
  **aggregation**, once the per-set cost/time baselines are known.

## Full score (SPEC §14.2)

`Full = 0.95·Objective + 0.05·blinded_review`. With no blinded review (the v0.1
default), `Full == Objective`.

## Materiality thresholds (SPEC §14.6)

A difference is only called material if it clears the threshold in
`configs/scoring/default.yaml` (e.g. ≥5pp task-success improvement, statistically
supported). Numerically-first ranks with overlapping confidence intervals are
reported as statistical ties.
