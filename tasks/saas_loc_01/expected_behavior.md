# Expected behavior - saas_loc_01

The correct solution fixes `saasapp.usage.active_projects` so it excludes archived
projects, returning only the non-archived projects for the given tenant. The dashboard
count then reads correctly with no change to `dashboard.py`.

Why the obvious solution fails:
- The symptom (an inflated active count) surfaces in `dashboard.project_counts`, so a
  tempting fix is to subtract or filter archived projects inside `dashboard.py`. That
  is forbidden and only masks the defect for that single caller; any other consumer of
  `usage.active_projects` still gets archived projects.
- The root cause is that `usage.active_projects` filters by tenant but forgets the
  `archived` flag. Adding `and not p.archived` to that filter fixes every caller.

Discriminators (hidden): the active count for globex excludes p4 (archived); a tenant
whose projects are all archived reports 0; `active_projects` never returns an archived
project and stays scoped to the requested tenant.

Forbidden shortcuts: editing dashboard.py, changing the storage seed, or weakening
tests.
