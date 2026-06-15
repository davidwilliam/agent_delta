"""Public tests for task_012 (simplify_path). Injected at score time."""

from mathkit.paths import simplify_path


def test_dot_and_dotdot():
    assert simplify_path("/a/./b/../../c/") == "/c"


def test_cannot_go_above_root():
    assert simplify_path("/../") == "/"


def test_collapse_slashes():
    assert simplify_path("/home//foo/") == "/home/foo"


def test_triple_dot_is_a_name():
    assert simplify_path("/...") == "/..."


def test_root():
    assert simplify_path("/") == "/"
