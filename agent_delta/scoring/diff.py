"""Diff metrics for diagnostic reporting (SPEC sections 7, 13.3).

Parses a unified diff into files touched, hunks, added/removed lines, the
test-to-code change ratio, diff locality, and patch entropy. These are
diagnostic (not ranking) signals unless explicitly promoted in the scoring config.
"""

from __future__ import annotations

import math


def _is_test_file(path: str, language: str) -> bool:
    if language == "go":
        return path.endswith("_test.go")
    base = path.rsplit("/", 1)[-1]
    return path.startswith("tests/") or "/tests/" in path or (
        base.startswith("test_") and base.endswith(".py")
    )


def parse_diff(diff_text: str, language: str = "python") -> dict:
    """Return diff metrics for a unified diff."""
    per_file: dict[str, list[int]] = {}
    cur: str | None = None
    hunks = 0
    for line in (diff_text or "").splitlines():
        if line.startswith("+++ "):
            p = line[4:].strip()
            cur = p[2:] if p.startswith("b/") else (None if p == "/dev/null" else p)
            if cur:
                per_file.setdefault(cur, [0, 0])
        elif line.startswith("@@"):
            hunks += 1
        elif line.startswith("+") and not line.startswith("+++"):
            if cur:
                per_file[cur][0] += 1
        elif line.startswith("-") and not line.startswith("---"):
            if cur:
                per_file[cur][1] += 1

    files = list(per_file)
    total = sum(a + r for a, r in per_file.values())
    test_lines = sum(a + r for f, (a, r) in per_file.items() if _is_test_file(f, language))
    code_lines = total - test_lines

    entropy = 0.0
    if total > 0:
        for a, r in per_file.values():
            p = (a + r) / total
            if p > 0:
                entropy -= p * math.log2(p)

    return {
        "files_touched": len(files),
        "hunks": hunks,
        "lines_added": sum(a for a, _ in per_file.values()),
        "lines_removed": sum(r for _, r in per_file.values()),
        "test_lines_changed": test_lines,
        "code_lines_changed": code_lines,
        "test_to_code_ratio": (test_lines / code_lines) if code_lines else None,
        "diff_locality": (1.0 / len(files)) if files else 1.0,
        "patch_entropy": entropy,
    }
