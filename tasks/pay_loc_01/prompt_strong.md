Fix the understated gross total in the `payments` reporting summary.

Context:
- `payments.reporting.summary()` returns `{"gross": ..., "count": ...}`.
- `count` is correct; `gross` is too low.
- `summary()` delegates the gross computation to a helper in another module.

Requirements:
1. Localize the root cause. The bug is in `payments.aggregate.gross_total`, which
   currently skips the first invoice (an off-by-one slice). It is not in
   `reporting.py`.
2. Fix `gross_total` so it sums the amount of every invoice in
   `storage.INVOICES`, including the first.
3. Do not edit `reporting.py`. Do not change the Invoice model or storage state.
4. Do not weaken or skip tests.

After the fix:
- `summary()["gross"]` must equal the sum of all invoice amounts.
- A single invoice yields a gross equal to that invoice's amount.
- Zero invoices yield a gross of 0.

When finished, run `pytest -q tests/`.
