You are working in the `saasapp` multi-tenant service.

Two related features are returning wrong results:
- `service.list_owned_projects(user)` returns no projects for users who clearly own
  projects (for example `alice` owns "Roadmap").
- `service.can_user_edit(user, project_id)` denies owners the right to edit their
  own projects.

Find the root cause and fix it so both features are correct. A correct fix should
not need to special-case each feature separately. Owners are determined by the
project's `owner_id`.

Do not change the seed data or the tests. Keep the change minimal. When finished,
run `pytest -q tests/` and summarize the root cause and your fix.
