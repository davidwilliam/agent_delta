"""Business logic (reference solution for hard_task_002).

create_project now blocks any non-active account (closed and suspended).
"""

from saasapp import ownership, policy, storage
from saasapp.models import Project


def list_visible_projects(user):
    return [p for p in storage.all_projects() if policy.can_view(user, p)]


def get_project(user, project_id):
    project = storage.find_project(project_id)
    if project is None:
        raise KeyError(project_id)
    if not policy.can_view(user, project):
        raise PermissionError(f"{user.id} may not view {project_id}")
    return project


def list_owned_projects(user):
    return [p for p in storage.all_projects()
            if ownership.is_owner(user, p) and policy.can_view(user, p)]


def can_user_edit(user, project_id):
    project = storage.find_project(project_id)
    if project is None:
        raise KeyError(project_id)
    return ownership.can_edit(user, project)


def create_project(user, name):
    """Create a project; only active accounts may create."""
    if storage.account_status(user.tenant_id) != "active":
        raise PermissionError("only active accounts can create projects")
    project = Project(id=storage.next_project_id(), tenant_id=user.tenant_id,
                      owner_id=user.id, name=name, archived=False)
    storage.add_project(project)
    return project
