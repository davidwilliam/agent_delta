"""Public tests for saas_concurrency_01 (sequential limit + one race guard)."""

import threading

import pytest

from saasapp import provisioning


@pytest.fixture(autouse=True)
def _reset():
    provisioning.reset()
    yield
    provisioning.reset()


def test_sequential_assigns_up_to_limit_then_raises():
    provisioning.assign("acme", "u1")
    provisioning.assign("acme", "u2")
    provisioning.assign("acme", "u3")
    assert sorted(provisioning.assigned("acme")) == ["u1", "u2", "u3"]
    with pytest.raises(ValueError):
        provisioning.assign("acme", "u4")


def test_concurrent_assigns_respect_seat_limit():
    successes = []
    errors = []
    lock = threading.Lock()

    def work(user):
        try:
            provisioning.assign("acme", user)
            with lock:
                successes.append(user)
        except ValueError:
            with lock:
                errors.append(user)

    threads = [threading.Thread(target=work, args=(f"u{i}",)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(successes) == 3
    assert len(errors) == 7
    assert len(provisioning.assigned("acme")) == 3
