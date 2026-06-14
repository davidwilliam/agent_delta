You are working in the `mathkit` Python package repository.

Please add a `median` function to the statistics module.

Requirements:
1. Add a `median(values)` function in `src/mathkit/stats.py`.
2. For an odd number of values, return the middle value.
3. For an even number of values, return the average of the two middle values.
4. The input may be unsorted; sort it as needed.
5. Raise `ValueError` if the input is empty (match the style of the existing functions).
6. Export `median` from the `mathkit` package so `from mathkit import median` works.
7. Keep the change minimal and consistent with existing conventions.
8. Do not modify unrelated behavior.

When finished, run the existing test suite (`pytest -q tests/`) to confirm nothing is broken, and summarize what you changed.
