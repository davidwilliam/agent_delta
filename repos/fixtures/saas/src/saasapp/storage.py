"""In-memory seed data and mutable state. Do not change the seed in tasks.

State (account statuses, projects, audit log) is mutable; tests reset it via
reset() in an autouse fixture so they stay independent.
"""

from saasapp.models import Project, User

USERS = {
    "alice": User(id="alice", tenant_id="acme", role="member"),
    "admin_acme": User(id="admin_acme", tenant_id="acme", role="admin"),
    "bob": User(id="bob", tenant_id="globex", role="member"),
}

_SEED_PROJECTS = [
    Project(id="p1", tenant_id="acme", owner_id="alice", name="Roadmap", archived=False),
    Project(id="p2", tenant_id="acme", owner_id="alice", name="Old Plan", archived=True),
    Project(id="p3", tenant_id="globex", owner_id="bob", name="Secret", archived=False),
    Project(id="p4", tenant_id="globex", owner_id="bob", name="Globex Archive", archived=True),
]
_SEED_ACCOUNTS = {"acme": "active", "globex": "active"}

PROJECTS = list(_SEED_PROJECTS)
ACCOUNT_STATUS = dict(_SEED_ACCOUNTS)
AUDIT = []  # list of (tenant_id, from_status, to_status)


def reset():
    """Restore mutable state to the seed (for test isolation)."""
    global PROJECTS, ACCOUNT_STATUS, AUDIT
    PROJECTS = list(_SEED_PROJECTS)
    ACCOUNT_STATUS = dict(_SEED_ACCOUNTS)
    AUDIT = []


def all_projects():
    return list(PROJECTS)


def find_project(project_id):
    for p in PROJECTS:
        if p.id == project_id:
            return p
    return None


def add_project(project):
    PROJECTS.append(project)


def next_project_id():
    return f"p{len(PROJECTS) + 1}"


def get_user(user_id):
    return USERS[user_id]


def account_status(tenant_id):
    return ACCOUNT_STATUS[tenant_id]


def set_account_status(tenant_id, status):
    ACCOUNT_STATUS[tenant_id] = status
