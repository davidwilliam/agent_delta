"""Hidden tests for saas_state_01: inbound guards, audit, and existing transitions."""

import pytest

from saasapp import lifecycle, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_trial_to_closed_allowed():
    storage.set_account_status("acme", "trial")
    lifecycle.transition("acme", "closed")
    assert storage.account_status("acme") == "closed"


def test_closed_to_trial_is_illegal():
    storage.set_account_status("acme", "closed")
    with pytest.raises(ValueError):
        lifecycle.transition("acme", "trial")


def test_active_to_trial_is_illegal():
    storage.set_account_status("acme", "active")
    with pytest.raises(ValueError):
        lifecycle.transition("acme", "trial")


def test_trial_to_active_records_audit():
    storage.set_account_status("acme", "trial")
    lifecycle.transition("acme", "active")
    assert ("acme", "trial", "active") in storage.AUDIT


def test_existing_active_closed_transitions_still_work():
    storage.set_account_status("acme", "active")
    lifecycle.transition("acme", "closed")
    assert storage.account_status("acme") == "closed"
    lifecycle.transition("acme", "active")
    assert storage.account_status("acme") == "active"
