Follow this process for the `pricingkit` split fix:

1. Read `src/split.ts` and identify how `splitEvenly` builds the parts.
2. State the invariant the result must satisfy: the parts sum exactly to
   `totalCents` and differ by at most 1 cent.
3. Make the smallest change to `splitEvenly` that enforces it, distributing the
   remainder over the first parts.
4. Run `npm run build`, then `node --test tests/*.test.mjs`.
5. If anything fails, debug once and re-run.
6. Review your diff against the invariant and confirm `money.ts` and `cart.ts` are
   untouched.
