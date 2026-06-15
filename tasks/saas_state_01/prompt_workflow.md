Follow this process to add a "trial" account state to `saasapp.lifecycle`:

1. Inspect `lifecycle.py` and `storage.py` to see how LEGAL_TRANSITIONS, the
   can_transition()/transition() flow, and storage.AUDIT work.
2. Plan the exact set of (from, to) pairs to add: trial->active and trial->closed
   only. Note which pairs must stay illegal (active->trial, closed->trial).
3. Make the minimal change in lifecycle.py: extend LEGAL_TRANSITIONS with the two new
   outbound trial transitions, and nothing else.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the existing active/closed transitions, the audit
   logging, and storage.py are unchanged.
