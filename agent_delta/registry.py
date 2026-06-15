"""Task and fixture registry.

Discovers tasks under tasks/ and fixture manifests under repos/manifests/, and
loads their definitions into lightweight dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from agent_delta import config


@dataclass
class Task:
    id: str
    dir: Path
    spec: dict[str, Any]

    @property
    def title(self) -> str:
        return self.spec.get("title", self.id)

    @property
    def category(self) -> str:
        return self.spec.get("category", "uncategorized")

    @property
    def task_type(self) -> str:
        """'implement' (default) or 'test_writing' (mutation-scored)."""
        return self.spec.get("task_type", "implement")

    @property
    def hardness_level(self) -> str:
        """H1..H5 (HARD-TASKS-SPEC section 4); H1 if unspecified."""
        return self.spec.get("hardness_level", "H1")

    @property
    def tier(self) -> str:
        """'core' (the graded hard suite) or 'supplementary' (single-file warmup).

        The HARD-TASKS-SPEC 16 multi-file ratio is measured over the core tier;
        supplementary tasks are kept for breadth but excluded from that ratio.
        """
        return self.spec.get("tier", "core")

    @property
    def known_llm_failure_mode(self) -> str | None:
        return self.spec.get("known_llm_failure_mode")

    @property
    def forbidden_changes(self) -> list[str]:
        """Human-readable forbidden shortcuts, surfaced in the prompt."""
        return self.spec.get("scope", {}).get("forbidden_changes", [])

    @property
    def forbidden_patterns(self) -> list[dict]:
        """Regexes that must not appear in the diff, each {pattern, label}."""
        return self.spec.get("scope", {}).get("forbidden_patterns", [])

    @property
    def max_lines_changed(self) -> int | None:
        return self.spec.get("scope", {}).get("max_lines_changed")

    @property
    def test_writing(self) -> dict[str, Any]:
        return self.spec.get("test_writing", {})

    def load_mutants(self) -> list[tuple[str, dict[str, str]]]:
        """Return [(mutant_name, {repo_relative_path: contents})] from mutants/."""
        mutants_dir = self.dir / "mutants"
        if not mutants_dir.is_dir():
            return []
        out = []
        for mdir in sorted(p for p in mutants_dir.iterdir() if p.is_dir()):
            files = {
                f.relative_to(mdir).as_posix(): f.read_text()
                for f in sorted(mdir.rglob("*")) if f.is_file()
            }
            out.append((mdir.name, files))
        return out

    @property
    def repo(self) -> str:
        return self.spec["repo"]

    @property
    def prompt(self) -> str:
        return (self.dir / self.spec.get("prompt_file", "prompt.md")).read_text()

    @property
    def prompts(self) -> dict[str, str]:
        """Declared author-written prompt variants, e.g. {minimal, strong, workflow}.

        HARD-TASKS-SPEC 6 / SPEC-ADDENDUM 14. Absent variants fall back to the
        generic prompt synthesis in modes.build_prompt.
        """
        return self.spec.get("prompts", {})

    def prompt_variant(self, kind: str) -> str | None:
        """Return the author-written prompt of this `kind`, or None if not declared."""
        fname = self.prompts.get(kind)
        if not fname:
            return None
        path = self.dir / fname
        return path.read_text() if path.exists() else None

    @property
    def scoring_weights(self) -> dict[str, float] | None:
        """Per-task objective weight overrides (HARD-TASKS-SPEC 13), if declared."""
        return self.spec.get("scoring_weights")

    @property
    def baseline_cmds(self) -> list[str]:
        return self.spec.get("tests", {}).get("baseline", [])

    @property
    def public_test_files(self) -> list[Path]:
        return [self.dir / p for p in self.spec.get("tests", {}).get("public", [])]

    @property
    def hidden_test_files(self) -> list[Path]:
        return [self.dir / p for p in self.spec.get("tests", {}).get("hidden", [])]

    @property
    def forbidden_paths(self) -> list[str]:
        return self.spec.get("scope", {}).get("forbidden_paths", [])

    @property
    def allowed_paths(self) -> list[str]:
        return self.spec.get("scope", {}).get("allowed_paths", [])

    @property
    def max_files_modified(self) -> int | None:
        return self.spec.get("scope", {}).get("max_files_modified")

    @property
    def timeout_seconds(self) -> int:
        return int(self.spec.get("execution", {}).get("timeout_minutes", 30)) * 60

    @property
    def max_cost_usd(self) -> float | None:
        return self.spec.get("execution", {}).get("max_cost_usd")

    @property
    def network(self) -> str:
        """'disabled' (default) or 'enabled' -> docker network none / bridge."""
        return self.spec.get("execution", {}).get("network", "disabled")

    @property
    def context_class(self) -> str:
        """'long' if the task needs >200k tokens of context, else 'normal' (SPEC 21)."""
        min_ctx = self.spec.get("context_requirement", {}).get("min_context_tokens", 0)
        return "long" if min_ctx > 200000 else "normal"


@dataclass
class Fixture:
    name: str
    manifest: dict[str, Any]
    source_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.source_path = config.ROOT / self.manifest["source_path"]

    @property
    def workdir(self) -> str:
        return self.manifest.get("workdir", "/repo")

    @property
    def language(self) -> str:
        return self.manifest.get("language", "python")

    @property
    def base_image(self) -> str:
        return self.manifest.get("base_image", "python:3.12-slim")

    @property
    def setup_cmds(self) -> list[str]:
        return self.manifest.get("setup", [])

    @property
    def image_env(self) -> dict[str, str]:
        """Environment baked into the image (e.g. offline flags for the toolchain)."""
        return self.manifest.get("image_env", {})

    @property
    def image_tag(self) -> str:
        return f"agentdelta/{self.name}:v0.1"


def load_task(task_id: str) -> Task:
    task_dir = config.TASKS_DIR / task_id
    spec_path = task_dir / "task.yaml"
    if not spec_path.exists():
        raise FileNotFoundError(f"No task.yaml for task {task_id!r} at {spec_path}")
    spec = yaml.safe_load(spec_path.read_text())
    return Task(id=task_id, dir=task_dir, spec=spec)


def list_tasks() -> list[str]:
    return sorted(
        p.name for p in config.TASKS_DIR.iterdir() if (p / "task.yaml").exists()
    )


def load_fixture(name: str) -> Fixture:
    manifest_path = config.MANIFESTS_DIR / f"{name}.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest for fixture {name!r} at {manifest_path}")
    return Fixture(name=name, manifest=yaml.safe_load(manifest_path.read_text()))
