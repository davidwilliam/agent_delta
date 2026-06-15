# Expected behavior - ts_loc_01

The minimal correct fix changes `roundCents` in `src/rounding.ts` from
`Math.trunc(x)` to `Math.round(x)`. `orderSummary` in `src/summary.ts` delegates
its tax rounding to `roundCents`, so fixing the helper corrects every summary that
goes through it, with no change to `summary.ts` itself.

Why the obvious solution fails:
- The visible symptom is wrong `tax` and `total` in `orderSummary`. A reader who
  patches `summary.ts` directly (for example wrapping the tax in `Math.round`)
  treats the symptom, leaves the shared `roundCents` helper broken for any other
  caller, and violates the scope (summary.ts is forbidden).
- The root cause is `roundCents` truncating instead of rounding. Truncation only
  shows up when the raw tax has a fractional part of 0.5 or more; for exact or
  small-fraction taxes truncation and rounding agree, so a casual check looks fine.

Discriminators: a 0.5 fractional tax rounds up (87.5 -> 88, not 87); fractions
above 0.5 round up and below 0.5 round down; exact whole-cent taxes are unchanged;
the total always equals subtotal plus tax; the fix lives only in `src/rounding.ts`
and leaves `summary.ts`, `money.ts`, and `cart.ts` untouched.
