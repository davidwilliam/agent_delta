"""Blinded review scaffolding (SPEC section 18).

Review is optional and secondary, capped at 5% of the Full Score (SPEC 14.2). It
must be blinded: the reviewer (human or an LLM judge run separately) sees the task
prompt, the diff, and the test result, but never the model name, mode, cost, or
latency. This module builds anonymized review packets and converts returned
0-5 rubric scores into a 0-100 review score; the actual judging is a separate step
that writes a review.json next to each run.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

# SPEC 18.2 rubric, each scored 0-5.
RUBRIC = [
    "correctness", "maintainability", "minimality",
    "test_quality", "risk_control", "explanation_quality",
]


def review_score(scores: dict[str, float]) -> float | None:
    """Mean of the provided 0-5 rubric scores, scaled to 0-100."""
    vals = [float(scores[c]) for c in RUBRIC if c in scores and scores[c] is not None]
    if not vals:
        return None
    return 20.0 * sum(vals) / len(vals)


def _anon_id(run_id: str) -> str:
    return "patch_" + hashlib.sha256(run_id.encode()).hexdigest()[:12]


def build_review_packet(task_prompt: str, record: dict, diff_text: str) -> dict[str, Any]:
    """Build a blinded packet: no model, mode, cost, or latency (SPEC 18.1)."""
    s = record.get("scoring", {})
    return {
        "anon_id": _anon_id(record["run_id"]),
        "task_prompt": task_prompt,
        "diff": diff_text,
        "test_result": {
            "public_tests": s.get("public_tests"),
            "hidden_tests": s.get("hidden_tests"),
            "regression_ok": s.get("regression_avoidance") == 1.0,
        },
        "rubric": {c: None for c in RUBRIC},
        "instructions": (
            "Score each rubric criterion 0-5. Do not guess the model. Judge only the "
            "diff, the task, and the test result."
        ),
    }


def load_review_score(run_dir: Path) -> float | None:
    """Load review.json (filled rubric) from a run dir and return its 0-100 score."""
    path = run_dir / "review.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    scores = data.get("rubric", data)
    return review_score(scores)
