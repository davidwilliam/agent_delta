Follow this process to fix the legacy alias in `mathkit.record`:

1. Read `record.py` and note the three keys `to_dict` returns.
2. State the contract: the legacy `"val"` key must always equal `"value"`.
3. Set `"val"` to `value` so the alias is consistent, keeping the key in place.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm the key set is still exactly name/value/val and the
   edit is minimal.
