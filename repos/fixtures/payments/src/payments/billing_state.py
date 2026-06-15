"""Billing account state machine.

NOTE (fixture): transition() does NOT validate the move against the legal set
and does NOT guard the terminal "canceled" state, so it accepts illegal
transitions and revives canceled accounts. The AgentDelta state-machine task
makes transition() reject illegal moves (raise ValueError) and treat "canceled"
as terminal.
"""

LEGAL = {("trialing", "active"), ("active", "past_due"), ("past_due", "active"),
         ("past_due", "canceled"), ("active", "canceled")}
_STATE = {}


def reset():
    _STATE.clear()


def state(acct):
    return _STATE.get(acct, "trialing")


def transition(acct, new):
    # BUG: does not validate the transition or guard the terminal state
    _STATE[acct] = new
    return new
