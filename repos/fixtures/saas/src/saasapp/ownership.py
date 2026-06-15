"""Ownership checks.

NOTE (fixture): is_owner has a bug -- it compares the user id to the project's
tenant_id instead of its owner_id, so owned-project listing and edit permission
are both wrong. The AgentDelta H2 task fixes the root cause here (used by both
callers), not the symptoms in the service layer.
"""

from saasapp import policy


def is_owner(user, project):
    # BUG: should compare project.owner_id to user.id.
    return project.owner_id == user.tenant_id


def can_edit(user, project):
    """A user may edit a project they own and can view."""
    return policy.can_view(user, project) and is_owner(user, project)
