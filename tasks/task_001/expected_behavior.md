# Expected behavior - task_001

A correct solution adds `median` to `src/mathkit/stats.py`:

```python
def median(values):
    if not values:
        raise ValueError("median() requires at least one value")
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2
```

and exports it from `src/mathkit/__init__.py`.

Key discriminators:
- Even-length input → average of the two middle values (not just one).
- Unsorted input → must sort first.
- Empty input → `ValueError`.
- Must not mutate the caller's list (use `sorted`, not `list.sort`).
