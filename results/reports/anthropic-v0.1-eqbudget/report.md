# AgentDelta report: anthropic-v0.1-eqbudget

Benchmark version: agentdelta-v0.1  
Agent: claude_code  
Tasks: 2 | Runs: 32 (invalid: 0)  
Models: claude-opus-4-6, claude-opus-4-7, claude-opus-4-8, claude-sonnet-4-6  
Modes: default, equal_budget

## Mode: default

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 100.0 | 100% (51%-100%) | 100% | 0% | $0.25 | 1.0m |
| 2 | claude-opus-4-7 | 97.3 | 100% (51%-100%) | 100% | 0% | $0.32 | 1.5m |
| 3 | claude-sonnet-4-6 | 96.8 | 100% (51%-100%) | 100% | 0% | $0.28 | 2.2m |
| 4 | claude-opus-4-6 | 95.3 | 100% (51%-100%) | 100% | 0% | $0.42 | 2.2m |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-sonnet-4-6 | +0.0 pp | +1.4 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +4.7 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-7 | +0.0 pp | +2.0 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | medium_feature |
| --- | ---: |
| claude-opus-4-8 | 100% |
| claude-opus-4-7 | 100% |
| claude-sonnet-4-6 | 100% |
| claude-opus-4-6 | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | $0.25 | 100% | yes |
| claude-sonnet-4-6 | $0.28 | 100% | no |
| claude-opus-4-7 | $0.32 | 100% | no |
| claude-opus-4-6 | $0.42 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 1.0m | 100% | yes |
| claude-opus-4-7 | 1.5m | 100% | no |
| claude-opus-4-6 | 2.2m | 100% | no |
| claude-sonnet-4-6 | 2.2m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 1.75 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-7 | 0.06 | 1.92 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-sonnet-4-6 | 0.00 | 1.00 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-6 | 0.00 | 1.00 | 0% | n/a | n/a | 1.00 | 0.00 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 187,170 | $0.25 | 1.0m | 2.5 | 72.5 |
| claude-opus-4-7 | 303,410 | $0.32 | 1.5m | 2.2 | 86.7 |
| claude-sonnet-4-6 | 266,991 | $0.28 | 2.2m | 3.0 | 100.0 |
| claude-opus-4-6 | 249,466 | $0.42 | 2.2m | 3.0 | 95.4 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 100.0 | 400.5 | 91.1 | 1.38 |
| claude-opus-4-7 | 97.3 | 306.4 | 65.1 | 1.12 |
| claude-sonnet-4-6 | 96.8 | 344.4 | 41.8 | 0.97 |
| claude-opus-4-6 | 95.3 | 226.4 | 42.9 | 1.00 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-sonnet-4-6 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Mode: equal_budget

### Level 1: Primary Assessment (SPEC.md)

Which model-agent system performs best, by objective evidence.

#### Primary ranking

| Rank | Model | Objective | Success | Hidden | Regression | Cost/Success | Median Time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | claude-opus-4-8 | 100.0 | 100% (51%-100%) | 100% | 0% | $0.25 | 1.1m |
| 2 | claude-opus-4-7 | 97.7 | 100% (51%-100%) | 100% | 0% | $0.35 | 1.4m |
| 3 | claude-sonnet-4-6 | 97.4 | 100% (51%-100%) | 100% | 0% | $0.26 | 2.3m |
| 4 | claude-opus-4-6 | 95.5 | 100% (51%-100%) | 100% | 0% | $0.43 | 2.2m |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-sonnet-4-6 | +0.0 pp | +1.9 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +4.5 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-7 | +0.0 pp | +2.2 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | medium_feature |
| --- | ---: |
| claude-opus-4-8 | 100% |
| claude-opus-4-7 | 100% |
| claude-sonnet-4-6 | 100% |
| claude-opus-4-6 | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | $0.25 | 100% | yes |
| claude-sonnet-4-6 | $0.26 | 100% | no |
| claude-opus-4-7 | $0.35 | 100% | no |
| claude-opus-4-6 | $0.43 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 1.1m | 100% | yes |
| claude-opus-4-7 | 1.4m | 100% | no |
| claude-opus-4-6 | 2.2m | 100% | no |
| claude-sonnet-4-6 | 2.3m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 2.25 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-7 | 0.00 | 2.12 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-sonnet-4-6 | 0.00 | 0.83 | 0% | n/a | n/a | 1.00 | 0.00 |
| claude-opus-4-6 | 0.08 | 0.82 | 0% | n/a | n/a | 1.00 | 0.00 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 193,852 | $0.25 | 1.1m | 2.5 | 77.4 |
| claude-opus-4-7 | 300,027 | $0.35 | 1.4m | 2.0 | 80.9 |
| claude-sonnet-4-6 | 274,735 | $0.26 | 2.3m | 2.8 | 100.0 |
| claude-opus-4-6 | 245,133 | $0.43 | 2.2m | 3.5 | 98.0 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 100.0 | 393.1 | 88.1 | 1.29 |
| claude-opus-4-7 | 97.7 | 280.5 | 64.8 | 1.21 |
| claude-sonnet-4-6 | 97.4 | 376.0 | 40.0 | 0.97 |
| claude-opus-4-6 | 95.5 | 221.7 | 41.3 | 0.98 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-sonnet-4-6 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Cross-Mode Synthesis (Level 2 definitive)

Modes available: default, equal_budget. Each material Default-Mode gain is re-checked across the normalized modes to decide whether it is intrinsic, amplified, or workflow-equivalent.

No material Default-Mode gains to synthesize.

## Limitations

- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
