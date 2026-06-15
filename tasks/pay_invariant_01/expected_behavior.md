# Expected behavior - pay_invariant_01

The correct solution adds a small refund ledger (a new `payments.refunds` module is
the minimal approach) that tracks the cumulative refunded amount per event and
enforces the invariant `sum(refunds for event) <= invoice.amount`.

Why the obvious solution fails:
- Handling a single refund (subtract or record one amount) passes the visible happy
  path but misses the cumulative case: several partial refunds can sum past the
  amount paid.
- Checking the bound but recording state before the check (or after raising) lets a
  rejected over-refund partially apply. The reference computes the prospective total
  and only commits when it is within bounds.

Discriminators (hidden): cumulative partials up to the paid amount succeed; the
refund that would exceed it raises and leaves the recorded total unchanged; zero and
negative amounts raise; unknown events raise; distinct events track independently.

Forbidden shortcuts: changing the Invoice model or storage seed, or weakening tests.
