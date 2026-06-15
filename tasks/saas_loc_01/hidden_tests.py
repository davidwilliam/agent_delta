"""Hidden tests for saas_loc_01: other tenants, all-archived, never count archived."""

import pytest

from saasapp import dashboard, storage, usage
from saasapp.models import Project


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_globex_active_count_excludes_archived():
    # globex has p3 (active) and p4 (archived); only p3 should count.
    assert dashboard.project_counts("globex")["active"] == 1


def test_tenant_with_all_archived_projects_counts_zero():
    storage.reset()
    storage.PROJECTS = [
        Project(id="z1", tenant_id="zeta", owner_id="alice", name="A", archived=True),
        Project(id="z2", tenant_id="zeta", owner_id="alice", name="B", archived=True),
    ]
    assert dashboard.project_counts("zeta")["active"] == 0


def test_counts_never_include_archived_projects():
    for tenant in ("acme", "globex"):
        active = usage.active_projects(tenant)
        assert all(not p.archived for p in active)


def test_active_projects_are_scoped_to_tenant():
    assert all(p.tenant_id == "acme" for p in usage.active_projects("acme"))
    assert all(p.tenant_id == "globex" for p in usage.active_projects("globex"))
