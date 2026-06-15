# Expected behavior - saas_state_01

The correct solution extends `LEGAL_TRANSITIONS` in `lifecycle.py` with exactly two
new pairs, ("trial","active") and ("trial","closed"), and changes nothing else.
`transition()` and `can_transition()` keep their existing behavior, so a successful
transition still appends (tenant, from, to) to `storage.AUDIT`.

Why the obvious solution fails:
- Adding the trial state without the outbound transitions leaves trial->active and
  trial->closed raising ValueError, so the happy path fails.
- Adding transitions in both directions (for example active->trial or closed->trial)
  passes the happy path but breaks the guard: moving an account INTO trial must stay
  illegal.
- Touching transition() to special-case trial can drop the audit entry; the audit
  append must remain on every successful transition.

Discriminators (hidden): trial->closed is allowed; closed->trial raises ValueError;
active->trial raises ValueError; a successful trial->active appends
(tenant,"trial","active") to storage.AUDIT; the existing active->closed and
closed->active transitions still work.

Forbidden shortcuts: changing existing transitions or the storage seed, modifying
storage.py, or weakening tests.
