from saasapp import storage

_TOKENS = {}


def reset():
    _TOKENS.clear()


def create_share(project_id):
    token = "tok-" + project_id
    _TOKENS[token] = project_id
    return token


def access_via_token(user, token):
    project_id = _TOKENS.get(token)
    if project_id is None:
        raise KeyError(token)
    project = storage.find_project(project_id)
    if project is None or user.tenant_id != project.tenant_id:
        raise PermissionError("token is scoped to another tenant")
    return project
