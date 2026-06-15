"""Hidden tests for pay_state_01: legal lifecycle, terminal state, and edge cases."""

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


def test_disputed_to_refunded_allowed():
    process_webhook("e1", 1000)
    payment_state.transition("e1", "disputed")
    assert payment_state.transition("e1", "refunded") == "refunded"
    assert payment_state.status("e1") == "refunded"


def test_paid_to_refunded_allowed():
    process_webhook("e1", 1000)
    assert payment_state.transition("e1", "refunded") == "refunded"


def test_refunded_is_terminal():
    process_webhook("e1", 1000)
    payment_state.transition("e1", "refunded")
    for target in ("paid", "disputed", "refunded"):
        with pytest.raises(ValueError):
            payment_state.transition("e1", target)
    assert payment_state.status("e1") == "refunded"


def test_unknown_event_raises_on_status_and_transition():
    with pytest.raises(KeyError):
        payment_state.status("nope")
    with pytest.raises(KeyError):
        payment_state.transition("nope", "disputed")


def test_audit_records_transitions_in_order():
    process_webhook("e1", 1000)
    payment_state.transition("e1", "disputed")
    payment_state.transition("e1", "paid")
    payment_state.transition("e1", "refunded")
    assert payment_state.audit() == [
        ("e1", "paid", "disputed"),
        ("e1", "disputed", "paid"),
        ("e1", "paid", "refunded"),
    ]


def test_distinct_events_track_independently():
    process_webhook("e1", 1000)
    process_webhook("e2", 500)
    payment_state.transition("e1", "disputed")
    assert payment_state.status("e1") == "disputed"
    assert payment_state.status("e2") == "paid"
    payment_state.transition("e2", "refunded")
    assert payment_state.status("e1") == "disputed"
    assert payment_state.status("e2") == "refunded"
