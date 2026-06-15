Follow this process for the `pricingkit` order-total bug:

1. Read `src/summary.ts` and observe how `orderSummary` computes `tax`.
2. Follow the call into the helper it uses for rounding (`src/rounding.ts`) and
   read that helper.
3. State why the tax can come out one cent too low (truncation versus rounding).
4. Make the smallest change at the root cause, in the rounding helper, so the tax
   rounds to the nearest cent. Do not edit `src/summary.ts`.
5. Run `npm run build`, then `node --test tests/*.test.mjs`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm the change is only in `src/rounding.ts` and that
   `summary.ts`, `money.ts`, and `cart.ts` are untouched.
