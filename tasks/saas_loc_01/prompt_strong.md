Fix the active-project count in the `saas` service.

`saasapp.dashboard.project_counts(tenant_id)` returns `{"active": N}`, but `N` wrongly
includes archived projects. The count should be the number of non-archived projects
for that tenant.

Localization matters here:
- `dashboard.project_counts` delegates to `saasapp.usage.active_projects(tenant_id)`.
- `usage.active_projects` is the helper that is supposed to return only the active
  (non-archived) projects, and it is where the bug actually is.
- Fix the root cause in `usage.py`. Editing `dashboard.py` is forbidden; subtracting
  archived projects in the dashboard only masks the bug for that one caller.

Requirements:
1. `dashboard.project_counts("acme")["active"] == 1` (only p1; p2 is archived).
2. `dashboard.project_counts("globex")["active"] == 1` (only p3; p4 is archived).
3. A tenant whose projects are all archived reports `0`.
4. `usage.active_projects` never returns an archived project and stays tenant-scoped.
5. Do not change the storage seed; do not weaken tests.

When finished, run `pytest -q tests/`.
