In the `saasapp` service, `service.list_owned_projects(user)` returns no projects
for users who clearly own some (for example `alice` owns "Roadmap"), and
`service.can_user_edit(user, project_id)` denies owners editing their own projects.
Find and fix the shared root cause, then run `pytest -q tests/`.
