You are working in the `mathkit` Python package repository.

Please add a new module `src/mathkit/intervals.py` with a function
`merge_intervals(intervals)`:

- `intervals` is a list of `[start, end]` pairs.
- Merge all overlapping intervals. Intervals that merely touch (for example
  `[1, 3]` and `[3, 5]`) should also be merged into `[1, 5]`.
- The input may be unsorted and may contain nested intervals (for example
  `[1, 10]` and `[2, 3]`).
- Return the merged intervals sorted by start. Return an empty list for empty
  input.

Keep the change minimal and consistent with the existing conventions. Add tests
as needed, run `pytest -q tests/`, and summarize what you handled.
