"""Public tests for mk_minimal_01 (one failing case + one regression guard)."""

from mathkit.csvlite import parse_row


def test_quoted_comma_is_one_field():
    # Fails at base: the naive split breaks the quoted field on its inner comma.
    assert parse_row('a,"b,c",d') == ["a", "b,c", "d"]


def test_plain_row_still_splits():
    # Passes at base: regression guard for the simple unquoted case.
    assert parse_row("a,b,c") == ["a", "b", "c"]
