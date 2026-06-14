# Expected behavior - task_008

Migrate `report.py` to use `mathkit.stats.mean` and remove `avg` from
`mathkit.legacy`:

```python
# report.py
from mathkit.stats import mean

def average_line(values):
    return f"average={mean(values):.2f}"
```

```python
# legacy.py  (avg removed)
```

Key discriminators:
- `avg` no longer exists on `mathkit.legacy`.
- `report.py` source references `mean`, not `avg`.
- `average_line` output is unchanged.
