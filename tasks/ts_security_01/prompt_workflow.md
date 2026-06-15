Follow this process for the `pricingkit` input-validation fix:

1. Read `src/discount.ts` and `src/money.ts` and identify how `applyDiscount`
   uses `subtotalCents` and the `discount` fields.
2. List the adversarial inputs that currently slip through: NaN, Infinity, a
   non-integer or negative `subtotalCents`, a non-integer or negative fixed
   `cents`, and a negative percent `value`.
3. ADD guards at the top of `applyDiscount` that throw an `Error` for each
   invalid case, leaving the existing computation and valid-input results
   unchanged.
4. Run `npm run build`, then `node --test tests/*.test.mjs`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm valid inputs still return the same numbers and the
   `Discount` type is untouched.
