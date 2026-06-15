"""Hidden tests for pay_state_02: legal lifecycle, terminal guard, and edge cases."""

import pytest

from payments import billing_state


@pytest.fixture(autouse=True)
def _reset():
    billing_state.reset()
    yield
    billing_state.reset()


def test_active_past_due_active_cycle_ok():
    billing_state.transition("a", "active")
    assert billing_state.transition("a", "past_due") == "past_due"
    assert billing_state.transition("a", "active") == "active"
    assert billing_state.state("a") == "active"


def test_active_to_canceled_ok():
    billing_state.transition("a", "active")
    assert billing_state.transition("a", "canceled") == "canceled"
    assert billing_state.state("a") == "canceled"


def test_canceled_is_terminal():
    billing_state.transition("a", "active")
    billing_state.transition("a", "canceled")
    with pytest.raises(ValueError):
        billing_state.transition("a", "active")
    assert billing_state.state("a") == "canceled"


def test_past_due_to_canceled_ok():
    billing_state.transition("a", "active")
    billing_state.transition("a", "past_due")
    assert billing_state.transition("a", "canceled") == "canceled"
    assert billing_state.state("a") == "canceled"


def test_illegal_transition_does_not_change_stored_state():
    billing_state.transition("a", "active")
    with pytest.raises(ValueError):
        billing_state.transition("a", "trialing")
    assert billing_state.state("a") == "active"
