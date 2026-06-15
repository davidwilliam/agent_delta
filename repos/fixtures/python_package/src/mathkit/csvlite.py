"""Minimal CSV row parser.

NOTE (fixture): `parse_row` is intentionally buggy on quoted fields. The
AgentDelta mk_minimal_01 task fixes it. It is untested by the baseline suite, so
the baseline stays green.
"""


def parse_row(line):
    """Split a single CSV line into its fields."""
    # BUG: naive split does not honor quotes, so a quoted comma is mis-split
    # and surrounding quotes are not stripped.
    return line.split(",")
