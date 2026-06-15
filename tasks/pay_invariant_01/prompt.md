You are working in the `payments` service. Invoices are created from webhooks
(`payments.webhook.process_webhook(event_id, amount)`); an invoice records the
`amount` paid for an event.

Add partial-refund support. Provide a way to refund part (or all) of an invoice for
a given event, and to query how much has been refunded so far. The critical rule is
that the total amount refunded for an event must never exceed the amount paid for
that event, even across several partial refunds.

Do not change the `Invoice` model or the storage seed. Keep the change minimal. When
finished, run `pytest -q tests/` and summarize what you added and how the invariant
is enforced.

## Required API (the tests import these exact names)

- Module `payments.refunds` exposing `refund(event_id, amount)` (returns the new cumulative refunded total, raises `ValueError` on a non-positive amount or an over-refund), `refunded_total(event_id)` (returns the amount refunded so far, 0 if none), and `reset()`.
