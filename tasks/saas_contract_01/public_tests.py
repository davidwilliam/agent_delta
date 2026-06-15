"""Public tests for saas_contract_01 (visible serialization contract).

Only valid same-tenant access is used (alice viewing her own project p1).
"""

import pytest

from saasapp import api, serialize, storage


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_serialize_has_full_contract():
    p1 = storage.find_project("p1")
    d = serialize.project_to_dict(p1)
    assert set(d) == {"id", "name", "tenant", "owner", "owner_id", "archived"}
    assert d["id"] == "p1"
    assert d["name"] == "Roadmap"
    assert d["tenant"] == "acme"
    assert d["owner"] == "alice"
    assert d["owner_id"] == "alice"


def test_api_handler_matches_serializer():
    p1 = storage.find_project("p1")
    expected = serialize.project_to_dict(p1)
    assert api.handle_project_detail("alice", "p1") == expected
