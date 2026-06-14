# Expected behavior — task_003

Add `slugify` to `src/mathkit/text.py` and export it:

```python
import re

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
```

Key discriminators:
- Runs of separators collapse to a single hyphen (`a--b__c → a-b-c`).
- Leading/trailing hyphens stripped (`---Foo--- → foo`).
- All-separator input → empty string.
- Digits preserved.
- Exported from `mathkit` (`from mathkit import slugify`).
