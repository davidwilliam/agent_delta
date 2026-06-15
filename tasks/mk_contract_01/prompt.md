`mathkit.record.to_dict(name, value)` builds the dict representation of a record. For
backward compatibility it includes a legacy `"val"` key alongside the modern
`"value"` key, and older consumers rely on `"val"` always carrying the same data as
`"value"`. Right now `"val"` is always `None`, which breaks those consumers.

Fix `to_dict` so the legacy `"val"` alias always equals `"value"`. Keep the legacy
key (do not drop or rename it) and keep the change minimal.

When finished, run `pytest -q tests/` and summarize the fix.

## Required API (the tests import these exact names)

- Module `mathkit.record` exposing `to_dict(name, value)` (returns a dict with keys `name`, `value`, and `val`).
