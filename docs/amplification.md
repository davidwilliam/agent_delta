# Agentic Amplification Assessment

This implements SPEC-ADDENDUM.md: separating intrinsic model capability from
gains that come from a newer model simply doing more work by default. The
question is not only "which model produced the best output?" but "which model
produced the best output per unit of cost, time, and agentic work, and could an
older cheaper model match it with a better workflow?".

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
