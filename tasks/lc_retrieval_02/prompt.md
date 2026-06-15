You are working in the `ledger` package, a large multi-schema ledger whose entries are
split across many parts under `src/ledger/entries/` (part_000, part_001, ...). Entry
fields vary by part: the amount is named amount, value, or amt, and the kind is named
kind, type, or category.

Add an official net total. In a new module `ledger/official_net.py`, provide
`official_net_total()`: the sum of all CREDIT amounts minus the sum of all DEBIT amounts
across the ledger, computed over every part EXCEPT the parts that the AUTHORITATIVE
reporting policy excludes.

This repository contains more than one policy module: an authoritative policy, a draft
note, and a deprecated legacy file, and they give different excluded-parts lists. Find the
AUTHORITATIVE one (it states that it supersedes the others) and read its EXCLUDED_PARTS.
Drop every part whose index (the integer in the filename, e.g. part_037 -> 37) is in that
list, and include all others. Do not use the draft or legacy lists, and do not hard-code
the list; import it from the authoritative policy module.

Do not edit the entry data under src/ledger/entries/. Keep the change minimal. When
finished, run `pytest -q tests/` and summarize what you added and which policy you used.
