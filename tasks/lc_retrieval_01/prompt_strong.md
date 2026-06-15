Add an official credit total to the `ledger` package.

Expose, in a new module `ledger/official_credit.py`:
- `official_credit_total()`: the sum of the amount of every CREDIT entry across the
  ledger, but counting only the parts that the AUTHORITATIVE reporting policy includes.

Requirements:
1. The set of parts to include is governed by an authoritative reporting cutoff. This
   repository contains more than one policy module: an authoritative one, a draft note,
   and a deprecated legacy file. Find the AUTHORITATIVE policy and use its cutoff. Ignore
   the draft and legacy values, which give different (wrong) cutoffs.
2. Include only parts whose index (the integer in the filename, e.g. part_037 -> 37) is
   strictly less than the authoritative REPORTING_CUTOFF. Read the cutoff from the
   authoritative policy module rather than hard-coding the number.
3. Entry fields are named differently across parts: the amount is amount, value, or amt,
   and the kind is kind, type, or category. Handle every schema variant.
4. Do not edit the ledger entry data under src/ledger/entries/, and do not weaken tests.

When finished, run `pytest -q tests/`.
