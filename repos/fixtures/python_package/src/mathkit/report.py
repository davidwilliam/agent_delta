"""Reporting helpers (AgentDelta fixture).

`average_line` uses the deprecated `avg`; the dependency_migration task migrates
it to mathkit.stats.mean and removes the dependency on mathkit.legacy.
"""

from mathkit.legacy import avg


def average_line(values):
    """Return a one-line average summary, e.g. 'average=3.00'."""
    return f"average={avg(values):.2f}"
