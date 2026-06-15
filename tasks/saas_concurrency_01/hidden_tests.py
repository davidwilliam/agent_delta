"""Hidden tests for saas_concurrency_01: deeper races, independence, idempotency."""

import threading

import pytest

from saasapp import provisioning


@pytest.fixture(autouse=True)
def _reset():
    provisioning.reset()
    yield
    provisioning.reset()


def _race(tenant, n):
    successes = []
    lock = threading.Lock()

    def work(user):
        try:
            provisioning.assign(tenant, user)
            with lock:
                successes.append(user)
        except ValueError:
            pass

    threads = [threading.Thread(target=work, args=(f"u{i}",)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return successes


def test_high_concurrency_acme_still_exactly_three():
    successes = _race("acme", 20)
    assert len(successes) == 3
    assert len(provisioning.assigned("acme")) == 3


def test_globex_limit_two_under_concurrency():
    successes = _race("globex", 20)
    assert len(successes) == 2
    assert len(provisioning.assigned("globex")) == 2


def test_distinct_tenants_independent_under_concurrency():
    def work(tenant, user):
        try:
            provisioning.assign(tenant, user)
        except ValueError:
            pass

    threads = []
    for i in range(20):
        threads.append(threading.Thread(target=work, args=("acme", f"a{i}")))
        threads.append(threading.Thread(target=work, args=("globex", f"g{i}")))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(provisioning.assigned("acme")) == 3
    assert len(provisioning.assigned("globex")) == 2


def test_reassigning_existing_user_is_idempotent():
    provisioning.assign("acme", "u1")
    provisioning.assign("acme", "u1")
    provisioning.assign("acme", "u1")
    assert provisioning.assigned("acme") == ["u1"]
    # Two more distinct users still fit; a third distinct user is rejected.
    provisioning.assign("acme", "u2")
    provisioning.assign("acme", "u3")
    with pytest.raises(ValueError):
        provisioning.assign("acme", "u4")
    assert len(provisioning.assigned("acme")) == 3
