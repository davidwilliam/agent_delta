"""Webhook processing.

NOTE (fixture): process_webhook is idempotent for sequential delivery, but it is
NOT safe under concurrent delivery of the same event -- two simultaneous calls
both pass the existence check before either writes, creating duplicate invoices.
The AgentDelta concurrency task makes it safe under concurrent delivery.
"""

from payments import storage
from payments.models import Invoice


def process_webhook(event_id, amount):
    """Create an invoice for event_id once, returning the existing one on replay."""
    existing = storage.find_by_event(event_id)
    if existing is not None:
        return existing
    invoice = Invoice(event_id=event_id, amount=amount)
    storage.append_invoice(invoice)
    return invoice
