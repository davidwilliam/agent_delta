You are working in the `payments` service. `payments.sequence` is an in-memory id
generator: `next_id()` returns the next id and increments an internal counter,
`reset()` clears the counter back to zero.

`next_id` does an unlocked read-modify-write with simulated latency: it reads the
current counter, waits, then writes back current + 1 and returns it. Under
concurrent callers, two callers both read the same starting value before either
writes, so they hand out the same id and the sequence skips values.

Make `next_id` safe under concurrent calls so that every returned id is unique and
monotonic: with N concurrent callers the returned ids are exactly the set 1..N.
Sequential calls must keep returning 1, 2, 3 in order, and after `reset()` the
sequence must restart at 1.

Do not remove the simulated latency, and keep the change minimal and in the
sequence layer. When finished, run `pytest -q tests/` and summarize what you
changed and how concurrency safety is enforced.
