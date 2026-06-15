"""Hidden tests for task_012 (simplify_path). Deeper edge cases."""

from mathkit.paths import simplify_path


def test_many_dotdot_past_root():
    assert simplify_path("/a/../../b/../c//.//") == "/c"


def test_trailing_dot():
    assert simplify_path("/a/b/.") == "/a/b"


def test_dotdot_chain():
    assert simplify_path("/x/y/z/../../w") == "/x/w"


def test_only_dots_segments():
    assert simplify_path("/././.") == "/"


def test_name_with_dots_preserved():
    assert simplify_path("/a/.../b") == "/a/.../b"


def test_no_trailing_slash():
    assert simplify_path("/foo/bar/") == "/foo/bar"
