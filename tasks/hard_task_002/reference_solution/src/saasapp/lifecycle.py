"""Account lifecycle transitions (reference solution for hard_task_002)."""

from saasapp import storage

LEGAL_TRANSITIONS = {
    ("active", "closed"),
    ("closed", "active"),
    ("active", "suspended"),
    ("suspended", "active"),
    ("suspended", "closed"),
}


def can_transition(current, new):
    return (current, new) in LEGAL_TRANSITIONS


def transition(tenant_id, new_status):
    """Move an account to new_status if legal, recording an audit entry."""
    current = storage.account_status(tenant_id)
    if not can_transition(current, new_status):
        raise ValueError(f"illegal transition {current} -> {new_status}")
    storage.set_account_status(tenant_id, new_status)
    storage.AUDIT.append((tenant_id, current, new_status))
