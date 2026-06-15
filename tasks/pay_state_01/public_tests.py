"""Public tests for pay_state_01 (visible happy path + one illegal-transition guard)."""

import pytest

from payments import payment_state, storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    payment_state.reset()
    yield
    storage.reset()
    payment_state.reset()


def test_default_status_is_paid_then_disputed():
    process_webhook("e1", 1000)
    assert payment_state.status("e1") == "paid"
    assert payment_state.transition("e1", "disputed") == "disputed"
    assert payment_state.status("e1") == "disputed"


def test_illegal_target_from_paid_raises():
    process_webhook("e2", 500)
    with pytest.raises(ValueError):
        payment_state.transition("e2", "shipped")
