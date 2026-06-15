Add partial-refund support to the `payments` service.

Expose, in the `payments` package:
- `refund(event_id, amount)`: record a refund of `amount` against the invoice for
  `event_id`, returning the new cumulative refunded total.
- `refunded_total(event_id)`: the amount refunded for that event so far.
- `reset()` on the new module so tests can isolate state.

Requirements:
1. The cumulative refunded total for an event must never exceed the invoice amount.
2. An over-refund attempt must raise and must NOT change the recorded total
   (no partial application).
3. A zero or negative refund amount must raise.
4. Refunding an unknown event must raise.
5. Several partial refunds that stay within the amount paid must all succeed.
6. Do not modify the Invoice model or storage seed; do not weaken tests.

When finished, run `pytest -q tests/`.
