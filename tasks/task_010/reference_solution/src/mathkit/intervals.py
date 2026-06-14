"""Interval utilities (reference solution for task_010)."""


def merge_intervals(intervals):
    """Merge overlapping and touching intervals; tolerant of unsorted/nested input."""
    if not intervals:
        return []
    ordered = sorted((list(iv) for iv in intervals), key=lambda iv: iv[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
