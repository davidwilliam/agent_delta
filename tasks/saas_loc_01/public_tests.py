"""Public tests for saas_loc_01 (visible: acme active count excludes archived)."""

import pytest

from saasapp import dashboard, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_acme_active_count_excludes_archived():
    # acme has p1 (active) and p2 (archived); only p1 should count.
    assert dashboard.project_counts("acme")["active"] == 1
