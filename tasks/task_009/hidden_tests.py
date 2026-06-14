"""Hidden tests for task_009 (long-context ledger totals).

A solution that handles only the first schema variant (amount/kind) undercounts,
because credits and debits are spread across all three schemas. These checks
confirm the full traversal and all variants are handled.
"""

from ledger.totals import total_credits, total_debits


def test_credits_exact():
    assert total_credits() == 205700


def test_debits_exact():
    assert total_debits() == 411400


def test_credits_plus_debits_is_grand_total():
    # Every entry is a credit or a debit; the two must cover all 24,200 entries.
    assert total_credits() + total_debits() == 205700 + 411400
