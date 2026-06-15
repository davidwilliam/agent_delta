# Expected behavior - task_012

Split on `/`, push real segments, drop `.` and empty, pop on `..` only when the
stack is non-empty, then join under root (see reference).

Discriminators: `..` past root must be a no-op (not produce `/..`), `...` and
longer dot-runs are ordinary names, redundant slashes collapse, and there is no
trailing slash except for root `/`.
