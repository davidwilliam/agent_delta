Follow this process to add the order status state machine to `pricingkit`:

1. Read `src/index.ts` and one existing module (for example `src/discount.ts`)
   to see how modules are written and re-exported. Note that NodeNext resolution
   means intra-package imports use a `.js` suffix.
2. Write out the legal transition table: pending -> paid, paid -> shipped,
   shipped -> delivered, pending -> cancelled, paid -> cancelled. Mark
   `delivered` and `cancelled` as terminal.
3. Create `src/order.ts` exporting `OrderStatus`, `canTransition`, and
   `transition`. `transition` returns `to` on a legal step and throws otherwise;
   `canTransition` is true exactly when `transition` would not throw.
4. Add `export * from "./order.js";` to `src/index.ts`.
5. Run `npm run build`, then `node --test tests/*.test.mjs`.
6. If anything fails, debug once and re-run. Confirm `src/money.ts` and
   `src/discount.ts` are untouched.
