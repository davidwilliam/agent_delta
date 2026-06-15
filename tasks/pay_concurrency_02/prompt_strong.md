Make `payments.sequence.next_id` safe under concurrent calls.

`next_id()` currently does an unlocked read-modify-write with simulated latency, so
concurrent callers read the same starting value and hand out duplicate ids.

Requirements:
1. Concurrent callers must never receive duplicate ids: with N concurrent callers
   the returned ids are exactly the set 1..N and the maximum is N.
2. Sequential calls must keep returning 1, 2, 3 in order.
3. After `reset()` the sequence must restart at 1.
4. Do not remove the simulated latency; keep it inside the critical section so it
   still models real work without reintroducing the race.
5. Do not weaken, skip, or delete tests; do not change other modules.

When finished, run `pytest -q tests/`.
