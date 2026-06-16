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


# --- sharded v2 export ---------------------------------------------------------
def _provider_bundle():
    return [
        {"report": {"suite": "anthropic-x", "benchmark_version": "0.1.0",
                    "models": ["claude-opus-4-8", "claude-sonnet-4-6"]},
         "records": [{"task_id": "t1", "model_id": "claude-opus-4-8", "provider": "anthropic",
                      "scoring": {"verified_success": True}}],
         "repro": None},
        {"report": {"suite": "openai-y", "benchmark_version": "0.1.0",
                    "models": ["gpt-5.4", "gpt-5-mini-2025-08-07"]},
         "records": [{"task_id": "t1", "model_id": "gpt-5.4", "provider": "openai",
                      "scoring": {"verified_success": True}}],
         "repro": None},
    ]


def test_model_provider_inference():
    from agent_delta.reporting.html import model_provider
    assert model_provider("claude-opus-4-8") == "anthropic"
    assert model_provider("gpt-5.4") == "openai"
    assert model_provider("gemini-2.5-pro") == "google"
    assert model_provider("mystery") == "unknown"


def test_sharded_export_index_and_shards():
    from agent_delta.reporting.json_export import EXPORT_SCHEMA_VERSION, build_sharded_export
    index, shards = build_sharded_export(_provider_bundle(), generated_at="t", baseline="b")
    assert index["schema_version"] == EXPORT_SCHEMA_VERSION == 2
    # one shard per suite, each with provider + report/records.
    assert set(shards) == {"anthropic-x", "openai-y"}
    assert shards["openai-y"]["provider"] == "openai"
    assert shards["anthropic-x"]["provider"] == "anthropic"
    # index suites point to shard files and carry provider + counts.
    by = {s["suite"]: s for s in index["suites"]}
    assert by["openai-y"]["file"] == "suites/openai-y.json"
    assert by["openai-y"]["provider"] == "openai" and by["openai-y"]["n_runs"] == 1
    # providers index groups suites + models.
    provs = {p["id"]: p for p in index["providers"]}
    assert set(provs) == {"anthropic", "openai"}
    assert provs["openai"]["suites"] == ["openai-y"]
    assert "gpt-5.4" in provs["openai"]["models"]
    assert provs["anthropic"]["label"].startswith("Anthropic")


def test_write_sharded_export(tmp_path):
    import json as _json
    from agent_delta.reporting.json_export import build_sharded_export, write_sharded_export
    index, shards = build_sharded_export(_provider_bundle(), generated_at="t", baseline="b")
    out = write_sharded_export(index, shards, tmp_path / "export")
    idx = _json.loads((out / "index.json").read_text())
    assert idx["schema_version"] == 2 and len(idx["suites"]) == 2
    for s in idx["suites"]:
        shard = _json.loads((out / s["file"]).read_text())  # each file referenced exists + parses
        assert shard["suite"] == s["suite"] and "report" in shard
