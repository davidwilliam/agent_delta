"""Public tests for pay_minimal_01 (visible off-by-one in proration)."""

from payments.proration import proration


def test_half_period_prorates_to_half():
    # Base divides by days_total - 1 (1000 * 15 // 29 == 517), not 500.
    assert proration(1000, 15, 30) == 500


def test_full_period_prorates_to_full():
    # Base gives 1000 * 30 // 29 == 1034, not 1000.
    assert proration(1000, 30, 30) == 1000
