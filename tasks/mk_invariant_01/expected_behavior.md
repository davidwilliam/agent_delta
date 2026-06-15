# Expected behavior - mk_invariant_01

The correct solution adds a small pure function `apply_transactions(start_balance,
transactions)` in a new `mathkit.ledger` module. It validates the start balance,
walks the transactions in order, and enforces the invariant `running balance >= 0`
at every step.

Why the obvious solution fails:
- Summing all transactions (or applying them without a per-step check) passes the
  visible happy path but misses the invariant: an intermediate withdrawal can drive
  the balance below zero even when the net total stays non-negative.
- Checking the bound but mutating the balance before the check (or after raising)
  lets a rejected overdraw partially apply. The reference computes the prospective
  balance and only commits it when it stays at or above zero.

Discriminators (hidden): a withdrawal exactly to zero succeeds; a negative
start_balance raises; an overdraw partway through raises and is not applied; an empty
list returns start_balance; a valid mixed sequence returns the correct final balance.

Forbidden shortcuts: weakening or skipping tests, or relying on shared mutable state
instead of a pure function.
