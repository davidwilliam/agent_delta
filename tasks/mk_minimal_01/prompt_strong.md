Fix `parse_row(line)` in `mathkit.csvlite` so it parses a single CSV line correctly.

Required behavior:
1. Top-level commas separate fields.
2. A comma inside a double-quoted field is part of the field, not a separator.
3. The double quotes surrounding a field are stripped from the result.
4. A doubled double-quote (`""`) inside a quoted field becomes one literal quote.
5. Leading and trailing spaces inside a field are preserved.
6. An empty line yields `['']`; a trailing comma yields a trailing empty field.

Examples:
- `parse_row('a,b,c') == ['a', 'b', 'c']`
- `parse_row('a,"b,c",d') == ['a', 'b,c', 'd']`
- `parse_row('"x""y"') == ['x"y']`
- `parse_row('"hello, world",ok') == ['hello, world', 'ok']`

Constraints: fix the function in place in `csvlite.py`, keep the change small, and do
not import the stdlib `csv` module. When finished, run `pytest -q tests/`.
