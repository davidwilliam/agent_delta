# Evaluation modes

Modes (SPEC-ADDENDUM section 5) are normalizations applied to a run. The task,
fixture, base commit, and scoring are identical across modes; only the conditions
change. Running the same task across modes is what lets cross-mode synthesis tell
intrinsic model capability apart from agentic amplification.

Definitions live in `configs/modes.yaml` (frozen, like the scoring config) and are
applied by `agent_delta/modes.py`.

## Implemented modes

| Mode | What it changes | Addendum |
| --- | --- | --- |
| `default` | Nothing. Each model as a normal user runs it. | 5.1 |
| `equal_budget` | Same token, message, time, and cost caps for every model. | 5.2 |
| `matched_workflow` | Prepends the same explicit workflow (inspect, plan, smallest change, test, debug once, re-test, review, summarize). | 5.3 |
| `strong_spec` | Appends the task's full acceptance criteria, forbidden paths, and definition of done. | 5.4 |
| `cost_matched` | Same dollar cap per task. | 5.6 |
| `time_matched` | Same wall-clock cap per task. | 5.7 |

Older-Model-Plus-Scaffold (5.5) is per-model differential support and is not yet
implemented.

## Running a mode

```bash
agentdelta run --task task_001 --model claude-opus-4-8 --mode equal_budget
agentdelta run --task task_001 --model claude-opus-4-6 --mode matched_workflow
```

Prompt transforms (`matched_workflow`, `strong_spec`) rewrite the sample input;
resource modes (`equal_budget`, `cost_matched`, `time_matched`) set the Inspect
token, message, time, and cost limits. Every run records its `mode`, so the same
suite directory can hold multiple modes and aggregation groups by mode.

## How modes drive the definitive verdict

`agentdelta report` adds a Cross-Mode Synthesis section that re-checks each
material Default-Mode gain against the normalized modes (see
`docs/amplification.md`):

- the gap shrinks under `equal_budget` -> Agentic Amplification (it was budget),
- the gap shrinks under `matched_workflow` or `strong_spec` -> Workflow-Equivalent
  (the older model catches up given the process or spec),
- the gap persists under `equal_budget` -> Intrinsic Capability.

With only Default Mode the verdict stays provisional; one normalized mode is
enough to confirm it.
