Follow this process to enforce the legal billing lifecycle in
`payments.billing_state`:

1. Read `billing_state.py` and note the `LEGAL` set, the default state "trialing",
   and that `transition` records any new state without checking it.
2. List the legal moves and observe that "canceled" has no legal outgoing
   transition, so it is terminal.
3. Add the smallest fix: read the current state, check `(current, new)` against
   `LEGAL`, raise `ValueError` if it is not allowed, and only then record and return
   the new state. Validate before writing so an illegal move leaves the state
   unchanged.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the `LEGAL` semantics are intact and no other module
   changed.
