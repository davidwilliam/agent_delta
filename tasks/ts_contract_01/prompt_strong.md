In the `pricingkit` TypeScript library, `receipt(items)` (`src/receipt.ts`) returns
a `Receipt` with a `total` field and a legacy `amount` alias.

Requirements:
1. The legacy `amount` field must always equal the `total` field, for every cart.
2. `total` must equal `subtotalCents(items)`, including the empty cart, where both
   are 0.
3. Do not change the `Receipt` shape or the `receipt` signature.
4. Do not change `cart.ts` or `money.ts`.
5. Do not weaken, skip, or delete tests.
6. Keep the patch minimal and localized to `src/receipt.ts`.

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
