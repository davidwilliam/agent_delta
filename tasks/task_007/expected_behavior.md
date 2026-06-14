# Expected behavior - task_007

Create `src/mathkit/summary.py` with `summarize`, `describe`, and `top_n` (see the
reference solution). Key discriminators:

- `summarize` returns all five keys with `span = maximum - minimum`; empty input
  raises `ValueError`.
- `describe` formats the mean to two decimals (`mean=1.50`).
- `top_n` is descending, clamps `n > len`, returns `[]` for `n == 0`, and raises
  `ValueError` for negative `n`.
