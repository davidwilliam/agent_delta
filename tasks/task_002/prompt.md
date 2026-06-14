You are working in the `mathkit` Python package repository.

There is a bug in `chunk()` in `src/mathkit/sequences.py`. When the input length
is not an exact multiple of `size`, the final partial chunk is silently dropped.

For example, `chunk([1, 2, 3, 4, 5], 2)` currently returns `[[1, 2], [3, 4]]`,
losing the trailing `[5]`.

Please fix `chunk` so that:
1. The final partial chunk is included when the length is not a multiple of size.
2. `chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]`.
3. A size larger than the sequence returns a single chunk containing all items.
4. Evenly divisible inputs still produce equal-sized chunks.
5. A non-positive `size` still raises `ValueError`.

Keep the change minimal and consistent with existing conventions. When finished,
run `pytest -q tests/` and summarize what you changed.
