"""In-memory wallet balance store with simulated write latency.

Reference solution for pay_concurrency_01. credit() does a read-modify-write
under a module-level lock, so concurrent credits to the same account never lose
updates. The simulated latency is preserved; only the read-modify-write is made
atomic.
"""

import threading
import time

_BALANCES = {}
_LOCK = threading.Lock()


def reset():
    with _LOCK:
        _BALANCES.clear()


def balance(acct):
    return _BALANCES.get(acct, 0)


def credit(acct, amount):
    with _LOCK:
        current = _BALANCES.get(acct, 0)
        time.sleep(0.002)  # simulated latency (do not remove); widens the race window
        _BALANCES[acct] = current + amount
        return _BALANCES[acct]
