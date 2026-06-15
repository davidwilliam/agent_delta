# Expected behavior - pay_state_01

The correct solution adds a new `payments.payment_state` module holding a per-event
status ledger and an audit list. A known event defaults to "paid", and `transition`
checks the (current, new) pair against the legal set before recording the new status
and appending (event_id, from, to) to the audit.

Why the obvious solution fails:
- Handling the visible path (paid then disputed) is easy, but a naive implementation
  often allows any "forward" move or forgets that "refunded" is terminal, so a
  transition out of "refunded" wrongly succeeds.
- Defaulting the status without consulting `storage.find_by_event` lets an unknown
  event report "paid" or accept a transition instead of raising KeyError.
- Recording the new status before validating the move lets an illegal transition
  partially apply. The reference validates against the explicit legal set first and
  only then records and audits.

Discriminators (hidden): disputed to refunded and paid to refunded succeed; every
transition out of refunded raises; status and transition on an event with no invoice
raise KeyError; the audit records transitions in order; distinct events track
independently.

Forbidden shortcuts: changing the Invoice model, storage, or webhook, or weakening
tests.
