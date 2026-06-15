import threading
import time

LIMITS = {"acme": 3, "globex": 2}
_ASSIGNED = {}
_LOCK = threading.Lock()


def reset():
    with _LOCK:
        _ASSIGNED.clear()


def assigned(tenant):
    return list(_ASSIGNED.get(tenant, []))


def assign(tenant, user):
    # Hold the lock across the whole check-then-act so the seat limit is enforced
    # atomically; the latency stays inside the critical section.
    with _LOCK:
        current = _ASSIGNED.get(tenant, [])
        if user in current:
            return len(current)
        if len(current) >= LIMITS[tenant]:
            raise ValueError("seat limit reached")
        time.sleep(0.002)  # widen the race window (do not remove)
        _ASSIGNED[tenant] = current + [user]
        return len(_ASSIGNED[tenant])
