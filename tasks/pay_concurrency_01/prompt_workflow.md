Follow this process to make `payments.wallet.credit` safe under concurrency:

1. Read `wallet.py` and trace what `credit` does: read current balance, sleep,
   write back current + amount.
2. State why this loses updates when two threads credit the same account at once.
3. Add the smallest fix that makes the read-modify-write atomic (for example a
   `threading.Lock` around the read, latency, and write). Keep the simulated
   latency in place.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the latency is still present and no other module
   changed.
