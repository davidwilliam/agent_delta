"""Business logic. Both paths below authorize through policy.can_view."""

from saasapp import policy, storage


def list_visible_projects(user):
    """Projects the user is allowed to view."""
    return [p for p in storage.all_projects() if policy.can_view(user, p)]


def get_project(user, project_id):
    """Fetch a single project, enforcing authorization.

    Raises KeyError if it does not exist, PermissionError if not viewable.
    """
    project = storage.find_project(project_id)
    if project is None:
        raise KeyError(project_id)
    if not policy.can_view(user, project):
        raise PermissionError(f"{user.id} may not view {project_id}")
    return project
