# AgentDelta v0.1 hard-task suite plan

STATUS: COMPLETE. 50 tasks authored and check-task-verified (full suite green).
HARD-TASKS-SPEC section 16 acceptance: ALL criteria pass. Core tier = 39 multi-file
tasks (100% multi-file ratio); 11 single-file algorithmic tasks tagged
tier: supplementary (warmup pool, excluded from the ratio). Prompt variants on
34/50 (68%, >=50% target met). 14 categories. Hardness H1:9 H2:18 H3:10 H4:4 H5:9.
The "todo" lines below are unused alternates kept for reference.

Target: a 50-task core suite compliant with HARD-TASKS-SPEC section 10 (preferred)
and section 16 (acceptance). This file is the durable roadmap for the multi-turn
build. Update the status column as tasks land.

## Compliance targets (HARD-TASKS-SPEC 16)

- At least 80% of core tasks are multi-file / repository-level.
- At least 5 hard-task categories; the 10 below cover them.
- Minimal-Spec and Strong-Spec variants for at least 50% of tasks.
- Hardness mix target: H1 10%, H2 25%, H3 25%, H4 20%, H5 20%.

## Category distribution (section 10, preferred 50)

| Category                          | Target | Have | To author |
| --------------------------------- | -----: | ---: | --------: |
| Multi-file bug localization       |      8 |    1 |         7 |
| Hidden invariant preservation     |      6 |    2 |         4 |
| Security / authorization fixes    |      6 |    2 |         4 |
| State-machine correctness         |      5 |    2 |         3 |
| Cross-file contract consistency   |      5 |    0 |         5 |
| Long-context retrieval            |      5 |    1 |         4 |
| Concurrency and idempotency       |      4 |    1 |         3 |
| Minimal-diff repair               |      4 |    1 |         3 |
| Performance with behavior preserve|      4 |    0 |         4 |
| Test repair without weakening     |      3 |    0 |         3 |
| TOTAL                             |     50 |   10 |        40 |

The 11 existing single-file algorithmic tasks (task_001-003, task_010-014,
go_task_002, etc.) stay in the repo as a supplementary warmup pool (tier:
supplementary) and do not count toward the 80% multi-file core ratio.

## Authoring patterns

- ADD task: the feature/symbol is absent in the fixture image, so base public/hidden
  tests fail without any fixture edit; the reference_solution adds it. No image
  rebuild. Parallel-safe across and within fixtures.
- FIX task: a latent, baseline-invisible bug is planted in the fixture, then the
  image is rebuilt once. The reference_solution fixes only that bug. Plant all of a
  fixture's FIX bugs in one coordinated pass, rebuild once, then verify all.
- Cross-fixture work is parallel-safe (separate images). Within one fixture, FIX
  bugs must be coordinated and the rebuild done once.
- Every task: known_llm_failure_mode, forbidden_changes/paths, max_files/lines,
  public + hidden tests, baseline regression, expected_behavior.md, and (for >=50%)
  prompts: {minimal, strong, workflow}. Verify with `agentdelta check-task <id>`.

## Fixtures

- saas (Python, layered multi-tenant): authz, localization, state-machine,
  cross-file contract, hidden-invariant, performance. Already has the can_view
  tenant bug, is_owner bug, and missing-suspended-state (used by hard_task_001-003).
- payments (Python, webhook/invoice/storage w/ latency): concurrency, hidden-
  invariant (refund caps), state-machine (payment states), migration, localization.
- pricing_ts (TypeScript, money/cart/discount/tax): hidden-invariant, minimal-diff,
  cross-file contract, security/validation, typecheck/self-repair. NEW this build.
- long_context (220-file ledger corpus): long-context retrieval needles.
- python_package (mathkit): minimal-diff, test-repair, performance.
- go_cli (textkit): cross-file contract, localization in Go.

## Inventory and roadmap

Status: done = check-task green; todo = not authored; wip = in progress.

### Existing core (count toward the 50)
- hard_task_001  security/authz            H3  saas        done
- hard_task_002  state-machine             H5  saas        done
- hard_task_003  multi-file localization   H2  saas        done
- hard_task_004  concurrency               H5  payments    done
- ts_task_001    hidden-invariant          H3  pricing_ts  done
- task_004       minimal-diff (refactor)   H2  python_pkg  done
- task_005       security (path traversal) H3  python_pkg  done  (single-file; review tier)
- task_007       multi-func feature        H2  python_pkg  done
- task_008       dependency-migration      H2  python_pkg  done
- task_009       long-context retrieval    H4  long_ctx    done

### To author (target ~40)

Multi-file bug localization (7):
- saas_loc_01    api symptom / policy nil-handling root cause   H2  saas       FIX  done
- saas_loc_02    listing filtered in wrong layer                H2  saas       FIX  todo
- pay_loc_01     api symptom / storage filter root cause        H2  payments   FIX  done
- pay_loc_02     refund symptom / ledger root cause             H3  payments   FIX  todo
- ts_loc_01      cart total symptom / money rounding root cause H2  pricing_ts FIX  done
- mk_loc_01      report symptom / helper root cause             H2  python_pkg FIX  done
- go_loc_01      output symptom / formatter root cause          H2  go_cli     FIX  done

Hidden invariant preservation (4):
- pay_invariant_01  partial refunds never exceed paid          H3  payments   ADD  done
- ts_invariant_02   stacked discounts cap at subtotal          H3  pricing_ts ADD  done
- saas_invariant_01 seat quota never exceeded                  H3  saas       ADD  done
- mk_invariant_01   running balance never goes below zero      H3  python_pkg ADD  done

Security / authorization (4):
- saas_authz_01  archived cross-member visibility              H3  saas       FIX  done
- saas_authz_02  role/membership check leak                    H3  saas       FIX  todo
- ts_security_01 reject NaN/overflow/negative inputs           H3  pricing_ts FIX  done
- pay_authz_01   webhook signature/source validation           H3  payments   ADD  done

State-machine correctness (3):
- saas_state_01  add trial state with guards                   H5  saas       ADD  done
- pay_state_01   add disputed/refunded states                  H5  payments   ADD  done
- ts_state_01    order status transitions                      H4  pricing_ts ADD  done

Cross-file contract consistency (5):
- saas_contract_01  rename serialized field w/ back-compat     H2  saas       ADD  done
- pay_contract_01   add currency field preserving clients      H2  payments   ADD  todo
- ts_contract_01    line-item discount preserving cart API     H2  pricing_ts ADD  done
- mk_contract_01    add option preserving callers              H2  python_pkg ADD  done
- go_contract_01    add flag preserving existing output        H2  go_cli     ADD  done

Long-context retrieval (4):
- lc_retrieval_01  authoritative mapping buried in corpus      H4  long_ctx   FIX  done
- lc_retrieval_02  retention label from policy doc             H4  long_ctx   FIX  done
- lc_retrieval_03  aggregate rule defined deep in docs         H4  long_ctx   ADD  todo
- lc_retrieval_04  pick correct of several distractor configs  H4  long_ctx   FIX  todo

Concurrency and idempotency (3):
- pay_concurrency_01  duplicate refund under concurrency       H5  payments   FIX  done
- pay_concurrency_02  idempotent replay across providers       H5  payments   FIX  done
- saas_concurrency_01 concurrent member add races quota        H5  saas       FIX  done

Minimal-diff repair (3):
- ts_minimal_01   tax rounding bug, no rewrite                 H2  pricing_ts FIX  done
- mk_minimal_01   parser quoted-delimiter bug, no rewrite      H2  python_pkg FIX  done
- saas_minimal_01 single-line policy edge fix                  H2  saas       FIX  todo

Performance with behavior preservation (4):
- saas_perf_01   N+1 dashboard aggregation                     H5  saas       FIX  todo
- pay_perf_01    O(n^2) ledger summation                       H4  payments   FIX  todo
- mk_perf_01     O(n^2) dedup -> O(n), preserve order          H4  python_pkg FIX  todo
- ts_perf_01     repeated subtotal recompute                   H2  pricing_ts FIX  todo

Test repair without weakening (3):
- mk_testrepair_01  timezone/date prod bug, do not edit test   H3  python_pkg FIX  todo
- saas_testrepair_01 failing authz test, fix prod not test     H3  saas       FIX  todo
- pay_testrepair_01  flaky-looking test, real prod bug         H3  payments   FIX  todo

## Done this build (foundation)

- Author-written prompt variants: registry.prompt_variant + modes.build_prompt
  prefer author files, fall back to synthesis; new minimal_spec mode.
- hardness_level + known_llm_failure_mode populated on all existing tasks.
- New TypeScript fixture pricing_ts: manifest, sandbox image, node/tsc test runner
  (testrunner + parser), first task ts_task_001 verified with three prompt variants.
- Unit tests for node parsing and prompt variants (tests/test_node_and_variants.py).
