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

## Classification with Default-Mode-only data

The current eval runs Default Mode. With only that data the report can identify
Cost-Inefficient, Time-Inefficient, Agentic-Amplification (provisional), and
No-Material-Gain outcomes, and it reports which additional modes are needed to
separate Intrinsic from Workflow-Equivalent gains. Those modes (Equal-Budget,
Matched-Workflow, Strong-Spec, Cost-Matched, Time-Matched, Older-Model-Plus-
Scaffold; ADDENDUM 5) are not yet implemented as run configurations; the report
labels Intrinsic and Amplification gains "provisional" until they are.

## Frozen config

Weights and thresholds live in `configs/scoring/amplification.yaml` and are frozen
before a run, exactly like the objective scoring config.

## Claim discipline

The report never states a newer model is categorically superior. It uses the
evidence-bound language required by ADDENDUM 12: better by which metric, in which
mode, at what cost, time, and token amplification, with what statistical support,
and whether the older model is expected to close the gap under a stronger
workflow.

## Not yet captured

Tool-call, shell-command, test-run, file-read, retry, and review-pass counts are
not yet extracted from the agent transcript, so the Agentic Work Index currently
uses tokens, wall-clock time, and file edits. Wiring those counts through the
scorer and run record is the next step to a complete Work Index.
