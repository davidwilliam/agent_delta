# AgentDelta report: anthropic-v0.1-hard

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
| 1 | claude-opus-4-8 | 100.0 | 100% (61%-100%) | 100% | 0% | $0.25 | 54s |
| 2 | claude-opus-4-7 | 99.1 | 100% (61%-100%) | 100% | 0% | $0.25 | 1.1m |
| 3 | claude-sonnet-4-6 | 97.1 | 100% (61%-100%) | 100% | 0% | $0.24 | 2.1m |
| 4 | claude-opus-4-6 | 95.8 | 100% (61%-100%) | 100% | 0% | $0.32 | 2.3m |

#### Material improvements over baseline (`claude-opus-4-6`)

A gain is material only if success improves by at least the configured threshold and the paired McNemar test is significant. Only material gains are escalated to Level 2.

| Model B | Success delta | Objective delta | Material? | Reason |
| --- | ---: | ---: | :---: | --- |
| claude-sonnet-4-6 | +0.0 pp | +1.3 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-8 | +0.0 pp | +4.2 | no | success delta +0.0 pp is below the 5 pp threshold |
| claude-opus-4-7 | +0.0 pp | +3.3 | no | success delta +0.0 pp is below the 5 pp threshold |

#### Category breakdown (success rate)

| Model | multi_file_bug_localization | security_fix | state_machine |
| --- | ---: | ---: | ---: |
| claude-opus-4-8 | 100% | 100% | 100% |
| claude-opus-4-7 | 100% | 100% | 100% |
| claude-sonnet-4-6 | 100% | 100% | 100% |
| claude-opus-4-6 | 100% | 100% | 100% |

#### Cost-success frontier

| Model | Cost/success | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-sonnet-4-6 | $0.24 | 100% | yes |
| claude-opus-4-7 | $0.25 | 100% | no |
| claude-opus-4-8 | $0.25 | 100% | no |
| claude-opus-4-6 | $0.32 | 100% | no |

#### Latency-success frontier

| Model | Median time | Success | On frontier |
| --- | ---: | ---: | :---: |
| claude-opus-4-8 | 54s | 100% | yes |
| claude-opus-4-7 | 1.1m | 100% | no |
| claude-sonnet-4-6 | 2.1m | 100% | no |
| claude-opus-4-6 | 2.3m | 100% | no |

#### Diagnostics

| Model | Failed-cmd ratio | Explore/edit | Timeout rate | First edit (s) | First test (s) | Diff locality | Patch entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 0.00 | 5.83 | 0% | n/a | n/a | 0.83 | 0.32 |
| claude-opus-4-7 | 0.00 | 4.83 | 0% | n/a | n/a | 0.83 | 0.32 |
| claude-sonnet-4-6 | 0.00 | 3.33 | 0% | n/a | n/a | 0.83 | 0.32 |
| claude-opus-4-6 | 0.17 | 4.08 | 0% | n/a | n/a | 0.83 | 0.33 |

### Level 2: Agentic Amplification Assessment (SPEC-ADDENDUM.md)

For the material Level 1 gains only: is the improvement intrinsic model capability, or does the newer model mainly do more work by default (more tokens, time, tool calls, retries, self-review)?

Agentic Work Index components in use: input_tokens, output_tokens, wall_clock_seconds, api_calls, tool_calls, shell_commands, test_runs, file_reads, file_edits, retry_count.

#### Resource use and Agentic Work Index

| Model | Mean tokens | Cost/task | Median Time | Files edited | Work Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 176,260 | $0.25 | 54s | 1.3 | 69.6 |
| claude-opus-4-7 | 221,327 | $0.25 | 1.1m | 1.3 | 79.0 |
| claude-sonnet-4-6 | 238,182 | $0.24 | 2.1m | 1.5 | 100.0 |
| claude-opus-4-6 | 200,506 | $0.32 | 2.3m | 1.3 | 87.2 |

#### Efficiency

| Model | Objective | Quality/$ | Quality/Minute | Quality/Work Unit |
| --- | ---: | ---: | ---: | ---: |
| claude-opus-4-8 | 100.0 | 404.8 | 110.1 | 1.44 |
| claude-opus-4-7 | 99.1 | 401.8 | 89.4 | 1.25 |
| claude-sonnet-4-6 | 97.1 | 396.5 | 44.6 | 0.97 |
| claude-opus-4-6 | 95.8 | 297.4 | 50.9 | 1.10 |

No material Level 1 gains were escalated to amplification analysis (3 comparison(s) excluded as non-material).

#### Not escalated to Level 2 (non-material)

- claude-sonnet-4-6 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-8 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.
- claude-opus-4-7 vs claude-opus-4-6: success delta +0.0 pp is below the 5 pp threshold.

## Limitations

- Only Default Mode was run; Intrinsic vs Workflow-Equivalent gains cannot be distinguished without Equal-Budget, Matched-Workflow, or Strong-Spec modes.
- Agentic Work Index components with no captured data in this run: review_passes (the index uses the remaining components).
