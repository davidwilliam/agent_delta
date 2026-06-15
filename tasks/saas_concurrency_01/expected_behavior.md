# Expected behavior - saas_concurrency_01

The correct solution makes the check-then-act in `provisioning.assign` atomic, for
example with a module-level `threading.Lock` held across the read of the current seat
holders, the membership check, the limit check, the simulated latency, and the write.
The simulated latency stays in place; only the check-then-act is serialized.

Why the obvious solution fails:
- The base `assign` reads the current seat holders, checks membership and the limit,
  sleeps, then writes back with no synchronization. Under concurrent assignments to
  the same tenant, several callers read the same under-limit state before any of them
  writes, so more than `LIMITS[tenant]` distinct users get seats. The simulated
  latency guarantees the overlap.
- Removing the latency to dodge the race is forbidden; it hides the bug rather than
  fixing the concurrency.

Discriminators (hidden): high-concurrency assignment to one tenant still admits
exactly the limit; a second tenant with a different limit is capped at its own limit;
distinct tenants stay independent under concurrency; re-assigning a user who already
holds a seat is idempotent and does not consume a new seat.

Forbidden shortcuts: removing the simulated latency, weakening tests, or changing
other modules.
