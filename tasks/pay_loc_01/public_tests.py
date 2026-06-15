"""Public tests for pay_loc_01 (visible symptom: understated gross)."""

import pytest

from payments import reporting, storage
from payments.webhook import process_webhook


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_summary_gross_is_true_sum_of_three_invoices():
    process_webhook("e1", 100)
    process_webhook("e2", 250)
    process_webhook("e3", 700)
    result = reporting.summary()
    # Base understates gross by dropping the first invoice (would be 950, not 1050).
    assert result["gross"] == 1050
    assert result["count"] == 3
