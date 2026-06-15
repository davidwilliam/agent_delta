"""Ownership checks (reference solution for hard_task_003)."""

from saasapp import policy


def is_owner(user, project):
    return project.owner_id == user.id


def can_edit(user, project):
    """A user may edit a project they own and can view."""
    return policy.can_view(user, project) and is_owner(user, project)
