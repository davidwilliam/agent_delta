"""Hidden tests for hard_task_003 (ownership root cause).

can_user_edit shares the buggy helper with list_owned_projects, so a service-only
patch of the listing leaves these failing.
"""

from saasapp import service, storage


def test_other_owner_can_edit_own():
    # bob owns the globex project p3 and should be able to edit it.
    assert service.can_user_edit(storage.get_user("bob"), "p3") is True


def test_other_owner_sees_owned():
    names = [p.name for p in service.list_owned_projects(storage.get_user("bob"))]
    assert "Secret" in names


def test_owner_does_not_own_foreign_project():
    names = [p.name for p in service.list_owned_projects(storage.get_user("alice"))]
    assert "Secret" not in names


def test_ownership_invariant():
    for user_id in ("alice", "bob"):
        user = storage.get_user(user_id)
        for project in service.list_owned_projects(user):
            assert project.owner_id == user.id
