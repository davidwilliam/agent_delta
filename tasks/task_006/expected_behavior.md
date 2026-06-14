# Expected behavior - task_006

Add `tests/test_textnorm.py` with tests that pin the real behavior of
`normalize_spaces`:

- collapsing runs of spaces (`"a   b"` -> `"a b"`) kills the strip-only, noop, and
  wrong-separator mutants,
- stripping the ends (`"  hi  "` -> `"hi"`) kills the noop mutant,
- handling tabs and newlines (`"a\t\nb"` -> `"a b"`),
- single word and empty string as boundary cases.

A weak suite that only checks a single already-normalized string would pass on the
correct code but fail to kill the mutants, scoring zero on the mutation metric.
