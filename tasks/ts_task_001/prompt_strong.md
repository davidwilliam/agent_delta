In the `pricingkit` TypeScript library, `applyDiscount(subtotalCents, discount)`
(`src/discount.ts`) must never return a total outside `[0, subtotalCents]`.

Requirements:
1. A percentage discount over 100% must clamp the total to 0, not go negative.
2. A fixed discount larger than the subtotal must clamp the total to 0.
3. Normal in-range discounts (e.g. 10% off 1000 -> 900) must be unchanged.
4. Do not change the rounding behaviour in `money.ts`.
5. Do not change the shape of the `Discount` type.
6. Do not weaken, skip, or delete tests.
7. Keep the patch minimal (a single, localized change).

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
