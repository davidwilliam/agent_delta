# Expected behavior - pay_concurrency_01

The correct solution makes the read-modify-write in `wallet.credit` atomic, for
example with a module-level `threading.Lock` held across the read, the simulated
latency, and the write. The simulated latency stays in place; only the update is
serialized.

Why the obvious solution fails:
- The base `credit` reads the current balance, sleeps, then writes back current +
  amount with no synchronization. Under concurrent credits to the same account, two
  callers read the same starting balance before either writes, so one update
  overwrites the other and the final balance is too low (lost updates). The
  simulated latency guarantees the overlap.
- Removing the latency to dodge the race is forbidden; it hides the bug rather than
  fixing the concurrency.

Discriminators (hidden): high-concurrency credits to one account sum exactly;
distinct accounts stay independent under concurrency; interleaved credits to two
accounts each total correctly; a single credit returns the new balance.

Forbidden shortcuts: removing the simulated latency, weakening tests, or changing
other modules.
