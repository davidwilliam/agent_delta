"""Authorization policy.

NOTE (fixture): can_view has a tenant-isolation bug -- it enforces the archived
rule but forgets to check that the project belongs to the user's tenant, so a
user can view another tenant's non-archived projects. The AgentDelta hard task
fixes this here (the root cause), not in the api layer.
"""


def can_view(user, project):
    """Whether `user` may view `project`.

    Intended rule: same tenant, and archived projects are visible only to admins.
    """
    # BUG: missing tenant-isolation check (project.tenant_id != user.tenant_id).
    if project.archived and user.role != "admin":
        return False
    return True
