"""Hidden tests for hard_task_002 (suspended state). Transitions + side effects."""

import pytest

from saasapp import lifecycle, service, storage
from saasapp.api import handle_list_projects


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_suspended_to_active():
    lifecycle.transition("acme", "suspended")
    lifecycle.transition("acme", "active")
    assert storage.account_status("acme") == "active"


def test_suspended_to_closed():
    lifecycle.transition("acme", "suspended")
    lifecycle.transition("acme", "closed")
    assert storage.account_status("acme") == "closed"


def test_closed_to_suspended_illegal():
    lifecycle.transition("acme", "closed")
    with pytest.raises(ValueError):
        lifecycle.transition("acme", "suspended")


def test_suspended_can_still_view():
    lifecycle.transition("acme", "suspended")
    assert "Roadmap" in handle_list_projects("alice")


def test_transition_is_audited():
    lifecycle.transition("acme", "suspended")
    assert ("acme", "active", "suspended") in storage.AUDIT
