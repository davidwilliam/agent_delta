# AgentDelta report: openai-hardest5-4x5

Benchmark version: agentdelta-v0.1  
Agent: codex_cli  
Tasks: 5 | Runs: 100 (invalid: 0)  
Models: gpt-5, gpt-5-mini-2025-08-07, gpt-5.1-2025-11-13, gpt-5.4  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | gpt-5-mini-2025-08-07 | 97.3 | 100% (87%-100%) | 100% | 0% | $0.01 | 1.6m |
| 2 | gpt-5.4 | 95.3 | 100% (87%-100%) | 100% | 0% | $0.08 | 1.1m |
| 3 | gpt-5.1-2025-11-13 | 92.9 | 100% (87%-100%) | 100% | 0% | $0.09 | 2.1m |
| 4 | gpt-5 | 91.6 | 100% (87%-100%) | 100% | 0% | $0.18 | 2.9m |

#### Material improvements over baseline (`gpt-5`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| gpt-5.1-2025-11-13 | +0.0 pp | +1.3 | no | success delta +0.0 pp is below the 5 pp threshold |
| gpt-5-mini-2025-08-07 | +0.0 pp | +5.7 | no | success delta +0.0 pp is below the 5 pp threshold |
| gpt-5.4 | +0.0 pp | +3.8 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | concurrency_idempotency | state_machine |
| --- | ---: | ---: |
| gpt-5-mini-2025-08-07 | 100% | 100% |
| gpt-5.4 | 100% | 100% |
| gpt-5.1-2025-11-13 | 100% | 100% |
| gpt-5 | 100% | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| gpt-5-mini-2025-08-07 | $0.01 | 100% | yes |
| gpt-5.4 | $0.08 | 100% | no |
| gpt-5.1-2025-11-13 | $0.09 | 100% | no |
| gpt-5 | $0.18 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| gpt-5.4 | 1.1m | 100% | yes |
| gpt-5-mini-2025-08-07 | 1.6m | 100% | no |
| gpt-5.1-2025-11-13 | 2.1m | 100% | no |
| gpt-5 | 2.9m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-5-mini-2025-08-07 | n/a | n/a | 0% | n/a | n/a | 0.86 | 0.38 |
| gpt-5.4 | n/a | 0.00 | 0% | n/a | n/a | 0.88 | 0.23 |
| gpt-5.1-2025-11-13 | n/a | n/a | 0% | n/a | n/a | 0.90 | 0.19 |
| gpt-5 | n/a | n/a | 0% | n/a | n/a | 0.90 | 0.20 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5-mini-2025-08-07 | 138,650 | $0.01 | 1.6m | 0.0 | 47.6 |
| gpt-5.4 | 75,520 | $0.08 | 1.1m | 1.1 | 48.5 |
| gpt-5.1-2025-11-13 | 233,403 | $0.09 | 2.1m | 0.0 | 63.5 |
| gpt-5 | 403,938 | $0.18 | 2.9m | 0.0 | 100.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| gpt-5-mini-2025-08-07 | 97.3 | 7098.2 | 58.6 | 2.04 |
| gpt-5.4 | 95.3 | 1152.0 | 85.2 | 1.96 |
| gpt-5.1-2025-11-13 | 92.9 | 1023.5 | 41.9 | 1.46 |
| gpt-5 | 91.6 | 523.2 | 25.0 | 0.92 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- gpt-5.1-2025-11-13 vs gpt-5: success delta +0.0 pp is below the 5 pp threshold.
- gpt-5-mini-2025-08-07 vs gpt-5: success delta +0.0 pp is below the 5 pp threshold.
- gpt-5.4 vs gpt-5: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: shell_commands, test_runs, file_reads, review_passes (the index uses the remaining components).
