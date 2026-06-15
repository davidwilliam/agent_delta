You are working in the `payments` service. Invoices are created from webhooks
(`payments.webhook.process_webhook(event_id, amount)`). Right now any caller can
trigger invoice creation: there is no check that a webhook actually came from the
trusted payment provider.

Add webhook signature verification. Webhook deliveries are signed with an
HMAC-SHA256 signature over the canonical payload `f"{event_id}:{amount}"` keyed by a
shared secret. Provide a way to verify a delivery and to create an invoice only when
the signature is valid. A delivery with an invalid signature must be rejected and
must create no invoice.

The verification must be done with the stdlib `hmac` and `hashlib` modules and must
compare signatures in constant time. Do not modify `webhook.py`, `storage.py`, or
`models.py`. Keep the change minimal. When finished, run `pytest -q tests/` and
summarize what you added and how an unsigned or tampered payload is rejected.

## Required API (the tests import these exact names)

- Module `payments.verify` exposing `expected_signature(event_id, amount, secret)` (returns the expected signature string), `verify_signature(event_id, amount, signature, secret)` (returns `True` only when the signature is valid), and `process_signed_webhook(event_id, amount, signature, secret)` (creates the invoice when valid, raises `PermissionError` otherwise).
