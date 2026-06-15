Add a payment status lifecycle to the `payments` service in a new module
`payments.payment_state`.

Expose:
- `status(event_id)`: the current status. If the event has an invoice but no recorded
  status, return "paid". If no invoice exists for the event, raise KeyError.
- `transition(event_id, new_status)`: move the event to `new_status` only if the
  transition from its current status is legal. Record it, append (event_id, from, to)
  to an audit list, and return the new status. Raise ValueError on an illegal
  transition and KeyError for an unknown event.
- `audit()`: the list of (event_id, from, to) tuples in order.
- `reset()`: clear the ledger and audit so tests can isolate state.

Legal transitions are exactly: (paid, disputed), (disputed, paid),
(disputed, refunded), (paid, refunded).

Requirements:
1. A status defaults to "paid" once the event's invoice exists.
2. "refunded" is terminal: no transition out of it is legal.
3. Any transition not in the legal set raises ValueError and leaves the status
   unchanged.
4. Use `storage.find_by_event` to decide whether an event has an invoice.
5. Do not modify the Invoice model, storage, or webhook; do not weaken tests.

When finished, run `pytest -q tests/`.
