You are working in the `saasapp` package. `saasapp.subscription` tracks each tenant's
billing plan in memory. `LEGAL` is the set of allowed `(from, to)` plan transitions,
`plan(tenant)` reads the current plan (defaulting to "free"), `change_plan(tenant,
new)` is meant to move a tenant to a new plan, and `reset()` clears the store.

`change_plan` currently stores the new plan unconditionally, without consulting
`LEGAL`. That means it allows illegal jumps. The plan ladder is
free <-> pro <-> enterprise, so for example free->enterprise is illegal (you must go
free->pro->enterprise) and enterprise->free is illegal (you must go
enterprise->pro->free).

Make `change_plan` reject any transition whose `(current, new)` pair is not in
`LEGAL` by raising `ValueError`, and apply only legal ones. A rejected transition
must leave the stored plan unchanged. Keep the `LEGAL` set and its semantics as they
are.

Make the change only in `subscription.py`, and keep it minimal. When finished, run
`pytest -q tests/` and summarize what you changed.

## Required API (the tests import these exact names)

- Module `saasapp.subscription` exposing `change_plan(tenant, new)` (returns the new plan, raises `ValueError` on an illegal plan change), `plan(tenant)` (returns the current plan), and `reset()`.
