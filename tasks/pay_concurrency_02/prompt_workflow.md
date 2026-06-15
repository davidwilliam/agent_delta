Follow this process to make `payments.sequence.next_id` safe under concurrency:

1. Read `sequence.py` and trace what `next_id` does: read the current counter,
   sleep, write back current + 1, return it.
2. State why this hands out duplicate ids when two threads call it at once.
3. Add the smallest fix that makes the read-modify-write atomic (for example a
   `threading.Lock` around the read, latency, and write). Keep the simulated
   latency in place.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the latency is still present and no other module
   changed.
