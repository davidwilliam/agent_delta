"""Tests for diff metrics, frontiers, and blinded review."""

from agent_delta.reporting.charts import cost_success_frontier, latency_success_frontier
from agent_delta.scoring.diff import parse_diff
from agent_delta.scoring.review import RUBRIC, build_review_packet, review_score

DIFF = """diff --git a/src/mathkit/stats.py b/src/mathkit/stats.py
--- a/src/mathkit/stats.py
+++ b/src/mathkit/stats.py
@@ -1,3 +1,5 @@
+def median(values):
+    return sorted(values)[len(values)//2]
-old line
diff --git a/tests/test_stats.py b/tests/test_stats.py
--- a/tests/test_stats.py
+++ b/tests/test_stats.py
@@ -1,1 +1,2 @@
+def test_median(): pass
"""


def test_parse_diff_counts_and_ratio():
    m = parse_diff(DIFF, "python")
    assert m["files_touched"] == 2
    assert m["hunks"] == 2
    assert m["lines_added"] == 3 and m["lines_removed"] == 1
    assert m["test_lines_changed"] == 1
    assert m["code_lines_changed"] == 3
    assert abs(m["test_to_code_ratio"] - (1 / 3)) < 1e-9
    assert m["diff_locality"] == 0.5  # two files
    assert m["patch_entropy"] > 0


def test_parse_diff_single_file_is_local():
    m = parse_diff("+++ b/a.py\n@@ -1 +1 @@\n+x\n", "python")
    assert m["files_touched"] == 1
    assert m["diff_locality"] == 1.0
    assert m["patch_entropy"] == 0.0


def test_cost_frontier_marks_dominated():
    models = {
        "cheap_good": {"cost_per_success_usd": 0.5, "success_rate": 0.9},
        "dear_worse": {"cost_per_success_usd": 2.0, "success_rate": 0.8},
        "dear_best": {"cost_per_success_usd": 3.0, "success_rate": 0.95},
    }
    pts = {p["model_id"]: p for p in cost_success_frontier(models)}
    assert pts["cheap_good"]["on_frontier"] is True
    assert pts["dear_worse"]["on_frontier"] is False   # dominated by cheap_good
    assert pts["dear_best"]["on_frontier"] is True      # best success, nothing dominates


def test_latency_frontier_runs():
    models = {
        "fast": {"median_time_to_success_s": 60, "success_rate": 0.8},
        "slow": {"median_time_to_success_s": 600, "success_rate": 0.8},
    }
    pts = {p["model_id"]: p for p in latency_success_frontier(models)}
    assert pts["fast"]["on_frontier"] is True
    assert pts["slow"]["on_frontier"] is False


def test_review_score_scales_to_100():
    assert review_score({c: 5 for c in RUBRIC}) == 100.0
    assert review_score({c: 0 for c in RUBRIC}) == 0.0
    assert review_score({"correctness": 4}) == 80.0
    assert review_score({}) is None


def test_review_packet_is_blinded():
    record = {"run_id": "x_opus-4-8_rep01", "scoring": {"public_tests": {"passed": 3}}}
    packet = build_review_packet("do the thing", record, "some diff")
    blob = str(packet)
    assert "opus" not in blob and "model" not in packet
    assert packet["anon_id"].startswith("patch_")
    assert packet["diff"] == "some diff"
    assert set(packet["rubric"]) == set(RUBRIC)
