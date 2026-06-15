You are working in the `payments` service. `payments.billing_state` tracks the
billing lifecycle of an account: `state(acct)` returns the current state
(defaulting to "trialing"), `transition(acct, new)` moves an account to a new
state, and `reset()` clears the store. The module defines a `LEGAL` set of allowed
(current, new) transitions.

`transition` currently records any new state without checking it. It accepts moves
that are not in `LEGAL`, and it revives "canceled" accounts even though canceled is
meant to be a terminal state.

Make `transition` reject any move that is not in `LEGAL` by raising `ValueError`,
and treat "canceled" as terminal so no transition may leave it. A rejected
transition must not change the stored state. Legal moves must still record the new
state and return it, and a new account must still default to "trialing".

Keep the change minimal and in the billing_state layer; keep the `LEGAL` semantics
intact. When finished, run `pytest -q tests/` and summarize what you changed and how
the legal transitions and the terminal state are enforced.

## Required API (the tests import these exact names)

- Module `payments.billing_state` exposing `transition(acct, new)` (returns the new state, raises `ValueError` on an illegal transition), `state(acct)` (returns the current state), and `reset()`.
