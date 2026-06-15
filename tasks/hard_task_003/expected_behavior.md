# Expected behavior - hard_task_003

Root cause: `ownership.is_owner` compares `project.owner_id` to `user.tenant_id`
instead of `user.id`. The one-line fix (see reference):

```python
def is_owner(user, project):
    return project.owner_id == user.id
```

Why localization matters: `is_owner` is used by both `service.list_owned_projects`
and `ownership.can_edit` (via `service.can_user_edit`). Patching only the service
listing leaves `can_user_edit` wrong, which the hidden test
`test_other_owner_can_edit_own` catches. The fix belongs at the shared helper.
