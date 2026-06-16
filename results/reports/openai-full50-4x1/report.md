# AgentDelta report: openai-full50-4x1

Benchmark version: agentdelta-v0.1  
Agent: codex_cli  
Tasks: 50 | Runs: 200 (invalid: 0)  
Models: gpt-5, gpt-5-mini-2025-08-07, gpt-5.1-2025-11-13, gpt-5.4  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | gpt-5.4 | 95.3 | 100% (93%-100%) | 100% | 0% | $0.09 | 1.1m |
| 2 | gpt-5-mini-2025-08-07 | 93.7 | 94% (84%-98%) | 96% | 0% | $0.01 | 1.6m |
| 3 | gpt-5.1-2025-11-13 | 90.8 | 96% (87%-99%) | 99% | 0% | $0.09 | 1.9m |
| 4 | gpt-5 | 89.8 | 96% (87%-99%) | 97% | 0% | $0.14 | 2.3m |

#### Failure taxonomy (valid failed runs)

| Model | Failure labels (count) |
| --- | --- |
| gpt-5.4 | none |
| gpt-5-mini-2025-08-07 | did_not_run_tests (3), hidden_tests_failed (3), incomplete_implementation (3), public_tests_failed (3) |
| gpt-5.1-2025-11-13 | did_not_run_tests (2), hidden_tests_failed (2), incomplete_implementation (2), public_tests_failed (2) |
| gpt-5 | did_not_run_tests (2), hidden_tests_failed (2), public_tests_failed (2), incomplete_implementation (1) |

#### Material improvements over baseline (`gpt-5`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| gpt-5.1-2025-11-13 | +0.0 pp | +1.1 | no | success delta +0.0 pp is below the 5 pp threshold |
| gpt-5-mini-2025-08-07 | -2.0 pp | +4.0 | no | success delta -2.0 pp is below the 5 pp threshold |
| gpt-5.4 | +4.0 pp | +5.5 | no | success delta +4.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | concurrency_idempotency | cross_file_contract | dependency_migration | hidden_invariant_preservation | long_context_retrieval | long_horizon | medium_feature | minimal_diff_repair | multi_file_bug_localization | multi_file_refactor | security_fix | small_bug_fix | state_machine | test_writing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-5.4 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| gpt-5-mini-2025-08-07 | 100% | 100% | 100% | 100% | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 83% | 100% |
| gpt-5.1-2025-11-13 | 100% | 100% | 100% | 100% | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| gpt-5 | 100% | 100% | 100% | 100% | 50% | 100% | 100% | 100% | 100% | 100% | 80% | 100% | 100% | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| gpt-5-mini-2025-08-07 | $0.01 | 94% | yes |
| gpt-5.1-2025-11-13 | $0.09 | 96% | yes |
| gpt-5.4 | $0.09 | 100% | yes |
| gpt-5 | $0.14 | 96% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| gpt-5.4 | 1.1m | 100% | yes |
| gpt-5-mini-2025-08-07 | 1.6m | 94% | no |
| gpt-5.1-2025-11-13 | 1.9m | 96% | no |
| gpt-5 | 2.3m | 96% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-5.4 | n/a | 0.00 | 0% | n/a | n/a | 0.82 | 0.33 |
| gpt-5-mini-2025-08-07 | n/a | n/a | 0% | n/a | n/a | 0.95 | 0.14 |
| gpt-5.1-2025-11-13 | n/a | n/a | 0% | n/a | n/a | 0.96 | 0.08 |
| gpt-5 | n/a | 0.00 | 0% | n/a | n/a | 0.96 | 0.07 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.4 | 87,848 | $0.09 | 1.1m | 1.2 | 61.4 |
| gpt-5-mini-2025-08-07 | 142,778 | $0.01 | 1.6m | 0.0 | 60.3 |
| gpt-5.1-2025-11-13 | 204,880 | $0.08 | 1.9m | 0.0 | 76.5 |
| gpt-5 | 287,899 | $0.13 | 2.3m | 0.2 | 100.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| gpt-5.4 | 95.3 | 1033.3 | 84.9 | 1.55 |
| gpt-5-mini-2025-08-07 | 93.7 | 6927.6 | 51.5 | 1.55 |
| gpt-5.1-2025-11-13 | 90.8 | 1075.6 | 45.1 | 1.19 |
| gpt-5 | 89.8 | 691.7 | 30.6 | 0.90 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- gpt-5.1-2025-11-13 vs gpt-5: success delta +0.0 pp is below the 5 pp threshold.
- gpt-5-mini-2025-08-07 vs gpt-5: success delta -2.0 pp is below the 5 pp threshold.
- gpt-5.4 vs gpt-5: success delta +4.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: shell_commands, test_runs, file_reads, review_passes (the index uses the remaining components).
