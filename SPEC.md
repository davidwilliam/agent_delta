Recommended project name: **AgentDelta**.

It is serious enough for a benchmark project, and it captures the core idea: you are not asking whether a new model is “cooler”; you are measuring the **delta** between agentic coding systems under controlled conditions.

On the model question: **I would not include Haiku in the 1M-context Anthropic cohort right now.** Anthropic’s current docs list **Claude Opus 4.8, Opus 4.7, Opus 4.6, and Claude Sonnet 4.6** as 1M-context models on the Claude API, Bedrock, and Vertex AI, with a Microsoft Foundry exception for Opus 4.8. The same docs list **Claude Haiku 4.5** with a **200k** context window, not 1M. ([Claude API Docs][1])

The project direction is also well supported by Inspect: `inspect_swe` exposes **Claude Code, Codex CLI, and Gemini CLI** as standard Inspect agents, runs them inside the sample sandbox, and proxies their model API calls back to Inspect so token/time limits and logs work normally. ([Meridian Labs AI][2]) Claude Code’s own model configuration docs also reinforce the need to avoid aliases for serious evals: aliases like `opus`, `sonnet`, `opus[1m]`, and `sonnet[1m]` exist, but aliases can update over time, so the spec should require pinned full model names. ([Claude API Docs][3])

Below is a draft `SPEC.md`.

# AgentDelta SPEC.md

**Project:** AgentDelta
**Subtitle:** Reproducible evaluation of frontier coding agents and model-upgrade deltas
**Status:** Draft v0.1
**Date:** 2026-06-13
**Initial owner:** David Silva
**Initial evaluator:** Claude Code
**Future evaluators:** Codex CLI, Gemini CLI
**Initial provider family:** Anthropic Claude
**Initial model cohort:** Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6
**Context-window requirement:** 1M-token context only for the initial Anthropic cohort

---

# 1. Purpose

AgentDelta is a reproducible evaluation framework for comparing frontier coding models as deployed through real agentic coding tools.

The project exists to answer a specific practical question:

> When a new frontier coding model is released and public commentary claims that it is dramatically superior to the previous model, is that claim supported by measurable evidence on real coding-agent workloads?

AgentDelta evaluates model upgrades and agentic coding systems through controlled, repeatable, auditable tasks. The output is not a vague preference judgment. The output is a structured report containing task-success rates, hidden-test results, regression rates, latency, token consumption, tool usage, cost, patch quality, and statistically meaningful ranking.

The first implementation will evaluate Anthropic Claude models through Claude Code. The architecture must support Codex CLI and Gemini CLI from the beginning, even if those integrations are implemented after the Claude Code baseline.

---

# 2. Core thesis

AgentDelta treats coding models as deployed systems, not as abstract chatbots.

For agentic coding, the evaluated object is not merely:

```text
model = neural network behind an API
```

The evaluated object is:

```text
agentic system =
  model
+ coding agent scaffold
+ tool permissions
+ system prompt
+ repository state
+ sandbox
+ context-management behavior
+ test-running behavior
+ editing behavior
+ retry behavior
+ cost and latency profile
```

Therefore, AgentDelta distinguishes between three evaluation modes:

1. **Model-upgrade mode**
   Same agent scaffold, different model versions.
   Example: Claude Code with Opus 4.6 vs Opus 4.7 vs Opus 4.8.

2. **Agent-product mode**
   Different agent products, each with its pinned model and native scaffold.
   Example: Claude Code vs Codex CLI vs Gemini CLI.
   This evaluates deployed coding-agent systems, not pure model capability.

3. **Controlled-model mode**
   Different providers or models evaluated through a common Inspect-native solver with standardized tools.
   This mode is used when the goal is to compare model capability while minimizing differences in the surrounding agent scaffold.

The initial release focuses on **model-upgrade mode** for Claude Code.

---

# 3. Non-goals

AgentDelta is not:

* A general AGI benchmark.
* A public popularity leaderboard.
* A subjective “which model feels better” comparison.
* A benchmark designed to maximize model scores.
* A benchmark based primarily on LLM-as-judge grading.
* A replacement for security, alignment, or safety evaluations.
* A claim that coding-agent performance generalizes to all domains.
* A claim that a model is globally superior because it wins a specific workload.

AgentDelta must avoid overclaiming. A valid conclusion is domain-specific, model-version-specific, agent-version-specific, and date-specific.

Example of an invalid conclusion:

```text
Opus 4.8 is better than Opus 4.7.
```

Example of a valid conclusion:

```text
In AgentDelta v0.1, using Claude Code version X, on 50 repo-based coding tasks with 5 repeated runs per task, Claude Opus 4.8 achieved a higher verified task-success rate than Claude Opus 4.7, with the largest gains on long-horizon multi-file tasks and no statistically meaningful improvement on small isolated bug fixes.
```

---

# 4. Initial model scope

## 4.1 Anthropic initial cohort

The first Anthropic evaluation cohort is:

```text
claude-opus-4-8
claude-opus-4-7
claude-opus-4-6
claude-sonnet-4-6
```

The initial requirement is that every included model must support a 1M-token context window under the selected access path.

## 4.2 Haiku exclusion

Haiku is excluded from the initial 1M-context cohort unless Anthropic releases a Haiku model with a 1M-token context window.

Current expected exclusion:

```text
claude-haiku-4-5
Reason: 200k context window, not 1M.
```

## 4.3 Future provider cohorts

Future cohorts may include:

```text
OpenAI models through Codex CLI
Google Gemini models through Gemini CLI
Provider-independent models through OpenCode
Open-weight models through a standardized Inspect-native agent
```

Each cohort must declare:

```text
provider
agent scaffold
model identifier
context window
pricing basis
API access path
model versioning semantics
tool availability
sandbox permissions
```

---

# 5. Evaluation principles

AgentDelta follows these principles.

## 5.1 Reproducibility over vibes

Every run must be reproducible or, when full determinism is impossible, auditable.

The benchmark must preserve:

```text
task prompt
repository base commit
agent version
model ID
model configuration
tool configuration
sandbox image
public test output
hidden test output
final diff
agent transcript
token usage
cost estimate
wall-clock time
run order
failure mode
```

## 5.2 Pinned versions

Every evaluation must pin:

```text
model ID
agent CLI version
Inspect version
inspect-swe version
Docker image digest
repository commit
dependency lockfiles
task manifest version
scoring script version
```

Aliases such as `opus`, `sonnet`, `opus[1m]`, or `latest` must not be used in official benchmark runs.

Aliases may be used only in exploratory local experiments, and those results must not be published as official AgentDelta results.

## 5.3 Same task, same state

Every model must receive the same task from the same initial repository state.

The benchmark must reset the repository before every run.

A valid run starts from:

```text
clean git worktree
known base commit
dependencies installed from lockfiles
baseline tests passing
no leftover files from previous runs
no hidden state from another model
```

## 5.4 Objective scoring first

Primary scoring must be based on objective signals:

```text
public tests
hidden tests
build result
lint result
type-check result
security checks
acceptance criteria
regression checks
runtime behavior
```

Subjective review is allowed only as a secondary layer.

## 5.5 No silent fallback

Silent model fallback invalidates a run.

If a tool, provider, or agent falls back to another model, the run must be marked invalid unless the purpose of the run is explicitly to evaluate fallback behavior.

## 5.6 Predeclared claims

AgentDelta must declare scoring rules and materiality thresholds before running the benchmark.

The benchmark must not change the scoring formula after seeing results.

## 5.7 Raw results over leaderboard numbers

The final rank matters, but raw results matter more.

Every report must include:

```text
raw per-task results
aggregate metrics
confidence intervals
model-by-task matrix
failure taxonomy
cost and latency summaries
category-level breakdown
scoring formula
limitations
```

---

# 6. System architecture

AgentDelta uses Inspect AI as the evaluation harness.

The architecture has these components:

```text
AgentDelta
├── Inspect task definitions
├── Inspect SWE agent adapters
│   ├── Claude Code adapter
│   ├── Codex CLI adapter
│   └── Gemini CLI adapter
├── Docker sandbox environment
├── Task registry
├── Repository fixture registry
├── Scorers
│   ├── test scorer
│   ├── hidden-test scorer
│   ├── regression scorer
│   ├── diff scorer
│   ├── cost scorer
│   ├── latency scorer
│   └── optional blinded-review scorer
├── Run orchestrator
├── Result store
├── Report generator
└── Reproducibility manifest
```

---

# 7. Repository structure

Recommended repository layout:

```text
agent-delta/
  SPEC.md
  README.md
  LICENSE
  pyproject.toml
  uv.lock or requirements.lock

  agent_delta/
    __init__.py
    config.py
    registry.py
    scoring/
      __init__.py
      objective.py
      cost.py
      latency.py
      diff.py
      stats.py
      review.py
    runners/
      __init__.py
      claude_code.py
      codex_cli.py
      gemini_cli.py
    reporting/
      __init__.py
      aggregate.py
      tables.py
      charts.py
      markdown.py
    schemas/
      task.schema.json
      run.schema.json
      report.schema.json

  evals/
    anthropic_claude_code.py
    codex_cli.py
    gemini_cli.py
    controlled_model.py

  tasks/
    task_001/
      task.yaml
      prompt.md
      public_tests.sh
      hidden_tests.sh
      expected_behavior.md
      scoring_notes.md
    task_002/
      task.yaml
      prompt.md
      public_tests.sh
      hidden_tests.sh
      expected_behavior.md
      scoring_notes.md

  repos/
    manifests/
      rails_api.yaml
      python_package.yaml
      node_service.yaml
      go_cli.yaml
    fixtures/
      rails_api/
      python_package/
      node_service/
      go_cli/

  sandboxes/
    claude-code/
      Dockerfile
      compose.yaml
    codex-cli/
      Dockerfile
      compose.yaml
    gemini-cli/
      Dockerfile
      compose.yaml
    common/
      base.Dockerfile

  configs/
    models/
      anthropic.yaml
      openai.yaml
      google.yaml
    agents/
      claude_code.yaml
      codex_cli.yaml
      gemini_cli.yaml
    scoring/
      default.yaml

  results/
    raw/
    normalized/
    reports/

  scripts/
    run_eval.py
    aggregate_results.py
    generate_report.py
    validate_task.py
    validate_reproducibility.py

  docs/
    methodology.md
    scoring.md
    task_authoring.md
    reproducibility.md
    limitations.md
```

---

# 8. Task design

## 8.1 Task definition

A task is a controlled coding assignment executed against a known repository state.

Each task must define:

```text
task ID
category
difficulty
repository fixture
base commit
prompt
allowed files or allowed scope
public tests
hidden tests
timeout
cost budget
acceptance criteria
failure conditions
expected artifacts
```

## 8.2 Task categories

The initial benchmark should include at least 50 tasks.

Recommended distribution:

| Category                      | Count | Purpose                                               |
| ----------------------------- | ----: | ----------------------------------------------------- |
| Small bug fixes               |    10 | Measures local reasoning and precision                |
| Medium feature additions      |    10 | Measures implementation completeness                  |
| Multi-file refactors          |     8 | Measures architecture awareness                       |
| Security fixes                |     6 | Measures correctness under risk-sensitive constraints |
| Test-writing tasks            |     6 | Measures verification and test design                 |
| Long-horizon repo tasks       |     6 | Measures sustained agentic work                       |
| Dependency or migration tasks |     4 | Measures real-world maintenance behavior              |

Minimum viable release:

```text
30 tasks
3 repeated runs per model
4 models
360 total runs
```

Preferred first serious release:

```text
50 tasks
5 repeated runs per model
4 models
1,000 total runs
```

Strong release:

```text
75 tasks
5 repeated runs per model
4 models
1,500 total runs
```

## 8.3 Task manifest

Each task must include a `task.yaml` file.

Example:

```yaml
id: task_017
title: Add CSV export with authorization
category: medium_feature
difficulty: 3
repo: rails_api
base_commit: abc123
language: ruby
framework: rails
prompt_file: prompt.md

context_requirement:
  min_context_tokens: 200000
  preferred_context_tokens: 1000000

execution:
  timeout_minutes: 30
  max_cost_usd: 5.00
  max_agent_turns: null
  network: disabled
  package_install: false

scope:
  allowed_paths:
    - app/
    - config/routes.rb
    - spec/
  forbidden_paths:
    - db/schema.rb
    - config/credentials.yml.enc
  max_files_modified: 8

tests:
  baseline:
    - bundle exec rspec
  public:
    - bundle exec rspec spec/requests/exports_spec.rb
  hidden:
    - ./eval/hidden/task_017.sh

acceptance_criteria:
  - CSV export endpoint exists.
  - Endpoint requires authorization.
  - Export includes expected fields.
  - Existing tests continue passing.
  - Hidden tests pass.
  - No unrelated files are modified.

scoring:
  objective_weight: 0.95
  review_weight: 0.05

notes:
  - This task is intended to detect overbroad edits.
  - A passing solution should not alter the authentication model.
```

## 8.4 Prompt file

The prompt must be written as a realistic user request.

It should not leak the hidden tests.

Example:

```markdown
You are working in this repository.

Please add a CSV export endpoint for the Orders resource.

Requirements:
1. Only authenticated users may export orders.
2. The export should include order ID, customer email, status, total, and created date.
3. Add or update tests as needed.
4. Keep the change minimal and consistent with existing conventions.
5. Do not modify unrelated behavior.

When finished, run the relevant tests and summarize what changed.
```

## 8.5 Public vs hidden tests

AgentDelta uses two test layers:

1. **Public tests**
   Visible in the repo or task description. These measure whether the model can satisfy known criteria.

2. **Hidden tests**
   Not shown to the model during the run. These measure generalization, edge cases, and regression safety.

For public reproducibility, hidden tests should be published with the final benchmark release or at least cryptographically committed before evaluation.

Recommended approach:

```text
Before benchmark:
  publish hash of hidden tests

During benchmark:
  keep hidden tests unavailable to the agent

After benchmark report:
  publish hidden tests or provide reproducibility package
```

For ongoing internal evaluation, maintain a private holdout suite and clearly label results as non-publicly reproducible.

---

# 9. Repository fixtures

AgentDelta should use controlled repository fixtures rather than only arbitrary public repositories.

Recommended fixture types:

| Fixture        | Language         | Purpose                            |
| -------------- | ---------------- | ---------------------------------- |
| rails_api      | Ruby/Rails       | API, auth, jobs, tests             |
| python_package | Python           | library logic, typing, packaging   |
| node_service   | TypeScript/Node  | API, async logic, test framework   |
| go_cli         | Go               | CLI, error handling, concurrency   |
| react_app      | TypeScript/React | frontend state and component tests |

Each fixture repository must include:

```text
clear dependency lockfiles
baseline passing test suite
intentional bugs or missing features
style conventions
moderate complexity
no secrets
no proprietary code
no external network dependency for tests
```

The first release may use fewer fixtures, but at least two languages/frameworks are recommended to avoid overfitting to one stack.

---

# 10. Agent adapters

## 10.1 Claude Code adapter

Initial agent:

```text
Claude Code through inspect_swe.claude_code()
```

Required configuration:

```text
agent version pinned
model ID pinned
1M context mode enabled where applicable
no aliases in official runs
network policy declared
web search disabled unless task explicitly requires it
fallback disabled or detected
MCP servers standardized
skills standardized
tool permissions standardized
```

Initial Anthropic model matrix:

```yaml
models:
  - id: claude-opus-4-8
    family: opus
    context_window: 1000000
    include: true

  - id: claude-opus-4-7
    family: opus
    context_window: 1000000
    include: true

  - id: claude-opus-4-6
    family: opus
    context_window: 1000000
    include: true

  - id: claude-sonnet-4-6
    family: sonnet
    context_window: 1000000
    include: true

  - id: claude-haiku-4-5
    family: haiku
    context_window: 200000
    include: false
    exclusion_reason: "Does not satisfy initial 1M-context requirement."
```

## 10.2 Codex CLI adapter

Future agent:

```text
Codex CLI through inspect_swe.codex_cli()
```

The Codex CLI evaluation must declare:

```text
Codex CLI version
OpenAI model ID
model context window
reasoning effort, if applicable
tool permissions
web search setting
sandbox restrictions
config overrides
```

The Codex CLI results must be labeled as either:

```text
model-upgrade mode
agent-product mode
controlled-model mode
```

## 10.3 Gemini CLI adapter

Future agent:

```text
Gemini CLI through inspect_swe.gemini_cli()
```

The Gemini CLI evaluation must declare:

```text
Gemini CLI version
Gemini model ID
model context window
reasoning configuration, if applicable
tool permissions
MCP configuration
web search setting
sandbox restrictions
quota or rate-limit conditions
```

## 10.4 Agent-product fairness

Claude Code, Codex CLI, and Gemini CLI do not have identical scaffolds. Therefore, cross-agent comparisons must not be described as pure model comparisons.

Correct phrasing:

```text
Claude Code with model X outperformed Codex CLI with model Y on this task suite.
```

Incorrect phrasing:

```text
Model X is better than model Y.
```

Unless controlled-model mode is used, the result includes both model and scaffold effects.

---

# 11. Execution protocol

Every run must follow the same lifecycle.

## 11.1 Pre-run validation

Before each run:

```text
1. Create fresh sandbox.
2. Checkout fixture repository at base commit.
3. Verify clean git status.
4. Install dependencies from lockfiles.
5. Run baseline test command.
6. Confirm baseline tests pass.
7. Load task prompt.
8. Load agent configuration.
9. Confirm model ID is pinned.
10. Confirm no model alias is used.
11. Confirm no fallback model is enabled or fallback detection is active.
12. Start run timer.
```

If baseline tests fail, the task run is invalid.

## 11.2 Agent run

During each run, the orchestrator must capture:

```text
agent stdout
agent stderr
agent event stream, if available
model requests
model responses, where available
tool calls
file reads
file writes
shell commands
failed shell commands
test commands
wall-clock time
token usage
cost estimate
rate-limit events
permission prompts
crashes
timeouts
```

## 11.3 Post-run scoring

After the agent stops:

```text
1. Capture final git diff.
2. Capture modified file list.
3. Run public tests.
4. Run hidden tests.
5. Run full regression suite.
6. Run linters or type checks, if declared.
7. Run static diff checks.
8. Compute objective score.
9. Archive all artifacts.
10. Reset repository.
```

## 11.4 Invalid runs

A run is invalid if:

```text
baseline tests fail before agent execution
wrong model is used
model fallback occurs without being part of the experiment
agent crashes for infrastructure reasons
sandbox cannot initialize
API outage prevents completion
rate limit prevents fair execution
repository state is contaminated by a previous run
```

Invalid runs must be reported separately and not silently discarded.

---

# 12. Randomization and repetition

## 12.1 Repeated runs

Because frontier API models and coding agents may be nondeterministic, AgentDelta requires repeated runs.

Recommended levels:

```text
Exploratory: 3 runs per task per model
Standard:    5 runs per task per model
Strong:     10 runs per task per model
```

The first serious Anthropic report should use:

```text
50 tasks
5 runs per task
4 models
1,000 total runs
```

## 12.2 Interleaved model order

Do not run all tasks for one model before moving to the next.

Use blocked randomization:

```text
For each task:
  randomize model order
  run each model once
  repeat for N repetitions
```

Example:

```text
task_017 repetition_1:
  opus-4.7
  sonnet-4.6
  opus-4.8
  opus-4.6

task_017 repetition_2:
  opus-4.6
  opus-4.8
  sonnet-4.6
  opus-4.7
```

This reduces bias from transient provider load, network conditions, local machine state, rate limits, and time-of-day effects.

---

# 13. Metrics

AgentDelta separates metrics into primary, secondary, and diagnostic metrics.

## 13.1 Primary metrics

Primary metrics determine rank.

| Metric                   | Definition                                            |
| ------------------------ | ----------------------------------------------------- |
| Verified task success    | Task satisfies all objective acceptance criteria      |
| Hidden-test pass rate    | Hidden tests passed divided by hidden tests attempted |
| Regression avoidance     | Existing behavior remains intact                      |
| Full completion rate     | Agent completes without human intervention            |
| Cost per successful task | Total cost divided by number of successful tasks      |
| Median time to success   | Median wall-clock time among successful runs          |
| Scope-control score      | Avoidance of unrelated or unauthorized changes        |

## 13.2 Secondary metrics

Secondary metrics explain why a model won or lost.

| Metric                    | Definition                                                            |
| ------------------------- | --------------------------------------------------------------------- |
| Public test pass rate     | Public tests passed                                                   |
| Build pass rate           | Build succeeds after patch                                            |
| Lint/type-check pass rate | Declared static checks pass                                           |
| Token consumption         | Input, output, cache read, cache write, reasoning tokens if available |
| API request count         | Number of model calls                                                 |
| Agent turn count          | Number of agent iterations                                            |
| Tool-call count           | Number of tool invocations                                            |
| Shell-command count       | Number of commands run                                                |
| Failed-command count      | Number of failed commands                                             |
| Test-run count            | Number of times the agent ran tests                                   |
| Files read                | Number of files inspected                                             |
| Files modified            | Number of files changed                                               |
| Lines added/removed       | Patch size                                                            |
| Timeout rate              | Runs exceeding timeout                                                |
| Crash rate                | Agent or tool failures                                                |
| Refusal rate              | Runs where the model refuses or fails due to policy                   |

## 13.3 Diagnostic metrics

Diagnostic metrics are not ranking metrics unless explicitly promoted in the scoring configuration.

Examples:

```text
first-test-run time
time before first edit
ratio of exploration to editing
ratio of failed commands to total commands
number of repeated failed commands
number of unnecessary file reads
number of unrelated file modifications
number of reverted edits
patch entropy
diff locality
test-to-code change ratio
```

---

# 14. Scoring

AgentDelta must publish both:

1. **Objective Score**
2. **Full Score**

The Objective Score excludes subjective review.

The Full Score may include a small blinded-review component.

## 14.1 Objective Score

Default formula:

```text
Objective Score =
  60% verified task success
  15% hidden-test score
  10% regression avoidance
   5% scope-control score
   5% cost-efficiency score
   5% time-efficiency score
```

The score is computed on a 0–100 scale.

## 14.2 Full Score

Default formula:

```text
Full Score =
  95% Objective Score
   5% blinded-review score
```

The blinded-review score may be removed entirely for reports that want objective-only ranking.

## 14.3 Cost-efficiency score

Cost-efficiency is normalized against the best model in the same evaluation set.

```text
cost_efficiency_score(model) =
  min(1.0, best_cost_per_success / model_cost_per_success)
```

Then convert to 0–100.

A model cannot compensate for poor correctness merely by being cheap. Therefore, cost efficiency has limited weight.

## 14.4 Time-efficiency score

Time-efficiency is normalized against the fastest successful model in the same evaluation set.

```text
time_efficiency_score(model) =
  min(1.0, best_median_time_to_success / model_median_time_to_success)
```

Then convert to 0–100.

A model cannot compensate for poor correctness merely by being fast.

## 14.5 Scope-control score

Scope-control measures whether the model stayed inside the intended task boundary.

Penalties apply for:

```text
modifying forbidden paths
changing unrelated files
deleting files without instruction
rewriting configuration unnecessarily
removing tests instead of fixing code
hardcoding hidden-test behavior
bypassing authentication or validation
introducing broad architectural changes for narrow tasks
```

## 14.6 Materiality thresholds

AgentDelta should avoid declaring victory for tiny differences.

Default thresholds:

```text
task-success improvement:
  material if >= 5 percentage points and statistically supported

cost improvement:
  material if >= 10% at comparable success

latency improvement:
  material if >= 10% at comparable success

regression reduction:
  material if >= 3 percentage points and statistically supported

category improvement:
  material if >= 10 percentage points in a category with enough tasks
```

A model may be ranked first while still being described as only marginally better.

---

# 15. Statistical analysis

AgentDelta must report uncertainty.

## 15.1 Binary outcomes

For pass/fail outcomes:

```text
success rate
95% confidence interval
paired win/loss/tie matrix
McNemar-style paired comparison where applicable
```

## 15.2 Continuous outcomes

For time, cost, token usage, and tool calls:

```text
median
mean
p25
p75
p90
bootstrap confidence interval
paired delta distribution
Wilcoxon signed-rank test where applicable
```

## 15.3 Multiple comparisons

When comparing many models and many categories, AgentDelta should avoid overclaiming from repeated testing.

Recommended approach:

```text
report raw p-values
report corrected p-values where formal significance is claimed
use Holm correction for families of pairwise comparisons
avoid presenting p-values as the only evidence
```

## 15.4 Statistical ties

If two models have materially overlapping confidence intervals and no clear paired advantage, AgentDelta must report them as statistically tied.

Example:

```text
Opus 4.8 ranks first numerically, but the difference from Opus 4.7 is not statistically meaningful on small bug-fix tasks.
```

---

# 16. Result schema

Each run must produce a structured result record.

Example:

```json
{
  "run_id": "2026-06-13T18-22-10Z_task-017_opus-4-8_rep-03",
  "benchmark_version": "agentdelta-v0.1",
  "task_id": "task_017",
  "task_category": "medium_feature",
  "repo": "rails_api",
  "base_commit": "abc123",
  "agent": "claude_code",
  "agent_version": "2.1.154",
  "provider": "anthropic",
  "model_id": "claude-opus-4-8",
  "context_window": 1000000,
  "model_config": {
    "effort": "high",
    "temperature": null,
    "top_p": null,
    "max_output_tokens": null,
    "fallback_disabled": true
  },
  "sandbox": {
    "docker_image": "agentdelta/claude-code@sha256:...",
    "network": "disabled",
    "os": "debian-bookworm",
    "cpu": "x86_64",
    "memory_gb": 16
  },
  "execution": {
    "start_time": "2026-06-13T18:22:10Z",
    "end_time": "2026-06-13T18:33:45Z",
    "wall_clock_seconds": 695,
    "timeout": false,
    "crash": false,
    "invalid": false
  },
  "usage": {
    "input_tokens": 184230,
    "output_tokens": 17291,
    "cache_read_tokens": 0,
    "cache_write_tokens": 0,
    "reasoning_tokens": null,
    "api_requests": 27,
    "estimated_cost_usd": 1.35
  },
  "agent_behavior": {
    "tool_calls": 43,
    "shell_commands": 16,
    "failed_shell_commands": 2,
    "test_runs": 3,
    "files_read": 29,
    "files_modified": 5,
    "lines_added": 218,
    "lines_removed": 74
  },
  "scoring": {
    "baseline_tests_passed": true,
    "public_tests_passed": true,
    "hidden_tests_passed": true,
    "regression_tests_passed": true,
    "scope_control_score": 1.0,
    "verified_success": true,
    "objective_score": 96.4,
    "review_score": 4.4,
    "full_score": 96.0
  },
  "artifacts": {
    "transcript_path": "results/raw/.../transcript.jsonl",
    "diff_path": "results/raw/.../final.diff",
    "stdout_path": "results/raw/.../stdout.txt",
    "stderr_path": "results/raw/.../stderr.txt",
    "test_output_path": "results/raw/.../tests.txt"
  }
}
```

---

# 17. Reporting format

Every benchmark report must include:

```text
benchmark version
evaluation date
model list
agent list
number of tasks
number of runs
task categories
hardware
sandbox configuration
agent versions
model IDs
context windows
pricing assumptions
scoring formula
primary ranking
objective-only ranking
category-level ranking
cost-success frontier
latency-success frontier
failure analysis
statistical uncertainty
limitations
raw result archive
```

## 17.1 Primary table

Example:

| Rank | Model             | Objective Score | Success | Hidden Tests | Regression Rate | Cost/Success | Median Time | Notes                           |
| ---: | ----------------- | --------------: | ------: | -----------: | --------------: | -----------: | ----------: | ------------------------------- |
|    1 | claude-opus-4-8   |            91.2 |     78% |          74% |              8% |        $0.82 |        9.7m | Strongest on long-horizon tasks |
|    2 | claude-opus-4-7   |            85.9 |     71% |          68% |             11% |        $0.91 |       10.8m | Close on small fixes            |
|    3 | claude-opus-4-6   |            80.4 |     66% |          61% |             14% |        $0.96 |       12.4m | More regressions                |
|    4 | claude-sonnet-4-6 |            77.8 |     63% |          59% |             10% |        $0.44 |        7.1m | Best cost profile               |

## 17.2 Category table

Example:

| Model             | Small Fixes | Features | Refactors | Security | Tests | Long-Horizon |
| ----------------- | ----------: | -------: | --------: | -------: | ----: | -----------: |
| claude-opus-4-8   |         86% |      82% |       76% |      72% |   78% |          70% |
| claude-opus-4-7   |         84% |      75% |       68% |      68% |   74% |          56% |
| claude-opus-4-6   |         80% |      70% |       60% |      64% |   70% |          48% |
| claude-sonnet-4-6 |         78% |      68% |       58% |      60% |   72% |          44% |

## 17.3 Permitted claims

AgentDelta reports must use evidence-bound language.

Allowed:

```text
On this benchmark, model A achieved a higher verified success rate than model B.
```

Allowed:

```text
Model A was more cost-efficient for successful tasks in this workload.
```

Allowed:

```text
The improvement was concentrated in long-horizon multi-file tasks.
```

Not allowed:

```text
Model A killed model B.
```

Not allowed:

```text
Nobody should use model B anymore.
```

Not allowed:

```text
Model A is categorically superior.
```

---

# 18. Blinded review

Subjective review is optional and secondary.

When used, it must be blinded.

## 18.1 Review packet

A reviewer sees:

```text
task prompt
final diff
test output
agent summary, anonymized
```

A reviewer must not see:

```text
model name
agent name, if comparing agents
run order
provider
whether the model is newer
cost
latency
```

## 18.2 Review rubric

Each reviewed patch receives 0–5 scores:

| Criterion           | Description                                         |
| ------------------- | --------------------------------------------------- |
| Correctness         | Does the patch solve the intended problem?          |
| Maintainability     | Is the code understandable and idiomatic?           |
| Minimality          | Is the patch appropriately scoped?                  |
| Test quality        | Are tests meaningful and aligned with the behavior? |
| Risk control        | Does the patch avoid dangerous or broad changes?    |
| Explanation quality | Is the final explanation accurate and useful?       |

The review score may contribute no more than 5% to the Full Score unless the report is explicitly a qualitative review report.

---

# 19. Cost model

AgentDelta must compute cost using provider-published pricing at the time of evaluation.

For each run:

```text
estimated_cost =
  input_token_cost
+ output_token_cost
+ cache_write_cost
+ cache_read_cost
+ reasoning_token_cost, if applicable
+ tool-use cost, if applicable
+ web-search cost, if applicable
```

The report must declare:

```text
pricing date
pricing source
currency
region or platform
discounts applied
batch discounts, if any
prompt caching behavior
fast mode or premium mode, if any
```

Cost-sensitive rankings must use:

```text
cost per successful task
cost per verified hidden-test pass
cost per category success
```

Raw cost alone is not a sufficient ranking metric.

---

# 20. Latency model

AgentDelta measures wall-clock time from agent start to agent termination.

Latency metrics:

```text
wall-clock seconds
time to first edit
time to first test run
time to success
median time among successful runs
timeout rate
p90 run time
```

Latency must be interpreted alongside success.

A fast failed run is not superior to a slower successful run unless the scoring configuration explicitly prioritizes exploratory speed.

---

# 21. Context-window policy

The initial Anthropic benchmark is restricted to models with a 1M-token context window.

The benchmark should include two task types:

1. **Normal-context tasks**
   Can be solved within 200k context.

2. **Long-context tasks**
   Designed to benefit from or require access to more than 200k tokens of repository, documentation, logs, or generated artifacts.

A model that does not meet the declared context-window requirement is excluded from the initial cohort.

Future reports may include a separate 200k-context cohort, but those results must not be mixed with 1M-context results without clear labeling.

---

# 22. Safety and sandboxing

AgentDelta runs autonomous coding agents. Therefore, all runs must occur inside isolated sandboxes.

Minimum sandbox requirements:

```text
no host filesystem access beyond mounted fixture
no real secrets
no production credentials
no persistent provider tokens inside fixture repos
network disabled by default
outbound network allowlist only when required
resource limits enforced
timeout enforced
process tree cleanup after run
artifact capture before cleanup
```

Tasks must avoid malicious dual-use content unless a separate safety benchmark is explicitly designed and approved.

Security-fix tasks are allowed when they involve benign defensive coding, such as:

```text
fixing path traversal
validating input
preventing insecure deserialization in a toy fixture
adding authorization checks
removing secret leakage from logs
```

---

# 23. Failure taxonomy

Every failed run must receive one or more failure labels.

Recommended labels:

```text
wrong_behavior
incomplete_implementation
public_tests_failed
hidden_tests_failed
regression_introduced
build_failed
lint_failed
typecheck_failed
timeout
agent_crash
provider_error
rate_limited
model_refusal
overbroad_edit
forbidden_file_modified
test_removed_or_weakened
hardcoded_solution
unnecessary_rewrite
dependency_breakage
security_regression
hallucinated_api
did_not_run_tests
looping_or_thrashing
```

The report must include failure frequencies per model.

---

# 24. Implementation phases

## Phase 0: Methodology lock

Deliverables:

```text
SPEC.md
scoring.md
task schema
run schema
initial model matrix
initial agent configuration
```

Exit criteria:

```text
methodology frozen for v0.1
scoring formula frozen
materiality thresholds frozen
initial task categories approved
```

## Phase 1: Claude Code baseline

Deliverables:

```text
Claude Code Inspect integration
Anthropic model matrix
10 pilot tasks
result schema implementation
artifact capture
basic aggregate report
```

Exit criteria:

```text
all four Anthropic models can run same task
runs produce structured JSON
public tests and hidden tests execute
cost and latency are recorded
invalid runs are detected
```

## Phase 2: Full Anthropic v0.1 benchmark

Deliverables:

```text
50 tasks
5 runs per task per model
1,000 total runs
statistical report
category-level analysis
failure taxonomy
raw artifacts archive
```

Exit criteria:

```text
publishable Anthropic model-upgrade report
clear ranking
confidence intervals
reproducibility package
limitations section
```

## Phase 3: Codex CLI adapter

Deliverables:

```text
Codex CLI Inspect integration
OpenAI model matrix
agent-product evaluation mode
controlled-model evaluation plan
```

Exit criteria:

```text
Codex CLI can run the same task suite
configuration is pinned
results are comparable at the agent-product level
```

## Phase 4: Gemini CLI adapter

Deliverables:

```text
Gemini CLI Inspect integration
Google model matrix
agent-product evaluation mode
controlled-model evaluation plan
```

Exit criteria:

```text
Gemini CLI can run the same task suite
configuration is pinned
results are comparable at the agent-product level
```

## Phase 5: Cross-agent report

Deliverables:

```text
Claude Code vs Codex CLI vs Gemini CLI report
agent-product ranking
controlled caveats
cost-success frontier
latency-success frontier
failure-mode comparison
```

Exit criteria:

```text
report clearly separates model effects from scaffold effects
no cross-agent result is mislabeled as a pure model comparison
```

---

# 25. Command-line interface

AgentDelta should provide a simple CLI.

Examples:

```bash
agentdelta validate-task tasks/task_017

agentdelta run \
  --suite anthropic-v0.1 \
  --agent claude-code \
  --model claude-opus-4-8 \
  --repetitions 5

agentdelta run-matrix \
  --suite anthropic-v0.1 \
  --models configs/models/anthropic.yaml \
  --agent configs/agents/claude_code.yaml \
  --randomize \
  --repetitions 5

agentdelta aggregate \
  --results results/raw/anthropic-v0.1 \
  --output results/reports/anthropic-v0.1

agentdelta report \
  --results results/reports/anthropic-v0.1 \
  --format markdown \
  --output reports/anthropic-v0.1.md
```

---

# 26. Configuration examples

## 26.1 Anthropic model config

```yaml
provider: anthropic
access_path: claude_api
context_requirement: 1000000

models:
  claude-opus-4-8:
    include: true
    family: opus
    context_window: 1000000
    effort: high
    fallback_allowed: false

  claude-opus-4-7:
    include: true
    family: opus
    context_window: 1000000
    effort: high
    fallback_allowed: false

  claude-opus-4-6:
    include: true
    family: opus
    context_window: 1000000
    effort: high
    fallback_allowed: false

  claude-sonnet-4-6:
    include: true
    family: sonnet
    context_window: 1000000
    effort: high
    fallback_allowed: false

  claude-haiku-4-5:
    include: false
    family: haiku
    context_window: 200000
    exclusion_reason: "Does not satisfy 1M context requirement."
```

## 26.2 Claude Code agent config

```yaml
agent: claude_code
inspect_swe_agent: claude_code
version: pinned
network: disabled
web_search: disabled
skills: []
mcp_servers: []
permission_mode: benchmark_sandbox
fallback_detection: required

settings:
  use_aliases: false
  require_pinned_model_id: true
  require_clean_worktree: true
  archive_transcript: true
  archive_diff: true
  archive_test_output: true
```

## 26.3 Scoring config

```yaml
objective_score:
  verified_task_success: 0.60
  hidden_test_score: 0.15
  regression_avoidance: 0.10
  scope_control: 0.05
  cost_efficiency: 0.05
  time_efficiency: 0.05

full_score:
  objective_score: 0.95
  blinded_review: 0.05

materiality:
  task_success_delta_pp: 5
  category_success_delta_pp: 10
  cost_delta_percent: 10
  latency_delta_percent: 10
  regression_delta_pp: 3
```

---

# 27. Reproducibility manifest

Each benchmark report must include a `reproducibility.json`.

Example:

```json
{
  "agentdelta_version": "0.1.0",
  "date": "2026-06-13",
  "suite": "anthropic-claude-code-v0.1",
  "inspect_version": "x.y.z",
  "inspect_swe_version": "x.y.z",
  "python_version": "3.12.x",
  "docker_version": "x.y.z",
  "host_os": "macOS or Linux",
  "sandbox_images": {
    "claude_code": "sha256:..."
  },
  "agents": {
    "claude_code": {
      "version": "2.1.154",
      "settings_hash": "sha256:..."
    }
  },
  "models": [
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-opus-4-6",
    "claude-sonnet-4-6"
  ],
  "tasks_hash": "sha256:...",
  "scoring_hash": "sha256:...",
  "hidden_tests_hash": "sha256:...",
  "run_order_seed": 123456
}
```

---

# 28. Publication standards

A public AgentDelta report must include:

```text
What was tested
What was not tested
Why the models were selected
Why some models were excluded
How many tasks were used
How many repeated runs were used
How invalid runs were handled
How much the benchmark cost
Whether the benchmark can be reproduced
Where raw artifacts are stored
Which claims are supported
Which claims are not supported
```

The report must avoid hype language.

Recommended report title style:

```text
AgentDelta v0.1: Claude Code Model-Upgrade Evaluation from Opus 4.6 to Opus 4.8
```

Recommended subtitle:

```text
A reproducible comparison of task success, regressions, cost, latency, and agent behavior across 1M-context Claude models.
```

---

# 29. Example conclusion template

A valid AgentDelta conclusion should follow this format:

```markdown
## Conclusion

On AgentDelta v0.1, using Claude Code version [VERSION], four Anthropic 1M-context models were evaluated across [N] coding tasks with [R] repeated runs per task.

The strongest model by Objective Score was [MODEL], with a verified task-success rate of [X]%.

Compared with [BASELINE], [MODEL] improved verified task success by [DELTA] percentage points, changed median cost per successful task by [DELTA]%, and changed median time to success by [DELTA]%.

The improvement was concentrated in:
- [CATEGORY]
- [CATEGORY]

The improvement was not statistically meaningful in:
- [CATEGORY]
- [CATEGORY]

The main observed failure modes were:
- [FAILURE]
- [FAILURE]

Therefore, the evidence supports the claim that [MODEL] is a better choice for [WORKLOAD TYPE], but does not support a general claim that it is categorically superior for all coding tasks.
```

---

# 30. Open questions

The following decisions remain open for v0.1:

```text
1. Exact number of initial tasks: 30, 50, or 75.
2. Exact programming-language mix.
3. Whether to include proprietary DataHubz/Rubro-style internal tasks or only public fixtures.
4. Whether hidden tests will be released after the report.
5. Whether blinded human review will be included in v0.1.
6. Whether long-context tasks must exceed 200k tokens or merely be eligible for 1M context.
7. Whether to include Sonnet 4.6 as a cost/performance baseline or treat it as a separate class from Opus.
8. Whether to run all models at the same effort level or use provider-recommended defaults.
9. Whether network access is always disabled or selectively enabled for dependency tasks.
10. Whether future cross-agent reports should prioritize native-agent comparison or controlled-model comparison.
```

---

# 31. Initial acceptance criteria for AgentDelta v0.1

AgentDelta v0.1 is complete when:

```text
1. The Claude Code adapter runs under Inspect.
2. The four initial Anthropic models can be evaluated with pinned model IDs.
3. At least 30 tasks are implemented.
4. Every task has public tests, hidden tests, and acceptance criteria.
5. Every run produces a structured result JSON.
6. Every run archives transcript, diff, test output, and metadata.
7. The report generator produces model rankings.
8. The scoring formula is frozen before the official run.
9. The benchmark reports confidence intervals.
10. The final report separates objective results from subjective interpretation.
```

Preferred v0.1 completion:

```text
50 tasks
5 repeated runs per task
1,000 total model-task runs
full statistical report
raw artifact archive
public methodology document
```

---

# 32. Guiding rule

AgentDelta exists to replace hype with measured evidence.

The project should make it difficult to say:

```text
The new model is better because everyone says so.
```

And easy to say:

```text
The new model is better on these tasks, by these metrics, under these conditions, with this level of uncertainty, at this cost.
```

[1]: https://docs.anthropic.com/en/docs/build-with-claude/context-windows "Context windows - Claude API Docs"
[2]: https://meridianlabs-ai.github.io/inspect_swe/ "Inspect SWE"
[3]: https://docs.anthropic.com/en/docs/claude-code/model-config "Model configuration - Claude Code Docs"
