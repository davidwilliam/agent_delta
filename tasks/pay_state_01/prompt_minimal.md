Add a payment status lifecycle to the `payments` service. Each event starts as
"paid" and may only move through legal transitions; "refunded" is final.
