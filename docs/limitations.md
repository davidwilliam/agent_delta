# Limitations

AgentDelta conclusions are domain-, model-version-, agent-version-, and
date-specific (SPEC §3, §17.3). The following limits apply to the current state.

## v0.1 slice

- **Eleven tasks, three fixtures, two languages.** task_001-009 (incl. the
  long-context task_009) and go_task_001-002 cover all seven SPEC §8.2 categories
  and both context classes, proving the pipeline, but this is not yet a benchmark:
  real conclusions need the full 50-task / 4-model / 5-repetition matrix (SPEC §8.2).
- **Long-context benefits, not strictly requires.** task_009 uses a ~228k-token
  fixture whose answer needs schema variants spread across many files. A
  resourceful agent can grep its way there rather than holding it all in context,
  so the long-context advantage is empirical (and is itself a good amplification
  case: intrinsic 1M context vs agentic navigation).
- **No real model run yet.** Every result so far is from the dry-run path or
  synthetic records; the live agent path has not been exercised.
- **Refactor scoring is a proxy.** task_004 verifies the helper exists, is used
  (source check), and behavior is preserved - it does not fully judge refactor
  quality. Deeper structural judgment would need the blinded-review layer.
- **Real model run still needs network.** Scoring runs fully offline (sandbox
  network is `none` by default), but a live agent run may need a restricted
  network for the inspect_swe model proxy; that path is unverified until a live
  run. See `docs/reproducibility.md`.
- **Pricing is placeholder.** `agent_delta/scoring/cost.py` must be reconciled
  with the live pricing page before any published cost figure.

## Inherent

- Cross-agent comparisons mix model and scaffold effects; only controlled-model
  mode isolates model capability (SPEC §10.4).
- Coding-agent performance does not generalize to all domains.
- A model winning this workload is not "categorically superior."
