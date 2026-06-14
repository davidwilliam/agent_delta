# Expected behavior - task_010

Create `src/mathkit/intervals.py` with `merge_intervals` (see reference). Sort by
start, then sweep merging when `start <= current_end` (so touching intervals
merge), taking `max` of ends (so nested intervals are absorbed).

Discriminators in the hidden tests: unsorted input (must sort), nested intervals
(must `max` the end), adjacency (`<=` not `<`), negatives, duplicates, single.
