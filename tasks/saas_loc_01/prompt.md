You are working in the `saas` service. The tenant dashboard reports an active project
count via `saasapp.dashboard.project_counts(tenant_id)`, which returns a dict like
`{"active": N}`. The count is wrong: it includes archived projects, so an "active"
count is inflated.

A project has an `archived` flag (see `saasapp.models.Project`). The dashboard count
should reflect only projects that are not archived, scoped to the given tenant.

The symptom is visible in `dashboard.project_counts`, but the dashboard is not where
the defect lives. Localize the real root cause, fix it there, and keep the change
minimal. Do not edit `dashboard.py` and do not change the storage seed. When finished,
run `pytest -q tests/` and summarize what you changed and why.
