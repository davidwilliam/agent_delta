Follow this process to make `saasapp.provisioning.assign` safe under concurrency:

1. Read `provisioning.py` and trace what `assign` does: read current seat holders,
   check membership, check the limit, sleep, then write back the updated list.
2. State why this lets a tenant exceed its limit when several threads assign distinct
   users at once: they all read the same under-limit state before any of them writes.
3. Add the smallest fix that makes the whole check-then-act atomic (for example a
   `threading.Lock` held across the read, both checks, the latency, and the write).
   Keep the simulated latency in place, inside the critical section.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the latency is still present and no other module changed.
