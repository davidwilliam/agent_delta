Follow this process to add partial refunds to `payments`:

1. Read `webhook.py`, `models.py`, and `storage.py` to see how an invoice and its
   amount are represented and looked up.
2. State the invariant the refund total must satisfy for each event.
3. Add the smallest refund API that enforces it (record total, reject over-refunds
   atomically, reject non-positive amounts and unknown events).
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the Invoice model and storage seed are unchanged.
