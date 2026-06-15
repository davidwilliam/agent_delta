Make `saasapp.subscription.change_plan` validate plan transitions.

`change_plan(tenant, new)` currently stores the new plan unconditionally, so it
allows illegal jumps. The plan ladder is free <-> pro <-> enterprise.

Requirements:
1. `change_plan` must apply a transition only when `(current, new)` is in `LEGAL`,
   where `current` is the tenant's current plan (default "free").
2. An illegal transition must raise `ValueError` and must leave the stored plan
   unchanged.
3. free->pro is legal; free->enterprise is illegal (must go free->pro->enterprise).
4. pro->enterprise and enterprise->pro are legal; enterprise->free is illegal (must
   go enterprise->pro->free); pro->free is legal.
5. Keep the `LEGAL` set and its semantics exactly as they are.
6. The fix is only in subscription.py. Do not weaken, skip, or delete tests; do not
   change other modules.

When finished, run `pytest -q tests/`.
