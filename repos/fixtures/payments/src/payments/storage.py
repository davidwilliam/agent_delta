"""In-memory invoice store with simulated write latency.

The latency in append_invoice models real I/O and widens the race window so that
unsafe check-then-act webhook handling reliably produces duplicates. Do not
remove it; the concurrency task must be solved in the webhook layer.
"""

import time

INVOICES = []


def reset():
    global INVOICES
    INVOICES = []


def find_by_event(event_id):
    for inv in INVOICES:
        if inv.event_id == event_id:
            return inv
    return None


def append_invoice(invoice):
    time.sleep(0.003)  # simulated write latency (do not remove)
    INVOICES.append(invoice)


def count_for_event(event_id):
    return sum(1 for inv in INVOICES if inv.event_id == event_id)
