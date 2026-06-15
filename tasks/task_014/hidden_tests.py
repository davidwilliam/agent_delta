"""Hidden tests for task_014 (calc). Deeper edge cases."""

from mathkit.calc import calc


def test_nested_parens():
    assert calc("2*(3+(4-1))") == 12


def test_positive_truncation():
    assert calc("10/3") == 3


def test_negative_truncation_in_expression():
    assert calc("1 + -10/3") == -2  # -10/3 -> -3, then 1 + (-3)


def test_chained_division():
    assert calc("100/3/3") == 11  # (100/3=33) / 3 = 11


def test_leading_unary():
    assert calc("-(2+3)*2") == -10


def test_deep_nesting():
    assert calc("((((5))))") == 5
