"""Hidden tests for task_013 (wildcard is_match). Deeper edge cases."""

from mathkit.wildcard import is_match


def test_only_stars_match_anything():
    assert is_match("anything", "******") is True
    assert is_match("", "******") is True


def test_full_string_required():
    assert is_match("aa", "a") is False
    assert is_match("aaa", "a*a") is True


def test_question_runs():
    assert is_match("abc", "???") is True
    assert is_match("ab", "???") is False


def test_mixed_wildcards():
    assert is_match("mississippi", "m*ss*?p*i") is True
    assert is_match("xaylmz", "x?y*z") is True


def test_empty_pattern():
    assert is_match("", "") is True
    assert is_match("a", "") is False
