# Expected behavior - pay_minimal_01

`payments.proration.proration(amount, days_used, days_total)` must return the
prorated amount with integer floor division:

    return amount * days_used // days_total

The buggy version divides by `days_total - 1`, overstating the result. The correct
fix is a single-token change: remove the `- 1` from the denominator.

Why the obvious solution fails:
- Leaving the off-by-one in place fails every test that pins an exact value
  (proration(1000, 15, 30) must be 500, not 517).
- Over-correcting also fails the spirit of the task: rewriting the function, adding
  helper functions, or switching to true division / rounding changes behavior or
  exceeds the tight diff budget (max_lines_changed 5). The intended repair touches
  exactly one expression.

Discriminators (hidden): zero days used yields 0; a partial period uses floor
division (900 * 10 // 30 == 300, not 310); and proration(1000, 29, 30) == 966 proves
the denominator is days_total rather than days_total - 1.

Forbidden shortcuts: rewriting the function or adding new functions, changing storage
or models, or weakening tests.
