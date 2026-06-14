"""Text utilities.

NOTE (fixture): `slugify` is intentionally missing. The AgentDelta task_003 adds
it. `word_count` is correct baseline behavior (regression surface).
"""


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in `text`."""
    return len(text.split())
