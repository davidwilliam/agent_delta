# AgentDelta sandbox image for a Python fixture.
#
# Build context is the repo root. Select the fixture with --build-arg FIXTURE=<name>.
# The fixture is copied to /repo, installed editable, and committed to a fresh git
# repo so the agent starts from a known clean base commit.
#
# NOTE: the Claude Code agent itself is NOT baked in. inspect_swe provisions the
# agent binary into the sandbox at runtime (see runners/claude_code.py `version`),
# which keeps this image small and fast to build. The dry-run path needs no agent.
# Base pinned by digest for reproducibility (SPEC 5.2) and to keep BuildKit's
# resolve deterministic — an unpinned tag can go stale locally and hang resolve.
# python:3.12-slim, refreshed 2026-06-13.
FROM python:3.12-slim@sha256:d764629ce0ddd8c71fd371e9901efb324a95789d2315a47db7e4d27e78f1b0e9

ARG FIXTURE=python_package

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GIT_AUTHOR_NAME=agentdelta GIT_AUTHOR_EMAIL=agentdelta@example.com \
    GIT_COMMITTER_NAME=agentdelta GIT_COMMITTER_EMAIL=agentdelta@example.com

RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo
COPY repos/fixtures/${FIXTURE}/ /repo/

# Editable install + dev deps (pytest). Baseline test deps come from the fixture.
RUN pip install -e ".[dev]"

# Establish the clean base commit the agent starts from.
RUN git init -q && git add -A && git commit -q -m "agentdelta base: ${FIXTURE} fixture"

# Keep the container alive for Inspect to exec into.
CMD ["sleep", "infinity"]
