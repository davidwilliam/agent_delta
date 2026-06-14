"""AgentDelta command-line interface (SPEC section 25, v0.1 subset)."""

from __future__ import annotations

import json

import click

from agent_delta import __version__, config
from agent_delta.registry import list_tasks, load_fixture, load_task


@click.group()
@click.version_option(__version__, prog_name="agentdelta")
def main() -> None:
    """AgentDelta: reproducible evaluation of frontier coding agents."""


@main.command("list-tasks")
def list_tasks_cmd() -> None:
    """List available tasks."""
    for tid in list_tasks():
        task = load_task(tid)
        click.echo(f"{tid:12s} [{task.category}] {task.title}")


@main.command("validate-task")
@click.argument("task_id")
def validate_task_cmd(task_id: str) -> None:
    """Validate a task's definition and referenced files."""
    task = load_task(task_id)
    problems: list[str] = []
    if not (task.dir / task.spec.get("prompt_file", "prompt.md")).exists():
        problems.append("missing prompt file")
    for p in task.public_test_files + task.hidden_test_files:
        if not p.exists():
            problems.append(f"missing test file: {p.name}")
    try:
        load_fixture(task.repo)
    except FileNotFoundError as e:
        problems.append(str(e))
    if problems:
        for p in problems:
            click.secho(f"  ✗ {p}", fg="red")
        raise SystemExit(1)
    click.secho(f"✓ {task_id} valid", fg="green")


@main.command("build-sandbox")
@click.option("--fixture", default="python_package", help="Fixture to build an image for.")
@click.option(
    "--method",
    type=click.Choice(["dockerfile", "run-commit"]),
    default="dockerfile",
    help="dockerfile = BuildKit (reproducible); run-commit = BuildKit-free fallback.",
)
def build_sandbox_cmd(fixture: str, method: str) -> None:
    """Build the Docker sandbox image for a fixture."""
    from agent_delta.sandbox_build import build_image, build_image_dockerfile

    if method == "dockerfile":
        build_image_dockerfile(fixture)
    else:
        build_image(fixture)


@main.command("run")
@click.option("--task", "task_id", required=True, help="Task ID, e.g. task_001.")
@click.option("--model", "model_id", default="claude-opus-4-8", help="Pinned model ID.")
@click.option("--repetitions", default=1, type=int, help="Repeated runs (epochs).")
@click.option("--suite", default="anthropic-claude-code-v0.1", help="Results suite name.")
@click.option("--dry-run", is_flag=True, help="Apply reference solution, no API calls.")
def run_cmd(task_id: str, model_id: str, repetitions: int, suite: str, dry_run: bool) -> None:
    """Run one task for one model and write run records."""
    from agent_delta.eval import run_task
    from agent_delta.reporting import write_run_records

    if not dry_run and model_id not in config.included_models():
        click.secho(
            f"Warning: {model_id} is not flagged include:true in the model config.",
            fg="yellow",
        )

    logs = run_task(task_id, model_id, repetitions=repetitions, dry_run=dry_run)
    paths = write_run_records(logs, suite=suite)
    click.secho(f"\nWrote {len(paths)} run record(s):", fg="green")
    for p in paths:
        record = json.loads(p.read_text())
        s = record["scoring"]
        click.echo(
            f"  {p.parent.name}: verified={s['verified_success']} "
            f"partial_obj={s['partial_objective_score']:.1f} "
            f"hidden={s['hidden_test_score']}"
        )


if __name__ == "__main__":
    main()
