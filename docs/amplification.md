# Agentic Amplification Assessment

This implements SPEC-ADDENDUM.md as a second-level assessment layered on top of
the SPEC.md primary benchmark. The two levels are produced together but are kept
distinct in both the report JSON and the Markdown.

## Two levels

- **Level 1 (SPEC.md): Primary Assessment.** Ranks the model-agent systems and
  decides which Model B over Model A gains are real and material. A gain is
  material only when success improves by at least the configured threshold (SPEC
  14.6) and the paired McNemar test is significant (SPEC 15). This answers "which
  performs best, and is the difference real?".
- **Level 2 (SPEC-ADDENDUM): Agentic Amplification Assessment.** Narrows down to
  *only* the material Level 1 gains and asks "why?": is the gain intrinsic model
  capability, or does the newer model mainly do more work by default (more
  tokens, time, tool calls, retries, self-review)? Non-material gains are recorded
  as excluded and never escalated, so amplification scrutiny is spent only where
  Level 1 found a genuine improvement.

`agentdelta report --level 1` or `--level 2` renders a single level; `--level
both` (default) renders both. The `report.json` always carries both under each
mode as `level1` and `level2`.

## What aggregation computes

`agentdelta aggregate` / `agentdelta report` read the per-run records and produce,
per evaluation mode and model:

- Authoritative objective score (SPEC 14), filling in the set-relative cost and
  time efficiency that per-run records leave deferred.
- Success rate with a Wilson 95% interval, plus a paired McNemar comparison
  against the baseline model.
- Agentic Work Index (ADDENDUM 6.1): normalized, weighted effort across tokens,
  time, and the agent-behavior counts that are captured, scaled so the
  heaviest-working system is 100.
- Quality per dollar, per minute, and per work unit (ADDENDUM 6.2 to 6.4).
- Token, cost, time, tool, retry, test, api, and work-index amplification ratios
  versus the baseline (ADDENDUM 6.5 to 6.10), with red flags at ratio >= 2.0.
- A classification of each Model B over Model A change (ADDENDUM 8).

## Cross-mode synthesis (definitive verdict)

The normalized run modes are implemented (see `docs/modes.md`). When a suite
contains more than one mode, `agentdelta report` adds a Cross-Mode Synthesis
section that re-checks each material Default-Mode gain across modes and reaches a
confirmed classification (`agent_delta/scoring/synthesis.py`):

- the gap shrinks under Equal-Budget -> Agentic Amplification Gain,
- the gap shrinks under Matched-Workflow or Strong-Spec -> Workflow-Equivalent Gain,
- the gap persists under Equal-Budget -> Intrinsic Capability Gain.

"Shrinks" means the success gap falls below the materiality threshold. Only gains
that Level 1 found material in Default Mode are synthesized, so the narrowing of
the two-level design is preserved. With only Default Mode present, the per-mode
Level 2 classification stays provisional and the synthesis section is omitted; a
single normalized mode is enough to confirm the verdict.

## Frozen config

Weights and thresholds live in `configs/scoring/amplification.yaml` and are frozen
before a run, exactly like the objective scoring config.

## Claim discipline

The report never states a newer model is categorically superior. It uses the
evidence-bound language required by ADDENDUM 12: better by which metric, in which
mode, at what cost, time, and token amplification, with what statistical support,
and whether the older model is expected to close the gap under a stronger
workflow.

## Agent-behavior capture

`agent_delta/scoring/behavior.py` extracts work signals from the Inspect sample's
event stream and the run record stores them under `agent_behavior`:

- `api_calls` and `retry_count` from model events,
- `tool_calls`, `shell_commands`, `failed_shell_commands`, `test_runs`,
  `files_read`, and `file_edits` from tool events.

Test runs are detected by matching the shell command text against common test
runners (pytest, go test, npm test, rspec, and so on). Tool classification is
pattern-based because tool names vary by agent and version; the record also
stores a raw `tool_histogram` of the exact tool names seen, so the classifier can
be tuned from a real transcript rather than guessed. The Agentic Work Index uses
whichever of these components have data and reports which it used, so it
strengthens automatically as runs populate more signals.

`review_passes` has no discrete transcript signal yet and stays uncaptured; the
report's Limitations section lists any Work Index component with no data for a
given run.
