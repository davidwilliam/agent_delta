You are working in the `payments` service. The module `payments.proration` exposes
`proration(amount, days_used, days_total)`, which should return the prorated portion
of `amount` for `days_used` out of `days_total`, using integer (floor) division:

    amount * days_used // days_total

There is an off-by-one bug in the denominator that makes the result slightly too
high. For example, `proration(1000, 15, 30)` should be `500` but is not. Fix it.

Make the smallest possible change: this is a one-token fix. Do not rewrite the
function, add new functions, or change the floor division. When finished, run
`pytest -q tests/` and summarize the fix.
