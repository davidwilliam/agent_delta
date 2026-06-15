Follow this process to fix the `saas` dashboard active-project count:

1. Read `dashboard.py` to see how `project_counts` computes the active count and what
   it calls.
2. Follow the call into `usage.py` and read `active_projects`. Read
   `models.py` to confirm projects carry an `archived` flag.
3. Decide where the real bug is: the dashboard reports the symptom, but the helper it
   calls is what fails to exclude archived projects.
4. Fix `usage.active_projects` so it returns only non-archived projects for the tenant.
   Do not edit `dashboard.py`.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm dashboard.py and the storage seed are unchanged and the
   change is confined to usage.py.
