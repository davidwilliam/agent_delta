In the `pricingkit` TypeScript library, `applyDiscount(subtotalCents, discount)`
(`src/discount.ts`) must reject invalid input by throwing an `Error`, instead of
returning NaN or a nonsense total.

Requirements:
1. `subtotalCents` must be a finite, non-negative integer (`Number.isInteger`
   and `>= 0`); otherwise throw.
2. For a `fixed` discount, `cents` must be a finite, non-negative integer;
   otherwise throw.
3. For a `percent` discount, `value` must be a finite number `>= 0`; otherwise
   throw.
4. Valid inputs must return exactly the same numbers as before (for example
   `applyDiscount(1000, { kind: "fixed", cents: 250 })` is still `750`).
5. Do not change the shape of the `Discount` type.
6. Do not weaken, skip, or delete tests.
7. Keep the patch minimal: only ADD the validation, do not change the existing
   computation.

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
