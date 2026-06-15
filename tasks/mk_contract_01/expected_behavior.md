# Expected behavior - mk_contract_01

The correct solution sets the legacy `"val"` key to `value` so that
`mathkit.record.to_dict(name, value)` returns
`{"name": name, "value": value, "val": value}`.

The `"val"` key is a backward-compatible alias that downstream consumers expect to
mirror `"value"`. At base it is hardcoded to `None`, breaking the contract.

Why the obvious shortcut fails:
- Dropping or renaming the `"val"` key removes the legacy alias and breaks the older
  consumers that depend on it. The fix must keep the key and make it equal `"value"`.

Discriminators (hidden): `"val"` equals `"value"` for several inputs, including `0`,
a negative number, and a string value; the key set is exactly name/value/val.

Forbidden shortcuts: removing or renaming the legacy `"val"` key, or weakening tests.
