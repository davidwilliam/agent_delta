You are working in the `saasapp` multi-tenant service (layers: models, storage,
policy, service, api).

There is a tenant-isolation bug: users are seeing projects that belong to other
tenants. For example, `alice` (tenant `acme`) currently sees the `globex` project
"Secret" in her project list, and can fetch it directly.

Fix the bug so that a user can only ever view projects in their own tenant, through
every path (both listing and direct fetch). The authoritative authorization rules
are documented in `docs/policy.md`.

Constraints:
- Preserve the existing archived-visibility rule (archived projects are visible
  only to admins, within their own tenant).
- Do not change the seed data, and do not modify the tests.
- Keep the change minimal and put it in the right layer.

When finished, run `pytest -q tests/` and summarize the root cause and your fix.
