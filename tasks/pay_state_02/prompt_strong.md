Make `payments.billing_state.transition` enforce the legal billing lifecycle.

`transition(acct, new)` currently records any new state without validating the move
and without guarding the terminal state, so it accepts illegal transitions and
revives canceled accounts.

Requirements:
1. A move is allowed only if `(current, new)` is in the module's `LEGAL` set.
2. Any move not in `LEGAL` raises `ValueError` and leaves the stored state
   unchanged.
3. "canceled" is terminal: it has no legal outgoing transition, so any move from
   canceled raises `ValueError`.
4. A new account still defaults to "trialing", and legal moves still record the new
   state and return it.
5. Keep the `LEGAL` set semantics intact; do not add transitions to dodge the
   checks. Do not weaken tests or change other modules.

When finished, run `pytest -q tests/`.
