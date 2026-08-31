# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own Execution Node scope, execution order, release state, host configuration, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-31
- **Project / repository:** `GrahamArdent/execution-node-control`
- **PROGRAMSTART lesson ID:** `PSL-007` primary; `PSL-009` strengthened observation; `PSL-015` confirmation
- **Checkpoint / acceptance surface:** EN-01 bounded GitHub-mediated control-plane installation, returned runtime evidence, correction/reverification, and resumed Mode-C closure; followed by EN-03 repository-vs-physical provisioning acceptance
- **Classification:** validation of `PSL-007`; strengthening evidence for `PSL-009`; confirmation of `PSL-015`

## What happened

Execution Node reached the exact real-world retest condition that remained open for `PSL-007`.

The active EN-01 work packet crossed a real operator/manual boundary: reviewed root-owned control-plane code had to be installed on the Ubuntu host through a pinned physical/admin action before repository work could become live runtime truth. The operator action did not itself count as system acceptance. After installation, ChatGPT-created typed GitHub requests were consumed by the node, bounded non-secret results were published back to GitHub, returned evidence was reconciled into the existing project authority, contradictory runtime evidence caused narrow corrections, and execution resumed from the existing closure point rather than restarting orientation or inventing another plan.

The same project also produced a second independent case for `PSL-009`. Repository CI, reviewed code state, installed runtime state, and physical-host behavior repeatedly established different claims. In particular, EN-03 PR #14 reached repository acceptance far enough to attempt physical execution, but the real Ubuntu 26.04 host exposed an Ansible 2.20.1 / sudo-rs privilege-escalation incompatibility. The correction preserved the system sudo provider and used the bounded local `sudo.ws` compatibility path; only a later exact-SHA physical run proved the provisioning checkpoint and idempotency behavior.

Post-implementation Challenge Gates also remained productive across this work. EN-01 adversarial review found a zero-argument trust-boundary regression after initially green checks, while live runtime acceptance exposed evidence over-retention and an incomplete network PASS predicate. Later EN-03 Challenge Gates continued to inspect exact completed behavior rather than equating green CI with safe closure.

## Evidence

- **Execution Node PR #1 — EN-01 accepted:** real ChatGPT → GitHub request → node execution → GitHub result → ChatGPT round trips completed; failed-unit disposition, service-independence, crash/restart recovery, privilege boundary, malformed/replay rejection, and final closure were reconciled without broad reorientation.
- **Execution Node PR #1 Learning Gate:** explicitly concluded that existing PROGRAMSTART methodology materially helped and that no new methodology feature was earned by EN-01 closure.
- **Execution Node PRs #5, #9, #11:** returned runtime evidence repeatedly updated the same current project authority and closure point rather than creating competing plans.
- **Execution Node PR #6 / #8:** post-implementation adversarial review found a zero-argument dispatcher boundary regression despite an initially green run; the defect was corrected and regression-tested.
- **Execution Node PR #13:** exact reviewed SHA physically executed twice; both applies were idempotent and Challenge Gate was CLEAR for the bounded Corepack/pnpm slice.
- **Execution Node PR #14:** first physical attempt failed before the new state surface because of the Ubuntu 26.04 sudo-rs / Ansible prompt incompatibility; a bounded compatibility correction was made without changing the system-wide sudo provider; later exact reviewed SHA physically passed with first apply `changed=1` for the expected checkpoint and second apply `changed=0 / unreachable=0 / failed=0`.
- **Current Execution Node work packet after PR #14:** accepted evidence is retained narrowly, whole-node acceptance remains explicitly open, and the next slice is derived from current authority rather than restarting the project.
- **Checks not claimed here:** this observation does not independently rerun Execution Node CI, host commands, or physical acceptance. It relies on the repository's durable PR/runtime evidence and does not claim newer PR #17 physical acceptance, which remains open at the time of this observation.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** preserved one project spine and one current packet; narrowed manual/operator gates to exact actions and return evidence; separated repository acceptance from installed/runtime/physical acceptance; reused still-valid evidence; resumed at the declared current slice; triggered post-implementation Challenge Gates on material trust/runtime boundaries.
- **What helped:** the operator-gate contract prevented installation from being confused with acceptance; `RESUME_AT`/current-packet discipline prevented repeated broad orientation; evidence invalidation allowed runtime contradictions to narrow corrections rather than invalidate unrelated accepted work; Challenge Gate review caught defects that planned tests did not.
- **What created friction or uncertainty:** Execution Node repeatedly needed to state which evidence plane a PASS belonged to because repository CI, installed runtime, and physical host evidence were materially different. This strengthens `PSL-009`, but the existing Work Packet/operator-gate primitives were sufficient to preserve truth without a dedicated new verification taxonomy.
- **Was existing methodology sufficient?** yes.

## Learning decision

- **Existing lesson match:** `PSL-007` directly matches the operator action → returned evidence → resume cycle. `PSL-009` matches the need to keep CI/repository/runtime/physical evidence claims distinct. `PSL-015` matches the productive post-implementation adversarial reviews.
- **Maturity before:** `PSL-007` validated at protocol level with end-to-end resumption still open; `PSL-009` observe; `PSL-015` validated.
- **Maturity after:** `PSL-007` fully validated with the end-to-end caveat removed; `PSL-009` remains observe but has materially stronger cross-project evidence; `PSL-015` remains validated with additional confirmation.
- **Why the evidence changes or does not change maturity:** EN-01 satisfies `PSL-007`'s named retest condition exactly. Execution Node is also the second project showing materially different verification planes, but existing current primitives handled the distinction successfully, so a new formal source/type subsystem is not yet earned. Repeated Challenge Gate success confirms `PSL-015` without requiring another methodology change.
- **PROGRAMSTART change required now:** none. Update only the acceptance learning ledger and this observation.

## Retest

- **PSL-007 next condition:** future operator/manual gates should remain available as counterevidence, especially where returned evidence contradicts prior assumptions or where a session is tempted to reorient broadly instead of resuming at the declared point.
- **PSL-009 next condition:** look for another real project where current Work Packet/operator-gate semantics fail to keep repository/runtime/provider/device/human claims distinct or create repeated material overhead. Only then consider a bounded verification-source/type policy.
- **PSL-015 next condition:** continue risk-triggered use; record counterevidence if activation becomes over-broad, ceremonial, or fails to protect a material invariant.
- **What evidence would be sufficient:** durable project evidence showing either clean resumption/source separation under current primitives or a concrete recurring failure mode that current primitives cannot represent without ambiguity.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks recorded in the Execution Node repository.
- [x] No unnecessary new PROGRAMSTART feature or lesson ID was manufactured.
