"""Hidden tests for mk_minimal_01: quoting rules and edge cases."""

from mathkit.csvlite import parse_row


def test_quoted_comma_kept_in_field():
    assert parse_row('"hello, world",ok') == ["hello, world", "ok"]


def test_surrounding_quotes_are_stripped():
    assert parse_row('"a","b"') == ["a", "b"]


def test_doubled_quote_is_literal():
    assert parse_row('"x""y"') == ['x"y']


def test_empty_quoted_field():
    assert parse_row('a,"",b') == ["a", "", "b"]


def test_trailing_empty_field():
    assert parse_row("a,b,") == ["a", "b", ""]


def test_leading_and_trailing_space_preserved():
    assert parse_row("a, b ,c") == ["a", " b ", "c"]


def test_empty_line_is_single_empty_field():
    assert parse_row("") == [""]


def test_plain_row_regression():
    assert parse_row("a,b,c") == ["a", "b", "c"]
