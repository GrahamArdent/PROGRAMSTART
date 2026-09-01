# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-31
- **Project / repository:** `GrahamArdent/execution-node-control`
- **PROGRAMSTART lesson ID:** `PSL-008`
- **Checkpoint / acceptance surface:** EN-03 Stage 4 required-tooling physical acceptance while EN-02 continued as a sibling Mode-C lane
- **Classification:** systemic / existing-lesson strengthening

## What happened

Execution Node legitimately had two current Mode-C lanes under one strategic spine: EN-03 provisioning/tooling work and EN-02 RTL8821CE evidence work. Repository-side independence was real, but both lanes shared one consequential mutable runtime resource: the single privileged installed `execution-node-control` release under `/opt/execution-node-control`.

General lane-conflict guidance and exact-SHA guards prevented unsafe acceptance, but they did not stop separate sessions from repeatedly installing different reviewed releases over the same shared resource. This caused several physical-install retries, stale exact-head candidates, duplicate Stage-4 reconciliation PRs, and one Class-2 `PASS` whose own machine evidence proved it had executed on the wrong installed SHA.

The problem was resolved only after the project explicitly declared one PR/SHA the sole physical-install owner and instructed sibling lanes to remain repository/read-only until that ownership was released.

## Evidence

- `execution-node-control` PR #32 physically accepted and merged the EN-02 H2C trace release while Stage 4 was preparing repository-side.
- Stage-4 PR #33 became stale because installing it after PR #32 would have removed the accepted H2C control capability.
- PR #35 (`abf804aa43903b035cbdfc036233f4d9a1fc0e4c`) and PR #37 (`beac5110cf6b4c72d1a20fc3ed9b75798877396d`) independently reconciled the same Stage-4 work onto post-H2C `main`; #37 was later closed as duplicate.
- The operator restored exact PR #35, but a later Class-2 request `req-stage4-v21-acceptance-abf804-20260831T1950Z` returned outer `PASS` while its own `installed_commit` and checkpoint source were `75ee8246b45ce06d0e864074983c67a83cbb65df`, proving a competing install had replaced the physical release. That PASS was explicitly invalidated for PR #35.
- A durable PR comment then declared PR #35 exact head the sole physical-install owner; EN-02 PR #36 was explicitly kept repository-only.
- After exact PR #35 was restored under that lock, fresh inventory passed, retry Class-2 returned `installed_commit` and checkpoint source exactly `abf804aa43903b035cbdfc036233f4d9a1fc0e4c`, first apply was checkpoint-only, second apply was `changed=0`, fresh status was healthy, and PR #35 merged as `23ed854343fe35453d1eb0667bd71a9b6d9a8eb9`.
- Exact-SHA/pre-mutation guards repeatedly stopped unsafe overwrites; the observed gap was coordination across invocations, not absence of local safety checks.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** PSL-008 required one selected packet per invocation, explicit lane conflicts/convergence, and prohibited inferring concurrent overlapping mutation. Operator-gate and exact-SHA evidence rules also required machine evidence to override descriptive request intent.
- **What helped:** those rules prevented false merge/acceptance. Exact installed-source evidence caught stale releases and invalidated the wrong-SHA Class-2 PASS instead of accepting it.
- **What created friction or uncertainty:** `LANE_CONFLICTS` identified overlap but did not create a cross-invocation exclusion rule for one shared consequential resource. Separate valid sessions could each believe their own packet was selected and cross the same physical install boundary.
- **Was existing methodology sufficient?** partially. It detected/recovered from collisions, but did not prevent the repeated resource race.

## Learning decision

- **Existing lesson match:** `PSL-008` — coordinated Mode-C lanes under one spine.
- **Maturity before:** validated
- **Maturity after:** implemented (strengthened rule awaiting a new real retest)
- **Why the evidence changes or does not change maturity:** this directly matches PSL-008's named retest condition of sibling lanes sharing a real mutable/conflict surface. Repeated collisions show that conflict/convergence notation alone is insufficient across independent invocations when one consequential resource can be mutated by both lanes.
- **PROGRAMSTART change required now:** bounded extension to `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`: when current lanes can mutate the same consequential external/runtime/provider/device/deployment resource, record `SHARED_MUTATION_RESOURCE`, exactly one `MUTATION_OWNER`, and `RELEASE_OR_TRANSFER_CONDITION`; sibling lanes may continue only with work proven unable to mutate that resource. Re-check owner/resource state immediately before consequential mutation. Do not add a scheduler, global lock service, portfolio registry, or new project lifecycle.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** another Mode-C project where sibling lanes share one consequential mutable provider/runtime/device/deployment resource across separate sessions or agents.
- **What evidence would be sufficient:** the second lane recognizes an active mutation owner before crossing the shared boundary, remains safely read-only/repository-only (or performs an explicit ownership transfer), and the previously observed stale-runtime/provenance collision does not recur. Counterevidence would be material ceremony or deadlock caused by the ownership fields when no real shared mutation exists.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The change extends an existing lesson and canonical Work Packet mechanism rather than manufacturing a new framework.
