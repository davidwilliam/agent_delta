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

Requirements:
1. Concurrent delivery of the same event creates exactly one invoice.
2. Sequential replay of the same event remains idempotent.
3. Distinct events each create their own invoice, including under concurrency.
4. The fix is in the webhook layer; storage latency and models are unchanged.
5. Do not remove or reduce the simulated write latency in storage.
6. Do not deduplicate by amount; distinct events with the same amount are distinct.
7. Do not weaken, skip, or delete tests.
8. Keep the patch minimal and in the webhook layer.

When finished, run `pytest -q tests/` and summarize.
