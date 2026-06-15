# AgentDelta report: anthropic-v0.1-frontier

Benchmark version: agentdelta-v0.1  
Agent: claude_code  
Tasks: 3 | Runs: 24 (invalid: 0)  
Models: claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-sonnet-4-6  
Modes: default

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 99.6 | 100% (61%-100%) | 100% | 0% | $0.24 | 55s |
| 2 | claude-opus-4-6 | 98.7 | 100% (61%-100%) | 100% | 0% | $0.22 | 1.2m |
| 3 | claude-opus-4-7 | 97.5 | 100% (61%-100%) | 100% | 0% | $0.28 | 1.3m |
| 4 | claude-sonnet-4-6 | 97.5 | 100% (61%-100%) | 100% | 0% | $0.23 | 1.7m |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-sonnet-4-6 | +0.0 pp | -1.2 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +0.8 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-7 | +0.0 pp | -1.2 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | medium_feature |
| --- | ---: |
| claude-opus-4-8 | 100% |
| claude-opus-4-6 | 100% |
| claude-opus-4-7 | 100% |
| claude-sonnet-4-6 | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-6 | $0.22 | 100% | yes |
| claude-sonnet-4-6 | $0.23 | 100% | no |
| claude-opus-4-8 | $0.24 | 100% | no |
| claude-opus-4-7 | $0.28 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 55s | 100% | yes |
| claude-opus-4-6 | 1.2m | 100% | no |
| claude-opus-4-7 | 1.3m | 100% | no |
| claude-sonnet-4-6 | 1.7m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 1.17 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-6 | 0.00 | 2.03 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-7 | 0.00 | 1.39 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-sonnet-4-6 | 0.15 | 1.17 | 0% | n/a | n/a | 1.00 | 0.00 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 158,844 | $0.24 | 55s | 2.0 | 60.0 |
| claude-opus-4-6 | 153,869 | $0.22 | 1.2m | 2.5 | 71.9 |
| claude-opus-4-7 | 245,824 | $0.28 | 1.3m | 2.2 | 75.9 |
| claude-sonnet-4-6 | 263,565 | $0.23 | 1.7m | 2.7 | 100.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 99.6 | 411.7 | 105.8 | 1.66 |
| claude-opus-4-6 | 98.7 | 447.3 | 76.2 | 1.37 |
| claude-opus-4-7 | 97.5 | 354.1 | 73.5 | 1.28 |
| claude-sonnet-4-6 | 97.5 | 417.9 | 46.1 | 0.97 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-sonnet-4-6 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
