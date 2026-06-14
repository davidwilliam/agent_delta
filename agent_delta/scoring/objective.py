"""Objective scoring per SPEC section 14.

The objective score combines absolute, per-run components (verified success,
hidden-test rate, regression avoidance, scope control) with set-relative
components (cost efficiency, time efficiency).

Because cost/time efficiency are normalized against the *best model in the
evaluation set*, they cannot be known at single-run scoring time. So:

  * `partial_objective_score` is computed per run over the absolute weights only
    (renormalized to sum to 1), and stored on each run record.
  * `objective_score` is the authoritative SPEC formula, computed at aggregation
    time once cost/time efficiency are known.

Default weights (SPEC 14.1):
  0.60 verified success
  0.15 hidden-test score
  0.10 regression avoidance
  0.05 scope control
  0.05 cost efficiency
  0.05 time efficiency
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

# SPEC 14.1 default weights.
W_SUCCESS = 0.60
W_HIDDEN = 0.15
W_REGRESSION = 0.10
W_SCOPE = 0.05
W_COST = 0.05
W_TIME = 0.05

# Weights that are knowable per-run (everything except cost/time efficiency).
_ABSOLUTE_WEIGHT = W_SUCCESS + W_HIDDEN + W_REGRESSION + W_SCOPE  # 0.90


@dataclass
class ObjectiveComponents:
    """Absolute (per-run) scoring components, each in [0, 1]."""

    verified_success: float  # 1.0 if all acceptance criteria met, else 0.0
    hidden_test_score: float  # fraction of hidden tests passed
    regression_avoidance: float  # 1.0 if baseline still passes, else 0.0
    scope_control: float  # 1.0 minus penalties for out-of-scope changes

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def partial_objective_score(c: ObjectiveComponents) -> float:
    """Per-run objective over absolute weights only, renormalized to 0-100.

    Cost/time efficiency are excluded (unknown until aggregation). The four
    absolute weights are renormalized to sum to 1 so the value stays on 0-100.
    """
    raw = (
        W_SUCCESS * c.verified_success
        + W_HIDDEN * c.hidden_test_score
        + W_REGRESSION * c.regression_avoidance
        + W_SCOPE * c.scope_control
    )
    return 100.0 * raw / _ABSOLUTE_WEIGHT


def objective_score(
    c: ObjectiveComponents,
    cost_efficiency: float,
    time_efficiency: float,
) -> float:
    """Authoritative SPEC 14.1 objective score on 0-100.

    cost_efficiency and time_efficiency are set-relative values in [0, 1]
    (see scoring.cost / scoring.latency), computed during aggregation.
    """
    raw = (
        W_SUCCESS * c.verified_success
        + W_HIDDEN * c.hidden_test_score
        + W_REGRESSION * c.regression_avoidance
        + W_SCOPE * c.scope_control
        + W_COST * cost_efficiency
        + W_TIME * time_efficiency
    )
    return 100.0 * raw


def full_score(objective: float, review: float | None = None) -> float:
    """SPEC 14.2 full score. If no review provided, full score == objective."""
    if review is None:
        return objective
    return 0.95 * objective + 0.05 * review
