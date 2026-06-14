# Limitations

AgentDelta conclusions are domain-, model-version-, agent-version-, and
date-specific (SPEC §3, §17.3). The following limits apply to the current state.

## v0.1 slice

- **Ten tasks, two fixtures, two languages.** task_001-008 on `python_package`
  and go_task_001-002 on `go_cli` cover all seven SPEC §8.2 categories across
  Python and Go and prove the pipeline, but this is not yet a benchmark: real
  conclusions need the full 50-task / 4-model / 5-repetition matrix (SPEC §8.2, §9).
- **Long-context is flagged, not exercised.** task_007 is marked long-context-
  eligible, but the fixtures are small; a task that genuinely requires >200k
  tokens of context (SPEC §21) needs a large fixture and is future work.
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
