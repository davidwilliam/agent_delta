Follow this process to fix the proration off-by-one in `payments`:

1. Read `payments/proration.py` and identify the formula it uses.
2. Compare it to the intended formula: amount * days_used // days_total.
3. Spot the off-by-one: the denominator is days_total - 1 instead of days_total.
4. Apply the smallest fix (remove the - 1). Do not rewrite the function or add
   helpers.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm it is a one-token change and nothing else moved.
