Follow this process to fix the tenant-isolation bug in `saasapp`:

1. Read the policy, service, and api layers, plus `docs/policy.md`, to see how
   project visibility is decided and where listing and direct fetch each check it.
2. State the invariant: a user can only view a project whose tenant matches the
   user's tenant, and archived projects are visible only to admins within that
   same tenant.
3. Make the smallest change at the shared decision point (the policy check used by
   both list and get), not in a single api handler, so both paths are covered.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff against the requirements: confirm the archived-visibility rule
   is preserved, the seed data in `storage.py` is unchanged, and no tests were
   weakened.
