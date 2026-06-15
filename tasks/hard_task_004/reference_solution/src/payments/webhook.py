"""Webhook processing (reference solution for hard_task_004).

A module-level lock makes the check-and-create atomic, so concurrent delivery of
the same event creates exactly one invoice while distinct events still each create
their own.
"""

import threading

from payments import storage
from payments.models import Invoice

_lock = threading.Lock()


def process_webhook(event_id, amount):
    """Create an invoice for event_id once, returning the existing one on replay."""
    with _lock:
        existing = storage.find_by_event(event_id)
        if existing is not None:
            return existing
        invoice = Invoice(event_id=event_id, amount=amount)
        storage.append_invoice(invoice)
        return invoice
