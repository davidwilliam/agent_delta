"""Public tests for saas_state_02 (legal transition + one illegal guard)."""

import pytest

from saasapp import subscription


@pytest.fixture(autouse=True)
def _reset():
    subscription.reset()
    yield
    subscription.reset()


def test_free_to_pro_succeeds():
    subscription.change_plan("acme", "pro")
    assert subscription.plan("acme") == "pro"


def test_free_to_enterprise_is_illegal():
    with pytest.raises(ValueError):
        subscription.change_plan("acme", "enterprise")
    assert subscription.plan("acme") == "free"
