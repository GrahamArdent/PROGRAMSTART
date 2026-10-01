# Reasoning Locality — Codex Usage Retrospective

Status: **subordinate / non-canonical evidence**.

This record does not own project scope, execution order, model availability, purchasing authority, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-10-01
- **Project / repository:** PROGRAMSTART
- **PROGRAMSTART lesson ID:** proposed new lesson; promotion depends on this bounded implementation and a real retest
- **Checkpoint / acceptance surface:** Context Locality / Knowledge Compounding experiments through Codex on the Execution Node
- **Classification:** systemic counterevidence + candidate improvement

## What happened

Two read-only Codex experiments used GPT-6 Sol with maximum requested reasoning. The first premium run materially changed the architecture: it showed that existing PROGRAMSTART already owns most proposed knowledge machinery and identified concrete retrieval/currentness defects. The second correctly compared retrieval strategies, but premium reasoning remained active while performing many mechanical repository reads, searches, parameter sweeps, and measurements after the core uncertainty had narrowed.

The second run hit the account usage limit before turn completion. This is evidence that model tier was inherited by the whole objective instead of being selected at each reasoning boundary.

## Evidence

- /home/graham/knowledge_compounding_experiment.jsonl: completed provider trace, 633,768 bytes.
- Completed usage: 976,937 input tokens; 876,416 cached input; 100,521 derived uncached input; 20,611 output; 9,909 reasoning-output tokens.
- /home/graham/retrieval_harness_codex.jsonl: 403,692-byte incomplete trace; 43 command executions; provider terminated the turn for usage-limit exhaustion, so exact final token accounting is unavailable.
- Retrieval result before termination: metadata-only missed decisive body evidence; full-body recovered evidence with large context expansion; bounded section retrieval preserved strong recall with materially smaller payloads.
- Exact usage evidence is retained as evidence, not converted into a permanent provider-price/model-capability claim.
## PROGRAMSTART behavior

- **What helped:** Cost Governance already requires the lowest-cost model/tier that meets measured quality/reliability; Context/Work Packet rules already support progressive disclosure; Learning Gate already requires owner-routed evidence.
- **What created friction:** there was no explicit rule to step down after premium uncertainty was resolved, and no standard run evidence distinguishing cached/uncached input, reasoning output, tool payload, outcome change, and termination reason.
- **Was existing methodology sufficient?** partially.

## Learning decision

- **Existing lesson match:** extends PSL-014 cost discipline and PSL-003 proportional rigor, but neither currently makes model tier local to a reasoning boundary or requires step-down.
- **Maturity before:** none.
- **Maturity after:** candidate.
- **Why:** one completed premium run plus one usage-limit counterexample is material enough for a bounded deterministic guardrail, but not enough to claim validated optimal routing.
- **PROGRAMSTART change required now:** bounded extension to Cost Governance plus deterministic contract tests; no new control plane, registry, scheduler, or model authority.

## Candidate rule — Reasoning Locality

Select model/reasoning tier at the smallest decision boundary that needs it. Premium reasoning is justified by unresolved novel inference, conflicting credible evidence, material architectural consequence, authority/safety ambiguity, or documented failure of a cheaper sufficient path. Once that condition is resolved, step down for mechanical retrieval, execution, measurement, formatting, and repetition. Re-escalate only when new material uncertainty appears.

Premium invocation evidence should record, when available: objective/run reference, model, reasoning effort, escalation reason, timestamps, input/cached/uncached/output/reasoning tokens, tool-result payload, wall time, termination reason, decision/assumption change, cheaper candidate, and observed step-down point. Missing provider telemetry remains unknown; never fabricate it.
## Retest

Replay a representative retrieval/decision task with cheap/default execution for mechanical work and premium reasoning only at unresolved consequential boundaries. Compare decision correctness, evidence completeness, authority/currentness safety, latency, and provider-reported usage. The lesson earns validation only if decision quality is maintained or improved without false admission/terminality/authority inversion while unnecessary premium consumption materially falls.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] Provider usage unavailable from the failed turn is recorded as unknown rather than estimated.
