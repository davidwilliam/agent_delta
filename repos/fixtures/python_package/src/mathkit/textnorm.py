"""Whitespace normalization (AgentDelta fixture).

`normalize_spaces` is correct but intentionally under-tested: the test_writing
task asks the agent to write thorough tests for it, and the scorer mutates this
file to check the tests actually catch bugs.
"""


def normalize_spaces(s: str) -> str:
    """Collapse runs of whitespace to single spaces and strip the ends."""
    return " ".join(s.split())
