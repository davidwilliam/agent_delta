Follow this process to make `saasapp.subscription.change_plan` validate transitions:

1. Read `subscription.py` and note that `LEGAL` holds the allowed `(from, to)` pairs,
   `plan()` reads the current plan (default "free"), and `change_plan()` currently
   writes the new plan with no validation.
2. State why this is wrong: it allows illegal jumps such as free->enterprise and
   enterprise->free, which should have to go through pro.
3. Make the minimal change in `change_plan`: look up the current plan, and if
   `(current, new)` is not in `LEGAL`, raise `ValueError` without writing; otherwise
   store the new plan and return it. Do not change the `LEGAL` set.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm an illegal transition leaves the stored plan unchanged
   and no other module changed.
