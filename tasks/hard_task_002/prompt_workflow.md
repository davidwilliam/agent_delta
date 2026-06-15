Follow this process to add the `suspended` account state to `saasapp`:

1. Read `saasapp/lifecycle.py` and the account checks in `saasapp/service.py` to
   see how states, the transition table, the audit log, and create-project gating
   work today.
2. State the invariant: legal transitions are `active -> suspended`,
   `suspended -> active`, and `suspended -> closed`; `closed -> suspended` is
   illegal and raises; a suspended account cannot create projects but can still
   view them.
3. Make the smallest change in each right place: add the state and its transitions
   to the table, and update the create-project check so suspended accounts are
   blocked there too. Do not change the existing active/closed transitions.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff against the requirements: confirm transitions are audited,
   active/closed behavior is unchanged, and the seed data and tests are untouched.
