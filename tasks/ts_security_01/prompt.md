You are working in the `pricingkit` TypeScript library.

`applyDiscount(subtotalCents, discount)` in `src/discount.ts` computes an order
total after a discount. It trusts its inputs: adversarial values such as NaN,
Infinity, a non-integer subtotal, a non-integer fixed `cents`, or a negative
amount flow straight through and produce NaN or a nonsense total.

Harden `applyDiscount` so it throws an `Error` on invalid input instead of
returning garbage, while keeping its behaviour on valid input identical:

1. `subtotalCents` must be a finite, non-negative integer (`Number.isInteger`
   and `>= 0`); otherwise throw.
2. For a `fixed` discount, `cents` must be a finite, non-negative integer;
   otherwise throw.
3. For a `percent` discount, `value` must be a finite number `>= 0`; otherwise
   throw.
4. Valid inputs must return exactly the same numbers as before, for example
   `applyDiscount(1000, { kind: "fixed", cents: 250 })` stays `750`.

Do not change the shape of the `Discount` type and do not change the
valid-input results. Only ADD the input validation.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the fix.
