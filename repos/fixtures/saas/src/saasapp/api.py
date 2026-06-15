"""Request handlers (the controller layer).

These delegate authorization to the service/policy layers. Patching tenant
filtering here would fix listing but miss the single-project path, so the real
fix belongs in the policy layer.
"""

from saasapp import service, storage


def handle_list_projects(user_id):
    user = storage.get_user(user_id)
    return [p.name for p in service.list_visible_projects(user)]


def handle_get_project(user_id, project_id):
    user = storage.get_user(user_id)
    return service.get_project(user, project_id).name
