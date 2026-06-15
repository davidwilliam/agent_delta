You are working in the `saasapp` service. Each customer (tenant) is allocated a fixed
number of seats, and users are assigned seats within their tenant.

Add per-tenant seat allocation with a hard quota. Provide a way to assign a seat to a
user under a tenant, to query how many distinct users currently hold a seat, and to
query a tenant's seat limit. The critical rule is that the number of distinct assigned
users for a tenant must never exceed that tenant's seat limit.

Seat limits are fixed per tenant (`acme` has 2 seats, `globex` has 1). Assigning a
user who already holds a seat must be a no-op (it must not raise and must not consume
another seat). An assignment that would exceed the limit must be rejected without
changing any state. Looking up or assigning under an unknown tenant must raise.

Do not modify `src/saasapp/storage.py` or `src/saasapp/models.py`, and do not change
the storage seed. Keep the change minimal. When finished, run `pytest -q tests/` and
summarize what you added and how the quota is enforced.

## Required API (the tests import these exact names)

- Module `saasapp.seats` exposing `assign(tenant_id, user_id)` (returns the new assigned count, idempotent per user, raises `ValueError` when the seat limit is exceeded and `KeyError` for an unknown tenant), `assigned_count(tenant_id)` (returns the number of assigned seats), `limit(tenant_id)` (returns the seat limit, raises `KeyError` for an unknown tenant), and `reset()`.
