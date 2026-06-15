In the `pricingkit` TypeScript library, add an exported function
`applyDiscounts(subtotalCents: number, discounts: Discount[]): number` to
`src/discount.ts`.

Requirements:
1. Apply the discounts in sequence to a running total.
2. The running total must never drop below 0 after any step: clamp with
   `Math.max(0, runningTotal - off)` after each discount.
3. A percent discount applies to the current running total, so percents compound
   (use `percentOfCents(runningTotal, value)`).
4. A fixed discount subtracts its `cents`.
5. An empty list returns the subtotal unchanged.
6. Keep the existing `applyDiscount` and the `Discount` type exactly as they are.
7. Do not change the rounding behaviour in `money.ts`.
8. Do not weaken, skip, or delete tests.

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
