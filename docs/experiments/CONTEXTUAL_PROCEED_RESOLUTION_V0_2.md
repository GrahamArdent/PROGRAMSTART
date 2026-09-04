# Contextual Proceed Resolution / Intent Ingress — V0.2

Status: **repository-level implementation / live chat-runtime integration not claimed**

Owner: **PROGRAMSTART Intent Ingress + existing Work Packet semantics**

Canonical authority is unchanged. `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` remains authoritative for Work Packet semantics. ADR `0025-intent-ingress-precedes-project-entry-mode.md` remains the Intent Ingress architecture decision. The Autonomous Controller remains the durable admission/continuation/wait-resume owner.

## 1. Reconciled decision

The V0.1 hypothesis survives Challenge with an important narrowing:

`ordinary conversation -> trusted semantic harvest -> current authority/currentness -> existing sealed Work Packet -> normal PROGRAMSTART admission -> Controller execution`

The canonical object is still the existing PROGRAMSTART **Work Packet**. V0.2 does **not** introduce a second `WorkSpecification` ontology, lifecycle, queue, durable conversation state machine, Controller, prompt platform, or orchestration engine.

The new conversation states are computed **Intent Ingress transition classifications**. They exist only to decide what the current interaction is ready to do. Durable execution state still belongs to the owning project and Autonomous Controller.

Long-form prompts remain derived renderings. They are not execution truth.

## 2. Current slice / compact Work Packet

```text
OBJECTIVE:
Resolve short contextual continuation language from trusted conversation semantics and current authority without losing accepted decisions, duplicating active work, weakening gates, or requiring operator boilerplate.

WHY_NOW / AUTHORITY:
Merged Intent Ingress V0.1 / ADR 0025 + current Work Packet semantics + current Controller interaction boundary.

BLOCKER_SCOPE:
none for repository proof; production semantic harvesting, authority/currentness resolution, and Controller admission integration remain separate integration frontiers.

SAFE_EXECUTION_LANE:
Lane B — reversible PROGRAMSTART repository code/tests/docs only.

CLOSURE_CONTROL:
PROGRAMSTART repository PR gate + post-implementation Challenge.

COORDINATED_MODE_C_LANES:
none for this bounded repository slice.

SELECTED_LANE:
Intent Ingress contextual transition resolution only.

LANE_INDEPENDENCE_EVIDENCE:
No Controller or Mission-Control runtime mutation is required to prove the PROGRAMSTART-side resolver contract.

LANE_CONFLICTS:
none identified on the intent-ingress files for this slice.

IN_SCOPE:
- trusted conversation-harvest contract;
- computed transition classification;
- existing-packet reuse/currentness revalidation;
- genuine-gate preservation;
- owner handoff resolution;
- stale-conversation correction;
- compact contextual worker rendering;
- deterministic scenario tests.

OUT_OF_SCOPE:
- LLM/chat-history harvester implementation;
- repository/runtime authority discovery implementation;
- Evidence Spine integration implementation;
- Controller admission/runtime implementation;
- Mission-Control UI/API implementation;
- new persistent conversation state;
- new Work Spec schema family;
- keyword/phrase parsing of `proceed`;
- new operator-facing CLI.

REQUIRED_CONTEXT:
ADR 0025, Intent Compilation V0.1 acceptance record, canonical Work Packet semantics, current Controller operator-interaction ownership.

ACCEPTANCE_CRITERIA:
- converged discussion compiles from material accepted state;
- active implementation reuses the current packet only when current authority and a complete recovered executable semantic harvest are unchanged;
- incomplete conversation harvest never counts as proof that an existing packet remains semantically current;
- accepted semantic drift replaces/readmits the packet even when authority is unchanged;
- partial recovered semantic drift triggers full semantic recovery rather than silent reuse or compilation from incomplete context;
- existing packet with unresolved current authority remains CONVERGED pending machine revalidation rather than being mislabeled execution-ready;
- wrong-owner work routes to the resolved owner;
- generic continuation never clears a genuine human gate;
- long conversation + short final command retains material accepted constraints only;
- current authority supersedes stale conversation state;
- safe reversible inference does not force an operator question;
- material consequence ambiguity does force an exact operator decision;
- handoff preserves owner/exclusions without carrying brainstorming noise;
- contextual handoff cannot carry accepted executable semantics absent from the sealed packet;
- already-complete work does not generate another packet;
- execution-context truncation recovers durable state rather than duplicating work;
- no persistent second state machine or second Controller is introduced.

TARGETED_VERIFICATION:
Focused contextual-resolution tests + existing intent-ingress/compiler regressions + repository Required PR Gate.

ADVERSARIAL_CLOSURE:
required — this change governs authority/currentness/gate-sensitive transitions.

DURABLE_UPDATES_IF_NEEDED:
this bounded acceptance record + PR evidence; methodology changes only if Challenge/real integration earns them.
```

## 3. Transition classification

`ConversationState` uses these computed classifications:

- `EXPLORE` — conversation has not converged enough for executable work, or a material semantic decision is still unresolved;
- `CONVERGED` — semantic direction is adequate but current machine-resolvable context, such as authority or complete conversation semantics, still needs retrieval;
- `HANDOFF_READY` — a packet can be compiled/recompiled but current authority resolves implementation to another owner;
- `EXECUTION_READY` — a current packet is reusable or a new packet can be compiled for normal admission;
- `EXECUTING` — an already-existing packet is current and durable execution should resume rather than replan;
- `GATED` — a genuine admitted human consequence gate remains active;
- `COMPLETE` — current acceptance is already satisfied and no work should be invented.

These values MUST NOT become a second persisted runtime lifecycle. A real integration may recompute them from conversation semantics + durable project/Controller state. In particular, an existing packet whose current authority or complete current semantic harvest has not yet been resolved is `CONVERGED`, not `EXECUTION_READY` or `EXECUTING`: the system knows the work identity but has not proven current admission readiness.

## 4. Contextual continuation semantics

The deterministic resolver never checks whether the final text equals `proceed`, `go ahead`, or another phrase. A trusted semantic harvester supplies the execution-relevant conversational state. This avoids brittle keyword semantics and lets equivalent short natural-language continuations behave consistently.

Resolution rules:

1. **Genuine human gate first** — preserve the exact gate, affected branch, return evidence, and safe parallel work. Generic continuation is never blanket approval.
2. **Already complete** — report closure/current state; do not manufacture another packet.
3. **Material semantic ambiguity** — surface only the exact outcome/consequence-changing decision.
4. **Execution underway but local packet missing** — recover the durable active Work Packet/Controller state; do not compile duplicate work because chat context was truncated.
5. **Existing packet without current authority** — retain it as `CONVERGED`, request machine currentness revalidation, and do not ask the operator to reconstruct authority JSON or declare execution-ready state prematurely. If the semantic harvest is also incomplete, recover both machine inputs before reuse.
6. **Existing packet + incomplete semantic harvest** — recover complete current conversation semantics before reuse even when no visible difference has yet been recovered. Absence of visible drift is not proof of semantic equivalence under truncation.
7. **Existing packet + unchanged authority + unchanged complete recovered executable semantics** — continue/resume the exact packet.
8. **Existing packet + changed accepted executable semantics** — recompile from a complete current harvest before Controller readmission even when authority itself is unchanged. If a partial harvest already proves material drift, recover complete semantics before deciding whether to replace the packet.
9. **Existing packet + authority drift** — recompile from current semantic harvest and current authority before readmission. Current repository/runtime truth supersedes stale chat.
10. **Exploratory/unconverged conversation** — synthesize the strongest current conclusion; do not fabricate a giant execution project.
11. **Converged but authority missing** — route authority/currentness retrieval as a system requirement.
12. **Converged + current authority** — compile to the existing Work Packet contract and either admit locally or hand off to the resolved owning repository.

## 5. Trusted conversation harvest / provenance

`ConversationHarvest` deliberately separates:

- objective;
- accepted decisions;
- rejected alternatives;
- brainstorming;
- superseded items;
- active constraints;
- explicit exclusions;
- unresolved material ambiguities;
- evidence-backed currentness corrections;
- execution-underway / acceptance-complete signals;
- active human consequence gate;
- existing durable Work Packet reference.

Material statements carry a compact provenance basis:

- `explicit_user_instruction`;
- `accepted_conversation_decision`;
- `current_project_authority`;
- `repository_evidence`;
- `runtime_evidence`;
- `programstart_default`;
- `system_inference`.

This is inspectable provenance, not hidden chain-of-thought.

Only execution-relevant accepted decisions, constraints, and explicit exclusions flow into the sealed packet's constraint projection. Rejected alternatives are optionally retained in contextual handoff as non-authoritative context. Brainstorming and superseded ideas are not rendered into the worker handoff.

The trusted harvester remains an integration boundary. V0.2 does not pretend a deterministic Python module can classify an arbitrary transcript correctly without a semantic producer.

## 6. Currentness and packet reuse

An existing sealed packet wins over a repeated generic continuation only when its integrity holds, current authority is unchanged, and a **complete** recovered executable semantic harvest matches the packet. `assess_authority_drift()` is used before reuse when a current `AuthoritySnapshot` is available, and the resolver separately compares executable intent semantics rather than treating authority currentness as sufficient by itself.

An incomplete harvest is not evidence of semantic equivalence. If the system cannot recover a complete current objective/kind/constraint projection, it returns a machine context-recovery requirement before packet reuse. This remains low-human-interaction behavior: the operator is not asked to reconstruct context that the system should recover.

If current authority has not yet been resolved, the packet is retained but the ingress classification remains `CONVERGED` until machine revalidation completes. Packet existence is not evidence that the packet is current.

If material authority/currentness changed **or** accepted executable semantics changed, the old packet is not silently reused. The replacement records `supersedes_specification_id` and requires normal Controller readmission.

If the available conversation harvest is incomplete but its recovered objective, intent kind, or constraints already prove material semantic drift from the active packet, the resolver records that stronger reason while still requiring complete semantic recovery before reuse or replacement. It does not compile from an incomplete harvest merely because some changed facts are visible.

If execution is known to be underway but the local conversation no longer carries the active packet, the resolver returns `recover_execution_state` instead of generating a new packet. This is the fail-safe against chat truncation creating duplicate work.

The contextual handoff renderer also fails closed when accepted executable constraint text is not sealed into the Work Packet. Conversation provenance therefore cannot become a parallel authority channel around packet integrity.

The existing `intent_id` remains a deterministic raw-intent label, so short utterances such as `Proceed.` can intentionally share it. The sealed `specification_id`/semantic digest remains the packet identity because it includes interpreted semantics and authority. No current PROGRAMSTART downstream consumer uses `intent_id` as a unique execution key; a future integration must not introduce that assumption without changing the contract deliberately.

## 7. Controller and Mission-Control boundary

V0.2 preserves the existing owner split:

- **PROGRAMSTART Intent Ingress** — semantic transition classification + Work Packet compilation boundary;
- **owning project authority** — project truth, scope, sequencing, gates, acceptance;
- **Autonomous Controller** — durable admission, semantic execution state, continuation, waits/resume, retries/recovery, human gates;
- **Mission-Control** — operator/client interaction plane;
- **Evidence Spine/current evidence owners** — evidence/provenance/currentness references, not execution state.

A future Mission-Control surface may submit a concise objective and display the compiled summary/inferences/gates, but it should consume this PROGRAMSTART capability rather than implement a second compiler.

## 8. Scenario coverage

The focused test suite covers the requested cases and additional anti-duplication/integrity boundaries:

1. converged discussion -> compile for admission;
2. active implementation -> reuse/resume existing packet;
3. wrong-owner idea -> owner handoff;
4. human consequence -> preserve exact gate and safe parallel work;
5. long conversation / short final command -> retain accepted constraints, exclude brainstorming;
6. stale conversation -> recompile from current authority/currentness;
7. safe ambiguity/inference -> continue without operator ceremony;
8. material ambiguity -> exact operator decision required;
9. cross-chat handoff -> owner/exclusions/rejected-context retained without brainstorming noise;
10. already complete -> report complete, create no packet;
11. unconverged exploration -> synthesize, not execute;
12. converged but authority absent -> machine authority-resolution requirement;
13. execution underway but packet absent -> durable state recovery, no duplicate compile;
14. existing packet but current authority absent -> retain packet as `CONVERGED` pending revalidation, no regeneration or premature ready/executing state;
15. tampered existing packet -> fail integrity before resolution;
16. same accepted semantics + short final wording -> reuse existing packet;
17. new accepted constraint + unchanged authority -> recompile/readmit;
18. partial recovered semantic drift -> recover complete current semantics rather than silently reuse/recompile;
19. accepted executable handoff semantics absent from the packet -> handoff rendering fails closed;
20. incomplete harvest with no visible drift -> recover complete semantics rather than treating missing context as proof that the packet is unchanged.

## 9. Adversarial Challenge findings and fixes

Challenge changed the design before closure:

1. **Conversation states could become a second Controller lifecycle.** Fixed by making them computed Intent Ingress classifications only, with no persistence/queue/lease semantics.
2. **`proceed` could become blanket approval.** Genuine human gates are evaluated before continuation and remain exact.
3. **Repeated short commands could create duplicate work.** Current sealed packets are reused; execution-with-missing-local-packet routes durable state recovery.
4. **Stale chat could replay superseded work.** Material authority drift forces recompile/readmission; explicit currentness corrections preserve discrepancy evidence.
5. **Wrong-owner conclusions could authorize local implementation.** Resolved owning authority determines `HANDOFF_READY` and target repository.
6. **Brainstorming/rejected options could be promoted accidentally.** Execution projection includes only accepted state/constraints/exclusions; brainstorming is excluded and rejected alternatives are context-only.
7. **Low-interaction could silently widen authority.** Safe inference may narrow execution, but authority/effects still come only from current `AuthoritySnapshot`; material consequence ambiguity requires operator judgment.
8. **Conversation truncation could silently lose critical state.** Known active execution without its packet fails toward durable recovery, not recompilation.
9. **A completed slice could be treated as another continuation request.** `COMPLETE` short-circuits packet generation.
10. **A large prompt could re-emerge as canonical.** Contextual handoff is explicitly derived and appends the existing sealed Work Packet renderer.
11. **Short utterances share raw `intent_id`.** Confirmed this identifier is not currently used as a unique execution key; packet identity remains `specification_id`/semantic digest. Documented as an integration invariant rather than widening V0.2 scope.
12. **Authority could remain unchanged while accepted semantics changed.** Fixed by comparing executable semantic signatures before packet reuse and recompiling/readmitting when accepted objective/kind/constraints changed.
13. **Partial conversation recovery could hide a newly recovered material constraint.** Fixed by failing toward complete semantic recovery when an incomplete harvest already proves drift.
14. **Contextual handoff prose could become an authority side-channel.** Fixed by rejecting handoff rendering when accepted executable constraints are absent from the sealed packet.
15. **Packet existence could be mistaken for current execution readiness.** Fixed by keeping existing-packet/no-current-authority transitions `CONVERGED` until machine currentness revalidation succeeds.
16. **No visible drift could be mistaken for proof after conversation truncation.** Fixed by requiring a complete semantic harvest before reuse; incomplete context routes machine recovery even when the recovered fragment does not yet contradict the packet.

Final Challenge must be rerun against the exact PR diff after repository validation.

## 10. Learning / maturity

What V0.2 proves at repository level:

- the existing Work Packet hypothesis remains viable without a second Work Spec ontology;
- conversation-state classification materially improves deterministic continuation handling after semantic harvesting;
- packet currentness has two independent dimensions that matter at ingress: current durable authority/evidence and current accepted executable conversation semantics;
- packet existence and packet currentness are distinct; unresolved currentness must not be mislabeled execution-ready;
- missing semantic evidence is not affirmative evidence that the packet remains unchanged;
- an existing packet can be reused/revalidated instead of regenerated on every generic continuation;
- human intervention can be limited to genuine admitted gates and material outcome-changing ambiguity;
- contextual worker prompts can be compressed to accepted decisions/provenance/currentness rather than whole-chat replay;
- contextual prose must remain subordinate to sealed packet semantics, not become another authority surface.

What V0.2 does **not** prove:

- ordinary ChatGPT history can yet be harvested deterministically and completely;
- the production semantic interpretation producer is selected/bound;
- owning authority/currentness can yet be resolved automatically for every project/runtime;
- Evidence Spine/currentness integration is live;
- a compiled packet has been admitted into the live Autonomous Controller;
- Mission-Control can yet submit a concise objective end to end;
- ordinary ChatGPT `proceed` is globally solved.

This work also exercised the degraded API/connector publication path already anticipated by `PSL-022`. No executable local candidate-validation workspace was available to this connected-tool path, so local/pre-push validation is not claimed. GitHub's Required PR Gate exposed deterministic Ruff/end-of-file debt; the formatter output was incorporated in a bounded correction and the ordinary repository workflow restored before authoritative revalidation. Because the deterministic debt reached remote CI first, this is **not** the positive shift-left retest required to validate `PSL-022`; it is supporting evidence that the degraded-capability clause and independent GitHub verifier are necessary. No broader methodology mechanism is promoted from this observation.

Those remaining integration frontiers are real, not reasons to add more repository scaffolding preemptively.

## 11. Learning disposition

The strongest reusable lesson remains narrower than “build a prompt compiler”:

> Treat ordinary conversation as a semantic ingress source, preserve accepted/rejected/currentness provenance, revalidate both durable authority and a complete accepted executable semantic harvest before packet reuse, distinguish packet existence from current execution readiness, reuse current sealed Work Packets whenever possible, and resolve continuation from conversation state + current authority. Keep the classification stateless and let the Controller own durable execution.

Do not promote a broader methodology mechanism until a real chat/authority/Controller integration retest demonstrates a gap that these existing primitives cannot cover.
