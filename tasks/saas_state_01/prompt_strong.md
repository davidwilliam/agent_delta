Add a new "trial" account state to `saasapp.lifecycle`.

Requirements:
1. Add these legal transitions: ("trial","active") and ("trial","closed").
2. Keep the existing transitions legal: ("active","closed") and ("closed","active").
3. These must remain ILLEGAL and raise ValueError: ("active","trial") and
   ("closed","trial").
4. Every successful transition must still append (tenant, from, to) to storage.AUDIT
   (the existing transition() already does this; keep it).
5. The fix is only in lifecycle.py (extend LEGAL_TRANSITIONS). Keep transition() and
   can_transition() behavior otherwise identical.
6. Do not modify storage.py or the storage seed; do not weaken tests.

When finished, run `pytest -q tests/`.
