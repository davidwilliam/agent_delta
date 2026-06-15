Make `payments.billing_state.transition` reject moves not in `LEGAL` (raise
ValueError) and treat "canceled" as terminal. An illegal move must not change the
stored state.
