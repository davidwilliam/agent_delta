"""Public tests for saas_invariant_01 (visible happy path + one quota guard)."""

import pytest

from saasapp import seats


@pytest.fixture(autouse=True)
def _reset():
    seats.reset()
    yield
    seats.reset()


def test_assign_up_to_limit_succeeds():
    assert seats.assign("acme", "u1") == 1
    assert seats.assign("acme", "u2") == 2
    assert seats.assigned_count("acme") == 2


def test_assign_over_limit_is_rejected():
    seats.assign("acme", "u1")
    seats.assign("acme", "u2")
    with pytest.raises(ValueError):
        seats.assign("acme", "u3")  # would be the 3rd seat for a limit of 2
    assert seats.assigned_count("acme") == 2
