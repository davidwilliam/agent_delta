"""Mutant: joins with a hyphen instead of a space."""


def normalize_spaces(s: str) -> str:
    return "-".join(s.split())
