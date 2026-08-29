# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-28
- **Project / repository:** `GrahamArdent/repo-watchtower`
- **PROGRAMSTART lesson ID:** `PSL-015`
- **Checkpoint / acceptance surface:** Watchtower V0.2 Slice 1 / PR #1 post-implementation review before merge
- **Classification:** systemic

## What happened

PROGRAMSTART Mode C correctly narrowed Watchtower from its long-term autonomous-remediation architecture to a bounded read-only observability slice. The slice established signed GitHub webhook intake, process-local delivery replay suppression, observe-only defaults, tests, CI, and a Watchtower-native V0.2 execution authority.

The implementation was then reported as ready to merge after green CI. A subsequent independent review of the completed PR found a realistic failure sequence that the original execution did not surface: the process-local delivery ID was recorded before downstream incident persistence completed. If persistence failed after the delivery was recorded, a legitimate provider retry could be suppressed and the incident lost.

The architecture and overall slice remained sound. The new evidence was a post-implementation counterexample against operation ordering, not a reversal of the product direction.

## Evidence

- repository / PR / commit / run / provider / runtime evidence: `GrahamArdent/repo-watchtower` PR #1, head `22a01f508520754f0cc05a5f4df876f6af362c6f`; CI run `33226463294` passed.
- exact current state relevant to the observation: PR #1 verifies GitHub webhook HMAC from raw bytes and adds an in-memory replay guard; the reviewed implementation records the delivery ID after JSON parsing but before `store.upsert(...)` for incident-producing events.
- verification actually performed: live PR metadata, CI result, PR patch, `src/app.ts`, `src/security/github-webhook.ts`, and `src/security/delivery-replay-guard.ts` were independently inspected.
- checks not performed / unavailable: no production runtime or real webhook delivery was exercised as part of this methodology observation; the issue was identified by code-path/counterexample analysis.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** correctly used Mode C, preserved Watchtower authority, bounded the work packet, strengthened the trust boundary, added tests/CI, and deliberately kept remediation/autonomy out of V0.2.
- **What helped:** proportional rigor, existing Challenge Gate concepts, evidence-earned complexity, and the Learning Gate all pointed toward conservative execution.
- **What created friction or uncertainty:** the completed high-risk implementation could be declared merge-ready without an explicit adversarial review of the actual diff. Existing verification focused on intended behavior and current tests rather than requiring a realistic counterexample/failure-sequence challenge.
- **Was existing methodology sufficient?** partially. The existing Challenge Gate already owns blast-radius and architecture/implementation alignment, so a new lifecycle/stage is not warranted. The closure invocation/enforcement is the gap.

## Learning decision

- **Existing lesson match:** none. This is distinct from evidence-source typing (`PSL-009`) and adaptive decision routing (`PSL-003`): the missing behavior occurs after implementation exists and before high-risk work is accepted/merge-ready.
- **Maturity before:** none
- **Maturity after:** implemented
- **Why the evidence changes or does not change maturity:** this is one materially strong real-project case at an Internet-facing trust boundary, and the required correction is bounded: extend the existing Challenge Gate/verification closure rather than add a new stage, agent, or artifact.
- **PROGRAMSTART change required now:** add a risk-triggered post-implementation adversarial closure pass to the existing Challenge Gate and orchestration contract. It must review the completed implementation, assume current tests may miss a defect, construct realistic failure sequences, and require targeted correction/tests when a counterexample violates an important invariant.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next PROGRAMSTART-assisted work packet that changes a material trust/security, persistence/idempotency/concurrency, migration, destructive/external-side-effect, or other high-impact/hard-to-reverse boundary and reaches PR/work-packet closure.
- **What evidence would be sufficient:** the adversarial closure pass is automatically activated by the actual changed surface, records at least one relevant counterexample/failure-sequence attempt, and either (a) finds/corrects a defect before merge-ready status or (b) clears the boundary with targeted evidence without adding broad ceremony.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The change extends an existing Challenge Gate rather than manufacturing a new lifecycle.
