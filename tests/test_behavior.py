"""Unit tests for agent-behavior extraction from the transcript event stream."""

from types import SimpleNamespace as SN

from agent_delta.scoring.behavior import classify_tool, extract_agent_behavior


def test_classify_tool_variants():
    assert classify_tool("bash", {"cmd": "ls"}) == "shell"
    assert classify_tool("Read", {"file": "x"}) == "read"
    assert classify_tool("Edit", {}) == "edit"
    assert classify_tool("Write", {}) == "edit"
    # Editor-style tools route on their command argument.
    assert classify_tool("str_replace_based_edit_tool", {"command": "view"}) == "read"
    assert classify_tool("str_replace_based_edit_tool", {"command": "str_replace"}) == "edit"
    assert classify_tool("Glob", {}) == "other"


def test_extract_counts():
    sample = SN(events=[
        SN(event="model", retries=0, error=None),
        SN(event="model", retries=2, error=None),
        SN(event="tool", function="bash", arguments={"cmd": "pytest -q tests/"}, failed=False, error=None),
        SN(event="tool", function="bash", arguments={"command": "ls -la"}, failed=True, error="boom"),
        SN(event="tool", function="Read", arguments={"file": "a.py"}),
        SN(event="tool", function="str_replace_based_edit_tool", arguments={"command": "str_replace"}),
        SN(event="tool", function="str_replace_based_edit_tool", arguments={"command": "view"}),
        SN(event="tool", function="Edit", arguments={}),
        SN(event="info"),  # ignored
    ])
    b = extract_agent_behavior(sample)
    assert b["api_calls"] == 2
    assert b["retry_count"] == 2
    assert b["tool_calls"] == 6
    assert b["shell_commands"] == 2
    assert b["test_runs"] == 1           # only the pytest command
    assert b["failed_shell_commands"] == 1
    assert b["files_read"] == 2          # Read + editor view
    assert b["file_edits"] == 2          # str_replace + Edit
    assert b["tool_histogram"]["bash"] == 2


def test_extract_empty():
    b = extract_agent_behavior(SN(events=[]))
    assert b["tool_calls"] == 0 and b["api_calls"] == 0
    assert b["review_passes"] is None


def test_test_command_detection_negative():
    sample = SN(events=[
        SN(event="tool", function="bash", arguments={"cmd": "echo testing the waters"},
           failed=False, error=None),
    ])
    # "testing" should not count as a test run.
    assert extract_agent_behavior(sample)["test_runs"] == 0
