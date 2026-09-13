# PROGRAMSTART Verification Economics

Purpose: keep verification rigorous while preventing autonomous iteration from multiplying paid or quota-limited CI work that has not been earned by evidence invalidation or an acceptance boundary.

Status: **PROGRAMSTART operational protocol / subordinate to project authority and the Challenge Gate**.

This protocol extends `docs/PROGRAMSTART_COST_GOVERNANCE.md`, Work Packet evidence reuse/invalidation, and `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`. It does **not** create a CI platform, testing repository, controller, queue, scheduler, evidence authority, or permission to skip required verification.

## 1. Core Rule

> **Validate cheaply while iterating; spend independent hosted verification only when evidence was invalidated or a meaningful acceptance boundary is reached.**

Cost reduction must come from removing redundant verification, cancelling superseded work, and selecting the smallest still-sufficient proof. It must never come from omitting a consequential test whose evidence was actually invalidated.

## 2. Why This Exists

Autonomous development can amplify CI unintentionally:

`Challenge -> small correction -> commit -> hosted CI -> another correction -> commit -> hosted CI -> exact-head checkpoint -> retry`

When one commit fans into several workflows, matrices, infrastructure validators, and scheduled suites, a sound Challenge loop can become an expensive execution loop even though the code change is small.

PROGRAMSTART therefore treats verification execution itself as a cost surface when hosted runner use, quota, elapsed time, provider spend, or contention becomes material.

## 3. Verification Cost Envelope

When verification cost is decision-relevant, derive only the fields needed for the current packet:

```text
VERIFICATION_COST_GATE: active
VERIFICATION_SURFACE:
ITERATION_TIER: [local | existing_worker | existing_runtime | hosted]
HOSTED_ACCEPTANCE_TRIGGER:
REUSABLE_EVIDENCE:
INVALIDATION_TRIGGERS:
EXPECTED_HOSTED_JOBS:
EXPENSIVE_STEPS:
SCHEDULED_CADENCE:
SUPERSESSION_POLICY:
RETRY_RULE:
POST_MERGE_RULE:
COST_OR_QUOTA_EVIDENCE:
```

Do not turn this into portfolio bookkeeping. Persist it only when it materially improves execution, resumption, or cost control.

## 4. Verification Tiers

Use the cheapest tier that can produce the required confidence at the current boundary.

### Tier 0 — local/static

Examples:
- syntax/compile checks;
- deterministic unit tests;
- lint/format/schema validation;
- focused Challenge reproducer.

Use during implementation whenever the current worker already has a suitable isolated environment.

### Tier 1 — existing worker/runtime

Examples:
- Compute Spine worker validation;
- isolated Execution Node test capability;
- existing project/runtime harness;
- provider-neutral integration tests already available in the ecosystem.

Reuse existing infrastructure rather than creating a new CI service merely to avoid hosted runner cost.

### Tier 2 — targeted independent hosted acceptance

Use GitHub-hosted or equivalent independent runners when independence from the implementation machine materially improves acceptance confidence. Run only the test families whose evidence is invalidated, plus any repository-wide baseline the owner explicitly requires.

### Tier 3 — full convergence/release verification

Run the complete required release/consequence suite when the boundary itself requires it. Verification economics never narrows a genuinely required whole-system gate.

## 5. Draft / Ready Acceptance Pattern

When GitHub pull-request lifecycle is an appropriate owner surface, the preferred high-churn pattern is:

- **draft PR** = iteration state; hosted acceptance jobs skip by default;
- **ready for review** = explicit exact-head hosted acceptance transition;
- **later commit to a ready PR** = prior exact-head acceptance is invalidated and the applicable hosted checks rerun;
- **superseded candidate** = in-progress hosted work should be cancelled when safe.

For GitHub Actions, workflows using this pattern must explicitly include the `ready_for_review` pull-request event. Do not assume the default `pull_request` event set will trigger on draft-to-ready transition.

A project may use a different machine-readable acceptance transition if its existing workflow already has one. GCRM title markers such as `[ci:quick]`, `[ci:db]`, `[ci:e2e]`, or `[ci:full]` are an example of an already-valid checkpoint model.

## 6. Evidence Reuse and Invalidation

Every specialized or expensive verification family should be able to answer:

1. What exact invariant does this prove?
2. What files/config/dependencies/runtime facts can invalidate it?
3. What evidence remains valid when unrelated code changes?
4. What smallest check re-establishes confidence after invalidation?

Rules:

- do not replay historical acceptance merely because another PR commit exists;
- do not use `run everything` as a substitute for impact reasoning;
- path filters are acceptable only when transitive invalidators are included;
- dependency manifests, workflow definitions, shared config, generated contracts, and pinned external baselines may be transitive invalidators even when the primary implementation path is unchanged;
- changing the verification workflow itself invalidates that workflow's acceptance logic and should normally exercise the changed path once before merge;
- age alone does not invalidate deterministic evidence unless the underlying dependency/environment is time-sensitive.

## 7. Concurrency and Supersession

Hosted CI should not keep testing an artifact that the owner has already superseded.

Preferred rule:

- concurrency keys identify the **PR / branch / logical acceptance stream**, not the commit SHA;
- `cancel-in-progress` may be used where a newer candidate fully supersedes the older candidate;
- do not cancel work whose partial completion has independent consequence or evidence value unless the owner has explicitly defined that behavior.

A concurrency key containing the candidate SHA usually prevents cancellation between successive revisions and therefore does not solve superseded-run amplification.

## 8. Matrices

A compatibility matrix is a verification surface, not a default ritual.

Keep matrix dimensions when they protect a current supported contract. Scope or reduce them when:

- only one runtime is production-supported;
- a compatibility dimension is historical spike evidence rather than current product support;
- the dimension can be invalidation-scoped to dependency/runtime-contract changes;
- a lower-cost recurring compatibility cadence preserves sufficient confidence.

Do not reduce a matrix merely because it is expensive if the project actually promises every tested runtime.

## 9. Expensive Infrastructure Validators

Infrastructure checks such as OpenTofu/Terraform initialization, Ansible collection installation, container builds, browser installation, local database startup, or full production-mode E2E should be invalidation-scoped when possible.

Always include transitive inputs. Example: if `requirements-ci.txt` pins `ansible-core`, that dependency file invalidates Ansible syntax validation even when `infra/ansible/**` is unchanged.

A workflow-file change should normally force the affected expensive paths once so the new classifier cannot mark itself safe without evidence.

## 10. Scheduled Verification

A schedule must earn its cadence.

Classify the scheduled job first:

- **regression verification** — proves repository/runtime behavior against current code/dependencies;
- **monitoring/currentness** — detects live provider/environment drift that can occur without code changes.

Regression suites should not run daily merely from habit if event-driven acceptance plus a lower recurring cadence provides the same decision value.

For a scheduled suite, record:

- what can change between executions without a code event;
- how quickly that change matters;
- recent failure yield;
- typical runner/runtime cost;
- manual/event-driven escape hatch;
- cadence invalidation condition.

Reducing a schedule must preserve manual or event-driven execution when an invalidating release/change needs proof sooner.

## 11. Post-Merge Verification

An exact-head PR acceptance remains reusable after merge when the merge operation does not create a materially different artifact or integration state.

Owners may retain a small main-branch smoke to detect:

- direct-main mutations;
- merge-commit integration differences;
- repository rules that require a main observation;
- packaging/build behavior genuinely created by merge.

Do not automatically replay every specialized PR acceptance family on main if the exact accepted source and its relevant dependencies are unchanged.

## 12. Retry Discipline

A failed hosted run is evidence, not an automatic retry order.

Before retry:

- classify code/test failure vs provider/runner/account failure;
- do not create a no-op commit merely to obtain another runner;
- prefer rerunning only the failed job/run when the exact candidate is unchanged;
- if a code correction changes the candidate, the old acceptance is invalid and the corrected candidate must run the applicable checks;
- repeated runner/account failures should become an external capability/cost gate, not a reason to bypass acceptance.

## 13. Self-Hosted Runner Boundary

Self-hosted GitHub runners may reduce hosted-minute consumption, but they are not the default answer.

Before introducing one, apply Effective Autonomy, Cost Governance, and trust-boundary review.

Do **not** place an unrestricted general-purpose GitHub runner on a privileged Execution Node merely to save money. A future self-hosted runner must be isolated, least-privileged, secret-minimized, and justified against its patching, persistence, supply-chain, credential, and operator-cost burden.

Existing Compute/Execution worker capabilities should be preferred for iteration when they already meet the requirement without turning them into a generic GitHub executor.

## 14. Challenge Gate Integration

Part B — Assumption/Evidence Validity:
- identify reusable verification evidence and its invalidation triggers.

Part E — Blast Radius/Verification Scope:
- select the smallest checks that restore invalidated confidence;
- explicitly reject both `run everything` and unjustified narrow testing.

Part G — Dependency Health:
- include dependency/version/provider changes that invalidate a specialized validation family.

Part H — Alignment:
- ensure workflow/path filters still cover the architecture, contract, auth, schema, runtime, and supported-version promises they claim to protect.

A post-implementation Challenge should include a realistic failure sequence for CI-policy changes. Example:

> A draft candidate is marked ready, but hosted acceptance never starts because the workflow does not subscribe to `ready_for_review`.

The CI policy is not accepted until that failure sequence is mechanically disproven.

## 15. Acceptance Evidence

For a CI-economics change, useful evidence can include:

- draft event created with job/workflow conclusion `skipped` and no runner-backed execution;
- ready transition launches the expected exact-head acceptance;
- an unrelated change runs only the generic baseline and not specialized historical workflows;
- a deliberate invalidating change does trigger its specialized workflow;
- changed workflow logic exercises its own classifier before merge;
- main smoke succeeds after merge if the owner retains one;
- no required release/consequence gate was removed;
- measured hosted-job or runner-minute amplification is materially lower.

## 16. PROGRAMSTART #107 Pilot Evidence

The protocol was promoted after real owner pilots rather than from theory alone:

- **Controller:** normal PR fanout was approximately eight hosted jobs. Draft migration runs skipped; ready-state migration executed all intentionally invalidated workflow families; a post-merge unrelated docs probe created only `controller-ci`, proving AC-02, AC-04, PROGRAMSTART-contract, AC-06, and contextual-runtime evidence was reused. The first implementation also exposed and corrected a missing `ready_for_review` trigger before merge.
- **Compute Spine:** draft CI skipped; ready-state acceptance remained green; OpenTofu, Ansible, and Compose checks became invalidation-scoped while unit/cross-layer tests stayed baseline. Challenge caught `requirements-ci.txt` as a transitive Ansible invalidator before merge.
- **Mission Control:** draft CI skipped; ready acceptance preserved install/test/typecheck/build. Challenge rejected an unsupported npm-cache optimization because the repository has no lockfile.
- **GCRM:** the existing marker-triggered checkpoint model was preserved. Seven consecutive scheduled medium production-mode E2Es over one week produced no failure/cancellation, while recent runs consumed roughly 19–20 minutes each; the regression cadence was reduced from daily to weekly with manual dispatch retained, and the cadence PR reused recent E2E evidence rather than rerunning it.

These examples are evidence for the rule, not universal repository templates. Each owner must derive its own invalidation surface.

## 17. Success Test

Verification economics is working when:

- ordinary autonomous iteration does not automatically create several paid hosted jobs per small correction;
- independent hosted acceptance still occurs before the owner requires merge/release acceptance;
- specialized proof executes when its inputs change and remains reusable when they do not;
- superseded candidates stop consuming runner capacity;
- scheduled tests run at a cadence justified by what can change and how quickly it matters;
- provider/account CI failures are not mistaken for product failures or bypass permission;
- the ecosystem can explain **why this verification is running now**, **what invalidated the prior evidence**, and **why this tier is sufficient**.
