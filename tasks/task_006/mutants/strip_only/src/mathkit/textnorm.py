"""Mutant: strips the ends but does not collapse internal whitespace."""


def normalize_spaces(s: str) -> str:
    return s.strip()
