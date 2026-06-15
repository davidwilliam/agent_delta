You are working in the `pricingkit` TypeScript library.

`applyDiscount(subtotalCents, discount)` in `src/discount.ts` returns the order
total after a discount. It currently subtracts the discount directly, so a large
discount can make the total negative, and a fixed discount bigger than the order
can make the customer "owe" a negative amount.

Fix `applyDiscount` so the returned total always stays within `[0, subtotalCents]`,
while leaving normal in-range discounts unchanged. Keep the change minimal and do
not change the rounding in `money.ts` or the shape of the `Discount` type.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the fix.
