"""Public tests for lc_retrieval_01 (official credit total). Injected at score time."""

from ledger.official_credit import official_credit_total


def test_official_credit_total():
    assert official_credit_total() == 140250
