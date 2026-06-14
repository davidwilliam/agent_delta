You are working in the `mathkit` Python package repository.

The function `normalize_spaces` in `src/mathkit/textnorm.py` collapses runs of
whitespace to single spaces and strips the ends. It currently has no tests.

Please write a thorough test suite for `normalize_spaces` in a new file under
`tests/` (for example `tests/test_textnorm.py`). Cover the meaningful behaviors:
collapsing multiple spaces, stripping leading and trailing whitespace, handling
tabs and newlines, single words, and empty input.

Do not modify any source files; only add tests. When finished, run
`pytest -q tests/` to confirm your tests pass, and summarize what you covered.
