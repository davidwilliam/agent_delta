# Expected behavior - hard_task_002

Two coordinated changes (see references):

1. `lifecycle.LEGAL_TRANSITIONS` gains `active->suspended`, `suspended->active`,
   `suspended->closed` (and `closed->suspended` stays illegal).
2. `service.create_project` blocks any non-active account (change the `== "closed"`
   guard to `!= "active"`), so suspended accounts cannot create.

Why both: a transition-table-only change makes the states reachable but leaves
`create_project` allowing suspended accounts to create projects (the guard only
blocked `closed`). The hidden test `test_suspended_cannot_create_project` catches
that. Viewing is not gated by account status, so suspended accounts can still view.
