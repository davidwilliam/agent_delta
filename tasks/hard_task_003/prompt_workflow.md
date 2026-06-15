Follow this process to fix owned-project listing and edit permission in `saasapp`:

1. Read `service.list_owned_projects` and `service.can_user_edit`, then trace what
   they both rely on to decide ownership (the `owner_id` comparison helper).
2. State the invariant: a user owns a project when the project's `owner_id` matches
   that user, and ownership is decided in one shared place that both features use.
3. Make the smallest change at that shared helper, not separately in each feature,
   so the same fix corrects both list and edit.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff against the requirements: confirm both `list_owned_projects`
   and `can_user_edit` are correct, and the seed data and tests are unchanged.
