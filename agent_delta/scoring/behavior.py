"""Extract agent-behavior counts from an Inspect sample transcript.

Feeds the Agentic Work Index and the tool/retry/test amplification ratios
(SPEC-ADDENDUM 6). Counts model calls, tool calls, shell commands, test runs,
file reads, and file edits from the sample's event stream.

The exact tool names an agent emits (Bash, Read, Edit, str_replace_editor, ...)
vary by agent and version, so classification is pattern-based and the raw
tool-name histogram is also returned, letting the patterns be tuned from a real
transcript without guessing. Events are read duck-typed via their `.event` tag
so this is testable without constructing full Inspect event objects.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

# Test-runner invocations, matched against the shell command text.
_TEST_CMD = re.compile(
    r"\b(pytest|py\.test|python\s+-m\s+(pytest|unittest)|unittest|tox|nox|"
    r"npm\s+(run\s+)?test|yarn\s+test|pnpm\s+test|jest|vitest|mocha|"
    r"go\s+test|cargo\s+test|rspec|bundle\s+exec\s+rspec|ctest|gradle\s+test|"
    r"mvn\s+test|dotnet\s+test)\b",
    re.IGNORECASE,
)

_SHELL = {"bash", "shell", "sh", "run", "execute", "exec", "terminal"}
_READ = {"read", "read_file", "view", "cat", "open", "viewfile"}
_EDIT = {
    "edit", "write", "write_file", "create", "create_file", "str_replace",
    "str_replace_editor", "str_replace_based_edit_tool", "multiedit", "multi_edit",
    "apply_patch", "patch", "insert", "notebookedit",
}
_CMD_KEYS = ("cmd", "command", "input", "code", "script")


def _command_text(args: dict[str, Any]) -> str:
    for key in _CMD_KEYS:
        if key in args and args[key]:
            v = args[key]
            return " ".join(map(str, v)) if isinstance(v, (list, tuple)) else str(v)
    return ""


def classify_tool(function: str, args: dict[str, Any]) -> str:
    """Return one of: shell, read, edit, other."""
    fn = (function or "").lower()
    # Editor-style tools carry the real action in a `command` argument.
    if "editor" in fn or "text_editor" in fn or fn.endswith("edit_tool"):
        cmd = str(args.get("command", "")).lower()
        if cmd in ("view", "read"):
            return "read"
        if cmd:
            return "edit"
        return "edit"
    if fn in _SHELL or "bash" in fn or "shell" in fn:
        return "shell"
    if fn in _READ or fn.startswith("read") or "view" in fn:
        return "read"
    if fn in _EDIT or "edit" in fn or "write" in fn or "str_replace" in fn or "patch" in fn:
        return "edit"
    return "other"


def extract_agent_behavior(sample: Any) -> dict[str, Any]:
    """Count agent behavior from an Inspect EvalSample's event stream."""
    events = getattr(sample, "events", None) or []
    api_calls = tool_calls = shell_commands = test_runs = 0
    files_read = file_edits = failed_shell = retry_count = model_errors = 0
    histogram: Counter = Counter()

    for ev in events:
        kind = getattr(ev, "event", None)
        if kind == "model":
            api_calls += 1
            retry_count += int(getattr(ev, "retries", 0) or 0)
            if getattr(ev, "error", None):
                model_errors += 1
        elif kind == "tool":
            tool_calls += 1
            fn = getattr(ev, "function", "") or ""
            histogram[fn.lower()] += 1
            args = getattr(ev, "arguments", None) or {}
            cat = classify_tool(fn, args)
            if cat == "shell":
                shell_commands += 1
                cmd = _command_text(args)
                if _TEST_CMD.search(cmd):
                    test_runs += 1
                if getattr(ev, "failed", False) or getattr(ev, "error", None):
                    failed_shell += 1
            elif cat == "read":
                files_read += 1
            elif cat == "edit":
                file_edits += 1

    return {
        "api_calls": api_calls,
        "tool_calls": tool_calls,
        "shell_commands": shell_commands,
        "failed_shell_commands": failed_shell,
        "test_runs": test_runs,
        "files_read": files_read,
        "file_edits": file_edits,
        "retry_count": retry_count,
        "model_errors": model_errors,
        # review_passes has no discrete transcript signal yet.
        "review_passes": None,
        "tool_histogram": dict(histogram),
    }
