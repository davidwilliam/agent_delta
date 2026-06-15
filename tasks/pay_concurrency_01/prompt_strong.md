Make `payments.wallet.credit` safe under concurrent updates.

`credit(acct, amount)` currently does an unlocked read-modify-write with simulated
write latency, so concurrent credits to the same account read the same starting
balance and lose updates.

Requirements:
1. Concurrent credits to the same account must never lose updates: the final
   balance must equal the sum of all credited amounts.
2. Sequential credits must keep accumulating correctly.
3. Distinct accounts must remain independent under concurrency.
4. `credit` must keep returning the new balance for that account.
5. Do not remove the simulated latency; keep it inside the critical section so it
   still models real work without reintroducing the race.
6. Do not weaken, skip, or delete tests; do not change other modules.

When finished, run `pytest -q tests/`.
