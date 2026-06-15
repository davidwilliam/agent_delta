"""Public tests for mk_contract_01 (one failing case + one regression guard)."""

from mathkit.record import to_dict


def test_val_mirrors_value():
    # Fails at base: the legacy "val" alias is wired to None instead of value.
    assert to_dict("x", 5) == {"name": "x", "value": 5, "val": 5}


def test_name_and_value_are_set():
    # The name and value fields themselves are populated correctly at base.
    d = to_dict("x", 5)
    assert d["name"] == "x"
    assert d["value"] == 5
