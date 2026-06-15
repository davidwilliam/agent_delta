"""Hidden tests for saas_contract_01: contract consistency and back-compat.

Only valid same-tenant access is used (alice viewing her own project p1), so the
fixture's latent cross-tenant policy/ownership bugs never come into play.
"""

import pytest

from saasapp import api, serialize, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_owner_alias_always_equals_owner():
    p1 = storage.find_project("p1")
    d = serialize.project_to_dict(p1)
    assert d["owner"] == d["owner_id"]


def test_archived_is_bool():
    p1 = storage.find_project("p1")
    d = serialize.project_to_dict(p1)
    assert isinstance(d["archived"], bool)
    assert d["archived"] is False


def test_handler_dict_equals_serializer_dict():
    p1 = storage.find_project("p1")
    assert api.handle_project_detail("alice", "p1") == serialize.project_to_dict(p1)


def test_serialization_preserves_name_and_id():
    p1 = storage.find_project("p1")
    d = serialize.project_to_dict(p1)
    assert d["id"] == p1.id
    assert d["name"] == p1.name


def test_handler_back_compat_alias_in_sync():
    d = api.handle_project_detail("alice", "p1")
    assert d["owner"] == d["owner_id"] == "alice"
