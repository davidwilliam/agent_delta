# Expected behavior - lc_retrieval_02

The correct solution adds `ledger/official_net.py` with `official_net_total()`, which
returns the sum of all credit amounts minus the sum of all debit amounts across every
schema variant, computed over every part EXCEPT those named in the AUTHORITATIVE excluded-
parts list. The list is read from `ledger.policy.official_policy` (EXCLUDED_PARTS =
[3, 17, 142]), which states that it supersedes every draft note and legacy file. The
expected value is -202935.

Why the obvious solutions fail:
- Excluding nothing yields the no-exclusion net 205700 - 411400 = -205700.
- Using the deprecated legacy exclusion list (ledger.legacy.old_policy, [5, 9]) yields
  -203816; it is explicitly superseded.
- The draft note (ledger.notes.draft_policy) excludes nothing and is explicitly NOT
  approved.
- Handling only the first schema variant (amount/kind) miscounts, because credits and
  debits are spread across the amount/value/amt and kind/type/category schemas.

Discriminators (hidden): the value equals the authoritative -202935; it is not the
no-exclusion net (-205700); it is not the legacy-exclusion net (-203816).

Forbidden shortcuts: using the draft or legacy exclusion list, editing the entry data
under src/ledger/entries/, or weakening tests.
