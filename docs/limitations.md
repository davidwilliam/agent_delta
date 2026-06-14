# Limitations

AgentDelta conclusions are domain-, model-version-, agent-version-, and
date-specific (SPEC §3, §17.3). The following limits apply to the current state.

## v0.1 slice

- **Five tasks, one fixture, one language.** The current suite (task_001-005 on
  the `python_package` fixture) spans four categories and proves the pipeline,
  but it is not yet a benchmark. Real conclusions need the full 50-task / 4-model
  / 5-repetition matrix across ≥2 languages (SPEC §8.2, §9).
- **Refactor scoring is a proxy.** task_004 verifies the helper exists, is used
  (source check), and behavior is preserved - it does not fully judge refactor
  quality. Deeper structural judgment would need the blinded-review layer.
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
