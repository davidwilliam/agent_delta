"""Tests for the language-aware test injection and output parsing."""

from agent_delta.scoring.testrunner import parse, parse_go_test, plan


def test_plan_python_isolates_in_tmp():
    targets, cmd = plan("python", "public", ["public_tests.py"], "/repo")
    assert targets["public_tests.py"].startswith("/tmp/")
    assert cmd[:3] == ["python", "-m", "pytest"]


def test_plan_go_writes_into_module():
    targets, cmd = plan("go", "hidden", ["hidden_test.go"], "/repo")
    assert targets["hidden_test.go"] == "/repo/agentdelta_eval/hidden/hidden_test.go"
    assert "go test" in cmd[-1]
    assert "agentdelta_eval/hidden" in cmd[-1]


def test_parse_go_counts_pass_fail():
    out = "=== RUN   TestA\n--- PASS: TestA (0.00s)\n=== RUN TestB\n--- FAIL: TestB (0.00s)\nFAIL\n"
    c = parse_go_test(out)
    assert c["passed"] == 1 and c["failed"] == 1 and c["total"] == 2


def test_parse_go_build_failure_is_error():
    out = ("# textkit/agentdelta_eval/public\n"
           "public_test.go:7:20: undefined: textkit.Capitalize\n"
           "FAIL\ttextkit/agentdelta_eval/public [build failed]\n")
    c = parse_go_test(out)
    assert c["error"] == 1 and c["total"] == 1 and c["passed"] == 0


def test_parse_dispatches_by_language():
    py = parse("python", "3 passed in 0.01s")
    assert py["passed"] == 3
    go = parse("go", "--- PASS: TestX (0.0s)\n")
    assert go["passed"] == 1


def test_plan_unknown_language_raises():
    try:
        plan("ruby", "public", ["x"], "/repo")
        assert False
    except ValueError:
        pass
