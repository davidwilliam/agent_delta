# AgentDelta report: anthropic-statemachine-4x10

Benchmark version: agentdelta-v0.1  
Agent: claude_code  
Tasks: 5 | Runs: 200 (invalid: 0)  
Models: claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-sonnet-4-6  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 99.7 | 100% (93%-100%) | 100% | 0% | $0.22 | 56s |
| 2 | claude-opus-4-7 | 99.2 | 100% (93%-100%) | 100% | 0% | $0.23 | 1.0m |
| 3 | claude-opus-4-6 | 95.8 | 100% (93%-100%) | 99% | 0% | $0.32 | 1.8m |
| 4 | claude-sonnet-4-6 | 92.9 | 94% (84%-98%) | 92% | 0% | $0.21 | 1.8m |

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
| claude-opus-4-7 | +0.0 pp | +3.4 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-sonnet-4-6 | -6.0 pp | -3.0 | no | success delta -6.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +3.9 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | state_machine |
| --- | ---: |
| claude-opus-4-8 | 100% |
| claude-opus-4-7 | 100% |
| claude-opus-4-6 | 100% |
| claude-sonnet-4-6 | 94% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-sonnet-4-6 | $0.21 | 94% | yes |
| claude-opus-4-8 | $0.22 | 100% | yes |
| claude-opus-4-7 | $0.23 | 100% | no |
| claude-opus-4-6 | $0.32 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 56s | 100% | yes |
| claude-opus-4-7 | 1.0m | 100% | no |
| claude-sonnet-4-6 | 1.8m | 94% | no |
| claude-opus-4-6 | 1.8m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 4.69 | 0% | n/a | n/a | 0.90 | 0.19 |
| claude-opus-4-7 | 0.00 | 2.95 | 0% | n/a | n/a | 0.90 | 0.19 |
| claude-opus-4-6 | 0.06 | 5.15 | 0% | n/a | n/a | 0.90 | 0.19 |
| claude-sonnet-4-6 | 0.00 | 2.46 | 0% | n/a | n/a | 0.93 | 0.13 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 190,442 | $0.22 | 56s | 1.2 | 76.1 |
| claude-opus-4-7 | 216,162 | $0.23 | 1.0m | 1.2 | 76.6 |
| claude-opus-4-6 | 207,816 | $0.32 | 1.8m | 1.3 | 100.0 |
| claude-sonnet-4-6 | 215,612 | $0.20 | 1.8m | 1.4 | 97.9 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 99.7 | 443.8 | 102.0 | 1.31 |
| claude-opus-4-7 | 99.2 | 439.6 | 87.7 | 1.30 |
| claude-opus-4-6 | 95.8 | 301.8 | 56.2 | 0.96 |
| claude-sonnet-4-6 | 92.9 | 464.6 | 49.6 | 0.95 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-sonnet-4-6 vs claude-opus-4-6: success delta -6.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
