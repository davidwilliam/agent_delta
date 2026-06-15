You are working in the `saasapp` multi-tenant service.

Two related features are returning wrong results:
- `service.list_owned_projects(user)` returns no projects for users who clearly own
  projects (for example `alice` owns "Roadmap").
- `service.can_user_edit(user, project_id)` denies owners the right to edit their
  own projects.

Find the root cause and fix it so both features are correct. A correct fix should
not need to special-case each feature separately. Owners are determined by the
project's `owner_id`.

Requirements:
1. `list_owned_projects` returns exactly the projects owned by the user (and
   viewable).
2. `can_user_edit` is true only for a project the user owns and can view.
3. The fix is at the shared root cause, so both owned-listing and edit-permission
   become correct without special-casing each feature.
4. Do not modify the seed data in `storage.py`.
5. Do not weaken or skip tests.
6. Keep the patch minimal.

When finished, run `pytest -q tests/` and summarize the root cause and your fix.
