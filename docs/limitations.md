# Limitations

AgentDelta conclusions are domain-, model-version-, agent-version-, and
date-specific (SPEC §3, §17.3). The following limits apply to the current state.

## v0.1 slice

- **Seven tasks, two fixtures, two languages.** task_001-005 on `python_package`
  and go_task_001-002 on `go_cli` span four categories across Python and Go and
  prove the pipeline, but this is not yet a benchmark. Real conclusions need the
  full 50-task / 4-model / 5-repetition matrix, and the categories test_writing,
  long_horizon, and dependency_migration are not yet represented (SPEC §8.2, §9).
- **No real model run yet.** Every result so far is from the dry-run path or
  synthetic records; the live agent path has not been exercised.
- **Refactor scoring is a proxy.** task_004 verifies the helper exists, is used
  (source check), and behavior is preserved - it does not fully judge refactor
  quality. Deeper structural judgment would need the blinded-review layer.
- **Network not locked down.** See `docs/reproducibility.md`.
- **Pricing is placeholder.** `agent_delta/scoring/cost.py` must be reconciled
  with the live pricing page before any published cost figure.

## Inherent

- Cross-agent comparisons mix model and scaffold effects; only controlled-model
  mode isolates model capability (SPEC §10.4).
- Coding-agent performance does not generalize to all domains.
- A model winning this workload is not "categorically superior."
