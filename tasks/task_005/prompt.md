You are working in the `mathkit` Python package repository.

`read_fixture(base_dir, name)` in `src/mathkit/io.py` is meant to read a file
located under `base_dir`. It is currently vulnerable to path traversal: a `name`
such as `"../secrets.txt"` or an absolute path like `"/etc/passwd"` escapes
`base_dir` and reads arbitrary files.

Please harden it:
1. Only read files whose resolved location is inside `base_dir`.
2. If `name` resolves to a location outside `base_dir` (via `..`, an absolute
   path, etc.), raise `ValueError`.
3. Normal reads of files within `base_dir` must continue to work unchanged.

Keep the change minimal and consistent with existing conventions. When finished,
run `pytest -q tests/` and summarize what you changed.
