# AgentDelta report: anthropic-v0.1-pilot

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
| 1 | claude-opus-4-8 | 98.5 | 100% (61%-100%) | 100% | 0% | $0.22 | 52s |
| 2 | claude-sonnet-4-6 | 98.2 | 100% (61%-100%) | 100% | 0% | $0.15 | 1.4m |
| 3 | claude-opus-4-7 | 98.0 | 100% (61%-100%) | 100% | 0% | $0.21 | 59s |
| 4 | claude-opus-4-6 | 95.0 | 100% (61%-100%) | 100% | 0% | $0.29 | 1.8m |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-sonnet-4-6 | +0.0 pp | +3.2 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +3.5 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-7 | +0.0 pp | +3.1 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | medium_feature | security_fix | small_bug_fix |
| --- | ---: | ---: | ---: |
| claude-opus-4-8 | 100% | 100% | 100% |
| claude-sonnet-4-6 | 100% | 100% | 100% |
| claude-opus-4-7 | 100% | 100% | 100% |
| claude-opus-4-6 | 100% | 100% | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-sonnet-4-6 | $0.15 | 100% | yes |
| claude-opus-4-7 | $0.21 | 100% | no |
| claude-opus-4-8 | $0.22 | 100% | no |
| claude-opus-4-6 | $0.29 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 52s | 100% | yes |
| claude-opus-4-7 | 59s | 100% | no |
| claude-sonnet-4-6 | 1.4m | 100% | no |
| claude-opus-4-6 | 1.8m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 1.83 | 0% | n/a | n/a | 0.67 | 0.53 |
| claude-sonnet-4-6 | 0.00 | 2.78 | 0% | n/a | n/a | 0.67 | 0.46 |
| claude-opus-4-7 | 0.06 | 2.08 | 0% | n/a | n/a | 0.67 | 0.52 |
| claude-opus-4-6 | 0.00 | 2.96 | 0% | n/a | n/a | 0.61 | 0.73 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 146,493 | $0.22 | 52s | 1.7 | 67.5 |
| claude-sonnet-4-6 | 185,752 | $0.15 | 1.4m | 2.0 | 86.5 |
| claude-opus-4-7 | 209,833 | $0.21 | 59s | 1.7 | 78.6 |
| claude-opus-4-6 | 187,741 | $0.29 | 1.8m | 2.5 | 100.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 98.5 | 455.9 | 107.8 | 1.46 |
| claude-sonnet-4-6 | 98.2 | 654.3 | 76.1 | 1.14 |
| claude-opus-4-7 | 98.0 | 470.1 | 99.1 | 1.25 |
| claude-opus-4-6 | 95.0 | 324.3 | 56.9 | 0.95 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-sonnet-4-6 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
