"""Per-tenant seat allocation with a hard quota (reference solution for saas_invariant_01).

The invariant is that the number of distinct assigned users for a tenant never
exceeds that tenant's seat limit. Assigning an already-assigned user is idempotent,
and an over-limit assignment is rejected before any state changes, so a rejected
assign never partially applies.
"""

SEAT_LIMITS = {"acme": 2, "globex": 1}

_ASSIGNED: dict[str, set] = {}


def reset():
    """Clear all seat assignments (for test isolation)."""
    _ASSIGNED.clear()


def limit(tenant_id):
    """The seat limit for `tenant_id`. Raises KeyError for an unknown tenant."""
    return SEAT_LIMITS[tenant_id]


def assigned_count(tenant_id):
    """Number of distinct users currently assigned a seat for `tenant_id`."""
    return len(_ASSIGNED.get(tenant_id, set()))


def assign(tenant_id, user_id):
    """Assign a seat to `user_id` under `tenant_id`, returning the new assigned count.

    Assigning a user who already holds a seat is a no-op and does not raise.
    Raises KeyError for an unknown tenant. Raises ValueError, without changing
    state, if assigning a new user would exceed the tenant's seat limit.
    """
    cap = SEAT_LIMITS[tenant_id]
    seats = _ASSIGNED.setdefault(tenant_id, set())
    if user_id in seats:
        return len(seats)
    if len(seats) + 1 > cap:
        raise ValueError("seat quota exceeded")
    seats.add(user_id)
    return len(seats)
