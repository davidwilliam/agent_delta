Follow this process to add transaction handling to `mathkit`:

1. Read an existing module under `src/mathkit/` (for example `stats.py`) to match
   the package conventions and how ValueError is used for invalid input.
2. State the invariant the running balance must satisfy as transactions are applied.
3. Add a new `mathkit.ledger` module exposing `apply_transactions(start_balance,
   transactions)` that enforces it: reject a negative start_balance, apply each
   transaction in order, and reject (without applying) any withdrawal that would
   drive the balance below zero. Keep the function pure.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm you only added the new module and did not change other
   modules or tests.
