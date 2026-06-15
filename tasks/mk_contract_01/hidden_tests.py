"""Hidden tests for mk_contract_01: the legacy alias contract."""

from mathkit.record import to_dict


def test_val_equals_value_for_many_inputs():
    cases = [("a", 0), ("b", -3), ("c", "hello"), ("d", 42), ("e", "")]
    for name, value in cases:
        d = to_dict(name, value)
        assert d["val"] == d["value"] == value


def test_zero_value_alias():
    assert to_dict("z", 0) == {"name": "z", "value": 0, "val": 0}


def test_string_value_alias():
    assert to_dict("s", "ok") == {"name": "s", "value": "ok", "val": "ok"}


def test_keys_are_exactly_name_value_val():
    assert set(to_dict("k", 1).keys()) == {"name", "value", "val"}
