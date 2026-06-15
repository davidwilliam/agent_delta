Add per-tenant seat allocation to the `saasapp` service.

Expose, in the `saasapp` package, a new module with:
- `SEAT_LIMITS`: a module-level mapping of tenant id to seat limit
  (`acme` is 2, `globex` is 1).
- `limit(tenant_id)`: the seat limit for a tenant.
- `assigned_count(tenant_id)`: the number of distinct users currently assigned a seat.
- `assign(tenant_id, user_id)`: assign a seat, returning the new assigned count.
- `reset()` on the new module so tests can isolate state.

Requirements:
1. The number of distinct assigned users for a tenant must never exceed its limit.
2. `assign` is idempotent: assigning a user who already holds a seat is a no-op,
   it must not raise and must not increase the assigned count.
3. An assignment that would exceed the limit must raise ValueError and must NOT add
   the user or otherwise change state (no partial application).
4. `limit` and `assign` on an unknown tenant must raise KeyError.
5. Distinct tenants are independent: one tenant being full must not affect another.
6. Do not modify `storage.py` or `models.py`, do not change the storage seed, and do
   not weaken tests.

When finished, run `pytest -q tests/`.
