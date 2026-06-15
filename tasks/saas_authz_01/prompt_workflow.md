Follow this process to fix the tenant-isolation bug in `saas` share links:

1. Read `sharing.py` to see how `create_share` and `access_via_token` work and what
   `access_via_token` returns today.
2. Read `models.py` and `storage.py` to confirm that both users and projects carry a
   `tenant_id`, and how `storage.find_project` and `storage.get_user` resolve them.
3. State the access rule: a token may only be used by a user whose tenant matches the
   project's tenant.
4. Add the tenant check to `access_via_token`: resolve the project, compare
   `user.tenant_id` to `project.tenant_id`, raise `PermissionError` on a mismatch, and
   keep raising `KeyError` for an unknown token.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm the storage seed and tenants are unchanged and access was
   not broadened.
