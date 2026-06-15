"""Public tests for hard_task_001 (tenant isolation). Injected at score time.

Includes the direct-fetch case, so a controller-list-only patch (the distractor)
fails here, not just in the hidden tests.
"""

import pytest

from saasapp import service, storage
from saasapp.api import handle_list_projects


def test_member_does_not_see_other_tenant_in_list():
    assert "Secret" not in handle_list_projects("alice")  # Secret is a globex project


def test_member_cannot_fetch_other_tenant_project():
    with pytest.raises(PermissionError):
        service.get_project(storage.get_user("alice"), "p3")  # p3 is globex


def test_member_still_sees_own_active_project():
    assert "Roadmap" in handle_list_projects("alice")


def test_other_member_sees_own_not_foreign():
    names = handle_list_projects("bob")
    assert "Secret" in names and "Roadmap" not in names
