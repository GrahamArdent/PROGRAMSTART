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
- active implementation reuses the current packet;
- wrong-owner work routes to the resolved owner;
- generic continuation never clears a genuine human gate;
- long conversation + short final command retains material accepted constraints only;
- current authority supersedes stale conversation state;
- safe reversible inference does not force an operator question;
- material consequence ambiguity does force an exact operator decision;
- handoff preserves owner/exclusions without carrying brainstorming noise;
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
- `CONVERGED` — semantic direction is adequate but current machine-resolvable context, such as authority or durable active packet state, still needs retrieval;
- `HANDOFF_READY` — a packet can be compiled/recompiled but current authority resolves implementation to another owner;
- `EXECUTION_READY` — a current packet is reusable or a new packet can be compiled for normal admission;
- `EXECUTING` — an already-existing packet is current and durable execution should resume rather than replan;
- `GATED` — a genuine admitted human consequence gate remains active;
- `COMPLETE` — current acceptance is already satisfied and no work should be invented.

These values MUST NOT become a second persisted runtime lifecycle. A real integration may recompute them from conversation semantics + durable project/Controller state.

## 4. Contextual continuation semantics

The deterministic resolver never checks whether the final text equals `proceed`, `go ahead`, or another phrase. A trusted semantic harvester supplies the execution-relevant conversational state. This avoids brittle keyword semantics and lets equivalent short natural-language continuations behave consistently.

Resolution rules:

1. **Genuine human gate first** — preserve the exact gate, affected branch, return evidence, and safe parallel work. Generic continuation is never blanket approval.
2. **Already complete** — report closure/current state; do not manufacture another packet.
3. **Material semantic ambiguity** — surface only the exact outcome/consequence-changing decision.
4. **Execution underway but local packet missing** — recover the durable active Work Packet/Controller state; do not compile duplicate work because chat context was truncated.
5. **Existing packet without current authority** — revalidate the packet; do not ask the operator to reconstruct authority JSON.
6. **Existing packet + unchanged authority** — continue/resume the exact packet.
7. **Existing packet + authority drift** — recompile from current semantic harvest and current authority before readmission. Current repository/runtime truth supersedes stale chat.
8. **Exploratory/unconverged conversation** — synthesize the strongest current conclusion; do not fabricate a giant execution project.
9. **Converged but authority missing** — route authority/currentness retrieval as a system requirement.
10. **Converged + current authority** — compile to the existing Work Packet contract and either admit locally or hand off to the resolved owning repository.

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

An existing sealed packet wins over a repeated generic continuation when it remains current. `assess_authority_drift()` is used before reuse when a current `AuthoritySnapshot` is available.

If material authority/currentness changed, the old packet is not silently reused. The replacement records `supersedes_specification_id` and requires normal Controller readmission.

If execution is known to be underway but the local conversation no longer carries the active packet, the resolver returns `recover_execution_state` instead of generating a new packet. This is the fail-safe against chat truncation creating duplicate work.

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

The focused test suite covers the requested cases and additional anti-duplication boundaries:

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
14. existing packet but current authority absent -> revalidate, no regeneration;
15. tampered existing packet -> fail integrity before resolution.

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

Final Challenge must be rerun against the exact PR diff after repository validation.

## 10. Learning / maturity

What V0.2 proves at repository level:

- the existing Work Packet hypothesis remains viable without a second Work Spec ontology;
- conversation-state classification materially improves deterministic continuation handling after semantic harvesting;
- an existing packet can be reused/revalidated instead of regenerated on every generic continuation;
- human intervention can be limited to genuine admitted gates and material outcome-changing ambiguity;
- contextual worker prompts can be compressed to accepted decisions/provenance/currentness rather than whole-chat replay.

What V0.2 does **not** prove:

- ordinary ChatGPT history can yet be harvested deterministically and completely;
- the production semantic interpretation producer is selected/bound;
- owning authority/currentness can yet be resolved automatically for every project/runtime;
- Evidence Spine/currentness integration is live;
- a compiled packet has been admitted into the live Autonomous Controller;
- Mission-Control can yet submit a concise objective end to end;
- ordinary ChatGPT `proceed` is globally solved.

Those are real integration frontiers, not reasons to add more repository scaffolding preemptively.

## 11. Learning disposition

The strongest reusable lesson remains narrower than “build a prompt compiler”:

> Treat ordinary conversation as a semantic ingress source, preserve accepted/rejected/currentness provenance, reuse current sealed Work Packets whenever possible, and resolve continuation from conversation state + current authority. Keep the classification stateless and let the Controller own durable execution.

Do not promote a broader methodology mechanism until a real chat/authority/Controller integration retest demonstrates a gap that these existing primitives cannot cover.
