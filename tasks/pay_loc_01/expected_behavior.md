# Expected behavior - pay_loc_01

The summary's `gross` is computed by `payments.aggregate.gross_total`, which
`payments.reporting.summary()` calls. The buggy helper slices
`storage.INVOICES[1:]`, silently dropping the first invoice, so the reported gross is
understated. The correct fix sums every invoice:

    return sum(inv.amount for inv in storage.INVOICES)

Why the obvious solution fails:
- The visible symptom (a too-low gross) surfaces through `reporting.summary()`, so
  the tempting move is to patch `reporting.py`. That is the wrong layer; `reporting`
  only assembles the dict and editing it is forbidden. The root cause is the
  off-by-one slice in `aggregate.gross_total`.
- Recomputing the sum inside `reporting.py` (for example summing INVOICES directly
  there) would mask the bug while leaving `gross_total` broken for any other caller,
  and it violates the forbidden_paths scope.

Discriminators (hidden): a single invoice must yield a gross equal to its amount
(base reports 0); zero invoices yield 0; the gross always equals the sum of all
amounts including the first. These fail unless `gross_total` itself is corrected.

Forbidden shortcuts: editing reporting.py, changing the Invoice model or storage
state, or weakening tests.
