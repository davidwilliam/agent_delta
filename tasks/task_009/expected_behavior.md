# Expected behavior - task_009

Add `src/ledger/totals.py` that aggregates across all parts and all schema
variants (see the reference solution). The three schemas are:

- variant 0: `{"amount": .., "kind": ..}`
- variant 1: `{"value": .., "type": ..}`
- variant 2: `{"amt": .., "category": ..}`

Key discriminators:
- Handling only variant 0 undercounts both totals (the data is split across all
  three), so `total_credits() == 205700` and `total_debits() == 411400` only hold
  when every variant is handled.
- The fixture is ~228k content tokens, so discovering all three schemas benefits
  from reading widely; this is the long-context discriminator (SPEC 21).
