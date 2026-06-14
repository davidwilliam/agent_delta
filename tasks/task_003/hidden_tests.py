"""Hidden tests for task_003 (add slugify). Edge cases."""

from mathkit.text import slugify


def test_slugify_collapses_repeated_separators():
    assert slugify("a--b__c") == "a-b-c"


def test_slugify_strips_edge_hyphens():
    assert slugify("---Foo---") == "foo"


def test_slugify_all_separators_is_empty():
    assert slugify("!!!") == ""


def test_slugify_keeps_digits():
    assert slugify("Version 2 Release") == "version-2-release"


def test_slugify_already_slug():
    assert slugify("already-slug") == "already-slug"
