# Expected behavior - task_014

Recursive-descent: `expr` handles `+`/`-`, `term` handles `*`/`/`, `factor`
handles unary `+`/`-`, parentheses, and integer literals (see reference).

Discriminators: truncate-toward-zero division via `int(a / b)` (Python `//`
floors and is wrong for negatives, e.g. `-10 // 3 == -4`), unary minus binding to
the following factor, left-associativity, and nested parentheses.
