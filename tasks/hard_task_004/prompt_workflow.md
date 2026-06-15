Follow this process to make webhook invoice creation safe under concurrency:

1. Read `payments/webhook.py` (and how it calls storage) to see the check-then-act
   sequence: it checks for an existing invoice, then writes, with simulated write
   latency in between.
2. State the invariant: for a given `event_id`, exactly one invoice may exist;
   replay returns it; distinct events each get their own invoice, even when two
   threads race.
3. Make the smallest change in the webhook layer to synchronize the check and the
   write so the race cannot create duplicates. Do not deduplicate by amount and do
   not touch storage latency or the models.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff against the requirements: confirm exactly one invoice per event
   under concurrency, replay stays idempotent, distinct events stay distinct, and
   storage latency, models, and tests are unchanged.
