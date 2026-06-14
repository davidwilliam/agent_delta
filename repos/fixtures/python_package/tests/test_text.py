"""Baseline tests for mathkit.text (must keep passing)."""

from mathkit.text import word_count


def test_word_count_basic():
    assert word_count("a b c") == 3


def test_word_count_empty():
    assert word_count("") == 0


def test_word_count_collapses_whitespace():
    assert word_count("  hello   world ") == 2
