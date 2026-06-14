"""Reproducibility manifest (SPEC sections 27, 5.2, 8.5).

Captures the pinned versions, content hashes, image digests, and run-order seed
that let a benchmark report be reproduced or at least audited. The hidden-test
hash is a cryptographic commitment (SPEC 8.5): publish it before evaluation so
that the hidden tests cannot be changed after seeing results.

`build_manifest` writes reproducibility.json; `validate_manifest` recomputes the
content hashes and checks they still match, flagging any drift.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

from agent_delta import __version__, config


def _sha256_paths(paths: list[Path]) -> str:
    """Stable hash over file contents, keyed by repo-relative path."""
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda x: x.as_posix()):
        if not p.is_file():
            continue
        rel = p.relative_to(config.ROOT).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def hidden_tests_hash() -> str:
    """Commitment over every task's hidden test files (SPEC 8.5)."""
    paths = [p for d in config.TASKS_DIR.iterdir() if d.is_dir()
             for p in d.glob("hidden_test*")]
    return _sha256_paths(paths)


def tasks_hash() -> str:
    """Hash over the visible task spec (task.yaml, prompt, public tests)."""
    paths = []
    for d in sorted(config.TASKS_DIR.iterdir()):
        if not d.is_dir():
            continue
        paths += [d / "task.yaml"]
        paths += list(d.glob("prompt.*"))
        paths += list(d.glob("public_test*"))
    return _sha256_paths([p for p in paths if p.exists()])


def scoring_hash() -> str:
    """Hash over the frozen scoring/amplification/modes configs."""
    return _sha256_paths(sorted((config.CONFIGS_DIR / "scoring").glob("*.yaml"))
                         + [config.CONFIGS_DIR / "modes.yaml"])


def _cmd(args: list[str]) -> str | None:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=20).stdout.strip() or None
    except Exception:
        return None


def collect_versions() -> dict[str, Any]:
    def ver(mod: str) -> str | None:
        try:
            return __import__(mod).__version__
        except Exception:
            return None

    return {
        "agentdelta_version": __version__,
        "inspect_version": ver("inspect_ai"),
        "inspect_swe_version": ver("inspect_swe"),
        "python_version": platform.python_version(),
        "docker_version": _cmd(["docker", "version", "--format", "{{.Server.Version}}"]),
        "host_os": platform.platform(),
    }


def image_digests(fixtures: list[str]) -> dict[str, str | None]:
    out = {}
    for fx in fixtures:
        from agent_delta.registry import load_fixture
        tag = load_fixture(fx).image_tag
        out[fx] = _cmd(["docker", "inspect", "--format", "{{.Id}}", tag])
    return out


def build_manifest(
    *, suite: str, date: str, models: list[str], tasks: list[str],
    fixtures: list[str], run_order_seed: int | None, agent: str = "claude_code",
) -> dict[str, Any]:
    agent_cfg = config.CONFIGS_DIR / "agents" / f"{agent}.yaml"
    return {
        "agentdelta_version": __version__,
        "date": date,
        "suite": suite,
        **collect_versions(),
        "agent": agent,
        "agent_settings_hash": _sha256_paths([agent_cfg]),
        "models": models,
        "tasks": tasks,
        "sandbox_images": image_digests(fixtures),
        "tasks_hash": tasks_hash(),
        "scoring_hash": scoring_hash(),
        "hidden_tests_hash": hidden_tests_hash(),
        "run_order_seed": run_order_seed,
    }


def write_manifest(manifest: dict, suite: str, out_root: Path | None = None) -> Path:
    out_root = out_root or (config.RESULTS_DIR / "reports" / suite)
    out_root.mkdir(parents=True, exist_ok=True)
    path = out_root / "reproducibility.json"
    path.write_text(json.dumps(manifest, indent=2))
    return path


def validate_manifest(manifest: dict) -> list[str]:
    """Recompute content hashes and report any drift (empty list = reproducible)."""
    problems = []
    checks = {
        "tasks_hash": tasks_hash(),
        "scoring_hash": scoring_hash(),
        "hidden_tests_hash": hidden_tests_hash(),
    }
    for key, current in checks.items():
        recorded = manifest.get(key)
        if recorded and recorded != current:
            problems.append(f"{key} changed: manifest {recorded[:23]}... now {current[:23]}...")
    for fx, digest in (manifest.get("sandbox_images") or {}).items():
        if not digest:
            problems.append(f"sandbox image for {fx} was not recorded")
    return problems
