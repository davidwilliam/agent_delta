"""Tiny data-file reader.

NOTE (fixture): `read_fixture` is intentionally vulnerable to path traversal - a
`name` containing '..' or an absolute path can escape `base_dir`. The AgentDelta
task_005 hardens it. Normal reads are the baseline behavior (regression surface).
"""

import os


def read_fixture(base_dir: str, name: str) -> str:
    """Read the text file `name` located under `base_dir`."""
    # VULNERABLE: no containment check - `name` can traverse outside base_dir.
    path = os.path.join(base_dir, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
