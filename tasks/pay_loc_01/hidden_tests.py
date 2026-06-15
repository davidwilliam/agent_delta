"""Hidden tests for pay_loc_01: root-cause cases the symptom patch would miss."""

import pytest

from payments import aggregate, reporting, storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_single_invoice_gross_equals_its_amount():
    process_webhook("e1", 500)
    # Base drops the only invoice and reports 0.
    assert reporting.summary()["gross"] == 500
    assert aggregate.gross_total() == 500


def test_zero_invoices_gross_is_zero():
    assert reporting.summary()["gross"] == 0
    assert aggregate.gross_total() == 0


def test_gross_always_equals_sum_of_all_amounts():
    amounts = [10, 20, 30, 40, 50]
    for i, amt in enumerate(amounts):
        process_webhook(f"e{i}", amt)
    assert aggregate.gross_total() == sum(amounts)
    assert reporting.summary()["gross"] == sum(amounts)


def test_two_invoices_include_the_first():
    process_webhook("e1", 111)
    process_webhook("e2", 222)
    assert reporting.summary()["gross"] == 333
