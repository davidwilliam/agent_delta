Add webhook signature verification to the `payments` service. Only a webhook whose
HMAC-SHA256 signature over `f"{event_id}:{amount}"` matches the shared secret may
create an invoice; an invalid signature must be rejected and create no invoice.
