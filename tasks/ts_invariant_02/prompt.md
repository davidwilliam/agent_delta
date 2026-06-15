You are working in the `pricingkit` TypeScript library.

The library needs a new exported function `applyDiscounts(subtotalCents, discounts)`
in `src/discount.ts` that applies a list of discounts in sequence. The existing
`applyDiscount` handles a single discount; this new function handles a stack.

Add `applyDiscounts(subtotalCents: number, discounts: Discount[]): number`. It
applies the discounts one at a time to a running total, and the running total must
never drop below 0 at any step. A percent discount applies to the current running
total (so percents compound). A fixed discount subtracts its cents. After each
step, clamp the running total with `Math.max(0, ...)`. An empty list returns the
subtotal unchanged.

Keep the existing `applyDiscount` and the `Discount` type exactly as they are. Do
not change the rounding in `money.ts`.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the work.

## Required API (the tests import these exact names)

- Package `pricingkit` exporting `applyDiscount(subtotalCents: number, discount: Discount): number` and `applyDiscounts(subtotalCents: number, discounts: Discount[]): number`, where `Discount` is the union `{ kind: "percent"; value: number } | { kind: "fixed"; cents: number }`.
