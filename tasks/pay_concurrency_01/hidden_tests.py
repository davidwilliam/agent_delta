"""Hidden tests for pay_concurrency_01: deeper races and independence."""

import threading

import pytest

from payments import wallet


@pytest.fixture(autouse=True)
def _reset():
    wallet.reset()
    yield
    wallet.reset()


def test_high_concurrency_sums_exactly():
    threads = [threading.Thread(target=wallet.credit, args=("a", 1)) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert wallet.balance("a") == 50


def test_distinct_accounts_independent_under_concurrency():
    def work(acct):
        for _ in range(10):
            wallet.credit(acct, 1)

    threads = [threading.Thread(target=work, args=(f"acct{i}",)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for i in range(5):
        assert wallet.balance(f"acct{i}") == 10


def test_interleaved_credits_two_accounts_each_total():
    barrier = threading.Barrier(40)

    def work(acct):
        barrier.wait()
        wallet.credit(acct, 1)

    threads = []
    for _ in range(20):
        threads.append(threading.Thread(target=work, args=("x",)))
        threads.append(threading.Thread(target=work, args=("y",)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert wallet.balance("x") == 20
    assert wallet.balance("y") == 20


def test_single_credit_returns_new_balance():
    assert wallet.credit("a", 5) == 5
    assert wallet.credit("a", 3) == 8
