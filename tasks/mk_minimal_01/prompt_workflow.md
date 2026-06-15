Follow this process to fix the CSV row parser in `mathkit.csvlite`:

1. Read `csvlite.py` and note why `line.split(",")` is wrong for quoted fields.
2. State the quoting rules: top-level commas separate fields; a comma inside double
   quotes is literal; surrounding quotes are stripped; a doubled double-quote (`""`)
   inside quotes is one literal quote; interior spaces are preserved.
3. Rewrite `parse_row` in place as a small char-by-char state machine that tracks
   whether it is inside a quoted field. Do not import the stdlib `csv` module.
4. Run `pytest -q tests/`.
5. If anything fails, debug once and re-run.
6. Review your diff: confirm only `parse_row` changed and the change stayed small.
