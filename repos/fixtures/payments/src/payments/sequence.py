"""Monotonic id sequence with simulated write latency.

NOTE (fixture): next_id() does an UNLOCKED read-modify-write with simulated
latency, so concurrent callers read the same starting value and get duplicate
ids. The latency models real work and widens the race window; do not remove it.
The AgentDelta concurrency task makes next_id() return unique, monotonic ids
under concurrency.
"""

import time

_COUNTER = {"n": 0}


def reset():
    _COUNTER["n"] = 0


def next_id():
    # BUG: read-modify-write without a lock; concurrent callers get duplicate ids
    current = _COUNTER["n"]
    time.sleep(0.001)  # widen the race window (do not remove)
    _COUNTER["n"] = current + 1
    return current + 1
