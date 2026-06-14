"""Cost-success and latency-success frontiers (SPEC section 17).

A model is on a frontier when no other model is at least as good on both axes
(higher success and lower cost, or higher success and lower time) with a strict
advantage on one. Rendered as a table marking the Pareto-efficient set; the
points are also suitable for plotting.
"""

from __future__ import annotations


def _pareto(points: list[dict]) -> list[dict]:
    """Mark each point on_frontier. x is minimized, y is maximized."""
    for p in points:
        if p["x"] is None or p["y"] is None:
            p["on_frontier"] = False
            continue
        p["on_frontier"] = not any(
            q is not p and q["x"] is not None and q["y"] is not None
            and q["x"] <= p["x"] and q["y"] >= p["y"]
            and (q["x"] < p["x"] or q["y"] > p["y"])
            for q in points
        )
    return points


def cost_success_frontier(models: dict) -> list[dict]:
    """Frontier of cost-per-success (minimize) vs success rate (maximize)."""
    points = [
        {"model_id": mid, "x": m.get("cost_per_success_usd"), "y": m.get("success_rate")}
        for mid, m in models.items()
    ]
    return _pareto(points)


def latency_success_frontier(models: dict) -> list[dict]:
    """Frontier of median time-to-success (minimize) vs success rate (maximize)."""
    points = [
        {"model_id": mid, "x": m.get("median_time_to_success_s"), "y": m.get("success_rate")}
        for mid, m in models.items()
    ]
    return _pareto(points)
