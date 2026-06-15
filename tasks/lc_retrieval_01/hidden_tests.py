"""Hidden tests for lc_retrieval_01 (official credit total).

The authoritative reporting policy (ledger.policy.official_policy) sets
REPORTING_CUTOFF = 150 and SUPERSEDES the draft note (cutoff 120) and the
deprecated legacy file (cutoff 200). A solution that sums all parts, or that uses
the draft or legacy cutoff, produces a different number. These checks confirm the
authoritative value was used.

The expected value (140250) and the discriminators below are computed against the
fixture data and baked in; they are not recomputed from the solution under test.
"""

from ledger.official_credit import official_credit_total

AUTHORITATIVE = 140250  # credits over parts 0..149 (cutoff 150)
ALL_PARTS_CREDITS = 205700  # task_009 grand credit total over every part
DRAFT_CUTOFF_120 = 112200  # credits over parts 0..119 (draft, not approved)
LEGACY_CUTOFF_200 = 187017  # credits over parts 0..199 (deprecated legacy)


def test_equals_authoritative_value():
    assert official_credit_total() == AUTHORITATIVE


def test_not_all_parts_total():
    # Must exclude parts >= the authoritative cutoff.
    assert official_credit_total() != ALL_PARTS_CREDITS
    assert official_credit_total() < ALL_PARTS_CREDITS


def test_not_draft_cutoff():
    assert official_credit_total() != DRAFT_CUTOFF_120


def test_not_legacy_cutoff():
    assert official_credit_total() != LEGACY_CUTOFF_200
