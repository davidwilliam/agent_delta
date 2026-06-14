# Expected behavior — task_002

Fix the loop bound in `chunk` so it walks the whole sequence:

```python
def chunk(seq, size):
    if size <= 0:
        raise ValueError("size must be a positive integer")
    return [list(seq[i : i + size]) for i in range(0, len(seq), size)]
```

Key discriminators:
- Non-multiple length → trailing partial chunk is kept (`[1,2,3,4,5]/2 → [[1,2],[3,4],[5]]`).
- `size > len(seq)` → one chunk with all items (base returns `[]`).
- Empty sequence → `[]`.
- Non-positive size → still `ValueError`.
