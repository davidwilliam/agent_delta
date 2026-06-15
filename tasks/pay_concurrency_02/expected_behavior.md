# Expected behavior - pay_concurrency_02

The correct solution makes the read-modify-write in `sequence.next_id` atomic, for
example with a module-level `threading.Lock` held across the read, the simulated
latency, and the write. The simulated latency stays in place; only the update is
serialized.

Why the obvious solution fails:
- The base `next_id` reads the current counter, sleeps, then writes back current +
  1 with no synchronization. Under concurrent callers, two callers read the same
  starting value before either writes, so both return the same id and the sequence
  skips values (duplicate ids, max below N). The simulated latency guarantees the
  overlap.
- Removing the latency to dodge the race is forbidden; it hides the bug rather than
  fixing the concurrency.

Discriminators (hidden): high-concurrency calls yield distinct ids; the returned
ids are exactly the set 1..N; after reset the sequence restarts at 1.

Forbidden shortcuts: removing the simulated latency, weakening tests, or changing
other modules.
