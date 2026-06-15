"""Public tests for saas_authz_01 (visible: same-tenant ok, cross-tenant denied)."""

import pytest

from saasapp import sharing, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    sharing.reset()
    yield
    storage.reset()
    sharing.reset()


def test_owner_in_tenant_can_access_token():
    alice = storage.get_user("alice")  # acme
    token = sharing.create_share("p1")  # p1 belongs to acme
    project = sharing.access_via_token(alice, token)
    assert project.id == "p1"


def test_cross_tenant_user_is_denied():
    bob = storage.get_user("bob")  # globex
    token = sharing.create_share("p1")  # p1 belongs to acme
    with pytest.raises(PermissionError):
        sharing.access_via_token(bob, token)
