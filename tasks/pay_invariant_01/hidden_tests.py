"""Hidden tests for pay_invariant_01: cumulative invariant and edge cases."""

import pytest

from payments import refunds, storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    refunds.reset()
    yield
    storage.reset()
    refunds.reset()


def test_multiple_partials_up_to_paid_succeed():
    process_webhook("e1", 1000)
    refunds.refund("e1", 300)
    refunds.refund("e1", 300)
    assert refunds.refund("e1", 400) == 1000
    assert refunds.refunded_total("e1") == 1000


def test_full_refund_in_one_shot():
    process_webhook("e1", 1000)
    assert refunds.refund("e1", 1000) == 1000


def test_over_refund_does_not_partially_apply():
    process_webhook("e1", 1000)
    refunds.refund("e1", 900)
    with pytest.raises(ValueError):
        refunds.refund("e1", 200)  # would reach 1100
    # The rejected refund must not have changed the recorded total.
    assert refunds.refunded_total("e1") == 900


def test_zero_and_negative_amounts_rejected():
    process_webhook("e1", 1000)
    with pytest.raises(ValueError):
        refunds.refund("e1", 0)
    with pytest.raises(ValueError):
        refunds.refund("e1", -50)
    assert refunds.refunded_total("e1") == 0


def test_unknown_event_raises():
    with pytest.raises((KeyError, ValueError)):
        refunds.refund("nope", 100)


def test_distinct_events_track_independently():
    process_webhook("e1", 1000)
    process_webhook("e2", 500)
    refunds.refund("e1", 600)
    refunds.refund("e2", 500)
    assert refunds.refunded_total("e1") == 600
    assert refunds.refunded_total("e2") == 500
    with pytest.raises(ValueError):
        refunds.refund("e2", 1)  # e2 already fully refunded
