# SPEC-ADDENDUM.md

**Project:** AgentDelta
**Addendum:** Agentic Amplification Assessment
**Status:** Draft v0.1
**Applies to:** AgentDelta SPEC.md
**Purpose:** Determine whether observed model improvements come from intrinsic model capability, increased agentic work, or workflow-equivalent scaffolding.


# 1. Motivation

AgentDelta’s primary SPEC defines how to compare frontier coding agents by measuring task success, hidden-test performance, regressions, cost, latency, token consumption, tool usage, and patch quality.

This addendum introduces a second-level assessment:

> When a newer model produces better results than an older model, is the improvement caused by better intrinsic model capability, or is it primarily the result of more agentic work performed by default?

This distinction is critical.

A public demonstration may show:

```text
Model A: creates a basic tic-tac-toe game.
Model B: creates a polished tic-tac-toe game with better UI, tests, accessibility, and cleaner structure.
Conclusion claimed: Model B is dramatically superior.
```

But the demonstration may omit that Model B:

```text
used 10x more input/output tokens
spent 30x more wall-clock time
performed multiple internal reasoning passes
ran more tool calls
generated and revised its own plan
used self-critique or judge loops
created tests and iterated until passing
used a stronger default scaffold
cost 20x more
```

In such a case, the result may be better, but the reason may not be that the underlying model is inherently more capable. It may be that the model or agent product performs more work by default.

AgentDelta must therefore distinguish:

```text
better model
better scaffold
more compute
more retries
more self-review
better prompting
better workflow
```

This addendum formalizes how to detect, measure, and report that distinction.


# 2. Core question

The Agentic Amplification Assessment answers the following question:

> If Model B outperforms Model A, could Model A achieve similar quality if given comparable workflow structure, prompt quality, review loops, tool access, time, or token budget?

This converts the comparison from:

```text
Which model produced the best output?
```

to:

```text
Which model produced the best output under comparable work, cost, time, and scaffolding conditions?
```

and:

```text
Which model provides the best quality per unit of agentic work?
```


# 3. Definitions

## 3.1 Intrinsic model capability

Intrinsic model capability refers to quality improvements attributable to the model itself under comparable conditions.

Examples:

```text
better reasoning with same prompt
better code generation with same budget
better repository understanding with same tool access
better correctness with same number of attempts
better hidden-test performance with similar cost and time
```

## 3.2 Agentic amplification

Agentic amplification is improvement caused by additional work performed around or by the model.

Examples:

```text
more planning
more decomposition
more file exploration
more retries
more test runs
more self-review
more LLM-as-judge passes
more prompt rewriting
more hidden scaffolding
longer reasoning
larger context consumption
more tool calls
longer execution time
```

Agentic amplification is not inherently bad. It may be highly valuable. However, it must be measured separately from intrinsic model capability.

## 3.3 Workflow-equivalent improvement

A workflow-equivalent improvement occurs when a weaker or older model can match the newer model’s output if given:

```text
a better task specification
a structured plan
a review checklist
explicit test requirements
a retry loop
an external judge
a stronger agent scaffold
more context
more time
more tokens
```

This matters because older models may be cheaper. If an older model plus a disciplined workflow achieves the same result at lower cost, users should know.

## 3.4 Default-user performance

Default-user performance measures what a normal user gets when using the model or agent with minimal prompt engineering and default settings.

This is still important because many users do not create detailed specifications or structured workflows.

## 3.5 Strong-user performance

Strong-user performance measures what happens when the user provides:

```text
clear acceptance criteria
explicit constraints
test requirements
review criteria
implementation boundaries
workflow instructions
```

This measures whether the model still has an advantage when the user supplies the discipline that a newer agent may otherwise provide automatically.


# 4. New evaluation category

AgentDelta adds a formal evaluation category:

```text
Agentic Amplification Assessment
```

This category does not replace the main benchmark. It supplements it.

The main benchmark answers:

```text
Which model-agent system performs best?
```

The addendum answers:

```text
Why does it perform best?
```

and:

```text
Is the improvement still meaningful after normalizing for cost, time, tokens, retries, and workflow?
```


# 5. Evaluation modes

AgentDelta must include multiple modes to isolate agentic amplification.

## 5.1 Default Mode

Default Mode evaluates each model or agent exactly as a normal user would use it.

Example:

```text
Claude Code + Opus 4.8, default settings
Claude Code + Opus 4.7, default settings
Claude Code + Opus 4.6, default settings
Claude Code + Sonnet 4.6, default settings
```

Purpose:

```text
Measure real default user experience.
```

Default Mode is allowed to favor a newer model if that model performs more work by default. However, the report must disclose the cost, time, token, and tool-use differences.

## 5.2 Equal-Budget Mode

Equal-Budget Mode imposes comparable resource budgets across models.

Budgets may include:

```text
maximum input tokens
maximum output tokens
maximum wall-clock time
maximum API calls
maximum agent turns
maximum tool calls
maximum shell commands
maximum test runs
maximum cost
```

Purpose:

```text
Measure quality under comparable resource constraints.
```

If Model B wins in Default Mode but loses or ties in Equal-Budget Mode, the report must flag the original improvement as potentially agentic-amplified.

## 5.3 Matched-Workflow Mode

Matched-Workflow Mode forces each model to follow the same explicit workflow.

Example workflow:

```text
1. Inspect relevant files.
2. Produce an implementation plan.
3. Make the smallest required change.
4. Run tests.
5. If tests fail, debug once.
6. Run tests again.
7. Review the diff against acceptance criteria.
8. Provide final summary.
```

Purpose:

```text
Determine whether a newer model’s advantage came from applying a workflow that could also be given to older models.
```

If an older model closes the quality gap under Matched-Workflow Mode, the report must disclose that the new model’s default advantage is at least partially workflow-equivalent.

## 5.4 Strong-Spec Mode

Strong-Spec Mode improves the task prompt for all models by adding:

```text
explicit acceptance criteria
forbidden changes
test expectations
edge cases
review checklist
definition of done
output requirements
```

Purpose:

```text
Test whether the newer model’s advantage persists when the user supplies a high-quality specification.
```

This directly addresses the scenario where Model B appears better because it implicitly improves the task or fills in missing requirements.

## 5.5 Older-Model Plus Scaffold Mode

Older-Model Plus Scaffold Mode gives the older model additional structured support.

Examples:

```text
Opus 4.6 + explicit planner
Opus 4.6 + test-first instruction
Opus 4.6 + review checklist
Opus 4.6 + one retry loop
Opus 4.6 + external judge
Opus 4.6 + same max time as Opus 4.8
Opus 4.6 + same token budget as Opus 4.8
```

Purpose:

```text
Determine whether the older, cheaper model can match the newer model when given similar agentic structure.
```

This mode is critical for practical migration decisions.

## 5.6 Cost-Matched Mode

Cost-Matched Mode gives each model the same dollar budget.

Example:

```text
Each model receives up to $2.00 per task.
```

Purpose:

```text
Measure which model produces the best verified result per dollar.
```

This may favor cheaper models that can make more attempts within the same budget.

## 5.7 Time-Matched Mode

Time-Matched Mode gives each model the same wall-clock budget.

Example:

```text
Each model receives up to 15 minutes per task.
```

Purpose:

```text
Measure which model produces the best verified result within the same practical time limit.
```

This prevents a slower model from being declared superior without disclosing that it consumed far more time.


# 6. Required new metrics

AgentDelta must add the following metrics for Agentic Amplification Assessment.

## 6.1 Agentic Work Index

The Agentic Work Index estimates how much work the system performed to produce the final answer.

Suggested formula:

```text
Agentic Work Index =
  weighted_sum(
    normalized_input_tokens,
    normalized_output_tokens,
    normalized_wall_clock_time,
    normalized_api_calls,
    normalized_tool_calls,
    normalized_shell_commands,
    normalized_test_runs,
    normalized_file_reads,
    normalized_file_edits,
    normalized_retry_count,
    normalized_review_passes
  )
```

The exact weights must be declared before the benchmark run.

Default weights:

```text
input tokens:       15%
output tokens:      15%
wall-clock time:    15%
API calls:          10%
tool calls:         10%
shell commands:      5%
test runs:          10%
file reads:          5%
file edits:          5%
retry count:         5%
review passes:       5%
```

The Agentic Work Index does not measure quality. It measures effort.

## 6.2 Quality per Agentic Work Unit

This metric measures efficiency.

```text
Quality per Agentic Work Unit =
  Objective Score / Agentic Work Index
```

A model may have the highest raw quality but lower quality per unit of work.

## 6.3 Quality per Dollar

```text
Quality per Dollar =
  Objective Score / estimated_cost_usd
```

This is especially important when comparing older cheaper models with newer expensive models.

## 6.4 Quality per Minute

```text
Quality per Minute =
  Objective Score / wall_clock_minutes
```

This measures practical productivity.

## 6.5 Token Amplification Ratio

For a newer model B compared against baseline model A:

```text
Token Amplification Ratio =
  total_tokens_B / total_tokens_A
```

Where:

```text
total_tokens = input_tokens + output_tokens + cache_write_tokens + cache_read_tokens + reasoning_tokens, where available
```

## 6.6 Cost Amplification Ratio

```text
Cost Amplification Ratio =
  cost_B / cost_A
```

## 6.7 Time Amplification Ratio

```text
Time Amplification Ratio =
  wall_clock_time_B / wall_clock_time_A
```

## 6.8 Tool Amplification Ratio

```text
Tool Amplification Ratio =
  tool_calls_B / tool_calls_A
```

## 6.9 Retry Amplification Ratio

```text
Retry Amplification Ratio =
  retries_B / retries_A
```

## 6.10 Test Amplification Ratio

```text
Test Amplification Ratio =
  test_runs_B / test_runs_A
```

## 6.11 Quality Delta per Extra Dollar

```text
Quality Delta per Extra Dollar =
  (Objective Score_B - Objective Score_A) /
  (Cost_B - Cost_A)
```

This answers:

```text
How much additional quality did the user buy with the additional cost?
```

## 6.12 Quality Delta per Extra Minute

```text
Quality Delta per Extra Minute =
  (Objective Score_B - Objective Score_A) /
  (Time_B - Time_A)
```

This answers:

```text
How much additional quality did the user receive for the additional time?
```


# 7. Red flags for agentic amplification

AgentDelta must flag a result as potentially agentic-amplified when Model B beats Model A but also shows one or more of the following:

```text
Token Amplification Ratio >= 2.0
Cost Amplification Ratio >= 2.0
Time Amplification Ratio >= 2.0
Tool Amplification Ratio >= 2.0
Retry Amplification Ratio >= 2.0
Test Amplification Ratio >= 2.0
API-call ratio >= 2.0
Agentic Work Index ratio >= 2.0
```

A stronger warning applies when:

```text
quality improvement is modest
but token/cost/time amplification is large
```

Example:

```text
Objective Score improves by 4 percentage points,
but cost increases by 300%.
```

This should not be described simply as “Model B is better.” It should be described as:

```text
Model B produced a modest quality improvement at substantially higher agentic cost.
```


# 8. Classification of improvement type

Every meaningful Model B over Model A improvement must be classified into one of the following categories.

## 8.1 Intrinsic Capability Gain

Use this classification when Model B outperforms Model A under comparable conditions.

Criteria:

```text
higher Objective Score
similar token budget
similar time budget
similar tool-call count
similar workflow
similar retry count
statistically meaningful improvement
```

Allowed claim:

```text
Model B appears to provide an intrinsic capability gain on this task category.
```

## 8.2 Agentic Amplification Gain

Use this classification when Model B wins primarily in Default Mode and consumes substantially more resources.

Criteria:

```text
higher Objective Score
much higher tokens, cost, time, or tool calls
advantage shrinks in Equal-Budget Mode
advantage shrinks in Matched-Workflow Mode
advantage shrinks when older model receives structured support
```

Allowed claim:

```text
Model B produced better outputs in default usage, but the improvement appears partially or primarily attributable to increased agentic work.
```

## 8.3 Workflow-Equivalent Gain

Use this classification when Model A can match Model B after receiving better instructions or scaffolding.

Criteria:

```text
Model B wins in Default Mode
Model A ties or nearly ties in Strong-Spec Mode
Model A ties or nearly ties in Matched-Workflow Mode
Model A remains cheaper or faster
```

Allowed claim:

```text
Model B’s default advantage appears workflow-equivalent: similar quality can be obtained from Model A with a stronger specification or process.
```

## 8.4 Cost-Inefficient Gain

Use this classification when Model B wins but the gain is not economically compelling.

Criteria:

```text
quality improvement is small
cost increase is large
cost per successful task worsens
Quality per Dollar decreases
```

Allowed claim:

```text
Model B improves raw quality but is not cost-efficient for this workload.
```

## 8.5 Time-Inefficient Gain

Use this classification when Model B wins but takes materially longer.

Criteria:

```text
quality improvement is small or moderate
time increase is large
Quality per Minute decreases
```

Allowed claim:

```text
Model B improves raw quality but is not time-efficient for this workload.
```

## 8.6 No Material Gain

Use this classification when differences are too small or statistically unsupported.

Criteria:

```text
small score delta
overlapping confidence intervals
no clear paired advantage
```

Allowed claim:

```text
The benchmark does not support a material difference between these models on this task category.
```


# 9. New report section

Every AgentDelta report must include a section titled:

```text
Agentic Amplification Analysis
```

This section must answer:

```text
1. Did the winning model use materially more tokens?
2. Did it cost materially more?
3. Did it take materially longer?
4. Did it use materially more tool calls?
5. Did it perform more retries or test loops?
6. Did it benefit from a stronger default workflow?
7. Did the older model close the gap under Strong-Spec Mode?
8. Did the older model close the gap under Matched-Workflow Mode?
9. Is the improvement intrinsic, amplified, workflow-equivalent, cost-inefficient, time-inefficient, or not material?
```


# 10. Required comparison tables

## 10.1 Raw quality table

| Model   | Objective Score | Success Rate | Hidden Tests | Regression Rate | Rank |
| ------- | --------------: | -----------: | -----------: | --------------: | ---: |
| Model B |            91.2 |          78% |          74% |              8% |    1 |
| Model A |            86.4 |          72% |          69% |             10% |    2 |

## 10.2 Resource amplification table

| Model   |    Tokens |  Cost |  Time | Tool Calls | Test Runs | Agentic Work Index |
| ------- | --------: | ----: | ----: | ---------: | --------: | -----------------: |
| Model B | 1,200,000 | $3.40 | 18.0m |         72 |         8 |                100 |
| Model A |   240,000 | $0.42 |  5.5m |         24 |         3 |                 31 |

## 10.3 Efficiency table

| Model   | Objective Score | Quality/$ | Quality/Minute | Quality/Work Unit |
| ------- | --------------: | --------: | -------------: | ----------------: |
| Model B |            91.2 |      26.8 |            5.1 |              0.91 |
| Model A |            86.4 |     205.7 |           15.7 |              2.79 |

## 10.4 Equal-budget table

| Model   |     Budget | Objective Score | Success Rate | Hidden Tests | Result             |
| ------- | ---------: | --------------: | -----------: | -----------: | ------------------ |
| Model B | $1.00/task |            82.0 |          68% |          64% | Lower than default |
| Model A | $1.00/task |            84.5 |          70% |          67% | Competitive        |

## 10.5 Workflow-equivalence table

| Condition             | Model A | Model B | Interpretation    |
| --------------------- | ------: | ------: | ----------------- |
| Default Mode          |     72% |     78% | B wins            |
| Strong-Spec Mode      |     77% |     79% | Gap narrows       |
| Matched-Workflow Mode |     79% |     80% | Near tie          |
| Cost-Matched Mode     |     81% |     76% | A wins per dollar |


# 11. Updated scoring interpretation

AgentDelta must distinguish between:

```text
Raw Best Model
Efficient Best Model
Best Default User Model
Best Strong User Model
Best Budget-Constrained Model
Best Long-Horizon Model
Best Small-Task Model
```

A single model may not win all categories.

Example:

```text
Model B is the Raw Best Model.
Model A is the Efficient Best Model.
Model B is the Best Default User Model.
Model A is competitive or superior for Strong Users under matched workflow and budget.
```

This is an important outcome, not a contradiction.


# 12. Claim rules

## 12.1 Claims that require Agentic Amplification Analysis

The following claims require amplification analysis before publication:

```text
Model B is better than Model A.
Model B is dramatically superior.
Model B makes Model A obsolete.
Model B changes the game.
Model B is the new default choice.
Model B is worth upgrading to.
Model B gives better coding results.
```

AgentDelta should not allow these claims unless the report specifies:

```text
better by which metric
under which mode
at what cost
at what latency
with how many tokens
with how many tool calls
with what statistical confidence
whether older models close the gap under stronger workflow
```

## 12.2 Preferred claim language

Use:

```text
Model B produced higher raw task success in Default Mode, but at 3.4x cost and 2.7x wall-clock time.
```

Use:

```text
Model B’s advantage persisted under Equal-Budget Mode, suggesting an intrinsic capability gain.
```

Use:

```text
Model B’s advantage largely disappeared under Matched-Workflow Mode, suggesting that its default benefit is partially workflow-equivalent.
```

Use:

```text
Model A remains the better cost-performance choice for users willing to provide stronger specifications and explicit review loops.
```

Avoid:

```text
Model B killed Model A.
```

Avoid:

```text
There is no reason to use Model A anymore.
```

Avoid:

```text
Model B is simply smarter.
```


# 13. Practical implication for users

AgentDelta reports must include a practical recommendation section.

The recommendation should distinguish between user types.

## 13.1 Weak-spec users

A weak-spec user provides minimal prompts and little workflow discipline.

For such users, a newer model or stronger agentic scaffold may be worth the additional cost.

Example recommendation:

```text
If you provide short prompts and expect the agent to infer requirements, Model B may be worth using despite higher cost because it performs more planning, verification, and self-correction by default.
```

## 13.2 Strong-spec users

A strong-spec user provides clear requirements, tests, acceptance criteria, and implementation constraints.

For such users, older or cheaper models may remain competitive.

Example recommendation:

```text
If you already provide strong specifications, explicit test requirements, and review loops, Model A may achieve comparable results at lower cost.
```

## 13.3 Budget-constrained users

Budget-constrained users care about cost per verified successful task.

Example recommendation:

```text
For teams optimizing cost per accepted patch, Model A remains preferable unless Model B’s higher success rate offsets its higher cost.
```

## 13.4 Time-constrained users

Time-constrained users care about wall-clock completion.

Example recommendation:

```text
For fast iteration loops, Model A may be preferable if Model B’s quality gain comes with materially longer completion time.
```

## 13.5 High-risk tasks

For high-risk tasks, raw quality may matter more than cost.

Example recommendation:

```text
For security-sensitive, compliance-sensitive, or high-impact code changes, Model B may be justified if its regression rate is lower and the improvement persists under controlled workflow comparisons.
```


# 14. Benchmark design additions

AgentDelta tasks should include paired variants:

## 14.1 Minimal-spec prompt

A short prompt similar to what a typical user may write.

Example:

```text
Create a tic-tac-toe game with a nice UI.
```

## 14.2 Strong-spec prompt

A detailed prompt with acceptance criteria.

Example:

```text
Create a tic-tac-toe game with:
- deterministic game-state management
- win/draw detection
- reset button
- keyboard accessibility
- responsive layout
- unit tests for game logic
- no external dependencies
- clear file structure
```

Purpose:

```text
Measure whether the new model’s advantage comes from filling in missing specification details.
```

## 14.3 Workflow prompt

A prompt that requires explicit process.

Example:

```text
Before coding, inspect the project structure.
Then write a short plan.
Then implement the smallest correct change.
Then run tests.
Then review your diff against the acceptance criteria.
Then fix issues once if needed.
```

Purpose:

```text
Measure whether older models improve when given the workflow newer models may perform implicitly.
```

## 14.4 Same-output target

For some tasks, define the desired output quality explicitly.

Purpose:

```text
Test whether older models can reach the same target when the expected standard is clearly defined.
```


# 15. Additional run matrix

For each major model comparison, AgentDelta should run the following matrix where feasible.

| Mode             | Model A                         | Model B            | Purpose                      |
| ---------------- | ------------------------------- | ------------------ | ---------------------------- |
| Default          | Default                         | Default            | Real user default behavior   |
| Equal Budget     | Same budget                     | Same budget        | Resource-normalized quality  |
| Strong Spec      | Same strong prompt              | Same strong prompt | Prompt-quality normalization |
| Matched Workflow | Same workflow                   | Same workflow      | Process normalization        |
| Cost Matched     | Same dollar cap                 | Same dollar cap    | Cost-normalized quality      |
| Time Matched     | Same time cap                   | Same time cap      | Latency-normalized quality   |
| A + Scaffold     | Older model with added workflow | Newer default      | Workflow-equivalence test    |

Not every public report must run every mode, but any report claiming upgrade value should run at least:

```text
Default Mode
Equal-Budget Mode
Strong-Spec Mode
Matched-Workflow Mode
Cost-Matched Mode
```


# 16. Example interpretation

Suppose the benchmark produces this result:

```text
Default Mode:
  Model A success: 70%
  Model B success: 82%
  Model B cost: 4x higher
  Model B time: 3x higher
  Model B tokens: 5x higher

Matched-Workflow Mode:
  Model A success: 80%
  Model B success: 83%

Cost-Matched Mode:
  Model A success: 79%
  Model B success: 72%
```

Correct interpretation:

```text
Model B provides a better default experience, especially for weak-spec users.
However, much of the improvement appears to come from additional agentic work.
When Model A is given a stronger workflow, the performance gap narrows substantially.
When cost is fixed, Model A performs better.
Therefore, Model B is not categorically superior. It is superior for default, low-discipline usage, while Model A remains highly competitive for users who provide better specifications and workflow structure.
```

Incorrect interpretation:

```text
Model B is obviously better.
```


# 17. Integration with original SPEC.md

This addendum does not replace the original AgentDelta SPEC.

The original SPEC remains authoritative for:

```text
task design
execution protocol
objective scoring
hidden tests
reproducibility
artifact capture
statistical reporting
agent adapters
sandboxing
publication standards
```

This addendum adds an additional interpretive layer:

```text
agentic amplification detection
resource-normalized comparison
workflow-equivalence testing
cost/time/token-adjusted reporting
claim discipline for model-upgrade conclusions
```

If there is a conflict between the original SPEC and this addendum:

```text
The original SPEC controls execution mechanics.
This addendum controls interpretation of upgrade claims.
```


# 18. Acceptance criteria for this addendum

AgentDelta satisfies this addendum when:

```text
1. Reports include Agentic Amplification Analysis.
2. Reports include token, cost, time, and tool amplification ratios.
3. Reports include Quality per Dollar and Quality per Minute.
4. Reports include at least one resource-normalized comparison mode.
5. Reports classify each major model improvement by type.
6. Reports avoid declaring a newer model categorically superior without resource-normalized evidence.
7. Reports identify when older cheaper models remain competitive under stronger workflow conditions.
8. Reports distinguish default-user value from intrinsic model superiority.
```

Preferred implementation:

```text
Default Mode
Equal-Budget Mode
Strong-Spec Mode
Matched-Workflow Mode
Cost-Matched Mode
Older-Model Plus Scaffold Mode
```


# 19. Guiding principle

AgentDelta must not merely ask:

```text
Which model produced the prettiest output?
```

It must ask:

```text
What did the model spend to produce that output?
```

and:

```text
Could an older, cheaper model have achieved the same result with a better specification or workflow?
```

A model upgrade is meaningful only when the improvement remains valuable after accounting for:

```text
tokens
cost
time
tool use
retries
workflow
scaffolding
statistical uncertainty
```

The final goal is not to punish newer models for doing more work. The goal is to make the tradeoff visible.

If a newer model is better because it does more work by default, that is still valuable for many users.

But it is not the same claim as:

```text
The underlying model is intrinsically superior.
```

AgentDelta exists to make that distinction measurable.
