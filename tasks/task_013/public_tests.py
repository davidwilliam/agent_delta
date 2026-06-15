"""Public tests for task_013 (wildcard is_match). Injected at score time."""

from mathkit.wildcard import is_match


def test_star_and_question():
    assert is_match("abc", "a*c") is True
    assert is_match("abc", "a?c") is True


def test_star_matches_empty():
    assert is_match("", "*") is True
    assert is_match("ac", "a*c") is True


def test_question_needs_a_char():
    assert is_match("", "?") is False


def test_classic_cases():
    assert is_match("adceb", "*a*b") is True
    assert is_match("acdcb", "a*c?b") is False
