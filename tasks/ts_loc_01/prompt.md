You are working in the `pricingkit` TypeScript library.

`orderSummary(items, taxRateBps)` in `src/summary.ts` returns an order summary
with `subtotal`, `tax`, and `total` in whole cents. For some tax rates it reports
a tax that is one cent too low, which also makes the total wrong. For example, a
subtotal of 1000 cents at 875 bps should owe 88 cents of tax (87.5 rounded to the
nearest cent), but it reports 87.

Find the root cause and fix it so the tax is rounded to the nearest cent and the
total equals subtotal plus tax. Note that `orderSummary` delegates its rounding to
a shared helper; fix the helper rather than special-casing the summary. Keep the
change minimal.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the fix.
