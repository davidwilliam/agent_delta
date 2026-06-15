You are working in the `payments` service. Invoices are created from webhooks
(`payments.webhook.process_webhook(event_id, amount)`); an invoice records the
`amount` paid for an event.

Add a payment status lifecycle. Each event whose invoice exists has a status that
defaults to "paid". Provide audited transitions between statuses, allowing only the
legal moves: paid to disputed, disputed to paid, disputed to refunded, and paid to
refunded. "refunded" is terminal, so no transition may leave it. An illegal
transition, or a transition or status query for an event with no invoice, must be
rejected.

Keep the change minimal and add it as a new module. Do not change the `Invoice`
model, storage, or webhook. When finished, run `pytest -q tests/` and summarize what
you added and how the legal transitions and the terminal state are enforced.

## Required API (the tests import these exact names)

- Module `payments.payment_state` exposing `transition(event_id, new_status)` (returns the new status, raises `ValueError` on an illegal transition and `KeyError` for an unknown event), `status(event_id)` (returns the current status, raises `KeyError` for an unknown event), `audit()` (returns the recorded transition history), and `reset()`.
