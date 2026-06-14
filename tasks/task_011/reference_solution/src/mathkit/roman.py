"""Roman numeral conversion (reference solution for task_011)."""

_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]
_SYMBOLS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def int_to_roman(n):
    """Convert an integer in 1..3999 to a Roman numeral string."""
    if not isinstance(n, int) or not (1 <= n <= 3999):
        raise ValueError("n must be an integer between 1 and 3999")
    out = []
    for value, symbol in _VALUES:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)


def roman_to_int(s):
    """Convert a Roman numeral string to an integer."""
    total = 0
    prev = 0
    for char in reversed(s):
        value = _SYMBOLS[char]
        if value < prev:
            total -= value
        else:
            total += value
            prev = value
    return total
