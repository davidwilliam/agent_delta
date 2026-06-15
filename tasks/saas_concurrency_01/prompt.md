You are working in the `saasapp` package. `saasapp.provisioning` tracks seat
assignments per tenant in memory. `LIMITS` maps each tenant to its maximum number
of seats. `assign(tenant, user)` gives `user` a seat on `tenant` and returns the new
seat count, `assigned(tenant)` lists the current seat holders, and `reset()` clears
the store.

`assign` does an unlocked check-then-act with simulated write latency: it reads the
current seat holders, checks whether the user already has a seat, checks the limit,
waits, then writes back the updated list. Under concurrent assignments to the same
tenant, several callers all read the same under-limit state before any of them
writes, so more users get seats than the limit allows.

Make `assign` safe under concurrent assignment so that no tenant ever exceeds its
seat limit: exactly `LIMITS[tenant]` distinct users succeed and the rest raise
`ValueError`. Sequential assigns must still fill a tenant up to its limit and then
raise, distinct tenants must stay independent, and re-assigning a user who already
holds a seat must stay idempotent.

Do not remove the simulated latency, and keep the change minimal and in the
provisioning layer. When finished, run `pytest -q tests/` and summarize what you
changed and how the seat limit is enforced under concurrency.
