"""Public tests for hard_task_004 (concurrency). Injected at score time."""

import threading

import pytest

from payments import storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_concurrent_same_event_creates_one():
    threads = [threading.Thread(target=process_webhook, args=("e1", 100)) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert storage.count_for_event("e1") == 1


def test_sequential_replay_idempotent():
    process_webhook("e1", 100)
    process_webhook("e1", 100)
    assert storage.count_for_event("e1") == 1


def test_distinct_events_separate():
    process_webhook("e1", 100)
    process_webhook("e2", 100)
    assert len(storage.INVOICES) == 2
