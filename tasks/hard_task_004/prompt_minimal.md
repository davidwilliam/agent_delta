In the `payments` service, `process_webhook(event_id, amount)` in
`payments/webhook.py` creates duplicate invoices when the same event arrives on
two threads at once. Make it safe under concurrent delivery so the same event
creates exactly one invoice, then run `pytest -q tests/`.
