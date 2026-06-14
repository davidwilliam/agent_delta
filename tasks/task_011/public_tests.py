"""Public tests for task_011 (roman numerals). Injected at score time."""

from mathkit.roman import int_to_roman, roman_to_int


def test_int_to_roman_basic():
    assert int_to_roman(4) == "IV"
    assert int_to_roman(9) == "IX"
    assert int_to_roman(58) == "LVIII"


def test_roman_to_int_basic():
    assert roman_to_int("IV") == 4
    assert roman_to_int("LVIII") == 58
