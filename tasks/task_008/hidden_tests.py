"""Hidden tests for task_008 (dependency migration).

Verifies the migration actually happened: avg removed, report references mean,
behavior preserved.
"""

import inspect

import mathkit.legacy
import mathkit.report
from mathkit.report import average_line


def test_avg_removed_from_legacy():
    assert not hasattr(mathkit.legacy, "avg")


def test_report_uses_mean_not_avg():
    src = inspect.getsource(mathkit.report)
    assert "avg" not in src
    assert "mean" in src


def test_behavior_unchanged():
    assert average_line([1, 2, 3]) == "average=2.00"
