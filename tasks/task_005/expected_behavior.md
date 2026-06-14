# Expected behavior — task_005

Harden `read_fixture` with a realpath-containment check:

```python
import os

def read_fixture(base_dir, name):
    base = os.path.realpath(base_dir)
    path = os.path.realpath(os.path.join(base, name))
    if path != base and not path.startswith(base + os.sep):
        raise ValueError(f"unsafe path: {name!r} escapes the base directory")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```

Key discriminators:
- `..` traversal and absolute paths raise `ValueError` (a naive "reject if `..`
  in name" misses the absolute-path case and fails `test_absolute_passwd_raises`).
- Resolution-based: containment is checked after `realpath`, so legitimate nested
  reads still work.
- Normal reads within `base_dir` unchanged.
