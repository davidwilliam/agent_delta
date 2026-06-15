You are working in the `saasapp` package. Account lifecycle transitions live in
`saasapp.lifecycle`. A transition is legal only if its (from, to) pair is in
`LEGAL_TRANSITIONS`; `lifecycle.transition(tenant_id, new_status)` applies a legal
transition and records an audit entry, and raises `ValueError` on an illegal one.

Add a new "trial" account state. An account in "trial" must be able to move to
"active" or to "closed". Accounts must NOT be allowed to move INTO "trial" from
"active" or from "closed". The existing "active" and "closed" transitions, and the
audit logging, must keep working exactly as before.

Make the change only in `lifecycle.py`, and keep it minimal. Do not change
`storage.py` or the storage seed. When finished, run `pytest -q tests/` and
summarize what you added.
