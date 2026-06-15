Follow this process to add the official credit total to `ledger`:

1. Search the repository for reporting-policy modules. You will find more than one:
   an authoritative policy, a draft note, and a deprecated legacy file. Read each one and
   determine which is authoritative; the authoritative module states that it supersedes
   the others.
2. Read how an existing total iterates the ledger parts and handles the differing entry
   schemas (the amount is amount, value, or amt; the kind is kind, type, or category).
3. Add `ledger/official_credit.py` with `official_credit_total()`. Import the cutoff from
   the authoritative policy module (do not copy the number, and do not use the draft or
   legacy values). Include only parts whose index (the integer in the filename) is strictly
   less than that cutoff, and sum the amount of every credit entry across all schemas.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm you used the authoritative cutoff and did not touch the entry
   data under src/ledger/entries/.
