# Expected behavior - hard_task_001

Root cause: `saasapp.policy.can_view` omits the tenant check. The minimal correct
fix adds it at the top of the policy function (see reference):

```python
def can_view(user, project):
    if project.tenant_id != user.tenant_id:
        return False
    if project.archived and user.role != "admin":
        return False
    return True
```

Why the policy layer: both `service.list_visible_projects` and
`service.get_project` authorize through `can_view`. Patching only the api list
handler (the tempting distractor) fixes listing but leaves direct fetch
vulnerable, so it fails `test_member_cannot_fetch_other_tenant_project` (public)
and the admin/invariant hidden tests.

Discriminators / failure modes detected:
- Controller-only fix -> direct-fetch tests still fail.
- Forgetting admins are tenant-scoped -> admin cross-tenant tests fail.
- Weakening the archived rule to "fix" visibility -> archived-rule test fails.
- Editing tests/storage to pass -> forbidden-path / forbidden-pattern violation.
