"""In-memory wallet balance store with simulated write latency.

NOTE (fixture): credit() does an UNLOCKED read-modify-write with simulated
latency, so concurrent credits to the same account lose updates. The latency
models real I/O and widens the race window; do not remove it. The AgentDelta
concurrency task makes credit() safe under concurrent updates.
"""

import time

_BALANCES = {}


def reset():
    _BALANCES.clear()


def balance(acct):
    return _BALANCES.get(acct, 0)


def credit(acct, amount):
    current = _BALANCES.get(acct, 0)
    time.sleep(0.002)  # simulated latency (do not remove); widens the race window
    _BALANCES[acct] = current + amount
    return _BALANCES[acct]
