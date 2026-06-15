"""Hidden tests for hard_task_004 (concurrency). Deeper races + invariants."""

import threading

import pytest

from payments import storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_high_concurrency_same_event_one_invoice():
    threads = [threading.Thread(target=process_webhook, args=("burst", 1)) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert storage.count_for_event("burst") == 1


def test_concurrent_distinct_events_all_created_once():
    # 10 distinct events, 3 threads each: exactly 10 invoices, one per event.
    threads = [threading.Thread(target=process_webhook, args=(f"e{i}", 50))
               for i in range(10) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(storage.INVOICES) == 10
    for i in range(10):
        assert storage.count_for_event(f"e{i}") == 1


def test_distinct_events_same_amount_not_deduped():
    process_webhook("a", 100)
    process_webhook("b", 100)
    assert len(storage.INVOICES) == 2


def test_concurrent_callers_get_an_invoice_each():
    results = []
    threads = [threading.Thread(target=lambda: results.append(process_webhook("x", 7)))
               for _ in range(15)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert storage.count_for_event("x") == 1
    assert all(r is not None for r in results) and len(results) == 15
