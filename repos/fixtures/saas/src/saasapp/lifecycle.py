"""Account lifecycle transitions.

NOTE (fixture): only active and closed states exist here. The AgentDelta H5 task
adds a 'suspended' state with its legal transitions. Transitions are audited.
"""

from saasapp import storage

# Legal (from, to) transitions. The H5 task extends this for 'suspended'.
LEGAL_TRANSITIONS = {
    ("active", "closed"),
    ("closed", "active"),
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
