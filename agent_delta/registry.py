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
    def repo(self) -> str:
        return self.spec["repo"]

    @property
    def prompt(self) -> str:
        return (self.dir / self.spec.get("prompt_file", "prompt.md")).read_text()

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
    def setup_cmds(self) -> list[str]:
        return self.manifest.get("setup", [])

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
