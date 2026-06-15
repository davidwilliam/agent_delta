import time

LIMITS = {"acme": 3, "globex": 2}
_ASSIGNED = {}


def reset():
    _ASSIGNED.clear()


def assigned(tenant):
    return list(_ASSIGNED.get(tenant, []))


def assign(tenant, user):
    # BUG: check-then-act without locking; concurrent callers exceed the limit
    current = _ASSIGNED.get(tenant, [])
    if user in current:
        return len(current)
    if len(current) >= LIMITS[tenant]:
        raise ValueError("seat limit reached")
    time.sleep(0.002)  # widen the race window (do not remove)
    _ASSIGNED[tenant] = current + [user]
    return len(_ASSIGNED[tenant])
