"""Tests for the website JSON export (docs/website_json_export.md)."""

import json
import math

from agent_delta.reporting.html import REPORT_SECTIONS
from agent_delta.reporting.json_export import (
    SCHEMA_VERSION,
    build_report_json,
    dump_report_json,
)


def _fake_bundle():
    return [
        {
            "report": {"suite": "suite-b", "benchmark_version": "0.1.0",
                       "models": ["m1"], "per_mode": {"default": {}}},
            "records": [{"task_id": "t1", "model_id": "m1",
                         "scoring": {"verified_success": True}}],
            "repro": {"agentdelta_version": "0.1.0"},
        },
        {
            "report": {"suite": "suite-a", "benchmark_version": "0.1.0", "models": []},
            "records": [],
            "repro": None,
        },
    ]


def test_envelope_top_level_keys():
    d = build_report_json(_fake_bundle(), generated_at="2026-06-15 07:19 UTC",
                          baseline="claude-opus-4-6")
    assert d["schema_version"] == SCHEMA_VERSION == 1
    assert d["benchmark_version"] == "0.1.0"
    assert d["generated_at"] == "2026-06-15 07:19 UTC"
    assert d["baseline"] == "claude-opus-4-6"
    assert {"schema_version", "benchmark_version", "generated_at", "baseline",
            "sections", "suites"} <= set(d)


def test_sections_match_report_sections():
    d = build_report_json(_fake_bundle(), generated_at="t", baseline="b")
    assert d["sections"] == [{"id": sid, "label": label} for sid, label in REPORT_SECTIONS]
    # Plain (un-escaped) labels in the JSON.
    assert {"id": "stack", "label": "Stack & requirements"} in d["sections"]


def test_suites_sorted_and_carry_report_records_repro():
    d = build_report_json(_fake_bundle(), generated_at="t", baseline="b")
    assert [s["suite"] for s in d["suites"]] == ["suite-a", "suite-b"]  # sorted by name
    for s in d["suites"]:
        assert {"suite", "report", "records", "repro"} <= set(s)
    # report is the exact build_report() object passed in.
    suite_b = next(s for s in d["suites"] if s["suite"] == "suite-b")
    assert suite_b["report"]["models"] == ["m1"]


def test_dump_is_strict_valid_json():
    d = build_report_json(_fake_bundle(), generated_at="t", baseline="b")
    text = dump_report_json(d)
    parsed = json.loads(text)  # JS-parseable
    assert parsed["schema_version"] == 1


def test_non_finite_floats_are_stripped():
    bundle = _fake_bundle()
    bundle[0]["report"]["bad"] = float("nan")
    bundle[0]["report"]["worse"] = float("inf")
    d = build_report_json(bundle, generated_at="t", baseline="b")
    text = dump_report_json(d)  # must not raise despite NaN/Inf inputs
    parsed = json.loads(text)
    rep = next(s["report"] for s in parsed["suites"] if s["suite"] == "suite-b")
    assert rep["bad"] is None and rep["worse"] is None
    # And the raw dump uses allow_nan=False (would raise on a stray non-finite).
    assert "NaN" not in text and "Infinity" not in text


def test_benchmark_version_array_when_suites_disagree():
    bundle = _fake_bundle()
    bundle[0]["report"]["benchmark_version"] = "0.2.0"
    d = build_report_json(bundle, generated_at="t", baseline="b")
    assert d["benchmark_version"] == ["0.1.0", "0.2.0"]
