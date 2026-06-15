"""Public tests for lc_retrieval_02 (official net total). Injected at score time."""

from ledger.official_net import official_net_total


def test_official_net_total():
    assert official_net_total() == -202935
