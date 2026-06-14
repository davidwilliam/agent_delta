"""Build the Docker sandbox image for a fixture.

Two strategies:

* `build_image` (default) — run + exec + commit. Starts a container from the base
  image, copies the fixture in, installs git + the fixture deps, creates the clean
  base commit, and commits the result. This avoids `docker build`/BuildKit, which
  can wedge on its image-`resolve` step on some Docker Desktop setups.
* `build_image_dockerfile` — the classic `docker build` path, kept for CI/envs
  where BuildKit is healthy and a fully declarative build is preferred.

Both produce an identical image: the fixture at /repo, editable-installed, with a
clean git base commit and `safe.directory` configured so the scorer's `git diff`
works regardless of file ownership.
"""

from __future__ import annotations

import subprocess

from agent_delta import config
from agent_delta.registry import load_fixture

BASE_IMAGE = "python:3.12-slim"


def _run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def build_image(fixture_name: str = "python_package") -> str:
    """Build via run + exec + commit (BuildKit-free). Returns the image tag."""
    fixture = load_fixture(fixture_name)
    tag = fixture.image_tag
    workdir = fixture.workdir
    container = f"agentdelta-build-{fixture_name}"

    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
    _run(["docker", "run", "-d", "--name", container, BASE_IMAGE, "sleep", "infinity"])
    try:
        # Copy the pristine fixture into the container working dir.
        _run(["docker", "cp", f"{fixture.source_path}/.", f"{container}:{workdir}"])

        setup_cmds = " && ".join(fixture.setup_cmds) if fixture.setup_cmds else "true"
        script = f"""
set -e
apt-get update -qq
apt-get install -y -qq --no-install-recommends git >/dev/null 2>&1
rm -rf /var/lib/apt/lists/*
cd {workdir}
{setup_cmds}
git config --system --add safe.directory {workdir}
git config --system user.email agentdelta@example.com
git config --system user.name agentdelta
git init -q && git add -A && git commit -q -m "agentdelta base: {fixture_name} fixture"
git rev-parse --short HEAD
"""
        _run(["docker", "exec", container, "bash", "-c", script])

        _run([
            "docker", "commit",
            "-c", f"WORKDIR {workdir}",
            "-c", 'CMD ["sleep", "infinity"]',
            container, tag,
        ])
    finally:
        subprocess.run(["docker", "rm", "-f", container], capture_output=True)

    print(f"\nBuilt {tag}")
    return tag


def build_image_dockerfile(fixture_name: str = "python_package") -> str:
    """Build via `docker build` (BuildKit). Returns the image tag."""
    fixture = load_fixture(fixture_name)
    dockerfile = config.SANDBOXES_DIR / "claude-code" / "Dockerfile"
    tag = fixture.image_tag
    _run([
        "docker", "build",
        "-f", str(dockerfile),
        "--build-arg", f"FIXTURE={fixture_name}",
        "-t", tag,
        str(config.ROOT),
    ])
    print(f"\nBuilt {tag}")
    return tag
