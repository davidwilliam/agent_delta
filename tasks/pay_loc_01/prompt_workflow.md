Follow this process to fix the understated gross total in `payments`:

1. Reproduce the symptom: call `payments.reporting.summary()` after creating a few
   invoices and observe that `gross` is lower than the true sum while `count` is
   correct.
2. Trace `summary()` in `reporting.py` to the helper it calls for the gross total.
3. Read that helper and identify why it understates the total (it drops one invoice).
4. Fix the root cause in the helper, not the symptom in `reporting.py`.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm only the aggregate helper changed and that reporting.py,
   the Invoice model, and storage are untouched.
