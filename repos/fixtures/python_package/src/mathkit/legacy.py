"""Deprecated helpers (AgentDelta fixture).

`avg` is a deprecated alias for mathkit.stats.mean. The dependency_migration task
removes it and migrates callers to mean.
"""

from mathkit.stats import mean


def avg(values):
    """Deprecated: use mathkit.stats.mean instead."""
    return mean(values)
