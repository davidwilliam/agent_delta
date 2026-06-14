"""Public tests for task_009 (long-context ledger totals). Injected at score time."""

from ledger.totals import total_credits, total_debits


def test_total_credits():
    assert total_credits() == 205700


def test_total_debits():
    assert total_debits() == 411400
