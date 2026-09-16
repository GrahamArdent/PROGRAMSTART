# PROGRAMSTART Learning Observation — PTT-02 Authority-First Proceed Retest

Status: **subordinate / non-canonical evidence**.

This record does not own Home Automation product scope, execution order, release state, Networking mutation, or PROGRAMSTART priority. It supplements rather than replaces `2026-09-16-ptt02-home-automation-safe-parallel-successor-derivation.md`, including that record's preserved partial-failure evidence.

## Observation identity

- **Date:** 2026-09-16
- **Project / repository:** Home Automation / `GrahamArdent/home-automation-control`
- **PROGRAMSTART lesson ID:** none — this retests existing authority/currentness, Work Packet, Effective Autonomy, Challenge, and Learning Gate semantics
- **Checkpoint / acceptance surface:** `PTT-02-HOME-AUTOMATION-SAFE-PARALLEL` standalone `Proceed` continuation after orientation
- **Classification:** confirmation

## What happened

The operator supplied standalone `Proceed` after a read-only PTT-02 orientation. Before any new mutation, the continuation refreshed only evidence capable of invalidating the prior execution decision.

That refresh materially changed the expected continuation: Home Automation WP-17 had already been terminalized by PR #52, and Execution Node #172 had separately been re-admitted for repository implementation while retaining external-owner/live-release sequencing. The continuation therefore did **not** repeat WP-17 terminalization and did **not** take Execution Node work from the Home Automation lane.

Fresh Home Automation authority instead supported one independent repository-only successor: `WP-18 — Canonical Capability Activation Gate / Default-Deny Exposure Contract`. WP-18 made seven execution-evidence gates machine-readable and kept execution, canonical ingress exposure, and agent authority fail-closed. Product PR #53 and terminalization PR #54 both merged after hosted exact-head CI/currentness checks. Home Automation issue #46 received the durable return. Execution Node #172 remained open and unmodified by this lane.

## Evidence

- Home Automation authority recovered before first new mutation:
  - WP-17 already terminal on `main` at `6b9301191c05e6088c0a8791f73884eb7bcb2119`;
  - `CURRENT_WORK_PACKET.md` and strategic spine both reflected that terminal state;
  - Execution Node #172 was OPEN and remained the fixed HA registry-reader owner;
  - Home Automation issue #46 still owned household/product acceptance;
  - active Networking mutation remained excluded from this lane.
- First new repository mutation occurred only after that recovery: branch `wp18/capability-activation-gate` in the Home Automation owner.
- WP-18 product PR #53:
  - exact reviewed head `3ff4f253305f1a293bfea62d2746a97ce21d8cc0`;
  - hosted `preflight-contract` run `35100931934` SUCCESS;
  - merge `be739fd7a423fa02e8976323a54a92864f8444cd`.
- WP-18 terminalization PR #54:
  - exact head `ba43b4f683bc6fc7cc26573194fd18fbacccf694`;
  - hosted `preflight-contract` run `35101147887` SUCCESS;
  - merge/current Home Automation `main` `5a51da93dc8d800971612ebe4427f2740d28c944`.
- Verification:
  - focused capability tests 20/20 PASS;
  - full Home Automation suite 154/154 PASS;
  - generated capability snapshot exact;
  - Python compilation PASS;
  - `git diff --check` PASS;
  - post-implementation Challenge found and corrected a forged-gate/non-boolean promotion weakness before publication.
- Durable product return: Home Automation issue #46 comment `5698143798`.
- Checks not performed / unavailable:
  - no fresh HA Area/Device/Entity registry read was claimed because #172 had not returned it;
  - no physical device outcome test was performed or inferred;
  - no Home Assistant runtime/config/provider mutation was performed;
  - no Networking/Transport mutation was performed.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** required current-authority/currentness recovery before successor execution; allowed changed durable evidence to replace the prior conversational continuation; preserved cross-owner mutation boundaries; then continued autonomously through implementation, Challenge, hosted CI, merge, durable terminalization, and Learning Gate.
- **What helped:** the authority hierarchy, Work Packet derivation, accepted-recommendation semantics, shared-mutation ownership, evidence reuse, Challenge Gate, and Learning Gate together prevented duplicate WP-17 work and prevented Home Automation from consuming #172 merely because its repository implementation had become available.
- **What created friction or uncertainty:** no new methodology friction was exposed in this retest. The main decision pressure was distinguishing useful independent Home Automation work from work that belonged to #172; existing owner/write-set semantics were sufficient.
- **Was existing methodology sufficient?** yes.

## Learning decision

- **Existing lesson match:** yes at the methodology-behavior level; the earlier PTT-02 observation already concluded authority-first sequencing was required and asked for a retest where no mutation occurs before currentness resolution.
- **Maturity before:** none — no new lesson was created by the earlier sequencing defect because current PROGRAMSTART already required the correct behavior.
- **Maturity after:** no change.
- **Why the evidence changes or does not change maturity:** this is materially stronger confirming evidence for the existing rule and directly satisfies the earlier PTT-02 retest condition, but it does not expose a missing methodology concept or justify a new lesson ID.
- **PROGRAMSTART change required now:** none.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** another real terminal/no-successor continuation where current durable authority changes materially between orientation and operator `Proceed`, especially with a tempting but foreign shared-mutation owner active.
- **What evidence would be sufficient:** mutation tools remain unused until currentness/ownership resolution; changed authority can cancel or redirect the expected successor; autonomous safe execution then proceeds without repeated generic approval; stronger consequence gates remain intact; terminal state is durable without transcript dependence.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The earlier PTT-02 partial-failure evidence remains preserved and is not rewritten as success.
- [x] No unnecessary PROGRAMSTART change or new lesson was manufactured.
