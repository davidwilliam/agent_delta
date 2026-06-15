Fix a tenant-isolation bug in the `saas` share-link feature.

`saasapp.sharing.access_via_token(user, token)` resolves a share token to its project,
but it never checks the accessing user's tenant. Any user holding a token can read
another tenant's project, which is a cross-tenant data leak.

Requirements:
1. `access_via_token(user, token)` returns the project only when
   `user.tenant_id` equals the project's `tenant_id`.
2. If the user is in a different tenant than the project, raise `PermissionError` and
   return no project.
3. An unknown token must still raise `KeyError` (keep the existing behavior).
4. An admin user in the project's tenant is allowed (the check is on tenant, not role
   or ownership).
5. Cross-tenant access must be denied in both directions.
6. Do not change the storage seed or the tenants of users/projects; do not weaken
   tests; do not broaden access.

When finished, run `pytest -q tests/`.
