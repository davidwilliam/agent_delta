"""Baseline test for mathkit.report (must keep passing).

Tests only the observable output of average_line, so it stays green both before
the dependency migration (avg) and after it (mean).
"""

from mathkit.report import average_line


def test_average_line():
    assert average_line([2, 4]) == "average=3.00"


def test_average_line_single():
    assert average_line([5]) == "average=5.00"
