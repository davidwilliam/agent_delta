You are working in the `saas` service. Projects can be shared via a link token:
`saasapp.sharing.create_share(project_id)` returns a token, and
`saasapp.sharing.access_via_token(user, token)` resolves a token back to its project.

There is a tenant-isolation bug. `access_via_token` returns the project for anyone who
holds the token, regardless of which tenant the user belongs to. That lets a user from
one tenant read another tenant's project (a cross-tenant data leak).

Each user and project carries a `tenant_id` (see `saasapp.models`). Fix
`access_via_token` so it returns the project only when the accessing user is in the
same tenant as the project; otherwise it must raise `PermissionError`. An unknown
token must still raise `KeyError`.

Do not change the storage seed or the tenants of users/projects. Keep the change
minimal. When finished, run `pytest -q tests/` and summarize what you changed.
