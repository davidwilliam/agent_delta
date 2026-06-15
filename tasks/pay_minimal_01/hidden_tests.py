"""Hidden tests for pay_minimal_01: edge cases and denominator proof."""

from payments.proration import proration


def test_zero_days_used_is_zero():
    assert proration(1000, 0, 30) == 0


def test_partial_period_floor_division():
    # Correct: 900 * 10 // 30 == 300. Base: 9000 // 29 == 310.
    assert proration(900, 10, 30) == 300


def test_denominator_is_days_total_not_minus_one():
    # 29000 // 30 == 966 (correct) vs 29000 // 29 == 1000 (buggy denominator).
    assert proration(1000, 29, 30) == 966


def test_general_formula_holds():
    assert proration(1200, 7, 31) == 1200 * 7 // 31
