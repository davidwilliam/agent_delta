You are working in the `mathkit` Python package repository.

Please add a new module `src/mathkit/paths.py` with `simplify_path(path)` that
canonicalizes an absolute Unix-style path (the input always begins with `/`).

Rules:
- Collapse multiple consecutive slashes into one.
- A `.` segment refers to the current directory and is removed.
- A `..` segment moves up one directory; at the root it has no effect (you cannot
  go above `/`).
- Any other segment is an ordinary directory name. Note that `...` (or longer
  runs of dots) is a normal name, not a parent reference.
- The result is the canonical absolute path with no trailing slash, except the
  root which is `/`.

Examples: `/a/./b/../../c/` -> `/c`; `/../` -> `/`; `/home//foo/` -> `/home/foo`;
`/...` -> `/...`.

Keep the change minimal. Add tests as needed, run `pytest -q tests/`, and
summarize.
