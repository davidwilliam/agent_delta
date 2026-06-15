In the `pricingkit` TypeScript library, `splitEvenly(totalCents, n)`
(`src/split.ts`) must split a total into `n` integer parts.

Requirements:
1. The `n` parts must sum exactly to `totalCents`, for exact divisions and for
   totals that leave a remainder.
2. The largest and smallest parts must differ by at most 1 cent.
3. The first `remainder` parts each receive one extra cent (e.g.
   `splitEvenly(100, 3)` returns `[34, 33, 33]`).
4. Every part is an integer; `n == 1` returns `[totalCents]`; a total of 0 returns
   all zeros.
5. Do not change `money.ts` or `cart.ts`.
6. Do not change the `splitEvenly` signature.
7. Do not weaken, skip, or delete tests.
8. Keep the patch minimal and localized to `src/split.ts`.

When finished, run `npm run build` and `node --test tests/*.test.mjs`.
