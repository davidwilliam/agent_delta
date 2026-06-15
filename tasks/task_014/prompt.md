You are working in the `mathkit` Python package repository.

Please add a new module `src/mathkit/calc.py` with `calc(expr)` that evaluates an
integer arithmetic expression and returns an `int`.

Requirements:
- Operators `+`, `-`, `*`, `/` with standard precedence (`*` and `/` bind tighter
  than `+` and `-`), left-associative.
- Parentheses for grouping.
- Unary minus (and unary plus), e.g. `-3 + 2` and `2 * -3`.
- Division truncates toward zero, so `-10 / 3 == -3` (not `-4`). Note Python's
  `//` floors, which is the wrong behavior here.
- Whitespace is ignored. Operands are non-negative integer literals.

Examples: `calc("1 + 2 * 3")` is 7; `calc("(1+2)*3")` is 9; `calc("2*-3")` is -6;
`calc("-10/3")` is -3.

Keep the change minimal. Add tests as needed, run `pytest -q tests/`, and
summarize.
