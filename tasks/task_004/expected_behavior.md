# Expected behavior — task_004

New `src/mathkit/validation.py`:

```python
def require_nonempty(values, name="values"):
    if not values:
        raise ValueError(f"{name} requires at least one value")
```

`src/mathkit/stats.py` updated to use it:

```python
from mathkit.validation import require_nonempty

def mean(values):
    require_nonempty(values, "mean()")
    return sum(values) / len(values)

def variance(values):
    require_nonempty(values, "variance()")
    mu = mean(values)
    return sum((x - mu) ** 2 for x in values) / len(values)
```

Key discriminators:
- The helper exists and raises `ValueError` on empty (list, tuple, string).
- `stats.py` source actually references `require_nonempty` (real refactor).
- `mean`/`variance` results and error behavior are unchanged.
