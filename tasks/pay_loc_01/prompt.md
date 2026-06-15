You are working in the `payments` service. Invoices are created from webhooks
(`payments.webhook.process_webhook(event_id, amount)`); each invoice records the
`amount` paid for an event. The reporting layer exposes
`payments.reporting.summary()`, which returns a dict with the `gross` total billed
and the `count` of invoices.

A bug report says the gross total in the summary is too low: it is understating the
amount billed. The `count` is correct, but `gross` is wrong. Locate the root cause
and fix it so that `gross` equals the sum of every invoice's amount.

Note: `summary()` only assembles the result; do not edit `reporting.py`. Fix the
underlying helper that computes the gross. Keep the change minimal. When finished,
run `pytest -q tests/` and summarize the root cause and your fix.
