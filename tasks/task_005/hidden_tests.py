"""Hidden tests for task_005 (fix path traversal). Edge cases."""

import pytest

from mathkit.io import read_fixture


def test_deep_traversal_raises(tmp_path):
    with pytest.raises(ValueError):
        read_fixture(str(tmp_path), "../../../../etc/passwd")


def test_absolute_passwd_raises(tmp_path):
    with pytest.raises(ValueError):
        read_fixture(str(tmp_path), "/etc/passwd")


def test_bare_parent_raises(tmp_path):
    with pytest.raises(ValueError):
        read_fixture(str(tmp_path), "..")


def test_legit_nested_still_reads(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "n.txt").write_text("nested")
    assert read_fixture(str(tmp_path), "sub/n.txt") == "nested"
