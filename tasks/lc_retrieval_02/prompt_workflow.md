Follow this process to add the official net total to `ledger`:

1. Search the repository for reporting-policy modules. You will find more than one:
   an authoritative policy, a draft note, and a deprecated legacy file. Read each one and
   determine which is authoritative; the authoritative module states that it supersedes
   the others, and it carries the excluded-parts list to use.
2. Read how an existing total iterates the ledger parts and handles the differing entry
   schemas (the amount is amount, value, or amt; the kind is kind, type, or category).
3. Add `ledger/official_net.py` with `official_net_total()`. Import EXCLUDED_PARTS from the
   authoritative policy module (do not copy the list, and do not use the draft or legacy
   values). Compute the sum of credit amounts minus the sum of debit amounts over every
   part whose index (the integer in the filename) is NOT in that list, across all schemas.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm you used the authoritative exclusion list and did not touch
   the entry data under src/ledger/entries/.
