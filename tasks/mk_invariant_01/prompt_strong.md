Add a new module `mathkit.ledger` to the `mathkit` package.

Expose `apply_transactions(start_balance, transactions)`:
- `start_balance` is an int and must be non-negative.
- `transactions` is an iterable of ints: positive values are deposits, negative
  values are withdrawals.
- Apply them in order to a running balance and return the final balance.

Requirements:
1. A negative `start_balance` must raise ValueError.
2. The running balance must never go below zero.
3. A withdrawal that would drive the balance below zero must raise ValueError and
   must NOT be applied (no partial application).
4. Deposits always apply.
5. A withdrawal that brings the balance to exactly zero is allowed.
6. An empty transaction list returns `start_balance` unchanged.
7. Keep the function pure (no shared mutable state); do not weaken tests.

When finished, run `pytest -q tests/`.
