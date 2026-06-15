"""Hidden tests for hard_task_001 (tenant isolation). Invariant + admin scope."""

import pytest

from saasapp import service, storage
from saasapp.api import handle_list_projects


def test_admin_is_tenant_scoped_in_list():
    # An acme admin must not see any globex project, archived or not.
    names = handle_list_projects("admin_acme")
    assert "Secret" not in names and "Globex Archive" not in names


def test_admin_cannot_fetch_other_tenant_project():
    with pytest.raises(PermissionError):
        service.get_project(storage.get_user("admin_acme"), "p3")


def test_archived_rule_preserved():
    # Member does not see own archived; admin does (same tenant).
    assert "Old Plan" not in handle_list_projects("alice")
    assert "Old Plan" in handle_list_projects("admin_acme")


def test_tenant_isolation_invariant():
    # Every visible project must belong to the viewer's tenant.
    for user_id in ("alice", "bob", "admin_acme"):
        user = storage.get_user(user_id)
        for project in service.list_visible_projects(user):
            assert project.tenant_id == user.tenant_id


def test_member_cannot_fetch_other_tenant_archived():
    with pytest.raises(PermissionError):
        service.get_project(storage.get_user("alice"), "p4")  # globex archived
