"""Public tests for mk_invariant_01 (visible happy path + one overdraw guard)."""

import pytest

from mathkit.ledger import apply_transactions


def test_deposits_and_withdrawals_stay_non_negative():
    assert apply_transactions(100, [50, -30, -20]) == 100


def test_overdraw_is_rejected():
    with pytest.raises(ValueError):
        apply_transactions(100, [-200])
