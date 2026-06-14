You are working in the `ledger` package, a large ledger split across many files
under `src/ledger/entries/` (`part_000.py` through `part_219.py`). Each part
defines an `ENTRIES` list of record dicts.

Please add `src/ledger/totals.py` with two functions:

1. `total_credits()` returns the sum of the amount of every credit entry across
   all parts.
2. `total_debits()` returns the sum of the amount of every debit entry across all
   parts.

Important: the entry record schema is not uniform across the parts. The field
names for the amount and the kind differ between parts. Inspect the data widely
to make sure you handle every variant, or your totals will be wrong.

When finished, run `pytest -q tests/` and summarize what schemas you found and how
you handled them.
