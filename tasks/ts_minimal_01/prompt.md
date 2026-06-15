You are working in the `pricingkit` TypeScript library.

`splitEvenly(totalCents, n)` in `src/split.ts` is meant to split a total into `n`
parts in whole cents. It currently floors each part and drops the remainder, so the
parts do not sum back to `totalCents` whenever `n` does not divide it evenly. For
example, `splitEvenly(100, 3)` returns `[33, 33, 33]`, which sums to 99 instead of
100.

Fix `splitEvenly` so it returns `n` integer parts that sum exactly to `totalCents`
and differ from each other by at most 1 cent, giving the first `remainder` parts one
extra cent. Keep the change minimal and stay inside `src/split.ts`; do not change
`money.ts` or `cart.ts`, and do not change the `splitEvenly` signature.

When finished, run `npm run build` and `node --test tests/*.test.mjs`, then
summarize the fix.

## Required API (the tests import these exact names)

- Package `pricingkit` exporting `splitEvenly(totalCents: number, n: number): number[]`.
