"""Reporting helpers (reference solution for task_008)."""

from mathkit.stats import mean


def average_line(values):
    """Return a one-line average summary, e.g. 'average=3.00'."""
    return f"average={mean(values):.2f}"
