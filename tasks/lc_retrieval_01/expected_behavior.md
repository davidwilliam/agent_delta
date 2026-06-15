# Expected behavior - lc_retrieval_01

The correct solution adds `ledger/official_credit.py` with `official_credit_total()`,
which sums the amount of every credit entry across all schema variants, counting only the
parts whose index is strictly less than the AUTHORITATIVE reporting cutoff. The cutoff is
read from `ledger.policy.official_policy` (REPORTING_CUTOFF = 150), which states that it
supersedes every draft note and legacy file. The expected value is 140250.

Why the obvious solutions fail:
- Summing every part (the task_009 approach) ignores the cutoff and yields 205700.
- Using the draft note cutoff (ledger.notes.draft_policy, 120) yields 112200; the draft is
  explicitly NOT approved.
- Using the deprecated legacy cutoff (ledger.legacy.old_policy, 200) yields 187017; it is
  explicitly superseded.
- Handling only the first schema variant (amount/kind) undercounts, because credits are
  spread across the amount/value/amt and kind/type/category schemas.

Discriminators (hidden): the value equals the authoritative 140250; it is not the
all-parts total (205700) and is strictly less than it; it is not the draft-cutoff result
(112200); it is not the legacy-cutoff result (187017).

Forbidden shortcuts: using the draft or legacy cutoff, editing the entry data under
src/ledger/entries/, or weakening tests.
