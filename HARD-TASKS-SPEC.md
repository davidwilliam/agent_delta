# HARD-TASKS-SPEC.md

**Project:** AgentDelta
**Document:** Hard Task Design Specification
**Status:** Draft v0.1
**Applies to:** AgentDelta SPEC.md and SPEC-ADDENDUM.md
**Purpose:** Define hard, objective, reproducible coding-agent tasks that expose known weaknesses of LLMs and agentic coding systems.


# 1. Purpose

AgentDelta evaluates frontier coding agents under realistic software-engineering conditions. This document defines the types of tasks that should be included in the benchmark when the goal is to expose meaningful differences between models and agents.

The purpose of this file is to answer:

> What kinds of coding tasks are fundamentally hard for LLMs and agentic coding systems to perform accurately?

A task is considered hard for AgentDelta when it requires more than surface-level code generation. It should require some combination of:

```text
repository understanding
multi-file reasoning
long-context retrieval
hidden invariant preservation
security or authorization judgment
state-machine correctness
test-driven verification
minimal-diff discipline
concurrency reasoning
performance preservation
migration safety
instruction adherence
failure recovery
```

AgentDelta should avoid tasks that are impressive in demos but weak as benchmarks.

Bad benchmark task:

```text
Create a tic-tac-toe game with a nice UI.
```

Better benchmark task:

```text
Fix a multi-tenant authorization bug in an existing codebase without weakening access controls, changing unrelated behavior, or modifying forbidden files. Hidden tests verify tenant isolation, regression safety, and edge cases.
```


# 2. Definition of a hard task

A hard task is not merely a long task. A hard task is one where an LLM or coding agent can produce something plausible while still being wrong.

A task qualifies as hard when it satisfies most of the following:

```text
1. It has objective pass/fail criteria.
2. It starts from a real or realistic repository state.
3. It requires reading and understanding multiple files.
4. The obvious solution is incomplete, unsafe, or wrong.
5. It contains hidden edge cases.
6. It includes explicit forbidden shortcuts.
7. It can detect regressions.
8. It rewards minimal, correct changes.
9. It penalizes overbroad rewrites.
10. It can be repeated across models.
11. It exposes known LLM failure modes.
12. It produces measurable artifacts: tests, diffs, tokens, time, cost, tool calls, and failure labels.
```

A task is weak when it is:

```text
purely subjective
mostly visual taste
single-file boilerplate
solvable from memorized examples
not objectively gradable
lacking hidden tests
lacking regression risk
lacking forbidden shortcuts
too dependent on external documentation
too ambiguous to score fairly
```


# 3. Known hard problems for LLM coding agents

This section describes known categories of difficulty that AgentDelta should deliberately test.

## 3.1 Repository-level reasoning

LLMs often perform better on isolated functions than on tasks requiring understanding of a full codebase. Real engineering tasks usually require reasoning across routes, controllers, services, models, tests, configuration, migrations, background jobs, and documentation.

Hardness pattern:

```text
The task cannot be solved correctly by editing one obvious file.
The correct fix requires understanding how multiple files interact.
```

Common failure modes:

```text
fixes the symptom instead of the cause
edits the wrong layer
duplicates existing logic
misses framework conventions
breaks another feature
modifies unrelated files
```

AgentDelta task examples:

```text
Fix an authorization bug where archived projects are still visible in team dashboards.

Add CSV export to an existing API while preserving current authorization and pagination behavior.

Change a serialized field name while preserving backward compatibility for existing clients.
```

Required scoring:

```text
public tests
hidden tests
full regression suite
diff scope check
forbidden-path check
```


## 3.2 Multi-file bug localization

LLMs frequently struggle to locate the true source of a bug when the user-facing symptom appears far from the root cause.

Hardness pattern:

```text
The failing behavior appears in one layer, but the bug originates elsewhere.
```

Example:

```text
Users with expired subscriptions can still download reports. The bug appears in the controller, but the real issue is a policy method that treats nil expiration dates incorrectly.
```

Common failure modes:

```text
patches controller instead of policy
adds redundant checks in the wrong layer
hardcodes special cases
breaks valid users
weakens authorization
fails hidden edge cases
```

Task requirements:

```text
at least 3 relevant files
at least 1 tempting wrong file
hidden tests for edge cases
minimal-diff expectation
```

Scoring signals:

```text
correct root-cause fix
hidden tests pass
no unrelated behavior change
no policy weakening
```


## 3.3 Hidden invariant preservation

LLMs often satisfy visible requirements while breaking deeper business invariants.

Hardness pattern:

```text
The requested feature is easy to implement naively, but hard to implement while preserving existing invariants.
```

Example:

```text
Add partial refunds, but ensure total_refunded_cents never exceeds total_paid_cents.
```

Common failure modes:

```text
handles happy path only
misses multiple sequential operations
misses negative values
misses concurrency
misses rounding edge cases
changes invariant definition
```

Recommended hidden tests:

```text
over-refund attempt
multiple partial refunds
zero amount
negative amount
currency rounding
concurrent refund attempts
refund after closed account
```

Required scoring:

```text
new feature tests pass
invariant tests pass
property-style tests pass when feasible
existing behavior remains unchanged
```


## 3.4 Long-context retrieval and “needle” use

Long context does not guarantee accurate use of context. LLMs may ignore relevant information, over-attend to recent files, or miss details buried in the middle of a large input.

Hardness pattern:

```text
The correct answer depends on a small detail located inside a large repository, documentation set, generated log, migration history, or configuration file.
```

Example:

```text
Fix the compliance report retention label using the official retention mapping documented in the internal policy file.
```

The relevant mapping may be buried in:

```text
docs/compliance/retention-policy.md
config/retention.yml
legacy migration notes
test fixtures
```

Common failure modes:

```text
invents plausible mapping
uses the wrong nearby mapping
ignores documentation
overfits to visible tests
chooses the most recent file instead of the authoritative file
```

Task requirements:

```text
large context corpus
one authoritative source
several plausible distractors
hidden tests for exact source-of-truth behavior
```

Scoring:

```text
correct source-of-truth used
hidden mapping tests pass
no invented constants
no unrelated configuration rewrites
```


## 3.5 Instruction adherence under negative constraints

LLMs may satisfy the main request while violating constraints. This is especially common when the forbidden path is the easiest way to make tests pass.

Hardness pattern:

```text
The model must solve the task while avoiding tempting shortcuts.
```

Example:

```text
Fix the flaky test without increasing timeouts, disabling retries, changing the assertion, or marking the test as skipped.
```

Common failure modes:

```text
weakens tests
skips tests
increases timeout
removes assertions
adds sleep calls
changes production behavior too broadly
```

Required task fields:

```text
forbidden changes
forbidden files
forbidden patterns
max diff size
allowed paths
```

Scoring:

```text
tests pass
forbidden changes absent
diff stays within scope
hidden tests pass
```


## 3.6 Minimal-diff repair

LLMs and coding agents often over-engineer. A newer or more agentic model may produce a polished solution but change too much.

Hardness pattern:

```text
The correct solution is small, but the agent is tempted to rewrite architecture.
```

Example:

```text
Fix a CSV import bug caused by quoted commas. Do not replace the importer, change the database schema, or introduce a new parsing library.
```

Common failure modes:

```text
large rewrite
new dependency
schema change
unrelated refactor
style-only churn
test rewrites
```

Scoring:

```text
functional tests pass
max files modified
max lines changed
no new dependency unless allowed
forbidden files unchanged
```

Minimal-diff repair is essential for AgentDelta because it helps detect when a newer model appears better by doing more work than necessary.


## 3.7 Cross-file contract consistency

LLMs often update one part of a contract while missing related clients, schemas, tests, docs, or compatibility layers.

Hardness pattern:

```text
A contract changes in one layer and must be propagated safely across the system.
```

Example:

```text
Rename API field `status` to `compliance_status` while preserving backward compatibility for existing clients.
```

Files likely involved:

```text
controller
serializer
OpenAPI schema
frontend client
request specs
documentation
compatibility adapter
```

Common failure modes:

```text
breaks old clients
updates API but not schema
updates schema but not tests
updates frontend but not backend
removes compatibility
changes unrelated response fields
```

Scoring:

```text
old clients pass
new clients pass
schema tests pass
hidden compatibility tests pass
no unrelated contract changes
```


## 3.8 State-machine correctness

LLMs frequently miss illegal transitions, lifecycle side effects, audit requirements, and edge cases in stateful systems.

Hardness pattern:

```text
The task introduces or modifies states, but correctness depends on legal transitions and side effects.
```

Example:

```text
Add a `suspended` state to the account lifecycle. Accounts may move from active to suspended, suspended to active, and suspended to closed, but never from closed to suspended.
```

Common failure modes:

```text
updates enum only
misses transition guard
misses audit log
misses UI or API behavior
allows illegal transition
breaks existing transitions
```

Scoring:

```text
valid transitions pass
invalid transitions fail
audit log emitted
existing states still work
hidden transition tests pass
```


## 3.9 Security-sensitive defensive fixes

Security tasks are hard because superficial fixes often pass visible tests but fail real adversarial cases.

Hardness pattern:

```text
The model must close a vulnerability without breaking legitimate behavior.
```

Allowed AgentDelta security tasks must be defensive, contained, and performed inside toy or controlled repositories.

Examples:

```text
Fix path traversal in file downloads.
Fix tenant isolation bug.
Prevent unsafe redirect.
Prevent secret leakage in logs.
Fix insecure file upload validation.
Fix mass-assignment vulnerability.
```

Common failure modes:

```text
blocks only the visible exploit
misses encoded bypass
breaks valid use cases
uses brittle string checks
weakens authorization
logs sensitive data during debugging
```

Scoring:

```text
known exploit blocked
hidden exploit variants blocked
valid behavior preserved
regression tests pass
no dangerous broad rewrite
```

Security tasks should include strict forbidden changes, because agents may “fix” the issue by disabling functionality.


## 3.10 Concurrency, idempotency, and race conditions

LLMs often reason sequentially. Concurrent behavior is hard because the failure may not appear in ordinary tests.

Hardness pattern:

```text
The code works in a single request but fails under simultaneous or repeated events.
```

Example:

```text
Fix duplicate invoice creation when two payment webhooks arrive concurrently.
```

Common failure modes:

```text
adds in-memory guard only
checks existence without locking
misses database uniqueness
breaks retry behavior
fails idempotency replay
handles one provider event but not another
```

Scoring:

```text
concurrency stress test passes
idempotency tests pass
no duplicate records
existing webhook behavior preserved
database constraint correct when appropriate
```

These tasks are especially valuable because generated code can look correct while remaining unsafe.


## 3.11 Test repair without test weakening

LLMs may pass benchmarks by editing tests instead of fixing production behavior.

Hardness pattern:

```text
The model must fix production code while preserving the failing test’s intent.
```

Example:

```text
The timezone-related test is failing. Fix the production code. Do not modify the failing test file.
```

Common failure modes:

```text
changes test expectation
freezes date incorrectly
hardcodes current date
skips test
changes fixture data instead of fixing logic
```

Scoring:

```text
failing tests pass
test file unchanged
hidden timezone cases pass
no hardcoded current date
no assertion weakening
```

This category directly tests benchmark-gaming behavior.


## 3.12 Performance optimization with behavior preservation

LLMs may optimize by changing semantics. A valid optimization must produce the same results faster or with fewer resources.

Hardness pattern:

```text
The model must improve performance without changing observable behavior.
```

Example:

```text
Optimize the dashboard query for large accounts without changing the returned data.
```

Common failure modes:

```text
changes result ordering
drops edge cases
filters too aggressively
adds caching with stale results
introduces N+1 elsewhere
optimizes visible case only
```

Scoring:

```text
golden output unchanged
query count below threshold
runtime below threshold
hidden large dataset passes
no stale-cache behavior
```

Performance tasks should use deterministic fixtures and clear thresholds.


## 3.13 Data migration and rollback safety

LLMs often write migrations that work only in simple cases and fail rollback, nulls, duplicates, or existing data.

Hardness pattern:

```text
The model must alter data shape while preserving existing records and rollback safety.
```

Example:

```text
Split `full_name` into `first_name` and `last_name` while preserving existing users and supporting rollback.
```

Common failure modes:

```text
destructive migration
no rollback
bad null handling
bad Unicode handling
bad single-name handling
data loss
schema mismatch
```

Scoring:

```text
migration succeeds
rollback succeeds
data integrity preserved
edge cases pass
schema consistent
```

Data migration tasks are strong because they test caution, not just code generation.


## 3.14 Dependency and framework migration

LLMs may hallucinate APIs, apply outdated migration patterns, or upgrade unrelated dependencies.

Hardness pattern:

```text
The model must adapt code to a new dependency or framework version using vendored documentation or controlled changelogs.
```

Example:

```text
Upgrade the validation library from v2 to v3 and fix breaking changes. Use only the migration notes included in docs/vendor/.
```

Common failure modes:

```text
hallucinates API
uses outdated syntax
upgrades unrelated packages
modifies lockfile incorrectly
breaks runtime behavior
relies on internet access
```

Scoring:

```text
build passes
tests pass
lockfile correct
only allowed dependencies changed
vendored docs followed
```

For reproducibility, external docs should be vendored into the repository or task context.


## 3.15 Specification inference from existing conventions

LLMs may invent a design when the correct approach is to follow existing codebase conventions.

Hardness pattern:

```text
The prompt is intentionally brief, but the repository contains analogous patterns that should guide the implementation.
```

Example:

```text
Add archive support for projects.
```

The repository may already contain archive behavior for:

```text
tasks
documents
users
reports
```

Common failure modes:

```text
invents new pattern
misses existing service structure
uses inconsistent naming
forgets audit log
forgets permissions
implements only UI or only backend
```

Scoring:

```text
matches existing conventions
hidden tests check consistency
no unnecessary abstraction
no duplicated architecture
```

This task category should be run in both Minimal-Spec Mode and Strong-Spec Mode to detect whether newer models are simply better at filling in missing requirements.


## 3.16 Self-repair after execution feedback

LLMs may fail to correctly interpret compiler errors, test failures, or stack traces. Some agents loop, patch randomly, or overfit to one error.

Hardness pattern:

```text
The first attempt is likely to fail, and the model must recover using execution feedback.
```

Example:

```text
Fix the implementation until the provided test passes. The first failure reveals a deeper mismatch between the interface and existing conventions.
```

Common failure modes:

```text
misreads error message
fixes the wrong file
introduces new failure
loops on same command
removes failing test
changes interface unnecessarily
```

Scoring:

```text
eventual tests pass
number of failed commands recorded
no test weakening
no repeated useless command loop
hidden tests pass
```

This category is especially useful for comparing agentic scaffolds.


## 3.17 Tool-use discipline

Coding agents may misuse tools: running irrelevant commands, reading too many files, editing before understanding, or failing to run tests.

Hardness pattern:

```text
The task requires targeted tool use, not brute-force exploration.
```

Example:

```text
Fix a localized validation bug in a large repository. The correct solution requires reading the validator, corresponding model, and tests. Excessive unrelated edits are penalized.
```

Common failure modes:

```text
reads many irrelevant files
edits before inspecting
does not run tests
runs wrong test command
repeats failed commands
overuses search without synthesis
```

Scoring:

```text
task correctness
tool calls
failed commands
time to first relevant file
time to first test
files read
files modified
```

This category supports the Agentic Amplification Assessment by measuring whether better results come from better reasoning or merely more tool use.


# 4. Hardness levels

AgentDelta tasks should be labeled by hardness level.

## H1: Local correctness

Single module or small file group. Hidden edge cases exist.

Example:

```text
Fix date parsing for leap years without changing public API.
```

## H2: Multi-file coordination

Requires coordinated changes across several files.

Example:

```text
Add API field and update serializer, schema, tests, and client.
```

## H3: Hidden invariant or security constraint

Requires preserving a non-obvious rule or defensive property.

Example:

```text
Add partial refund support while preventing over-refunds.
```

## H4: Long-context or repository-wide reasoning

Requires finding relevant information in a large codebase or documentation corpus.

Example:

```text
Use the authoritative compliance mapping buried in documentation to fix a report generator.
```

## H5: Systemic correctness under adversarial conditions

Requires correctness under concurrency, migration, security, performance, or state-machine stress.

Example:

```text
Prevent duplicate invoice creation under concurrent webhook delivery while preserving retry semantics.
```

Recommended v0.1 distribution:

```text
H1: 10%
H2: 25%
H3: 25%
H4: 20%
H5: 20%
```

AgentDelta should avoid a suite dominated by H1 tasks, because H1 tasks are less likely to distinguish frontier coding agents meaningfully.


# 5. Required task anatomy

Each hard task must include:

```text
task_id
title
category
hardness_level
known_llm_failure_mode
repository_fixture
base_commit
prompt_file
minimal_spec_prompt, if applicable
strong_spec_prompt, if applicable
workflow_prompt, if applicable
public_tests
hidden_tests
baseline_tests
acceptance_criteria
forbidden_changes
allowed_paths
forbidden_paths
max_files_modified, if applicable
max_lines_changed, if applicable
timeout
cost_budget
scoring_weights
failure_labels
```

Example task manifest:

```yaml
id: hard_task_023
title: Prevent duplicate invoices under concurrent webhooks
category: concurrency_idempotency
hardness_level: H5
known_llm_failure_mode: sequential_reasoning_under_concurrency

repo: rails_api
base_commit: abc123
language: ruby
framework: rails

prompts:
  minimal: prompt_minimal.md
  strong: prompt_strong.md
  workflow: prompt_workflow.md

execution:
  timeout_minutes: 30
  max_cost_usd: 5.00
  network: disabled

scope:
  allowed_paths:
    - app/
    - spec/
    - db/migrate/
  forbidden_paths:
    - config/credentials.yml.enc
    - spec/support/payment_gateway_fake.rb
  max_files_modified: 8
  max_lines_changed: 300

tests:
  baseline:
    - bundle exec rspec
  public:
    - bundle exec rspec spec/requests/webhooks_spec.rb
  hidden:
    - ./eval/hidden/concurrent_webhook_test.sh

acceptance_criteria:
  - Duplicate invoices are not created under concurrent webhook delivery.
  - Webhook replay remains idempotent.
  - Existing successful payment flow still works.
  - Existing failed payment flow still works.
  - Hidden concurrency tests pass.
  - No test is weakened or skipped.

forbidden_changes:
  - Do not disable webhook retries.
  - Do not skip or weaken tests.
  - Do not remove existing payment states.
  - Do not store idempotency only in memory.

failure_labels:
  - hidden_tests_failed
  - regression_introduced
  - test_weakened
  - concurrency_not_fixed
  - overbroad_edit
```


# 6. Prompt variants

Hard tasks should support multiple prompt variants when feasible.

## 6.1 Minimal-Spec Prompt

Represents weak-user/default-user behavior.

Example:

```text
Fix duplicate invoice creation when payment webhooks are sent more than once.
```

Purpose:

```text
Measures default inference, planning, and initiative.
```

## 6.2 Strong-Spec Prompt

Represents a disciplined user who provides requirements.

Example:

```text
Fix duplicate invoice creation when two payment webhooks arrive concurrently.

Requirements:
1. Preserve valid webhook retry behavior.
2. Ensure invoice creation is idempotent.
3. Do not use in-memory locks as the only protection.
4. Add or update tests for replay and concurrency.
5. Do not weaken existing tests.
6. Keep the patch minimal.
```

Purpose:

```text
Measures whether the model still has an advantage when requirements are explicit.
```

## 6.3 Workflow Prompt

Forces the same process across models.

Example:

```text
Before editing:
1. Inspect the webhook controller, invoice model, and existing webhook tests.
2. Identify the current idempotency mechanism.
3. Write a short implementation plan.
4. Make the smallest correct change.
5. Run the relevant tests.
6. Review the diff against the acceptance criteria.
```

Purpose:

```text
Determines whether a newer model’s advantage comes from implicit workflow rather than intrinsic capability.
```


# 7. Hidden tests

Hidden tests are central to AgentDelta hard tasks.

A visible test often checks the happy path. A hidden test should check:

```text
edge cases
negative cases
adversarial inputs
regression behavior
forbidden shortcuts
compatibility
concurrency
security bypasses
large datasets
migration rollback
```

Hidden tests should not be arbitrary. They must be aligned with the task’s acceptance criteria.

Bad hidden test:

```text
Checks an undocumented behavior unrelated to the task.
```

Good hidden test:

```text
Checks an edge case implied by the acceptance criteria but not explicitly present in public tests.
```

Hidden tests should be cryptographically committed before official benchmark execution.

Recommended policy:

```text
1. Freeze hidden tests before model runs.
2. Store hash in reproducibility manifest.
3. Do not expose hidden tests to the agent.
4. Publish hidden tests after the official report when public reproducibility is desired.
```


# 8. Forbidden shortcut detection

Each task must identify likely shortcut behaviors.

Examples:

```text
removing a failing test
weakening an assertion
skipping validation
hardcoding expected output
adding sleep to hide race condition
disabling security checks
bypassing authorization
changing fixtures instead of code
rewriting schema unnecessarily
removing public API compatibility
```

The scoring system must include explicit detectors where possible.

Detector examples:

```text
grep for skipped tests
check git diff for forbidden files
compare assertion counts
check timeout values
run hidden adversarial tests
inspect dependency changes
check API schema compatibility
```

A model that passes public tests by shortcutting should fail the task.


# 9. Relationship to Agentic Amplification Assessment

Hard tasks must support analysis of whether a model is genuinely better or merely doing more work.

For each task, AgentDelta should collect:

```text
input tokens
output tokens
total tokens
wall-clock time
API calls
tool calls
shell commands
failed commands
test runs
file reads
file edits
retry count
diff size
cost
```

For hard tasks, this distinction matters.

Example:

```text
Model B solves 10% more tasks but uses 5x tokens, 4x time, and 6x tool calls.
```

This may indicate agentic amplification rather than intrinsic model superiority.

Each hard task should therefore be compatible with:

```text
Default Mode
Equal-Budget Mode
Strong-Spec Mode
Matched-Workflow Mode
Cost-Matched Mode
Time-Matched Mode
Older-Model Plus Scaffold Mode
```

A hard task is especially valuable when it can reveal that:

```text
a newer model wins by default
but an older model closes the gap when given a stronger spec or workflow
```


# 10. Recommended v0.1 hard-task suite

For AgentDelta v0.1, use 50 tasks.

Recommended distribution:

| Category                                            | Count |
| --------------------------------------------------- | ----: |
| Multi-file bug localization                         |     8 |
| Hidden invariant preservation                       |     6 |
| Security-sensitive defensive fixes                  |     6 |
| State-machine correctness                           |     5 |
| Cross-file contract consistency                     |     5 |
| Long-context retrieval                              |     5 |
| Concurrency and idempotency                         |     4 |
| Minimal-diff repair                                 |     4 |
| Performance optimization with behavior preservation |     4 |
| Test repair without test weakening                  |     3 |

Alternative 30-task minimum suite:

| Category                           | Count |
| ---------------------------------- | ----: |
| Multi-file bug localization        |     5 |
| Hidden invariant preservation      |     4 |
| Security-sensitive defensive fixes |     4 |
| State-machine correctness          |     3 |
| Cross-file contract consistency    |     3 |
| Long-context retrieval             |     3 |
| Concurrency and idempotency        |     3 |
| Minimal-diff repair                |     2 |
| Performance optimization           |     2 |
| Test repair without weakening      |     1 |

The 50-task suite is preferred for the first serious public report.


# 11. Task construction guidelines

## 11.1 Prefer realistic repositories

Use repositories with:

```text
routing or entry points
domain models
tests
configuration
documentation
multiple layers
style conventions
existing analogous patterns
```

Avoid toy scripts unless the purpose is to isolate a specific failure mode.

## 11.2 Include distractors

Hard tasks should include plausible but wrong paths.

Example:

```text
The bug appears in the controller, but the correct fix is in the policy.
```

Distractors should be realistic, not artificial tricks.

## 11.3 Require correctness, not cosmetics

Avoid tasks where success depends on taste.

Bad:

```text
Make the dashboard look more modern.
```

Better:

```text
Fix the dashboard query so it returns the same rows in under 200ms on the large fixture dataset.
```

## 11.4 Penalize unnecessary broadness

A solution that rewrites large parts of the system should not automatically be rewarded.

Use:

```text
max files modified
max lines changed
forbidden paths
review flags
scope-control score
```

## 11.5 Require regression safety

Every task should run enough existing tests to detect collateral damage.

At minimum:

```text
targeted public tests
hidden tests
relevant regression tests
```

For high-risk tasks:

```text
full suite
contract tests
security tests
migration rollback tests
```


# 12. Failure labels

Hard tasks should assign one or more failure labels.

Required failure-label vocabulary:

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
authorization_regression
concurrency_not_fixed
migration_not_reversible
performance_regression
state_transition_invalid
hallucinated_api
did_not_run_tests
looping_or_thrashing
ignored_source_of_truth
missed_existing_convention
```

Each failure should be assigned based on artifacts, not speculation.


# 13. Scoring profile for hard tasks

Default hard-task scoring:

```text
60% verified task success
15% hidden-test score
10% regression avoidance
5% scope-control score
5% cost-efficiency score
5% time-efficiency score
```

For security, concurrency, migration, and state-machine tasks, hidden tests may receive more weight.

Recommended adjusted scoring for high-risk tasks:

```text
50% verified task success
25% hidden-test score
10% regression avoidance
5% scope-control score
5% cost-efficiency score
5% time-efficiency score
```

A task cannot receive full credit if:

```text
hidden tests fail
security is weakened
authorization is weakened
tests are skipped
forbidden files are modified
data migration is destructive
```


# 14. Examples of hard task templates

## 14.1 Authorization bug

```text
Title:
Fix tenant isolation in report downloads.

Prompt:
Users from one tenant can sometimes download reports belonging to another tenant when using a shared report URL. Fix the issue without changing the public URL format or disabling shared links.

Hidden tests:
- cross-tenant access blocked
- same-tenant shared access allowed
- expired links blocked
- admin access still works

Known LLM failure modes:
- adds controller-only check
- breaks shared links entirely
- weakens admin behavior
- changes URL format
```

## 14.2 State-machine change

```text
Title:
Add suspended account state.

Prompt:
Add a suspended state to the account lifecycle. Suspended accounts cannot create new projects but can view existing invoices. Preserve all existing closed-account behavior.

Hidden tests:
- active to suspended allowed
- suspended to active allowed
- closed to suspended blocked
- suspended cannot create project
- suspended can view invoices

Known LLM failure modes:
- enum-only change
- misses permission side effect
- allows illegal transition
- breaks closed accounts
```

## 14.3 Long-context source-of-truth task

```text
Title:
Fix retention label mapping.

Prompt:
Compliance reports are being generated with the wrong retention label. Use the official retention mapping from the repository documentation and fix the generator.

Hidden tests:
- correct label for each report type
- legacy mapping not used
- unknown report type handled
- generated report metadata unchanged otherwise

Known LLM failure modes:
- invents mapping
- uses outdated mapping
- edits generated fixture
- hardcodes visible case only
```

## 14.4 Concurrency task

```text
Title:
Prevent duplicate invoices under concurrent webhooks.

Prompt:
When two payment webhooks arrive at the same time, duplicate invoices may be created. Fix the issue while preserving webhook replay behavior.

Hidden tests:
- concurrent webhook delivery
- repeated webhook replay
- failed payment replay
- valid duplicate events with different IDs

Known LLM failure modes:
- in-memory lock only
- existence check without transaction
- disables retry
- breaks failed payment handling
```

## 14.5 Minimal-diff parser task

```text
Title:
Fix quoted comma parsing in CSV import.

Prompt:
CSV imports fail when a quoted field contains a comma. Fix the bug without replacing the importer or introducing a new dependency.

Hidden tests:
- quoted comma
- escaped quote
- empty quoted field
- newline in quoted field, if supported
- existing simple CSV still works

Known LLM failure modes:
- rewrites parser
- adds dependency
- handles only visible example
- changes import schema
```


# 15. Hardness audit checklist

Before adding a task to AgentDelta, answer:

```text
1. What known LLM weakness does this task test?
2. Can success be measured objectively?
3. What is the tempting wrong solution?
4. What hidden tests detect the wrong solution?
5. What existing behavior must remain unchanged?
6. What files or changes are forbidden?
7. What would over-engineering look like?
8. Can the task run without external network access?
9. Can the task be reset to a clean state?
10. Can the task be run across all target agents?
11. Can tokens, time, cost, tool calls, and diffs be captured?
12. Does the task support Minimal-Spec and Strong-Spec variants?
13. Does the task reveal whether a newer model is intrinsically better or merely doing more work?
```

A task should not be accepted into the official suite unless these questions have clear answers.


# 16. Acceptance criteria for HARD-TASKS-SPEC compliance

A benchmark suite complies with this spec when:

```text
1. At least 80% of tasks require multi-file or repository-level reasoning.
2. Every task has objective public and hidden scoring.
3. Every task declares the known LLM failure mode it targets.
4. Every task has forbidden shortcut checks.
5. Every task preserves regression behavior.
6. Every task captures resource usage.
7. The suite includes at least five hard-task categories.
8. The suite includes at least one long-context task.
9. The suite includes at least one hidden-invariant task.
10. The suite includes at least one security or authorization task.
11. The suite includes at least one concurrency, migration, or state-machine task.
12. The suite supports Agentic Amplification Assessment.
```

Preferred compliance for v0.1:

```text
50 tasks
5 repeated runs per model
public tests
hidden tests
regression tests
resource metrics
failure labels
Minimal-Spec and Strong-Spec variants for at least 50% of tasks
```


# 17. Guiding principle

AgentDelta hard tasks should make it difficult for a model to look impressive while being wrong.

The benchmark should not ask:

```text
Can the model generate a plausible answer?
```

It should ask:

```text
Can the model make the correct change, in the correct place, with the correct scope, while preserving hidden invariants, passing hidden tests, avoiding shortcuts, and doing so at an acceptable cost in time, tokens, and money?
```

A model that produces a beautiful but incorrect patch should fail.

A model that passes visible tests by weakening the system should fail.

A model that solves the task only by consuming excessive resources should be reported accordingly.

The purpose of hard tasks is not to embarrass models. The purpose is to measure whether they can behave like careful software engineers under realistic constraints.