"""Hidden tests for pay_concurrency_02: deeper races, reset, and exact id set."""

import threading

import pytest

from payments import sequence


@pytest.fixture(autouse=True)
def _reset():
    sequence.reset()
    yield
    sequence.reset()


def _collect_concurrent(n):
    ids = []
    lock = threading.Lock()

    def work():
        nid = sequence.next_id()
        with lock:
            ids.append(nid)

    threads = [threading.Thread(target=work) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return ids


def test_high_concurrency_yields_distinct_ids():
    ids = _collect_concurrent(100)
    assert len(set(ids)) == 100
    assert max(ids) == 100


def test_ids_are_exactly_the_set_one_to_n():
    ids = _collect_concurrent(100)
    assert set(ids) == set(range(1, 101))


def test_reset_restarts_the_sequence_at_one():
    _collect_concurrent(30)
    sequence.reset()
    assert sequence.next_id() == 1
    assert sequence.next_id() == 2
