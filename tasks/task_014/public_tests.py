"""Public tests for task_014 (calc). Injected at score time."""

from mathkit.calc import calc


def test_precedence():
    assert calc("1 + 2 * 3") == 7


def test_parentheses():
    assert calc("(1+2)*3") == 9


def test_unary_minus():
    assert calc("2*-3") == -6


def test_truncate_toward_zero():
    assert calc("-10/3") == -3


def test_left_associative():
    assert calc(" 7 - 3 - 2 ") == 2
