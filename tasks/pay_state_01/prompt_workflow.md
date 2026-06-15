Follow this process to add a payment status lifecycle to `payments`:

1. Read `webhook.py`, `models.py`, and `storage.py` to see how an invoice is created
   and looked up (`storage.find_by_event`).
2. List the states and the legal transitions, and note that "refunded" is terminal.
3. Add a new `payments.payment_state` module with a per-event status ledger and an
   audit list. Default a known event to "paid", enforce only legal transitions,
   record each transition, and raise ValueError on illegal moves and KeyError for
   unknown events.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the Invoice model, storage, and webhook are unchanged.
