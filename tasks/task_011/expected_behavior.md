# Expected behavior - task_011

Create `src/mathkit/roman.py` with `int_to_roman` and `roman_to_int` (see
reference). The standard approach is a greedy value/symbol table including the
subtractive pairs (CM, CD, XC, XL, IX, IV), and a right-to-left scan for parsing
(subtract when a symbol is smaller than the one to its right).

Discriminators: the subtractive cases (40/90/400/900), large composites
(1994 = MCMXCIV), round-trips, and the 1..3999 bounds.
