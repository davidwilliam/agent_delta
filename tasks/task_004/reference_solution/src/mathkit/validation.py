"""Validation helpers (reference solution for task_004)."""


def require_nonempty(values, name: str = "values") -> None:
    """Raise ValueError if `values` is empty; otherwise return None."""
    if not values:
        raise ValueError(f"{name} requires at least one value")
