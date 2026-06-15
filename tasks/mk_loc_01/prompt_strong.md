`mathkit.leaderboard.percent(score, max_score)` should return the score as a
whole-number percentage of `max_score`, but every value it returns is too low. For
example `percent(100, 100)` returns 99 and `percent(50, 100)` returns 49.

Requirements:
1. `percent(score, max_score)` must equal `round(100 * score / max_score)` for every
   in-range input.
2. `leaderboard.py` only forwards to a scoring helper; the bug is in that helper.
   Fix the helper and leave `leaderboard.py` unchanged.
3. Keep the change minimal: divide by `max_score`, not by `max_score + 1`.
4. Do not weaken, skip, or delete tests.

When finished, run `pytest -q tests/`.
