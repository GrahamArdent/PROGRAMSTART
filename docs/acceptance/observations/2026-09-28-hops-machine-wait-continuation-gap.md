# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

## Observation identity
- **Date:** 2026-09-28
- **Project / repository:** PROGRAMSTART #158 HOPS convergence
- **PROGRAMSTART lesson ID:** PSL-013 (strengthening/counterevidence); related wait/resume semantics
- **Checkpoint / acceptance surface:** P01 PR-gate wait -> merge -> successor packet continuation
- **Classification:** systemic counterevidence

## What happened
P01 was already authorized through terminal completion and its successor P02 was already defined. The Required PR Gate was a routine machine wait. The session reported the pending gate and returned control to the operator twice instead of boundedly rechecking and continuing when the gate passed. The operator had to prompt again even though no new authority, decision, secret, spend, or human action was required.

## Evidence
- PROGRAMSTART already requires accepted gate evidence to resume automatically without redundant `proceed`.
- `wait_wake_retry` is already represented as implemented/proven for durable machine evidence.
- P01 Required PR Gate later completed successfully and PROGRAMSTART PR #170 merged as `27e5b5038cc1deaf1d107ff3c143c4a453d621ab` without any new operator authority.
- The redundant operator interaction is therefore counterevidence to dominant-path conformance, not evidence that the rule was absent.

## PROGRAMSTART behavior
- **What PROGRAMSTART did:** supplied correct resume semantics but did not make routine machine-wait continuation explicit enough at the dominant packet execution boundary.
- **What helped:** exact gate evidence and existing wait/resume ownership made the correct behavior unambiguous once challenged.
- **What created friction or uncertainty:** a routine CI wait was surfaced as a conversational stopping point and successor continuation was treated as needing another prompt.
- **Was existing methodology sufficient?** partially: the principle existed, but the observed execution path failed to conform.

## Learning decision
- **Existing lesson match:** PSL-013 directly requires Learning Gate wiring into dominant closure; existing automatic-resume semantics cover redundant `proceed` after accepted evidence.
- **Maturity before:** implemented
- **Maturity after:** implemented (strengthened; validation remains open)
- **Why:** this is real counterevidence that documented automatic behavior can still fail at a routine machine wait/packet-successor boundary.
- **PROGRAMSTART change required now:** bounded strengthening of the dominant orchestration contract and parity acceptance scenario; no new subsystem.

## Retest
- **Next real condition:** an already-authorized packet encounters a routine machine gate/transient retry and then satisfies it while its already-authorized successor is ready.
- **Sufficient evidence:** bounded wait/recheck continues automatically through accepted evidence and into the successor until a genuine human/authority/checkpoint boundary, with no generic operator `continue`.

## Safety / authority check
- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
