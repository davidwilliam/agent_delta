"""Public tests for pay_concurrency_02 (sequential happy path + one race guard)."""

import threading

import pytest

from payments import sequence


@pytest.fixture(autouse=True)
def _reset():
    sequence.reset()
    yield
    sequence.reset()


def test_sequential_next_id_counts_up():
    assert sequence.next_id() == 1
    assert sequence.next_id() == 2
    assert sequence.next_id() == 3


def test_concurrent_next_id_returns_unique_ids():
    ids = []
    lock = threading.Lock()

    def work():
        nid = sequence.next_id()
        with lock:
            ids.append(nid)

    threads = [threading.Thread(target=work) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(set(ids)) == 50
    assert max(ids) == 50
