"""Text utilities (reference solution for task_003)."""

import re


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in `text`."""
    return len(text.split())


def slugify(text: str) -> str:
    """Return a lowercase, hyphen-separated slug of `text`."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
