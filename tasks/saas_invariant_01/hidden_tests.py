"""Hidden tests for saas_invariant_01: idempotency, isolation, and edge cases."""

import pytest

from saasapp import seats


@pytest.fixture(autouse=True)
def _reset():
    seats.reset()
    yield
    seats.reset()


def test_reassign_existing_user_is_idempotent():
    seats.assign("acme", "u1")
    assert seats.assigned_count("acme") == 1
    # Re-assigning the same user does not raise and does not consume a new seat.
    assert seats.assign("acme", "u1") == 1
    assert seats.assigned_count("acme") == 1


def test_idempotent_reassign_does_not_exceed_limit():
    seats.assign("acme", "u1")
    seats.assign("acme", "u2")
    # u1 already holds a seat, so re-assigning stays at the limit, no raise.
    assert seats.assign("acme", "u1") == 2
    assert seats.assigned_count("acme") == 2


def test_distinct_tenants_are_independent():
    assert seats.assign("globex", "g1") == 1
    with pytest.raises(ValueError):
        seats.assign("globex", "g2")  # globex limit is 1
    # acme is unaffected by globex being full.
    assert seats.assign("acme", "u1") == 1
    assert seats.assigned_count("globex") == 1


def test_over_limit_attempt_does_not_add_user():
    seats.assign("globex", "g1")
    with pytest.raises(ValueError):
        seats.assign("globex", "g2")
    assert seats.assigned_count("globex") == 1
    # g2 was never assigned, so freeing g1 conceptually is not needed: g2 is absent.
    seats.reset()
    seats.assign("globex", "g1")
    assert seats.assigned_count("globex") == 1


def test_unknown_tenant_raises():
    with pytest.raises(KeyError):
        seats.limit("nope")
    with pytest.raises(KeyError):
        seats.assign("nope", "x1")
