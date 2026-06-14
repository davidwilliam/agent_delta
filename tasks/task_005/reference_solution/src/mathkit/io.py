"""Tiny data-file reader (reference solution for task_005)."""

import os


def read_fixture(base_dir: str, name: str) -> str:
    """Read the text file `name` located under `base_dir` (containment-checked)."""
    base = os.path.realpath(base_dir)
    path = os.path.realpath(os.path.join(base, name))
    if path != base and not path.startswith(base + os.sep):
        raise ValueError(f"unsafe path: {name!r} escapes the base directory")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
