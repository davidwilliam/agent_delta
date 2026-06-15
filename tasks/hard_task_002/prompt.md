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

Do not change the seed data or the tests. Keep the change minimal and put each
part in the right place. When finished, run `pytest -q tests/` and summarize.
