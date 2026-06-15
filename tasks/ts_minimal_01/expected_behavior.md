# Expected behavior - ts_minimal_01

The minimal correct fix computes the dropped remainder and distributes it one cent
at a time over the first parts. The reference uses
`base = Math.floor(totalCents / n)`, `remainder = totalCents - base * n`, then
returns `n` parts where the first `remainder` parts are `base + 1` and the rest are
`base`. This guarantees the parts sum exactly to `totalCents` and differ by at most
1 cent.

Why the obvious solution fails:
- The base code returns `n` copies of `Math.floor(totalCents / n)`, discarding the
  remainder. When `n` divides `totalCents` exactly the result is correct, so the bug
  is invisible on exact divisions.
- Hidden tests exercise totals that leave a remainder (e.g. 100/3, 99/4, 12345/11)
  and check that the parts sum to the total and that the max and min differ by at
  most 1.

Discriminators: remainder distributed so parts sum to the total; max-min part <= 1;
`n == 1` returns `[total]`; a total of 0 returns all zeros; the fix stays in
`split.ts` and leaves `money.ts` and `cart.ts` untouched.
