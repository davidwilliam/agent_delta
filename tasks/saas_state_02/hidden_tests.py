"""Hidden tests for saas_state_02: legal chains, illegal guards, no side effects."""

import pytest

from saasapp import subscription


@pytest.fixture(autouse=True)
def _reset():
    subscription.reset()
    yield
    subscription.reset()


def test_pro_to_enterprise_allowed():
    subscription.change_plan("acme", "pro")
    subscription.change_plan("acme", "enterprise")
    assert subscription.plan("acme") == "enterprise"


def test_enterprise_to_pro_allowed():
    subscription.change_plan("acme", "pro")
    subscription.change_plan("acme", "enterprise")
    subscription.change_plan("acme", "pro")
    assert subscription.plan("acme") == "pro"


def test_enterprise_to_free_is_illegal():
    subscription.change_plan("acme", "pro")
    subscription.change_plan("acme", "enterprise")
    with pytest.raises(ValueError):
        subscription.change_plan("acme", "free")
    assert subscription.plan("acme") == "enterprise"


def test_pro_to_free_allowed():
    subscription.change_plan("acme", "pro")
    subscription.change_plan("acme", "free")
    assert subscription.plan("acme") == "free"


def test_illegal_transition_does_not_change_stored_plan():
    subscription.change_plan("acme", "pro")
    assert subscription.plan("acme") == "pro"
    # An illegal jump from pro must leave the stored plan untouched.
    with pytest.raises(ValueError):
        subscription.change_plan("acme", "startup")  # illegal target, not in LEGAL
    assert subscription.plan("acme") == "pro"
    subscription.change_plan("acme", "enterprise")
    with pytest.raises(ValueError):
        subscription.change_plan("acme", "free")  # enterprise->free is illegal
    assert subscription.plan("acme") == "enterprise"
