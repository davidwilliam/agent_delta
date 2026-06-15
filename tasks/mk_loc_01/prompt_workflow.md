Follow this process to fix the leaderboard percentage in `mathkit`:

1. Read `leaderboard.py` and confirm `percent` just forwards to a scoring helper.
2. Open the helper that `percent` calls and read how it computes the percentage.
3. Identify the off-by-one in the denominator (it divides by `max_score + 1`).
4. Fix the helper so it divides by `max_score`, leaving `leaderboard.py` untouched.
5. Run `pytest -q tests/`.
6. If anything fails, debug once and re-run.
7. Review your diff: confirm only the scoring helper changed and the edit is minimal.
