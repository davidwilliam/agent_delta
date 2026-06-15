"""Public tests for pay_invariant_01 (visible happy path + one over-refund guard)."""

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


def test_partial_refund_records_total():
    process_webhook("e1", 1000)
    assert refunds.refund("e1", 400) == 400
    assert refunds.refunded_total("e1") == 400


def test_over_refund_is_rejected():
    process_webhook("e1", 1000)
    refunds.refund("e1", 400)
    with pytest.raises(ValueError):
        refunds.refund("e1", 700)  # 400 + 700 > 1000
