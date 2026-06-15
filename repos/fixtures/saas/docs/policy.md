# Authorization policy (source of truth)

Visibility of a project to a user is decided by `saasapp.policy.can_view` and must
follow these rules:

1. **Tenant isolation (invariant):** a user may only view projects belonging to
   their own tenant. A user must never see another tenant's project, through any
   path (listing or direct fetch).
2. **Archived projects:** an archived project is visible only to `admin` users,
   and only within their own tenant. Members never see archived projects.
3. **Admins are tenant-scoped:** an admin has elevated rights only within their
   own tenant, never across tenants.

All authorization decisions go through the policy layer so that every caller
(`service.list_visible_projects`, `service.get_project`, and the api handlers)
enforces the same rules.
