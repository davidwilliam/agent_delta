"""Baseline tests (must keep passing).

These cover same-tenant behavior only, which the current policy already gets
right. The cross-tenant isolation bug is latent here and is exercised by the
injected task tests, so the baseline stays green at the fixture base.
"""

import pytest

from saasapp import service, storage
from saasapp.api import handle_get_project, handle_list_projects


def test_member_sees_own_active_project():
    names = handle_list_projects("alice")
    assert "Roadmap" in names


def test_member_does_not_see_own_archived_project():
    names = handle_list_projects("alice")
    assert "Old Plan" not in names


def test_admin_sees_own_archived_project():
    names = handle_list_projects("admin_acme")
    assert "Old Plan" in names


def test_get_own_project():
    assert handle_get_project("alice", "p1") == "Roadmap"


def test_get_missing_project_raises():
    with pytest.raises(KeyError):
        service.get_project(storage.get_user("alice"), "nope")
