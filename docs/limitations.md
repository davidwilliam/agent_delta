# Limitations

AgentDelta conclusions are domain-, model-version-, agent-version-, and
date-specific (SPEC §3, §17.3). The following limits apply to the current state.

## v0.1 slice

- **One task, one fixture.** `task_001` (add `median`) on the `python_package`
  fixture proves the pipeline; it is not a benchmark. Real conclusions need the
  full 50-task / 4-model / 5-repetition matrix (SPEC §8.2).
- **No aggregation/statistics yet.** Per-run records carry only the absolute
  objective components and `partial_objective_score`. Set-relative cost/time
  efficiency, confidence intervals, paired comparisons, and rankings are Phase 2.
- **Network not locked down.** See `docs/reproducibility.md`.
- **Pricing is placeholder.** `agent_delta/scoring/cost.py` must be reconciled
  with the live pricing page before any published cost figure.

## Inherent

- Cross-agent comparisons mix model and scaffold effects; only controlled-model
  mode isolates model capability (SPEC §10.4).
- Coding-agent performance does not generalize to all domains.
- A model winning this workload is not "categorically superior."
