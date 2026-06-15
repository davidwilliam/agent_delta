# Expected behavior - pay_authz_01

The correct solution adds a small `payments.verify` module that authenticates webhook
deliveries with an HMAC-SHA256 signature over the canonical payload
`f"{event_id}:{amount}"` keyed by a shared secret, and creates an invoice only when
the supplied signature matches. An invalid signature raises `PermissionError` and
creates no invoice.

Why the obvious solution fails:
- Trusting the payload and calling `process_webhook` without verifying the signature
  creates invoices for forged or tampered deliveries.
- Signing only the event_id (not the amount) lets an attacker change the amount while
  keeping a valid-looking signature; the canonical payload must bind both fields.
- Comparing signatures with `==` leaks timing information and is the rejected
  shortcut here; the reference uses `hmac.compare_digest`.
- Letting `verify_signature` raise on a bad signature (instead of returning False)
  breaks the verify/act split the tests rely on.

Discriminators (hidden): a valid signature creates exactly one invoice; a tampered
amount, a wrong secret, and any non-matching signature are rejected with no invoice;
a valid signature replayed twice stays idempotent (still one invoice, matching
`process_webhook` semantics); `verify_signature` returns False (not an exception) for
a bad signature.

Forbidden shortcuts: modifying `webhook.py`, `storage.py`, or `models.py`; using a
non-constant-time comparison; or weakening tests.
