You are working in the `mathkit` Python package repository.

Please add a new module `src/mathkit/wildcard.py` with `is_match(text, pattern)`
that returns whether `text` matches `pattern` in full (the entire text must match
the entire pattern).

The pattern may contain two wildcards:
- `?` matches any single character.
- `*` matches any sequence of characters, including the empty sequence.

All other characters match themselves. Handle multiple `*` in a row, an empty
text, and an empty pattern.

Examples: `is_match("abc", "a*c")` is True; `is_match("abc", "a?c")` is True;
`is_match("", "*")` is True; `is_match("", "?")` is False;
`is_match("adceb", "*a*b")` is True; `is_match("acdcb", "a*c?b")` is False.

Keep the change minimal. Add tests as needed, run `pytest -q tests/`, and
summarize.
