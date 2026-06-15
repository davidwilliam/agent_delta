Make `saasapp.provisioning.assign` safe under concurrent assignment.

`assign(tenant, user)` currently does an unlocked check-then-act with simulated
write latency, so concurrent callers to the same tenant all read the same under-limit
state before any of them writes, and more users get seats than `LIMITS[tenant]`
allows.

Requirements:
1. Concurrent assignments to one tenant must never exceed its seat limit: exactly
   `LIMITS[tenant]` distinct users succeed and every other caller raises ValueError.
2. Sequential assigns must fill a tenant up to its limit, after which the next
   distinct user raises ValueError.
3. Distinct tenants must remain independent under concurrency, each capped at its
   own limit.
4. Re-assigning a user who already holds a seat must stay idempotent and must not
   consume a new seat.
5. Do not remove the simulated latency; keep it inside the critical section so it
   still models real work without reintroducing the race.
6. Do not weaken, skip, or delete tests; do not change other modules.

When finished, run `pytest -q tests/`.
