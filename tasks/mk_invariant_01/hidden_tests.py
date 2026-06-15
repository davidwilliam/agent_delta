"""Hidden tests for mk_invariant_01: balance invariant and edge cases."""

import pytest

from mathkit.ledger import apply_transactions


def test_withdrawal_exactly_to_zero_is_allowed():
    assert apply_transactions(100, [-100]) == 0


def test_negative_start_balance_raises():
    with pytest.raises(ValueError):
        apply_transactions(-1, [])


def test_empty_transactions_returns_start_balance():
    assert apply_transactions(75, []) == 75


def test_mixed_sequence_returns_correct_final_balance():
    assert apply_transactions(50, [100, -30, 10, -80, 25]) == 75


def test_overdraw_partway_through_raises_and_is_not_applied():
    transactions = [50, -200, 200]
    with pytest.raises(ValueError):
        apply_transactions(100, transactions)
    # The offending withdrawal must not have been applied. Re-running the safe
    # prefix (everything before the overdraw) yields the balance at that point.
    assert apply_transactions(100, [50]) == 150
