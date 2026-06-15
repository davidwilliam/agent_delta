# AgentDelta report: anthropic-hardest5-4x5

Benchmark version: agentdelta-v0.1  
Agent: claude_code  
Tasks: 5 | Runs: 100 (invalid: 0)  
Models: claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-sonnet-4-6  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 98.8 | 100% (87%-100%) | 100% | 0% | $0.24 | 1.1m |
| 2 | claude-opus-4-7 | 97.5 | 100% (87%-100%) | 100% | 0% | $0.27 | 1.2m |
| 3 | claude-opus-4-6 | 94.6 | 100% (87%-100%) | 100% | 0% | $0.37 | 2.2m |
| 4 | claude-sonnet-4-6 | 89.7 | 88% (70%-96%) | 90% | 0% | $0.20 | 1.5m |

#### Failure taxonomy (valid failed runs)

| Model | Failure labels (count) |
| --- | --- |
| claude-opus-4-8 | none |
| claude-opus-4-7 | none |
| claude-opus-4-6 | none |
| claude-sonnet-4-6 | did_not_run_tests (3), hidden_tests_failed (3), incomplete_implementation (3), public_tests_failed (3) |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-opus-4-7 | +0.0 pp | +2.9 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-sonnet-4-6 | -12.0 pp | -4.9 | no | success delta -12.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +4.2 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | concurrency_idempotency | state_machine |
| --- | ---: | ---: |
| claude-opus-4-8 | 100% | 100% |
| claude-opus-4-7 | 100% | 100% |
| claude-opus-4-6 | 100% | 100% |
| claude-sonnet-4-6 | 100% | 40% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-sonnet-4-6 | $0.20 | 88% | yes |
| claude-opus-4-8 | $0.24 | 100% | yes |
| claude-opus-4-7 | $0.27 | 100% | no |
| claude-opus-4-6 | $0.37 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 1.1m | 100% | yes |
| claude-opus-4-7 | 1.2m | 100% | no |
| claude-sonnet-4-6 | 1.5m | 88% | no |
| claude-opus-4-6 | 2.2m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.01 | 3.72 | 0% | n/a | n/a | 0.90 | 0.19 |
| claude-opus-4-7 | 0.00 | 3.96 | 0% | n/a | n/a | 0.90 | 0.19 |
| claude-opus-4-6 | 0.04 | 5.46 | 0% | n/a | n/a | 0.90 | 0.20 |
| claude-sonnet-4-6 | 0.00 | 5.72 | 0% | n/a | n/a | 0.96 | 0.08 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 182,500 | $0.24 | 1.1m | 1.5 | 73.1 |
| claude-opus-4-7 | 210,754 | $0.27 | 1.2m | 1.2 | 72.8 |
| claude-opus-4-6 | 233,318 | $0.37 | 2.2m | 1.2 | 100.0 |
| claude-sonnet-4-6 | 200,961 | $0.18 | 1.5m | 1.2 | 89.2 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 98.8 | 411.8 | 77.6 | 1.35 |
| claude-opus-4-7 | 97.5 | 366.0 | 83.5 | 1.34 |
| claude-opus-4-6 | 94.6 | 254.5 | 45.0 | 0.95 |
| claude-sonnet-4-6 | 89.7 | 506.3 | 52.7 | 1.01 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-sonnet-4-6 vs claude-opus-4-6: success delta -12.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
