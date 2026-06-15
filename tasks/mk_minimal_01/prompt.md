You are working in the `mathkit` package. The module `mathkit.csvlite` exposes
`parse_row(line)`, which is supposed to split a single CSV line into its fields.

The current implementation just does `line.split(",")`, so it breaks on quoted
fields: a comma inside a double-quoted field is wrongly treated as a separator, and
the surrounding quotes are not stripped.

Fix `parse_row` so that it parses quoted fields correctly: commas inside a
double-quoted field are part of the field, surrounding double quotes are stripped, and
a doubled double-quote (`""`) inside a quoted field becomes one literal quote.
Interior spaces must be preserved. Fix the function in place in `csvlite.py`; do not
import the stdlib `csv` module. When finished, run `pytest -q tests/` and summarize
the change.
