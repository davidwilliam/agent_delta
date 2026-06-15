"""Public tests for pay_concurrency_01 (sequential happy path + one race guard)."""

import threading

import pytest

from payments import wallet


@pytest.fixture(autouse=True)
def _reset():
    wallet.reset()
    yield
    wallet.reset()


def test_sequential_credits_accumulate():
    wallet.credit("a", 100)
    wallet.credit("a", 100)
    assert wallet.balance("a") == 200


def test_concurrent_credits_no_lost_updates():
    threads = [threading.Thread(target=wallet.credit, args=("a", 1)) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert wallet.balance("a") == 20
