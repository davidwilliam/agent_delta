Follow this process for the `pricingkit` discount fix:

1. Read `src/discount.ts` and `src/money.ts` and identify how `applyDiscount`
   computes the total.
2. State the invariant the total must satisfy.
3. Make the smallest change to `applyDiscount` that enforces it.
4. Run `npm run build`, then `node --test tests/*.test.mjs`.
5. If anything fails, debug once and re-run.
6. Review your diff against the invariant and confirm `money.ts` is untouched.
