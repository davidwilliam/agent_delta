"""Sequence utilities.

NOTE (fixture): `chunk` has an intentional bug - it drops the final partial
chunk when the length is not a multiple of `size`. The AgentDelta task_002 fixes
it. `dedupe` is correct baseline behavior (regression surface).
"""

from collections.abc import Sequence


def chunk(seq: Sequence, size: int) -> list[list]:
    """Split `seq` into consecutive chunks of length `size`."""
    if size <= 0:
        raise ValueError("size must be a positive integer")
    chunks: list[list] = []
    # BUG: stops at len(seq) - size + 1, so a trailing partial chunk is dropped.
    for i in range(0, len(seq) - size + 1, size):
        chunks.append(list(seq[i : i + size]))
    return chunks


def dedupe(seq: Sequence) -> list:
    """Return items with duplicates removed, preserving first-seen order."""
    seen: set = set()
    out: list = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
