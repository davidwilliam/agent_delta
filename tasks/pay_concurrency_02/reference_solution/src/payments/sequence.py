"""Monotonic id sequence with simulated write latency.

Reference solution for pay_concurrency_02. next_id() does a read-modify-write
under a module-level lock, so concurrent callers always get unique, monotonic
ids. The simulated latency is preserved; only the read-modify-write is made
atomic.
"""

import threading
import time

_COUNTER = {"n": 0}
_LOCK = threading.Lock()


def reset():
    with _LOCK:
        _COUNTER["n"] = 0


def next_id():
    with _LOCK:
        current = _COUNTER["n"]
        time.sleep(0.001)  # widen the race window (do not remove)
        _COUNTER["n"] = current + 1
        return current + 1
