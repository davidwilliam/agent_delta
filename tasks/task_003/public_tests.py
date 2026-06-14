"""Public tests for task_003 (add slugify). Injected at score time."""

from mathkit import slugify as slugify_pkg
from mathkit.text import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_lowercases():
    assert slugify("UPPER") == "upper"


def test_slugify_collapses_spaces():
    assert slugify("  Multiple   Spaces ") == "multiple-spaces"


def test_slugify_exported_from_package():
    assert slugify_pkg("Hello World") == "hello-world"
