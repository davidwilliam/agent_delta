`mathkit.record.to_dict(name, value)` returns a record dict with three keys:
`"name"`, `"value"`, and a legacy `"val"` alias. The contract is that `"val"` always
equals `"value"`, but `to_dict` currently sets `"val"` to `None`.

Requirements:
1. `to_dict(name, value)` must return exactly the keys `"name"`, `"value"`, and
   `"val"`, with no extras and none removed.
2. `"val"` must always equal `"value"` for any input, including `0`, a negative
   number, and a string value.
3. Keep the legacy `"val"` key: do not drop it or rename it.
4. Do not weaken, skip, or delete tests.

When finished, run `pytest -q tests/`.
