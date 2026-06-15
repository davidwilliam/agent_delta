"""Partial refunds for invoices (reference solution for pay_invariant_01).

The invariant is that the cumulative refunded amount for an event never exceeds the
amount paid on that event's invoice. Over-refunds are rejected before any state is
recorded, so a rejected refund never partially applies.
"""

from payments import storage

_REFUNDED: dict[str, int] = {}


def reset():
    """Clear the refund ledger (for test isolation)."""
    _REFUNDED.clear()


def refunded_total(event_id):
    """The amount refunded for `event_id` so far (0 if none)."""
    return _REFUNDED.get(event_id, 0)


def refund(event_id, amount):
    """Record a refund of `amount` against the invoice for `event_id`.

    Returns the new cumulative refunded total. Raises ValueError on a non-positive
    amount or an over-refund, and KeyError if the event has no invoice.
    """
    invoice = storage.find_by_event(event_id)
    if invoice is None:
        raise KeyError(event_id)
    if amount <= 0:
        raise ValueError("refund amount must be positive")
    new_total = _REFUNDED.get(event_id, 0) + amount
    if new_total > invoice.amount:
        raise ValueError("cumulative refund exceeds amount paid")
    _REFUNDED[event_id] = new_total
    return new_total
