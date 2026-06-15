# Expected behavior - saas_invariant_01

The correct solution adds a small seat ledger (a new `saasapp.seats` module is the
minimal approach) that tracks the set of distinct assigned users per tenant and
enforces the invariant `assigned_count(tenant) <= limit(tenant)`.

Why the obvious solution fails:
- Counting assignments with a plain counter passes the visible happy path but breaks
  idempotency: assigning the same user twice double-counts and can falsely fill or
  overflow the quota. The reference stores a set of user ids, so a repeat assign is a
  no-op.
- Checking the bound but mutating state before the check (or after raising) lets a
  rejected over-limit assign partially apply (the user gets added even though the call
  raised). The reference only commits when the new distinct user fits within the
  limit.

Discriminators (hidden): re-assigning an existing user does not raise and does not
increase the count; an over-limit attempt raises and does not add the user; distinct
tenants are independent (one full tenant does not block another); unknown tenants
raise on both limit() and assign().

Forbidden shortcuts: modifying storage.py or models.py, changing the storage seed, or
weakening tests.
