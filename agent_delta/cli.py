"""AgentDelta command-line interface (SPEC section 25, v0.1 subset)."""

from __future__ import annotations

import json
from pathlib import Path

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


@main.command("check-task")
@click.argument("task_id", required=False)
@click.option("--all", "check_all", is_flag=True, help="Check every task.")
def check_task_cmd(task_id: str | None, check_all: bool) -> None:
    """Verify a task fails at base and passes with its reference solution."""
    from agent_delta.taskcheck import check_task

    ids = list_tasks() if check_all else [task_id]
    if not check_all and not task_id:
        raise click.UsageError("Provide a TASK_ID or use --all.")

    failures = 0
    for tid in ids:
        r = check_task(tid)
        mark = click.style("✓", fg="green") if r.ok else click.style("✗", fg="red")
        click.echo(
            f"{mark} {tid:10s} "
            f"base(pub {r.base_public.failed + r.base_public.error}✗/"
            f"{r.base_public.total}, hid {r.base_hidden.failed + r.base_hidden.error}✗/"
            f"{r.base_hidden.total}) → "
            f"after(base {'ok' if r.after_baseline_ok else 'FAIL'}, "
            f"pub {r.after_public.passed}/{r.after_public.total}, "
            f"hid {r.after_hidden.passed}/{r.after_hidden.total})"
        )
        if not r.ok:
            failures += 1
            if not r.non_trivial:
                click.secho("    ! tests pass at base - task may be trivial", fg="yellow")
            if not r.solvable:
                click.secho("    ! reference solution does not fully pass", fg="yellow")
    if failures:
        raise SystemExit(1)


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


@main.command("aggregate")
@click.option("--results", "results_dir", required=True, help="Dir of run records (results/raw/<suite>).")
@click.option("--suite", required=True, help="Suite name for the report.")
@click.option("--baseline", default=None, help="Baseline model ID for amplification (default: oldest).")
def aggregate_cmd(results_dir: str, suite: str, baseline: str | None) -> None:
    """Aggregate run records into report.json (scores, stats, amplification)."""
    from agent_delta.reporting import build_report, write_report_json

    report = build_report(Path(results_dir), suite=suite, baseline=baseline)
    path = write_report_json(report, suite)
    click.secho(f"Wrote {path}", fg="green")
    for mode, data in report["per_mode"].items():
        ranked = ", ".join(
            f"{data['models'][mid]['model_id']} {data['models'][mid]['objective_score']:.1f}"
            for mid in data["ranking"]
        )
        click.echo(f"  [{mode}] {ranked}")


@main.command("report")
@click.option("--results", "results_dir", default=None, help="Dir of run records (defaults from suite).")
@click.option("--suite", required=True, help="Suite name.")
@click.option("--baseline", default=None, help="Baseline model ID for amplification.")
@click.option("--output", default=None, help="Markdown output path.")
def report_cmd(results_dir: str | None, suite: str, baseline: str | None, output: str | None) -> None:
    """Generate a Markdown report from run records."""
    from agent_delta.reporting import build_report, render, write_report_json

    rdir = Path(results_dir) if results_dir else (config.RAW_RESULTS_DIR / suite)
    report = build_report(rdir, suite=suite, baseline=baseline)
    write_report_json(report, suite)
    md = render(report)
    out = Path(output) if output else (config.RESULTS_DIR / "reports" / suite / "report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    click.secho(f"Wrote {out}", fg="green")


if __name__ == "__main__":
    main()
