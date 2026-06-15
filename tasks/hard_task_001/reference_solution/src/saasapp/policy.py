"""Authorization policy (reference solution for hard_task_001)."""


def can_view(user, project):
    """Whether `user` may view `project`.

    Rule: same tenant, and archived projects are visible only to admins.
    """
    if project.tenant_id != user.tenant_id:
        return False
    if project.archived and user.role != "admin":
        return False
    return True
