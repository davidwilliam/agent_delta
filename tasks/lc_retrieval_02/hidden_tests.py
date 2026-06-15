"""Hidden tests for lc_retrieval_02 (official net total).

The authoritative reporting policy (ledger.policy.official_policy) sets
EXCLUDED_PARTS = [3, 17, 142] and SUPERSEDES the draft note (no exclusions) and
the deprecated legacy file (exclusions [5, 9]). A solution that excludes nothing,
or that uses the legacy exclusion list, produces a different net. These checks
confirm the authoritative exclusion list was honored.

The expected value (-202935) and the discriminators below are computed against the
fixture data and baked in; they are not recomputed from the solution under test.
"""

from ledger.official_net import official_net_total

AUTHORITATIVE = -202935  # net excluding parts [3, 17, 142]
NO_EXCLUSION = -205700  # 205700 credits - 411400 debits over every part
LEGACY_EXCLUSION = -203816  # net excluding the deprecated legacy parts [5, 9]


def test_equals_authoritative_value():
    assert official_net_total() == AUTHORITATIVE


def test_not_no_exclusion_net():
    # Must drop the authoritative excluded parts.
    assert official_net_total() != NO_EXCLUSION


def test_not_legacy_exclusion_net():
    assert official_net_total() != LEGACY_EXCLUSION
