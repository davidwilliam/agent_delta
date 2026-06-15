You are working in the `payments` service. `payments.wallet` is an in-memory
balance store: `credit(acct, amount)` adds `amount` to an account and returns the
new balance, `balance(acct)` reads it, and `reset()` clears the store.

`credit` does an unlocked read-modify-write with simulated write latency: it reads
the current balance, waits, then writes back current + amount. Under concurrent
credits to the same account, two callers both read the same starting balance before
either writes, so updates are lost and the final balance is too low.

Make `credit` safe under concurrent updates so that concurrent credits to the same
account never lose updates and the final balance equals the sum of all credits.
Sequential credits must keep accumulating correctly, and distinct accounts must
stay independent.

Do not remove the simulated latency, and keep the change minimal and in the wallet
layer. When finished, run `pytest -q tests/` and summarize what you changed and how
concurrency safety is enforced.
