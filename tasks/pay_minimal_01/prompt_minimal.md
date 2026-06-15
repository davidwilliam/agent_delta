`payments.proration.proration(amount, days_used, days_total)` has an off-by-one in
the denominator. Fix it with the smallest possible change so it returns
amount * days_used // days_total.
