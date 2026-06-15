"""Public tests for mk_loc_01 (one failing case + one regression guard)."""

from mathkit.leaderboard import percent


def test_full_score_is_100_percent():
    # Fails at base: the off-by-one denominator understates 100/100 as 99.
    assert percent(100, 100) == 100


def test_half_score_is_50_percent():
    # Fails at base for the same reason; the correct value is 50.
    assert percent(50, 100) == 50
