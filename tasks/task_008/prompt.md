You are working in the `mathkit` Python package repository.

`mathkit.legacy.avg` is a deprecated alias for `mathkit.stats.mean`. The
`average_line` function in `src/mathkit/report.py` still depends on it.

Please migrate off the deprecated helper:
1. Update `average_line` in `report.py` to use `mathkit.stats.mean` instead of
   `mathkit.legacy.avg`.
2. Remove `avg` from `mathkit.legacy`.
3. The observable output of `average_line` must not change.

Keep the change focused. When finished, run `pytest -q tests/` and summarize the
migration.
