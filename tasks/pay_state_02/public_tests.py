"""Public tests for pay_state_02 (visible happy path + one illegal-transition guard)."""

import pytest

from payments import billing_state


@pytest.fixture(autouse=True)
def _reset():
    billing_state.reset()
    yield
    billing_state.reset()


def test_trialing_to_active_ok():
    assert billing_state.transition("a", "active") == "active"
    assert billing_state.state("a") == "active"


def test_trialing_to_canceled_is_illegal():
    with pytest.raises(ValueError):
        billing_state.transition("a", "canceled")
    assert billing_state.state("a") == "trialing"
