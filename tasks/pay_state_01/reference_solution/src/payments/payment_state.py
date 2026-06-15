"""Payment status lifecycle for invoices (reference solution for pay_state_01).

Each event whose invoice exists has a status. The status defaults to "paid" once an
invoice exists. Transitions are audited and only legal transitions are allowed;
"refunded" is terminal, so no transition out of it is legal.
"""

from payments import storage

_LEGAL = {
    ("paid", "disputed"),
    ("disputed", "paid"),
    ("disputed", "refunded"),
    ("paid", "refunded"),
}

_STATUS: dict[str, str] = {}
_AUDIT: list[tuple[str, str, str]] = []


def reset():
    """Clear the status ledger and audit (for test isolation)."""
    _STATUS.clear()
    _AUDIT.clear()


def status(event_id):
    """Return the current status for `event_id`.

    Defaults to "paid" when the event has an invoice but no recorded status.
    Raises KeyError if no invoice exists for the event.
    """
    if storage.find_by_event(event_id) is None:
        raise KeyError(event_id)
    return _STATUS.get(event_id, "paid")


def transition(event_id, new_status):
    """Move `event_id` to `new_status`, enforcing legality from the current status.

    Records the new status, appends (event_id, from, to) to the audit, and returns
    the new status. Raises KeyError for an unknown event and ValueError on an
    illegal transition.
    """
    current = status(event_id)
    if (current, new_status) not in _LEGAL:
        raise ValueError(f"illegal transition: {current} -> {new_status}")
    _STATUS[event_id] = new_status
    _AUDIT.append((event_id, current, new_status))
    return new_status


def audit():
    """Return the list of (event_id, from, to) transition tuples in order."""
    return _AUDIT
