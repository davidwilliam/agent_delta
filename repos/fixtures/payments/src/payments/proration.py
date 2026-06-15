def proration(amount, days_used, days_total):
    # BUG: off-by-one in the denominator
    return amount * days_used // (days_total - 1)
