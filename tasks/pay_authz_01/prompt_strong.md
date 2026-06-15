Add webhook signature verification to the `payments` service.

Expose, in the `payments` package, a new module `payments.verify` with:
- `expected_signature(event_id, amount, secret)`: the hex HMAC-SHA256 of the
  canonical payload `f"{event_id}:{amount}"` keyed by `secret` (utf-8).
- `verify_signature(event_id, amount, signature, secret)`: return True only if
  `signature` matches the expected one; otherwise return False.
- `process_signed_webhook(event_id, amount, signature, secret)`: when the signature
  is valid, delegate to `payments.webhook.process_webhook(event_id, amount)` and
  return the invoice; otherwise raise `PermissionError` and create no invoice.

Requirements:
1. Use the stdlib `hmac` and `hashlib` modules only (offline, no network).
2. Compare signatures in constant time with `hmac.compare_digest`. Do not use a
   plain `==` comparison.
3. A tampered amount, a wrong secret, or any non-matching signature must be rejected
   and must create no invoice.
4. `verify_signature` returns False for a bad signature; it does not raise.
5. A valid signature replayed twice is idempotent: still one invoice for the event.
6. Do not modify `webhook.py`, `storage.py`, or `models.py`; do not weaken tests.

When finished, run `pytest -q tests/`.
