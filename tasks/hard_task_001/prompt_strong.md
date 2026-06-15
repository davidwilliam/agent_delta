You are working in the `saasapp` multi-tenant service (layers: models, storage,
policy, service, api).

There is a tenant-isolation bug: users are seeing projects that belong to other
tenants. For example, `alice` (tenant `acme`) currently sees the `globex` project
"Secret" in her project list, and can fetch it directly.

Fix the bug so that a user can only ever view projects in their own tenant, through
every path (both listing and direct fetch). The authoritative authorization rules
are documented in `docs/policy.md`.

Requirements:
1. A user can only view projects in their own tenant, via both listing and direct
   fetch.
2. The archived-visibility rule is preserved: archived projects are visible only
   to admins, within their own tenant.
3. Admins remain scoped to their own tenant, with no cross-tenant access.
4. Existing baseline tests continue to pass.
5. Do not weaken or remove the existing archived-visibility rule.
6. Do not modify the seed data in `storage.py`.
7. Do not weaken or skip tests.
8. Keep the patch minimal and put it in the right layer.

When finished, run `pytest -q tests/` and summarize the root cause and your fix.
