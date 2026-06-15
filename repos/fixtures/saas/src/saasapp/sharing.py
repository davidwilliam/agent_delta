from saasapp import storage

_TOKENS = {}


def reset():
    _TOKENS.clear()


def create_share(project_id):
    token = "tok-" + project_id
    _TOKENS[token] = project_id
    return token


def access_via_token(user, token):
    # BUG: does not verify the user's tenant; allows cross-tenant access
    project_id = _TOKENS.get(token)
    if project_id is None:
        raise KeyError(token)
    return storage.find_project(project_id)
