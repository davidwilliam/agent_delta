# Expected behavior - ts_task_001

The minimal correct fix clamps the returned total to `[0, subtotalCents]`. The
reference clamps the lower bound with `Math.max(0, subtotalCents - off)`, which is
sufficient because `off` is non-negative for valid discounts, so the result can
never exceed the subtotal either.

Why the obvious solution fails:
- The base code returns `subtotalCents - off` directly. The visible normal-discount
  tests (10% off, small fixed amount) pass, so the bug looks absent.
- Hidden tests exercise the edges: a percentage over 100% and a fixed amount at or
  above the subtotal both drive the naive result negative.

Discriminators: over-large discount -> 0 (not negative); in-range discounts
unchanged; the fix stays in `discount.ts` and leaves `money.ts` and the `Discount`
type untouched.
