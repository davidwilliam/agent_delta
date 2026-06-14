"""Public tests for task_005 (fix path traversal). Injected at score time."""

import pytest

from mathkit.io import read_fixture


def test_normal_read_still_works(tmp_path):
    (tmp_path / "data.txt").write_text("hello\n")
    assert read_fixture(str(tmp_path), "data.txt") == "hello\n"


def test_parent_traversal_raises(tmp_path):
    (tmp_path.parent / "secret.txt").write_text("top secret")
    with pytest.raises(ValueError):
        read_fixture(str(tmp_path), "../secret.txt")


def test_absolute_path_raises(tmp_path):
    with pytest.raises(ValueError):
        read_fixture(str(tmp_path), "/etc/hostname")
