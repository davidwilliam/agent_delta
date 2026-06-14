"""Reference test suite for normalize_spaces (kills all task_006 mutants)."""

from mathkit.textnorm import normalize_spaces


def test_collapses_multiple_spaces():
    assert normalize_spaces("a   b") == "a b"


def test_strips_ends():
    assert normalize_spaces("  hi  ") == "hi"


def test_handles_tabs_and_newlines():
    assert normalize_spaces("a\t\nb") == "a b"


def test_single_word():
    assert normalize_spaces("hello") == "hello"


def test_empty_string():
    assert normalize_spaces("") == ""
