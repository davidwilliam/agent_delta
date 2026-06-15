In the `pricingkit` TypeScript library, `orderSummary(items, taxRateBps)` in
`src/summary.ts` returns `{ subtotal, tax, total }` in whole cents. The reported
tax is sometimes one cent too low, which makes the total wrong too.

Requirements:
1. The tax must be rounded to the nearest cent. A raw tax of 87.5 must become 88,
   not 87.
2. The total must always equal subtotal plus tax.
3. Cases where truncation and rounding agree (for example an exact whole-cent tax)
   must keep working.
4. Trace the symptom to its root cause: `orderSummary` computes its tax through a
   shared rounding helper. Fix that helper in `src/rounding.ts`; do not edit
   `src/summary.ts`, and do not change the `OrderSummary` shape or the
   `orderSummary` signature.
5. Do not change `src/money.ts` or `src/cart.ts`.
6. Do not weaken, skip, or delete tests.
7. Keep the patch minimal (a single, localized change).

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
