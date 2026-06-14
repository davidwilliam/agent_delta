"""Sequence utilities (reference solution for task_002)."""

from collections.abc import Sequence


def chunk(seq: Sequence, size: int) -> list[list]:
    """Split `seq` into consecutive chunks of length `size`."""
    if size <= 0:
        raise ValueError("size must be a positive integer")
    return [list(seq[i : i + size]) for i in range(0, len(seq), size)]


def dedupe(seq: Sequence) -> list:
    """Return items with duplicates removed, preserving first-seen order."""
    seen: set = set()
    out: list = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
