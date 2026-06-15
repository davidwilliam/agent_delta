"""Hidden tests for mk_loc_01: percentage correctness across inputs."""

from mathkit.leaderboard import percent


def test_zero_score_is_zero():
    assert percent(0, 100) == 0


def test_full_small_scale():
    assert percent(1, 1) == 100


def test_three_quarters():
    assert percent(3, 4) == 75


def test_matches_plain_percentage_formula():
    cases = [(0, 100), (1, 1), (3, 4), (50, 100), (100, 100), (2, 3), (7, 8)]
    for score, max_score in cases:
        assert percent(score, max_score) == round(100 * score / max_score)
