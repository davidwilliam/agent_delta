Follow this process to add per-tenant seat allocation to `saasapp`:

1. Read `models.py` and `storage.py` to see how tenants and users are represented.
2. State the invariant the seat allocation must satisfy for each tenant.
3. Add the smallest seat API that enforces it: track distinct assigned users per
   tenant, make re-assigning an existing user idempotent, reject an over-limit assign
   atomically (no partial application), and raise on an unknown tenant.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm `storage.py`, `models.py`, and the storage seed are
   unchanged.
