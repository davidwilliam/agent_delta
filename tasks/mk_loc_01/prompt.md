The `mathkit` leaderboard shows each entrant's score as a percentage via
`mathkit.leaderboard.percent(score, max_score)`. The percentages it reports are
slightly too low: a perfect run (`percent(100, 100)`) shows 99 instead of 100.

Track down why the percentage is wrong and fix it at the source. `leaderboard.py`
itself is just a thin wrapper, so do not edit it; the real defect is in the helper it
calls. Keep the change minimal.

When finished, run `pytest -q tests/` and summarize what was wrong and where you
fixed it.
