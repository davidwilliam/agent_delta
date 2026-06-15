"""In-memory seed data. Do not change the seed in tasks; tests rely on it."""

from saasapp.models import Project, User

USERS = {
    "alice": User(id="alice", tenant_id="acme", role="member"),
    "admin_acme": User(id="admin_acme", tenant_id="acme", role="admin"),
    "bob": User(id="bob", tenant_id="globex", role="member"),
}

PROJECTS = [
    Project(id="p1", tenant_id="acme", owner_id="alice", name="Roadmap", archived=False),
    Project(id="p2", tenant_id="acme", owner_id="alice", name="Old Plan", archived=True),
    Project(id="p3", tenant_id="globex", owner_id="bob", name="Secret", archived=False),
    Project(id="p4", tenant_id="globex", owner_id="bob", name="Globex Archive", archived=True),
]


def all_projects():
    return list(PROJECTS)


def find_project(project_id):
    for p in PROJECTS:
        if p.id == project_id:
            return p
    return None


def get_user(user_id):
    return USERS[user_id]
