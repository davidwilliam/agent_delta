You are working in the `payments` service. `process_webhook(event_id, amount)` in
`payments/webhook.py` creates an invoice for an event, returning the existing
invoice on replay.

It is idempotent for sequential delivery, but it is NOT safe under concurrent
delivery: when the same event arrives on two threads at once, both pass the
existence check before either writes, so duplicate invoices are created.

Make `process_webhook` safe under concurrent delivery:
- Concurrent delivery of the same `event_id` must create exactly one invoice.
- Sequential replay must remain idempotent.
- Distinct events must each create their own invoice, including under concurrency.

The storage layer simulates real write latency; do not remove it, and do not
change the models. Do not deduplicate by amount. Keep the change minimal and in
the webhook layer. When finished, run `pytest -q tests/` and summarize.
