"""Language-aware injection and parsing of public/hidden tests.

Public and hidden tests are injected into the sandbox at score time and run
there. Different languages need different injection sites and runners, so this
module returns, per language, the files to write and the command to run, plus a
parser for the runner's output. Both the Inspect scorer (async sandbox) and the
author-time task checker (subprocess docker) share these strategies.

Python: tests run in isolation from /tmp and import the editable-installed
package. Go: tests are written into an external test package under the module and
run with `go test` so they compile against the fixture.
"""

from __future__ import annotations

import re

_PYTEST_SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors|skipped)")


def parse_pytest_summary(output: str) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    for n, kind in _PYTEST_SUMMARY.findall(output):
        key = "error" if kind.startswith("error") else kind
        counts[key] += int(n)
    counts["total"] = counts["passed"] + counts["failed"] + counts["error"]
    return counts


def parse_go_test(output: str) -> dict[str, int]:
    passed = len(re.findall(r"--- PASS:", output))
    failed = len(re.findall(r"--- FAIL:", output))
    total = passed + failed
    error = 0
    # A compile failure (missing symbol) or panic prints no PASS/FAIL lines.
    # Count it as an error so the run reads as failing, not as "no tests".
    if total == 0 and re.search(r"build failed|undefined:|cannot find|^panic:", output, re.MULTILINE):
        error, total = 1, 1
    return {"passed": passed, "failed": failed, "error": error, "skipped": 0, "total": total}


def plan(language: str, label: str, filenames: list[str], workdir: str):
    """Return (targets, command).

    targets maps each filename to the path it must be written to inside the
    sandbox; command runs those tests. `label` is "public" or "hidden".
    """
    if language == "python":
        targets = {name: f"/tmp/agentdelta_{label}__{name}" for name in filenames}
        cmd = ["python", "-m", "pytest", "-q", "--tb=line", *targets.values()]
        return targets, cmd
    if language == "go":
        pkg_dir = f"{workdir}/agentdelta_eval/{label}"
        targets = {name: f"{pkg_dir}/{name}" for name in filenames}
        cmd = ["bash", "-c", f"cd {workdir} && go test -v -count=1 ./agentdelta_eval/{label}/"]
        return targets, cmd
    raise ValueError(f"Unsupported fixture language: {language!r}")


def injection(language: str, label: str, files: dict[str, str], workdir: str):
    """Return (writes, command) where writes is a list of (path, content)."""
    targets, cmd = plan(language, label, list(files), workdir)
    return [(targets[name], content) for name, content in files.items()], cmd


def parse(language: str, output: str) -> dict[str, int]:
    if language == "go":
        return parse_go_test(output)
    return parse_pytest_summary(output)
