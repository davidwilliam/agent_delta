"""Billing account state machine (reference solution for pay_state_02).

transition() validates the (current, new) move against the explicit legal set
before recording it, and treats "canceled" as terminal (no legal outgoing
transition), so illegal moves raise ValueError and the stored state is unchanged.
"""

LEGAL = {("trialing", "active"), ("active", "past_due"), ("past_due", "active"),
         ("past_due", "canceled"), ("active", "canceled")}
_STATE = {}


def reset():
    _STATE.clear()


def state(acct):
    return _STATE.get(acct, "trialing")


def transition(acct, new):
    current = state(acct)
    if (current, new) not in LEGAL:
        raise ValueError(f"illegal transition: {current} -> {new}")
    _STATE[acct] = new
    return new
