You are working in the `mathkit` Python package repository.

Please add a new `summary` module that turns a list of numbers into a compact
report.

Create `src/mathkit/summary.py` with three functions:

1. `summarize(values)` returns a dict with keys `count`, `mean`, `minimum`,
   `maximum`, and `span` (where `span = maximum - minimum`). Raise `ValueError`
   on empty input.
2. `describe(values)` returns a one-line string of the form
   `"count=3 mean=2.00 min=1 max=3 span=2"` (mean formatted to two decimals).
   Raise `ValueError` on empty input.
3. `top_n(values, n)` returns the `n` largest values in descending order. Return
   an empty list when `n` is 0, the whole sorted list when `n` exceeds the
   length, and raise `ValueError` when `n` is negative.

Reuse existing helpers where it makes sense, add tests as needed, and keep the
change consistent with the existing conventions. When finished, run
`pytest -q tests/` and summarize what you built.
