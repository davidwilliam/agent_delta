You are working in the `mathkit` Python package repository.

Please add a new module `src/mathkit/roman.py` with two functions:

1. `int_to_roman(n)` converts an integer in the range 1..3999 to a Roman numeral
   string, using standard subtractive notation (4 = IV, 9 = IX, 40 = XL,
   90 = XC, 400 = CD, 900 = CM). Raise `ValueError` for n outside 1..3999.
2. `roman_to_int(s)` converts a valid Roman numeral string back to an integer.

The two must round-trip: `roman_to_int(int_to_roman(n)) == n` for all n in
1..3999.

Keep the change minimal and consistent with the existing conventions. Add tests
as needed, run `pytest -q tests/`, and summarize what you implemented.
