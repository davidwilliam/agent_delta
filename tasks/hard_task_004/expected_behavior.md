# Expected behavior - hard_task_004

Make the check-and-create atomic. The minimal correct fix is a module-level lock
around the existence check and the write (see reference); a per-event lock or an
atomic `dict.setdefault` registry also works.

Why the obvious fixes fail:
- The base check-then-act lets concurrent callers all pass the existence check
  before any write completes (the storage write latency guarantees the overlap),
  so duplicates are created.
- An unlocked in-memory `seen` set has the same race (check membership, then add,
  non-atomically).
- Removing the storage latency or deduping by amount is forbidden and breaks the
  intent (the latency is fixed; distinct events with equal amounts are distinct).

Discriminators: concurrent same-event -> exactly one invoice; concurrent distinct
events -> each created once (the lock must not drop or merge them).
