# Expected behavior - saas_state_02

The correct solution makes `change_plan` consult `LEGAL` before writing: it reads the
tenant's current plan (default "free"), checks whether `(current, new)` is in `LEGAL`,
raises `ValueError` if not, and otherwise stores the new plan and returns it. The
`LEGAL` set and its semantics are left unchanged.

Why the obvious solution fails:
- The base `change_plan` stores the new plan unconditionally, so it allows illegal
  jumps. The plan ladder is free <-> pro <-> enterprise: free->enterprise must go
  through pro, and enterprise->free must go through pro. Storing the target directly
  skips the guard.
- Validating but still mutating on rejection (writing first, then raising) leaves the
  stored plan changed; the rejection must be a no-op on state.

Discriminators (hidden): pro->enterprise and enterprise->pro are legal; enterprise->
free raises ValueError; pro->free is legal; an illegal transition (for example an
unknown target, or enterprise->free) leaves the stored plan untouched.

Forbidden shortcuts: changing the LEGAL set semantics, weakening tests, or changing
other modules.
