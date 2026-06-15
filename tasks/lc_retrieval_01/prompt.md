You are working in the `ledger` package, a large multi-schema ledger whose entries are
split across many parts under `src/ledger/entries/` (part_000, part_001, ...). Entry
fields vary by part: the amount is named amount, value, or amt, and the kind is named
kind, type, or category.

Add an official credit total. In a new module `ledger/official_credit.py`, provide
`official_credit_total()`: the sum of the amount of every CREDIT entry across the ledger,
counting only the parts that the AUTHORITATIVE reporting policy includes.

This repository contains more than one policy module: an authoritative policy, a draft
note, and a deprecated legacy file, and they give different cutoffs. Find the
AUTHORITATIVE one (it states that it supersedes the others) and read its REPORTING_CUTOFF.
Include only parts whose index (the integer in the filename, e.g. part_037 -> 37) is
strictly less than that cutoff. Do not use the draft or legacy values, and do not
hard-code the number; import it from the authoritative policy module.

Do not edit the entry data under src/ledger/entries/. Keep the change minimal. When
finished, run `pytest -q tests/` and summarize what you added and which policy you used.
