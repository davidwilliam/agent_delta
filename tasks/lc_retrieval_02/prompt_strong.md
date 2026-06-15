Add an official net total to the `ledger` package.

Expose, in a new module `ledger/official_net.py`:
- `official_net_total()`: the sum of all CREDIT amounts minus the sum of all DEBIT
  amounts across the ledger, computed over every part EXCEPT the parts that the
  AUTHORITATIVE reporting policy excludes.

Requirements:
1. The parts to exclude are governed by an authoritative excluded-parts list. This
   repository contains more than one policy module: an authoritative one, a draft note,
   and a deprecated legacy file. Find the AUTHORITATIVE policy and use its EXCLUDED_PARTS.
   Ignore the draft and legacy lists, which differ and are wrong here.
2. A part's index is the integer in its filename (e.g. part_037 -> 37). Drop every part
   whose index is in the authoritative EXCLUDED_PARTS, and include all others. Read the
   list from the authoritative policy module rather than hard-coding it.
3. Entry fields are named differently across parts: the amount is amount, value, or amt,
   and the kind is kind, type, or category. Handle every schema variant.
4. Do not edit the ledger entry data under src/ledger/entries/, and do not weaken tests.

When finished, run `pytest -q tests/`.
