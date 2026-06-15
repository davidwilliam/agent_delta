Fix the off-by-one bug in `payments.proration`.

Context:
- `proration(amount, days_used, days_total)` should return
  `amount * days_used // days_total` (integer floor division).
- It currently divides by `days_total - 1`, which overstates the result.

Requirements:
1. Correct the denominator so it is `days_total`, not `days_total - 1`.
2. Make the smallest possible change. This is a one-token fix: do not rewrite the
   function, do not add new functions, and do not change the floor division operator.
3. Do not weaken or skip tests.

After the fix:
- proration(1000, 15, 30) == 500
- proration(1000, 30, 30) == 1000
- proration(1000, 0, 30) == 0

When finished, run `pytest -q tests/`.
