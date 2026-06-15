"""Baseline tests (must keep passing).

These cover behavior that is already correct at the fixture base: same-tenant
visibility, and the active/closed account lifecycle. The latent bugs (cross-tenant
isolation, ownership, and the missing suspended state) are exercised by the
injected task tests, so the baseline stays green here.
"""

import pytest

from saasapp import lifecycle, service, storage
from saasapp.api import handle_get_project, handle_list_projects


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_member_sees_own_active_project():
    assert "Roadmap" in handle_list_projects("alice")


def test_member_does_not_see_own_archived_project():
    assert "Old Plan" not in handle_list_projects("alice")


def test_admin_sees_own_archived_project():
    assert "Old Plan" in handle_list_projects("admin_acme")


def test_get_own_project():
    assert handle_get_project("alice", "p1") == "Roadmap"


def test_get_missing_project_raises():
    with pytest.raises(KeyError):
        service.get_project(storage.get_user("alice"), "nope")


def test_active_account_can_create():
    project = service.create_project(storage.get_user("alice"), "New")
    assert project.tenant_id == "acme"


def test_closed_account_cannot_create():
    lifecycle.transition("acme", "closed")
    with pytest.raises(PermissionError):
        service.create_project(storage.get_user("alice"), "Nope")


def test_legal_transitions_active_closed():
    lifecycle.transition("acme", "closed")
    assert storage.account_status("acme") == "closed"
    lifecycle.transition("acme", "active")
    assert storage.account_status("acme") == "active"
