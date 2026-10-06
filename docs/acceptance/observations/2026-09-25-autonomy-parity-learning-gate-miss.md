# PROGRAMSTART Learning Observation — Autonomy-Parity Learning-Gate Miss

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-25
- **Project / repository:** autonomy-parity first live integration
- **PROGRAMSTART lesson ID:** `PSL-013`
- **Checkpoint / acceptance surface:** operator correction plus cross-owner acceptance during `ecosystem-contracts` / Execution Node convergence
- **Classification:** counterevidence

## What happened

The current PROGRAMSTART orchestration contract says the Learning Gate should run at meaningful checkpoints, including material operator corrections, Authority Gaps, cross-repository dependency acceptance, and PROGRAMSTART-caused friction.

This run contained all of those conditions. The operator corrected the handling of a missing `sqlite3` CLI, the first private-ingress replay exposed a cross-owner continuation gap, `ecosystem-contracts` owner admission reached accepted/merged state, and Execution Node owner-handoff admission reached accepted/merged state.

The Learning Gate did not surface on its own at those checkpoints. It was evaluated only after the operator explicitly reminded the orchestration to capture learning and investigate why the gate had not caught it.

## Evidence

- Current `start-programstart-project.prompt.md` requires the Learning Gate at meaningful acceptance checkpoints and specifically calls out operator correction, Authority Gap, and cross-owner convergence.
- Current `docs/PROGRAMSTART_LEARNING_LOOP.md` lists packet closure, cross-repository dependency acceptance, PROGRAMSTART friction, and direct retest of an open lesson as default triggers.
- PROGRAMSTART PR #122 is currently open with positive evidence proposing PSL-013 validation from Home Automation WP-19, where the Learning Gate reportedly ran without operator prompting.
- In this autonomy-parity run, no Learning Gate classification was produced at the earlier eligible checkpoints until the operator reminder.
- The accepted `first_wave_machinery_priority` still places automatic Challenge/Learning triggering later in the remaining parity machinery sequence, so Backbone-level automatic triggering is not yet fully implemented.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** documented the correct trigger rules but did not produce the Learning Gate result uniformly across this execution path.
- **What helped:** once explicitly invoked, the Learning Loop correctly deduplicated against PSL-013/PSL-021 and exposed the central-ledger shared-mutation collision rather than creating duplicate lessons.
- **What created friction or uncertainty:** learning capture still depended on operator recall in this path, which is the exact failure mode PSL-013 is intended to remove.
- **Was existing methodology sufficient?** the methodology text is sufficient; execution/trigger propagation is not yet uniformly sufficient.

## Learning decision

- **Existing lesson match:** `PSL-013`.
- **Maturity before:** `implemented` on current main; PR #122 proposes `validated`.
- **Maturity after:** no central-rollup change here; this is counterevidence that must be reconciled with PR #122 before PSL-013 can be treated as uniformly validated.
- **Why the evidence changes or does not change maturity:** one closure path may successfully invoke the gate while another still misses it. That narrows the claim from “automatic Learning Gate works generally” to “automatic invocation is path-dependent until parity machinery and trigger propagation are proven end to end.”
- **PROGRAMSTART change required now:** do not add a second learning system. Preserve the counterevidence, reconcile it into the existing PSL-013 lane, and ensure the remaining autonomy-parity machinery includes mechanical Challenge/Learning triggering rather than relying on ChatGPT/operator memory.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next autonomy-parity packet or cross-owner convergence after automatic Challenge/Learning triggering is implemented.
- **What evidence would be sufficient:** the Learning Gate is evaluated automatically at the first qualifying checkpoint without operator prompting, returns either a legitimate no-op or durable observation, respects shared-mutation ownership, and does not block product progress.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] No unnecessary new PROGRAMSTART lesson ID was manufactured.
