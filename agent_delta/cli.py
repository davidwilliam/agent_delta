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
    if task.task_type == "test_writing":
        if not task.load_mutants():
            problems.append("test_writing task has no mutants/")
    else:
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
    type=click.Choice(["auto", "dockerfile", "run-commit"]),
    default="auto",
    help="auto picks dockerfile for python, run-commit otherwise.",
)
def build_sandbox_cmd(fixture: str, method: str) -> None:
    """Build the Docker sandbox image for a fixture."""
    from agent_delta.registry import load_fixture
    from agent_delta.sandbox_build import build_image, build_image_dockerfile

    if method == "auto":
        method = "dockerfile" if load_fixture(fixture).language == "python" else "run-commit"
    if method == "dockerfile":
        build_image_dockerfile(fixture)
    else:
        build_image(fixture)


@main.command("run")
@click.option("--task", "task_id", required=True, help="Task ID, e.g. task_001.")
@click.option("--model", "model_id", default="claude-opus-4-8", help="Pinned model ID.")
@click.option("--repetitions", default=1, type=int, help="Repeated runs (epochs).")
@click.option("--suite", default="anthropic-claude-code-v0.1", help="Results suite name.")
@click.option("--mode", default="default", help="Evaluation mode (see configs/modes.yaml).")
@click.option("--scaffold-model", default=None,
              help="Model that receives the scaffold under older_plus_scaffold (default: oldest).")
@click.option("--network", type=click.Choice(["disabled", "enabled"]), default=None,
              help="Override sandbox network (a real model run needs 'enabled').")
@click.option("--dry-run", is_flag=True, help="Apply reference solution, no API calls.")
def run_cmd(task_id: str, model_id: str, repetitions: int, suite: str, mode: str,
            scaffold_model: str | None, network: str | None, dry_run: bool) -> None:
    """Run one task for one model in one mode and write run records."""
    from agent_delta.eval import run_task
    from agent_delta.modes import available_modes, is_scaffolded
    from agent_delta.reporting import write_run_records

    if mode not in available_modes():
        raise click.UsageError(f"Unknown mode {mode!r}; choose from: {', '.join(available_modes())}")
    if not dry_run and model_id not in config.included_models():
        click.secho(
            f"Warning: {model_id} is not flagged include:true in the model config.",
            fg="yellow",
        )
    if is_scaffolded(mode, model_id, scaffold_model):
        click.secho(f"{model_id} runs WITH scaffold (older_plus_scaffold).", fg="cyan")

    logs = run_task(task_id, model_id, repetitions=repetitions, dry_run=dry_run,
                    mode=mode, scaffold_model=scaffold_model, network=network)
    paths = write_run_records(logs, suite=suite, mode=mode)
    click.secho(f"\nWrote {len(paths)} run record(s):", fg="green")
    for p in paths:
        record = json.loads(p.read_text())
        execu = record.get("execution", {})
        if execu.get("invalid"):
            click.secho(f"  {p.parent.name}: INVALID ({execu.get('invalid_reason')})", fg="yellow")
            continue
        s = record["scoring"]
        po = s.get("partial_objective_score")
        click.echo(
            f"  {p.parent.name}: verified={s['verified_success']} "
            f"partial_obj={po:.1f} hidden={s['hidden_test_score']}"
            if po is not None else f"  {p.parent.name}: verified={s['verified_success']}"
        )


@main.command("run-matrix")
@click.option("--suite", required=True, help="Results suite name.")
@click.option("--tasks", default=None, help="Comma-separated task IDs (default: all).")
@click.option("--models", default=None, help="Comma-separated model IDs (default: included).")
@click.option("--repetitions", default=1, type=int, help="Repetitions per task per model.")
@click.option("--mode", default="default", help="Evaluation mode.")
@click.option("--seed", default=12345, type=int, help="Run-order randomization seed.")
@click.option("--randomize/--no-randomize", default=True, help="Blocked-randomize model order.")
@click.option("--network", type=click.Choice(["disabled", "enabled"]), default=None,
              help="Override sandbox network (a real model run needs 'enabled').")
@click.option("--dry-run", is_flag=True, help="Apply reference solution, no API calls.")
def run_matrix_cmd(suite, tasks, models, repetitions, mode, seed, randomize, network, dry_run):
    """Run the task x model x repetition matrix with blocked randomization."""
    from datetime import datetime, timezone

    from agent_delta.matrix import run_matrix
    from agent_delta.reproducibility import build_manifest, write_manifest

    task_ids = tasks.split(",") if tasks else list_tasks()
    model_ids = models.split(",") if models else list(config.included_models())
    total = len(task_ids) * len(model_ids) * repetitions
    click.secho(f"Running {total} run(s): {len(task_ids)} tasks x {len(model_ids)} "
                f"models x {repetitions} reps (mode={mode}, seed={seed}).", fg="cyan")

    def progress(rep, task_id, model_id):
        click.echo(f"  rep {rep} | {task_id} | {model_id}")

    order_log, fixtures = run_matrix(
        suite, task_ids, model_ids, repetitions=repetitions, mode=mode, seed=seed,
        randomize=randomize, dry_run=dry_run, network=network, on_run=progress,
    )
    date = datetime.now(timezone.utc).date().isoformat()
    manifest = build_manifest(
        suite=suite, date=date, models=model_ids, tasks=task_ids,
        fixtures=fixtures, run_order_seed=seed if randomize else None,
    )
    manifest["run_order"] = order_log
    path = write_manifest(manifest, suite)
    click.secho(f"\nWrote reproducibility manifest: {path}", fg="green")
    click.echo("Run `agentdelta report --suite <suite>` to aggregate.")


@main.command("validate-reproducibility")
@click.option("--suite", required=True, help="Suite whose reproducibility.json to check.")
def validate_repro_cmd(suite: str) -> None:
    """Recompute content hashes and check them against the recorded manifest."""
    import json

    from agent_delta.reproducibility import validate_manifest

    path = config.RESULTS_DIR / "reports" / suite / "reproducibility.json"
    if not path.exists():
        raise click.UsageError(f"No reproducibility.json at {path}")
    problems = validate_manifest(json.loads(path.read_text()))
    if problems:
        for p in problems:
            click.secho(f"  drift: {p}", fg="red")
        raise SystemExit(1)
    click.secho(f"reproducible: content hashes match {path}", fg="green")


@main.command("review-packets")
@click.option("--suite", required=True, help="Suite under results/raw to build packets for.")
def review_packets_cmd(suite: str) -> None:
    """Write blinded review packets (packet.json) next to each run for judging."""
    import json

    from agent_delta.registry import load_task
    from agent_delta.scoring.review import build_review_packet

    root = config.RAW_RESULTS_DIR / suite
    count = 0
    for run_json in sorted(root.rglob("run.json")):
        record = json.loads(run_json.read_text())
        diff = (run_json.parent / "final.diff")
        diff_text = diff.read_text() if diff.exists() else ""
        try:
            prompt = load_task(record["task_id"]).prompt
        except Exception:
            prompt = ""
        packet = build_review_packet(prompt, record, diff_text)
        (run_json.parent / "packet.json").write_text(json.dumps(packet, indent=2))
        count += 1
    click.secho(f"Wrote {count} blinded review packet(s) under {root}", fg="green")
    click.echo("Fill each packet's rubric (0-5) into a review.json next to it, then re-run report.")


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
            for mid in data["level1"]["ranking"]
        )
        click.echo(f"  [{mode}] L1 ranking: {ranked}")
        material = [i["model_b"] for i in data["level1"]["improvements"] if i["material"]]
        click.echo(f"  [{mode}] L2 escalated (material gains): {', '.join(material) or 'none'}")


@main.command("report")
@click.option("--results", "results_dir", default=None, help="Dir of run records (defaults from suite).")
@click.option("--suite", required=True, help="Suite name.")
@click.option("--baseline", default=None, help="Baseline model ID for amplification.")
@click.option("--level", type=click.Choice(["1", "2", "both"]), default="both",
              help="1 = primary assessment only; 2 = amplification only; both (default).")
@click.option("--output", default=None, help="Markdown output path.")
def report_cmd(results_dir: str | None, suite: str, baseline: str | None,
               level: str, output: str | None) -> None:
    """Generate a Markdown report from run records."""
    from agent_delta.reporting import build_report, render, write_report_json

    rdir = Path(results_dir) if results_dir else (config.RAW_RESULTS_DIR / suite)
    report = build_report(rdir, suite=suite, baseline=baseline)
    write_report_json(report, suite)
    levels = (1, 2) if level == "both" else (int(level),)
    md = render(report, levels=levels)
    out = Path(output) if output else (config.RESULTS_DIR / "reports" / suite / "report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    click.secho(f"Wrote {out}", fg="green")


if __name__ == "__main__":
    main()
