# Expected behavior - mk_loc_01

The correct solution fixes the off-by-one in the scoring helper so that
`mathkit.leaderboard.percent(score, max_score)` returns
`round(100 * score / max_score)`.

`leaderboard.percent` simply forwards to `scoring.normalize`, which divides by
`max_score + 1` instead of `max_score`. The root-cause fix is to divide by
`max_score` in `scoring.py`.

Why the obvious shortcut fails:
- The symptom is visible through `leaderboard.percent`, so an agent may try to patch
  `leaderboard.py` (for example by passing a tweaked argument or post-correcting the
  result). That edits the wrong file, leaves the shared helper wrong for any other
  caller, and is forbidden by scope.

Discriminators (hidden): `percent(0, 100) == 0`, `percent(1, 1) == 100`,
`percent(3, 4) == 75`, and every value matches `round(100 * score / max_score)`.

Forbidden shortcuts: editing `leaderboard.py`, or weakening tests.
