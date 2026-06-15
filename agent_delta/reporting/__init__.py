"""Reporting: turn Inspect eval logs into AgentDelta run records and reports."""

from agent_delta.reporting.aggregate import build_report, write_report_json
from agent_delta.reporting.html import REPORT_SECTIONS, render_html
from agent_delta.reporting.json_export import build_report_json, dump_report_json
from agent_delta.reporting.markdown import render
from agent_delta.reporting.result import write_run_records

__all__ = ["write_run_records", "build_report", "write_report_json", "render", "render_html",
           "REPORT_SECTIONS", "build_report_json", "dump_report_json"]
