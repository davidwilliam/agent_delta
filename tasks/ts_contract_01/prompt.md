You are working in the `pricingkit` TypeScript library.

`receipt(items)` in `src/receipt.ts` builds a `Receipt` from a cart. The `Receipt`
has a `total` field and a legacy `amount` field. The `amount` field is a
backward-compatible alias that must always equal `total`, but the current code
hardcodes `amount` to 0, which breaks every caller that still reads the alias.

Fix `receipt` so the legacy `amount` field always equals `total`. Keep the change
minimal and stay inside `src/receipt.ts`; do not change `cart.ts` or `money.ts`, and
do not change the `Receipt` shape or the `receipt` signature.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the fix.

## Required API (the tests import these exact names)

- Package `pricingkit` exporting `receipt(items: LineItem[]): Receipt` and `subtotalCents(items: LineItem[]): number`.
