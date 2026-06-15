Follow this process for the `pricingkit` receipt fix:

1. Read `src/receipt.ts` and `src/cart.ts` and identify how `receipt` builds the
   `Receipt` and where `total` comes from.
2. State the contract the `Receipt` must satisfy: the legacy `amount` alias always
   equals `total`.
3. Make the smallest change to `receipt` that enforces it.
4. Run `npm run build`, then `node --test tests/*.test.mjs`.
5. If anything fails, debug once and re-run.
6. Review your diff against the contract and confirm `cart.ts` and `money.ts` are
   untouched.
