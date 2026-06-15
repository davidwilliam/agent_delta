"""Public tests for hard_task_002 (suspended state). Injected at score time."""

import pytest

from saasapp import lifecycle, service, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_active_to_suspended():
    lifecycle.transition("acme", "suspended")
    assert storage.account_status("acme") == "suspended"


def test_suspended_cannot_create_project():
    lifecycle.transition("acme", "suspended")
    with pytest.raises(PermissionError):
        service.create_project(storage.get_user("alice"), "New")


def test_existing_active_closed_unchanged():
    lifecycle.transition("acme", "closed")
    assert storage.account_status("acme") == "closed"
    lifecycle.transition("acme", "active")
    assert storage.account_status("acme") == "active"
