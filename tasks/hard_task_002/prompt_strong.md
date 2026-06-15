You are working in the `saasapp` multi-tenant service. Accounts currently have an
`active` and a `closed` state (see `saasapp/lifecycle.py` and the account checks
in `saasapp/service.py`).

Add a new `suspended` account state with these rules:
- Legal transitions: `active -> suspended`, `suspended -> active`, and
  `suspended -> closed`.
- `closed -> suspended` is illegal and must raise (as illegal transitions already do).
- A suspended account cannot create projects, but its users can still view
  projects.
- Preserve all existing active/closed behavior, and keep transitions audited.

Requirements:
1. Accounts can transition `active -> suspended`, `suspended -> active`, and
   `suspended -> closed`.
2. The transition `closed -> suspended` is illegal and raises.
3. Suspended accounts cannot create projects but can still view projects.
4. Transitions are recorded in the audit log, and existing active/closed behavior
   is unchanged.
5. Do not change the existing active/closed transitions.
6. Do not modify the seed data in `storage.py`.
7. Do not weaken or skip tests.
8. Keep the patch minimal and put each part in the right place.

When finished, run `pytest -q tests/` and summarize.
