# Expected behavior - ts_invariant_02

The correct solution adds `applyDiscounts(subtotalCents, discounts)` that folds the
discounts over a running total, clamping the running total to a lower bound of 0
after each step. Percent discounts compound because the amount off is computed
against the current running total via `percentOfCents(runningTotal, value)`; fixed
discounts subtract their cents. An empty list returns the subtotal unchanged.

Why the obvious solution fails:
- A naive implementation computes each discount against the original subtotal, or
  clamps only the final result instead of after each step. Both pass simple visible
  cases but break the running-clamp invariant when discounts stack.
- For example, two fixed discounts of 600 on a subtotal of 1000 must yield 0: the
  first drives the running total to 400, and the second clamps to 0. A final-only
  clamp on independent subtractions would compute 1000 - 600 - 600 = -200 -> 0,
  which happens to match here, but a percent applied to the original subtotal rather
  than the running total diverges (10% then 100 fixed must be 1000 -> 900 -> 800).

Discriminators: stacked percent-then-fixed compounds on the running total (800);
two large fixed discounts clamp to 0; empty list is a no-op; the addition stays in
`discount.ts` and leaves `applyDiscount`, the `Discount` type, and `money.ts`
unchanged.
