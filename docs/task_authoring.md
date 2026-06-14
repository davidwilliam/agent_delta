# Task authoring

A task is a controlled coding assignment against a known fixture state (SPEC §8).

## Files in `tasks/<id>/`

| File | Purpose |
| --- | --- |
| `task.yaml` | Manifest: id, category, repo, scope, tests, acceptance (schema: `agent_delta/schemas/task.schema.json`) |
| `prompt.md` | Realistic user request. **Must not leak the hidden tests.** |
| `public_tests.py` | Encodes stated acceptance criteria. Injected at score time. |
| `hidden_tests.py` | Edge cases / generalization. Never shown to the agent. |
| `expected_behavior.md` | Human reference for what a correct solution looks like. |
| `reference_solution/` | *(optional)* Mirror of repo files; used only by `--dry-run`. |

## Rules

- Public and hidden tests import the installed package and are run from `/tmp` in
  the sandbox - they are **never** committed into the fixture the agent sees.
- Hidden tests must include the discriminating edge cases (the ones a lazy or
  partial solution fails). That is what separates models.
- Set `scope.forbidden_paths` and `max_files_modified` to detect overbroad edits.
- Keep baseline tests (in the fixture) green; they are the regression surface.

## Validate

```bash
agentdelta validate-task <id>        # static: prompt + test files + fixture exist
agentdelta check-task <id>           # dynamic: fails at base, passes with reference
agentdelta check-task --all          # check every task
```

`check-task` spins up the sandbox container and asserts the task is both
**non-trivial** (public/hidden tests fail on the clean base - the tests really
detect the missing/buggy behavior) and **solvable** (after applying
`reference_solution/`, the baseline + public + hidden suites all pass). Run it on
every new task; a task that passes at base or whose reference doesn't pass is a
bug in the task, not a strong eval.

## The fixture must stay green at base

All tasks share one fixture base commit, so the fixture must contain every task's
latent bug/missing-feature simultaneously while its **baseline** suite still
passes. Put the discriminating cases only in the injected public/hidden tests,
never in the fixture's own `tests/` (those are the regression surface).

## Languages

Public/hidden test injection is language-aware (`agent_delta/scoring/testrunner.py`),
driven by the fixture manifest's `language`.

- **python**: test files run in isolation from `/tmp` and import the editable
  installed package (`from mathkit import ...`).
- **go**: test files are written into an external test package under the module
  at `agentdelta_eval/<public|hidden>/` and run with `go test`. Each file must
  declare `package eval` and import the fixture module (for example
  `import "textkit"`). A missing symbol at base produces a build failure, which
  the parser counts as a failing (non-trivial) result.

To add another language, give it an `injection` plan and an output parser in
`testrunner.py` and set `language` plus `base_image` in the fixture manifest.

## Test-writing tasks (mutation scoring)

Set `task_type: test_writing` and a `test_writing.target_path` in `task.yaml`. The
agent writes tests (only test files, source is forbidden by scope). Instead of
injected public/hidden tests, the scorer runs the agent's tests against the
correct code (they must pass) and then against each planted mutant under
`tasks/<id>/mutants/<name>/<repo-relative-path>` (they must fail). The mutation
kill rate becomes the hidden-test score, and `mutation_threshold` (default 1.0)
gates verified success. Author mutants as small bugs that the baseline suite does
not already catch, so only a good new test kills them. The `reference_solution/`
holds a test file that kills every mutant (used by `--dry-run` and `check-task`).
