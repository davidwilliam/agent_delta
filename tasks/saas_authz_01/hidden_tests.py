"""Hidden tests for saas_authz_01: unknown token, admin, both-direction denial."""

import pytest

from saasapp import sharing, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    sharing.reset()
    yield
    storage.reset()
    sharing.reset()


def test_unknown_token_raises_keyerror():
    alice = storage.get_user("alice")
    with pytest.raises(KeyError):
        sharing.access_via_token(alice, "tok-does-not-exist")


def test_admin_in_tenant_can_access_token():
    admin = storage.get_user("admin_acme")  # acme admin
    token = sharing.create_share("p1")  # acme project
    assert sharing.access_via_token(admin, token).id == "p1"


def test_cross_tenant_denied_both_directions():
    alice = storage.get_user("alice")  # acme
    bob = storage.get_user("bob")  # globex

    acme_token = sharing.create_share("p1")  # acme project
    globex_token = sharing.create_share("p3")  # globex project

    # acme user cannot use a globex token
    with pytest.raises(PermissionError):
        sharing.access_via_token(alice, globex_token)
    # globex user cannot use an acme token
    with pytest.raises(PermissionError):
        sharing.access_via_token(bob, acme_token)


def test_same_tenant_returns_the_right_project():
    bob = storage.get_user("bob")  # globex
    token = sharing.create_share("p3")  # globex project
    project = sharing.access_via_token(bob, token)
    assert project.id == "p3"
    assert project.tenant_id == bob.tenant_id
