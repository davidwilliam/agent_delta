"""Public tests for saas_state_01 (visible trial happy path + one inbound guard)."""

import pytest

from saasapp import lifecycle, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_trial_to_active_succeeds():
    storage.set_account_status("acme", "trial")
    lifecycle.transition("acme", "active")
    assert storage.account_status("acme") == "active"


def test_active_to_trial_is_illegal():
    storage.set_account_status("acme", "active")
    with pytest.raises(ValueError):
        lifecycle.transition("acme", "trial")
