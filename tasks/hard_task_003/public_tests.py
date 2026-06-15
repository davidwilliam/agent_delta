"""Public tests for hard_task_003 (ownership root cause). Injected at score time."""

from saasapp import service, storage


def test_owner_sees_owned_project():
    names = [p.name for p in service.list_owned_projects(storage.get_user("alice"))]
    assert "Roadmap" in names


def test_owner_can_edit_own_project():
    assert service.can_user_edit(storage.get_user("alice"), "p1") is True


def test_non_owner_cannot_edit():
    # bob is in another tenant and does not own p1.
    assert service.can_user_edit(storage.get_user("bob"), "p1") is False
