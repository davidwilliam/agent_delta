from mathkit import scoring


def percent(score, max_score):
    return scoring.normalize(score, max_score)
