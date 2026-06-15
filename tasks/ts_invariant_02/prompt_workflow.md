Follow this process to add `applyDiscounts` to `pricingkit`:

1. Read `src/discount.ts` and `src/money.ts`. Note how `applyDiscount` computes
   the amount off and how `percentOfCents` works.
2. State the invariant: the running total must stay at or above 0 after every
   discount in the list.
3. Add `applyDiscounts(subtotalCents, discounts)` that folds the discounts over a
   running total, clamping with `Math.max(0, ...)` after each step. Percent
   discounts apply to the current running total; fixed discounts subtract their
   cents. An empty list returns the subtotal.
4. Leave `applyDiscount` and the `Discount` type unchanged.
5. Run `npm run build`, then `node --test tests/*.test.mjs`.
6. If anything fails, debug once and re-run.
7. Review your diff and confirm `money.ts` is untouched.
