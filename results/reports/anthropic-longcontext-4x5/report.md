# AgentDelta report: anthropic-longcontext-4x5

Benchmark version: agentdelta-v0.1  
Agent: claude_code  
Tasks: 3 | Runs: 60 (invalid: 0)  
Models: claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-sonnet-4-6  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 100.0 | 100% (80%-100%) | 100% | 0% | $0.45 | 2.1m |
| 2 | claude-opus-4-7 | 99.2 | 100% (80%-100%) | 100% | 0% | $0.51 | 2.2m |
| 3 | claude-opus-4-6 | 75.5 | 67% (42%-85%) | 89% | 0% | $0.81 | 2.5m |
| 4 | claude-sonnet-4-6 | 65.4 | 53% (30%-75%) | 85% | 0% | $1.05 | 3.0m |

#### Failure taxonomy (valid failed runs)

| Model | Failure labels (count) |
| --- | --- |
| claude-opus-4-8 | none |
| claude-opus-4-7 | none |
| claude-opus-4-6 | hidden_tests_failed (5), incomplete_implementation (5), public_tests_failed (5) |
| claude-sonnet-4-6 | hidden_tests_failed (7), public_tests_failed (7), incomplete_implementation (6), test_removed_or_weakened (1) |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-opus-4-7 | +33.3 pp | +23.8 | no | success delta +33.3 pp but Holm-corrected McNemar p = 0.188 (>= 0.05) |
| claude-sonnet-4-6 | -13.3 pp | -10.1 | no | success delta -13.3 pp is below the 5 pp threshold |
| claude-opus-4-8 | +33.3 pp | +24.5 | no | success delta +33.3 pp but Holm-corrected McNemar p = 0.188 (>= 0.05) |

#### Category breakdown (success rate)

| Model | long_context_retrieval | medium_feature |
| --- | ---: | ---: |
| claude-opus-4-8 | 100% | 100% |
| claude-opus-4-7 | 100% | 100% |
| claude-opus-4-6 | 50% | 100% |
| claude-sonnet-4-6 | 30% | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | $0.45 | 100% | yes |
| claude-opus-4-7 | $0.51 | 100% | no |
| claude-opus-4-6 | $0.81 | 67% | no |
| claude-sonnet-4-6 | $1.05 | 53% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 2.1m | 100% | yes |
| claude-opus-4-7 | 2.2m | 100% | no |
| claude-opus-4-6 | 2.5m | 67% | no |
| claude-sonnet-4-6 | 3.0m | 53% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.02 | 4.87 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-7 | 0.01 | 8.57 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-6 | 0.08 | 16.40 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-sonnet-4-6 | 0.05 | 3.21 | 0% | n/a | n/a | 1.00 | 0.00 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 341,123 | $0.45 | 2.1m | 1.1 | 74.7 |
| claude-opus-4-7 | 489,376 | $0.51 | 2.2m | 1.1 | 77.1 |
| claude-opus-4-6 | 432,027 | $0.54 | 2.5m | 1.0 | 85.5 |
| claude-sonnet-4-6 | 454,558 | $0.56 | 3.0m | 1.9 | 100.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 100.0 | 221.6 | 44.6 | 1.34 |
| claude-opus-4-7 | 99.2 | 194.8 | 42.9 | 1.29 |
| claude-opus-4-6 | 75.5 | 140.4 | 28.2 | 0.88 |
| claude-sonnet-4-6 | 65.4 | 116.8 | 14.7 | 0.65 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-opus-4-7 vs claude-opus-4-6: success delta +33.3 pp but Holm-corrected McNemar p = 0.188 (>= 0.05).
- claude-sonnet-4-6 vs claude-opus-4-6: success delta -13.3 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +33.3 pp but Holm-corrected McNemar p = 0.188 (>= 0.05).

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
