"""Webhook signature verification (reference solution for pay_authz_01).

Webhook payloads are authenticated with an HMAC-SHA256 signature over the canonical
payload ``f"{event_id}:{amount}"`` keyed by a shared secret. An invoice is created
only when the supplied signature matches the expected one, compared in constant time
to avoid leaking timing information. An invalid signature raises PermissionError and
creates no invoice.
"""

import hashlib
import hmac

from payments.webhook import process_webhook


def expected_signature(event_id, amount, secret):
    """Return the hex HMAC-SHA256 of f"{event_id}:{amount}" keyed by secret."""
    payload = f"{event_id}:{amount}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def verify_signature(event_id, amount, signature, secret):
    """Return True only if signature matches the expected one (constant time)."""
    return hmac.compare_digest(expected_signature(event_id, amount, secret), signature)


def process_signed_webhook(event_id, amount, signature, secret):
    """Create an invoice only when the signature is valid, else raise PermissionError."""
    if not verify_signature(event_id, amount, signature, secret):
        raise PermissionError("invalid webhook signature")
    return process_webhook(event_id, amount)
