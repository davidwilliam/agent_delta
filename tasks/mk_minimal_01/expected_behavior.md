# Expected behavior - mk_minimal_01

`mathkit.csvlite.parse_row(line)` must split a single CSV line into fields while
honoring double-quoted fields:

- Top-level commas separate fields.
- A comma inside a double-quoted field is part of the field, not a separator.
- The double quotes surrounding a field are stripped from the result.
- A doubled double-quote (`""`) inside a quoted field is a single literal quote.
- Interior leading and trailing spaces are preserved.
- An empty line yields `['']`; a trailing comma yields a trailing empty field.

Examples:
- `parse_row('a,b,c') == ['a', 'b', 'c']`
- `parse_row('a,"b,c",d') == ['a', 'b,c', 'd']`
- `parse_row('"x""y"') == ['x"y']`
- `parse_row('"hello, world",ok') == ['hello, world', 'ok']`
- `parse_row('a,"",b') == ['a', '', 'b']`
- `parse_row('') == ['']`

Why the obvious solution fails:
- The shipped `return line.split(",")` passes the plain unquoted case but mis-splits
  a quoted comma into two fields and leaves the surrounding quotes in the values. It
  also cannot represent a doubled-quote escape.

The reference fix is a small char-by-char state machine that tracks whether it is
inside a quoted field. It does not import the stdlib `csv` module; the task is to fix
the parser itself.

Discriminators (hidden): quoted comma kept in one field, surrounding quotes stripped,
doubled-quote escape, empty quoted field, trailing empty field, preserved interior
spaces.

Forbidden shortcuts: importing the `csv` module, rewriting the parser into a
different module, or weakening tests.
