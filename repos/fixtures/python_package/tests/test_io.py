"""Baseline tests for mathkit.io (must keep passing).

Covers normal reads only. Path-traversal hardening is exercised by task_005's
injected tests, so the baseline stays green at the fixture base.
"""

from mathkit.io import read_fixture


def test_read_fixture_reads_file(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("hello\n")
    assert read_fixture(str(tmp_path), "data.txt") == "hello\n"


def test_read_fixture_nested(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "n.txt").write_text("nested")
    assert read_fixture(str(tmp_path), "sub/n.txt") == "nested"
