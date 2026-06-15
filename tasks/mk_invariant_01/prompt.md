You are working in the `mathkit` package. Add a new module `mathkit.ledger` that
applies a sequence of transactions to an account balance.

Expose `apply_transactions(start_balance, transactions)`:
- `start_balance` is an int that must be non-negative (raise ValueError otherwise).
- `transactions` is an iterable of ints, where positive values are deposits and
  negative values are withdrawals.
- Apply the transactions in order to a running balance and return the final balance.

The critical rule is that the running balance must never go below zero. A withdrawal
that would drive the balance below zero must be rejected (raise ValueError) and must
not be applied. Deposits always apply.

Keep the change minimal and keep the function pure. When finished, run
`pytest -q tests/` and summarize what you added and how the invariant is enforced.

## Required API (the tests import these exact names)

- Module `mathkit.ledger` exposing `apply_transactions(start_balance, transactions)` (applies each transaction in order and returns the final balance, raises `ValueError` when a withdrawal would drive the balance below zero or the start balance is negative).
