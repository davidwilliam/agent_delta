"""Hidden tests for task_011 (roman numerals). Subtractive + round-trip + bounds."""

import pytest

from mathkit.roman import int_to_roman, roman_to_int


def test_subtractive_tens_hundreds():
    assert int_to_roman(40) == "XL"
    assert int_to_roman(90) == "XC"
    assert int_to_roman(400) == "CD"
    assert int_to_roman(900) == "CM"


def test_large_composites():
    assert int_to_roman(1994) == "MCMXCIV"
    assert int_to_roman(3888) == "MMMDCCCLXXXVIII"
    assert roman_to_int("MCMXCIV") == 1994


def test_round_trip():
    for n in (1, 3, 49, 944, 2023, 3999):
        assert roman_to_int(int_to_roman(n)) == n


def test_out_of_range_raises():
    with pytest.raises(ValueError):
        int_to_roman(0)
    with pytest.raises(ValueError):
        int_to_roman(4000)
