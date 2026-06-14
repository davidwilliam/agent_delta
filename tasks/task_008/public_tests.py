"""Public tests for task_008 (dependency migration). Injected at score time."""

from mathkit.report import average_line


def test_average_line_works():
    assert average_line([2, 4]) == "average=3.00"


def test_average_line_other():
    assert average_line([10, 20, 30]) == "average=20.00"
