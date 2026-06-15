"""Baseline tests (must keep passing).

Sequential idempotency and distinct-event behavior are already correct at base.
The concurrency bug is latent here and exercised by the injected task tests.
"""

import pytest

from payments import storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_sequential_replay_is_idempotent():
    process_webhook("e1", 100)
    process_webhook("e1", 100)
    assert storage.count_for_event("e1") == 1


def test_distinct_events_create_separate_invoices():
    process_webhook("e1", 100)
    process_webhook("e2", 100)
    assert len(storage.INVOICES) == 2
