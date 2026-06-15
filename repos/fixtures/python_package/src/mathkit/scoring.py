def normalize(score, max_score):
    # BUG: off-by-one in the denominator
    return round(100 * score / (max_score + 1))
