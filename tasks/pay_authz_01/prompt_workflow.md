Follow this process to add webhook signature verification to `payments`:

1. Read `webhook.py`, `models.py`, and `storage.py` to see how `process_webhook`
   creates an invoice and how an event is looked up.
2. State the canonical payload and signing scheme: HMAC-SHA256 over
   `f"{event_id}:{amount}"` keyed by a shared secret, compared in constant time.
3. Add the smallest verification API in a new `payments.verify` module:
   compute the expected signature, verify a supplied signature, and create an
   invoice only when verification passes (raising `PermissionError` otherwise).
4. Make sure an invalid signature, a tampered amount, or a wrong secret creates no
   invoice, and that `hmac.compare_digest` is used instead of `==`.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm `webhook.py`, `storage.py`, and `models.py` are
   unchanged.
