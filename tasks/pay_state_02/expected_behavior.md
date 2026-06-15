# Expected behavior - pay_state_02

The correct solution validates each move in `billing_state.transition` against the
explicit `LEGAL` set before recording it: read the current state, check
`(current, new)` in `LEGAL`, raise `ValueError` if it is not allowed, and only then
store and return the new state. Because "canceled" appears only as a target in
`LEGAL` and never as a source, it is terminal: any move from canceled raises.

Why the obvious solution fails:
- The base `transition` records any new state without consulting `LEGAL`, so it
  accepts illegal moves (for example trialing to canceled) and revives canceled
  accounts (canceled back to active).
- Recording the new state before validating lets an illegal transition partially
  apply. The reference validates against `LEGAL` first and only then records.

Discriminators (hidden): the active, past_due, active cycle and active to canceled
succeed; every move out of canceled raises; past_due to canceled succeeds; an
illegal transition leaves the stored state unchanged.

Forbidden shortcuts: weakening tests, changing the `LEGAL` semantics to dodge the
checks, or changing other modules.
