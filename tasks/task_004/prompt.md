You are working in the `mathkit` Python package repository.

Both `mean` and `variance` in `src/mathkit/stats.py` duplicate the same guard:

```python
if not values:
    raise ValueError("... requires at least one value")
```

Please refactor this duplication into a shared helper:

1. Create `src/mathkit/validation.py` with a function
   `require_nonempty(values, name="values")` that raises
   `ValueError` when `values` is empty and otherwise returns `None`.
2. Update `mean` and `variance` in `stats.py` to call `require_nonempty`
   instead of their inline checks.
3. The observable behavior of `mean` and `variance` must not change - they must
   still raise `ValueError` on empty input and return the same results otherwise.

Keep the change focused. When finished, run `pytest -q tests/` and summarize the
refactor.
