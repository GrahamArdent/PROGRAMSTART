# Convergence Output + Durable Storage — Settled Implementation Plan

**Date:** 2026-10-05  
**Status:** IMPLEMENTATION PLAN CONVERGED / NON-AUTHORITATIVE  
**Mode:** Mode C planning only  
**Implementation authorized by this file:** No  
**Canonical authority changed by this file:** None  
**PROGRAMSTART base used:** `26bab1de14b6c4f01e17e4a6c2fd980ec743af1f`  
**Related design evidence:** Execution Readiness Convergence draft PR #207 and the 2026-10-05 read-only Standard Convergence Output + Durable Packet Storage experiment.

> This plan is a durable implementation proposal. It does not itself change PROGRAMSTART methodology, create the archive, or authorize downstream mutation.

---

## 1. Objective

Adopt the settled operator experience:

- keep the chat/operator-facing response compact when a complete artifact exists;
- produce one complete Markdown **Convergence Packet** containing the material Challenge cycle, final recommendation, decision log, GO/NO-GO, residuals, and next step;
- durably route final packets by ownership rather than creating one global source of truth;
- preserve current PROGRAMSTART authority boundaries;
- avoid a new repository, new lifecycle, second Challenge Gate, or global decision database.

The target user experience in a host that supports attachments is:

```text
[Markdown packet]

<brief result>

GO / NO-GO: ...
Recommended next step: ...
```

The methodology must remain host-neutral: an environment that cannot attach/download a file returns or writes the same Markdown artifact through its supported artifact/path mechanism.

---

## 2. Protected outcome

A material PROGRAMSTART design/plan/review exercise can be resumed or understood without reading the chat transcript, while:

1. the operator-facing response stays concise;
2. the full reasoning remains available in one Markdown artifact;
3. the artifact never silently becomes project authority;
4. accepted project decisions still reconcile into the real owning repository;
5. cross-project packet storage does not become a backlog, queue, or global decision system;
6. repeated Challenge review stops when the current candidate produces no new material corrective delta.

---

## 3. Challenge cycle and material corrections

### C-01 — Do not create a new canonical control file

**Initial idea:** introduce a canonical Convergence Packet protocol file.

**Challenge:** this would split planning/reference/output semantics away from the existing Planning Operating Model and create another primary concern owner.

**Correction:** `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` owns the reusable Convergence Packet/output/storage semantics. No new canonical control file.

---

### C-02 — Do not make core methodology ChatGPT-specific

**Initial idea:** canonical rule requiring a “download link” and a fixed 150-word answer.

**Challenge:** PROGRAMSTART is used through multiple execution environments. File attachment/download capabilities are host-specific.

**Correction:** canonical semantics require a **concise operator summary + complete Markdown packet when activated**. The reusable convergence prompt may use a target of 150 words unless the operator asks for another limit, but file delivery adapts to host capability.

---

### C-03 — Do not change every prompt standard

**Initial idea:** add the output contract to both workflow and operator prompt standards.

**Challenge:** most prompts do not produce a durable convergence result. Global prompt-standard changes would add ceremony and cause unrelated prompts to emit artifacts.

**Correction:** add one reusable guidance/task prompt dedicated to Challenge convergence + reporting. It follows the existing workflow prompt standard and references canonical owners; no global mandatory artifact section is added to every prompt.

---

### C-04 — Do not create a separate Markdown template unless it earns itself

**Initial idea:** add `templates/convergence/CONVERGENCE_PACKET.md`.

**Challenge:** a separate template duplicates the packet structure already expressible in the Planning Operating Model and the dedicated prompt, creates another distribution/bootstrap surface, and can drift.

**Correction:** define the semantic packet structure once in the Planning Operating Model; the dedicated prompt renders it. Add a standalone template only later if real reuse outside prompts proves it materially reduces friction.

---

### C-05 — Separate canonical adoption from operator-workspace instantiation

**Initial idea:** modify PROGRAMSTART and Portfolio Operations in one logical change.

**Challenge:** canonical-before-dependent requires the reusable storage/output semantics to be accepted before the external operator workspace is changed to instantiate them.

**Correction:** two sequential PRs:
1. PROGRAMSTART canonical-methodology adoption;
2. Portfolio Operations archive instantiation after PROGRAMSTART acceptance.

---

### C-06 — Do not turn Portfolio Operations into the unresolved-owner inbox

**Initial idea:** use a convergence-packets folder for any final packet without a project home.

**Challenge:** Portfolio Operations already has Idea Ledger and Conversation Capture Inbox semantics. A catch-all packet folder would become a second inbox.

**Correction:** the archive stores only genuinely cross-project/operator-reference packets. Ambiguous-owner material continues through existing owner-routing/capture mechanisms. Project-specific packets belong with the project.

---

### C-07 — Delivery copy and durable copy are not competing truth

**Initial idea:** downloadable Markdown plus repository Markdown could become independently edited copies.

**Challenge:** two maintained copies create divergence.

**Correction:** generate one final packet body. The chat attachment is a delivery copy; the repository copy, when warranted, is a durable reference copy with `DURABLE_REF` / owner references. Neither outranks canonical project authority.

---

### C-08 — “Settled” remains shorthand, not a new state

**Challenge:** Decision Closure already has owner-settlement semantics.

**Correction:** normative result is `CONVERGENCE: CLEAR FOR DECLARED SCOPE`; “settled” remains operator shorthand.

---

## 4. Settled architecture

### 4.1 PROGRAMSTART owns the reusable semantics

Primary canonical owner:

- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`

It should gain a bounded section such as **Convergence Output and Durable Packet Routing** defining:

- activation conditions;
- compact operator-summary behavior;
- full Markdown packet semantics;
- material-only Challenge/decision history;
- authority labels;
- owner-based durable routing;
- no-auto-archive rules;
- no raw transcript requirement;
- no backlog/priority/execution semantics;
- ambiguity behavior;
- delivery-copy vs durable-reference-copy distinction.

### 4.2 Challenge Gate owns Challenge behavior

Small delta to:

- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`

Add the general convergence rule:

> When a Challenge materially changes the candidate at a deliberate design/plan/convergence review, the revised candidate must be challenged again before that boundary may be reported clear. Stop after the first fresh pass on the current candidate that yields no new material corrective delta unless another existing stronger review is independently required.

This is not a new gate or new lifecycle.

### 4.3 One reusable operator entry point

Add one workflow guidance/task prompt:

- proposed path: `.github/prompts/programstart-convergence-packet.prompt.md`

Proposed responsibility:

1. resolve whether the task is a design/plan/recommendation/convergence review;
2. load the smallest current authority needed;
3. identify the exact candidate;
4. invoke the existing Challenge Gate with stage/risk-appropriate parts;
5. incorporate material corrective deltas;
6. re-Challenge materially revised candidates;
7. stop on the first fresh clear current candidate;
8. render the full Markdown Convergence Packet;
9. return a concise operator summary;
10. recommend the correct durable storage route;
11. write/persist only when the current environment is authorized to do so and the owner is clear.

It must be **read-only by default** unless the operator separately authorizes durable repository mutation.

It must not define a second Challenge checklist.

### 4.4 Prompt registration/discoverability

Update:

- `config/registry/prompting.json`
- `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`

Register the new prompt as a workflow guidance/task prompt and index it for discoverability.

Do not invent a new prompt class.

### 4.5 No global prompt-standard mandate

Do **not** change:

- `.github/prompts/PROMPT_STANDARD.md`
- `.github/prompts/OPERATOR_PROMPT_STANDARD.md`

unless implementation-time validation proves the new prompt cannot be expressed cleanly under the current standards.

Current evidence says it can.

### 4.6 Decision/changelog reconciliation

Because the PROGRAMSTART implementation changes durable methodology behavior:

- update `PROGRAMBUILD/DECISION_LOG.md` with the accepted output/storage/convergence decision;
- update `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md`;
- perform current ADR triage;
- create/update an ADR only if the then-current ADR threshold says the change crosses it.

Do not pre-commit to a new ADR solely because this plan exists.

---

## 5. Convergence Packet contract

When activated, the packet should contain the smallest complete reconstructable result.

### Required metadata

```text
TITLE:
DATE:
MODE:
DECLARED_SCOPE:
CONVERGENCE_STATUS:
AUTHORITY_STATUS:
OWNER_REFS:
EVIDENCE_BASIS:
MUTATIONS_PERFORMED:
DURABLE_REF:
```

### Required semantic sections

1. **Executive conclusion**
2. **Objective / candidate evaluated**
3. **Current authority + evidence basis**
4. **Material Challenge cycle**
   - retain only findings that changed the candidate or boundary;
   - do not preserve repetitive drafts.
5. **Final converged recommendation/design/plan**
6. **Decision log**
7. **Residuals / unresolved blockers**
8. **GO / NO-GO**
9. **Recommended next step**
10. **Durable owner/reconciliation references**

### Authority vocabulary

Use compact labels such as:

- `NON_AUTHORITATIVE_REFERENCE`
- `DERIVED_FROM_CURRENT_AUTHORITY`
- `OWNER_RECONCILIATION_REQUIRED`
- `OWNER_RECONCILED`

The packet itself remains derived unless it is genuinely the recognized owner artifact.

---

## 6. Activation rules

Create a full Convergence Packet when at least one is true:

- the operator explicitly asks for the Markdown packet;
- the exercise runs repeated PROGRAMSTART Challenge/convergence;
- a material plan/design/recommendation is expected to be implemented later;
- the result is a handoff to another chat/agent/person;
- the Challenge materially changes the candidate;
- reconstruction from chat would be costly/unreliable;
- a durable non-authoritative decision/rationale record has real reuse value.

Do not require a packet for:

- routine status;
- simple factual Q&A;
- trivial text edits;
- ordinary implementation details already durably represented;
- repeated analysis with no durable reuse value.

---

## 7. Concise operator response contract

The dedicated convergence prompt should produce:

1. artifact/download/path reference;
2. concise result;
3. GO / NO-GO;
4. one recommended next step;
5. essential caveat only when material.

Default target: **150 words or less** when the complete packet is available.

Operator-requested limits override the default.

The word target is an interaction convention, not universal project authority and not grounds to omit a safety/blocker/currentness fact.

---

## 8. Durable storage routing

### Route A — project-specific

Store the durable reference packet in the owning repository using an existing suitable non-authoritative report/design/note surface.

Prefer existing project conventions over a universal folder name.

The packet must reference canonical owner state rather than duplicate it.

### Route B — PROGRAMSTART methodology

Store PROGRAMSTART methodology design/implementation packets in an existing non-authoritative PROGRAMSTART surface, currently `devlog/notes/` when appropriate.

This implementation plan uses that route.

### Route C — genuine cross-project/operator reference

After PROGRAMSTART methodology is accepted, instantiate a bounded archive in `GrahamArdent/portfolio-operations`.

Proposed folder:

- `convergence-packets/`

Exact path must be re-checked against current Portfolio Operations instructions at implementation time.

### Route D — owner unclear

Do not use the convergence archive as a catch-all inbox.

Use existing owner-routing/capture semantics such as:

- project search/reconciliation;
- Portfolio Operations `CONVERSATION_CAPTURE_INBOX.md`;
- `IDEA_LEDGER.md`;

depending on the meaning being preserved.

A downloadable packet may still be returned while durable owner placement remains unresolved.

---

## 9. Portfolio Operations dependent instantiation

Only after the PROGRAMSTART methodology PR is accepted.

Proposed changes:

### 9.1 Create `convergence-packets/README.md`

Contract:

- final/converged packets only;
- non-authoritative;
- no raw transcripts;
- no secrets;
- no queue/backlog/status semantics;
- no automatic execution;
- no automatic prioritization;
- no recurring broad scans;
- retrieve on explicit request, owner reference, or relevant trigger;
- each packet should point to canonical owner records where they exist;
- use sortable names such as `YYYY-MM-DD-<short-slug>.md`.

### 9.2 Update Portfolio Operations `README.md`

Add the folder as a derived reference surface explicitly outside the live attention queue.

State that Portfolio refresh/auto-progress must not scan it routinely.

### 9.3 Update root `AGENTS.md`

Add the smallest instruction needed so supported agents:

- treat the archive as derived/non-authoritative;
- do not scan it as a backlog;
- do not use it to override owner truth;
- write there only when the packet is genuinely cross-project/operator-reference material.

Do not add a nested AGENTS file unless later evidence shows root instructions are insufficient.

### 9.4 Do not modify live attention surfaces merely because a packet was archived

No automatic update to:

- `PROJECT_REGISTRY.yaml`
- `PORTFOLIO_STATUS.md`
- `OPERATOR_ACTIONS.md`
- `PORTFOLIO_HISTORY.md`

unless the packet's underlying owner truth independently changes portfolio attention.

---

## 10. Exact implementation sequence

### Gate 0 — currentness / collision preflight

Before editing:

1. re-read PROGRAMSTART main/current relevant authority;
2. inspect open PRs touching:
   - Planning Operating Model;
   - Challenge Gate;
   - prompt registry;
   - File Index;
   - Decision Log/Changelog;
3. re-read PR #207 only as design evidence; it is not authority;
4. confirm no colliding canonical lane;
5. re-read Portfolio Operations main + `AGENTS.md` before planning the dependent PR.

If collision exists, rebase/reconcile or defer the conflicting file rather than creating parallel authority.

### Gate 1 — PROGRAMSTART canonical PR

Modify only the minimum earned files:

1. `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
2. `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`
3. `.github/prompts/programstart-convergence-packet.prompt.md` (new)
4. `config/registry/prompting.json`
5. `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`
6. `PROGRAMBUILD/DECISION_LOG.md`
7. `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md`
8. focused tests if needed by §11

Do not modify Work Packet, Portfolio Control, prompt standards, source-of-truth instructions, Matrix, Controller, or runtime unless implementation evidence proves a real dependency.

### Gate 2 — exact candidate Challenge

Before treating the PROGRAMSTART PR as ready:

1. run applicable current Challenge Gate parts;
2. specifically attack:
   - shadow authority;
   - forced artifact ceremony;
   - prompt duplication;
   - host-specific assumptions;
   - project-state leakage into PROGRAMSTART;
   - unresolved owner routing;
   - archive becoming backlog;
3. if material correction is required, update the exact candidate;
4. re-Challenge the revised head;
5. stop at first fresh clear head.

### Gate 3 — deterministic validation

Use current repository-owned commands.

At minimum, based on current JIT doctrine:

```text
uv run programstart validate --check all
uv run programstart drift
```

Also run the focused prompt/contract tests added or affected by the implementation.

Remote Required PR Gate must validate the exact current head before merge.

### Gate 4 — owner acceptance

Merge only after normal PROGRAMSTART acceptance rules are satisfied.

Re-read merged owner truth before the dependent Portfolio Operations change.

### Gate 5 — Portfolio Operations dependent PR

Create the bounded archive instantiation from §9.

Do not copy project packets into it as part of bootstrap.

The first real archived packet should arrive from a genuine future cross-project/operator convergence result.

### Gate 6 — Portfolio verification

Run the repository's current validation required by its then-current instructions.

Challenge specifically:

- can archive content alter attention priority by mere existence?
- can an agent confuse a packet with current owner truth?
- does a portfolio refresh scan the archive?
- can sensitive/raw chat content leak into the archive?
- is owner routing still explicit?

Correct and re-Challenge if material deltas arise.

---

## 11. Acceptance tests / fixtures

PROGRAMSTART implementation should prove at least:

### AT-01 — prompt is registered and compliant

The new convergence prompt is in the workflow prompt registry and passes existing prompt lint/compliance.

### AT-02 — no second Challenge Gate

The prompt references `PROGRAMBUILD_CHALLENGE_GATE.md` and does not embed a competing A–H protocol.

### AT-03 — material correction forces re-Challenge

A fixture where Pass 1 changes scope/authority/verification cannot report the revised candidate clear until a fresh Challenge occurs.

### AT-04 — one-pass clear remains valid

A simple candidate with no material delta can stop after one current clear pass.

### AT-05 — packet remains derived

The rendered packet explicitly exposes authority status/owner references and cannot imply execution authority solely from `CLEAR`.

### AT-06 — concise response is separate from full packet

The reusable prompt distinguishes compact operator result from the complete Markdown artifact.

### AT-07 — host neutrality

The contract does not require a UI-specific download mechanism to be considered valid.

### AT-08 — owner routing

Fixtures cover:
- project-owned;
- PROGRAMSTART methodology;
- cross-project/operator reference;
- owner unclear.

### AT-09 — archive is not unresolved-owner capture

Owner-unclear result routes to existing capture/reconciliation behavior rather than cross-project convergence archive.

### AT-10 — no trivial artifact ceremony

Routine status/simple Q&A is not forced into a persisted Convergence Packet.

### AT-11 — archive does not drive portfolio priority

Portfolio instantiation docs explicitly prohibit routine scans and priority/execution semantics.

### AT-12 — durable/reference copy does not replace canonical owner

A packet with `OWNER_RECONCILED` points to the owner; changing packet prose alone cannot change project truth.

---

## 12. Test implementation recommendation

Prefer one focused PROGRAMSTART contract test rather than many string tests:

- proposed: `tests/test_convergence_packet_contract.py`

It should verify the cross-file invariants that are actually machine-checkable:

- new prompt registered;
- prompt references Planning Operating Model and Challenge Gate;
- prompt declares derived/non-authoritative output boundary;
- required authority/status/GO-NO-GO/next-step concepts exist;
- no execution-authority claim is present;
- owner-routing branches are represented.

Existing prompt compliance/registry/schema tests should cover the rest.

Do not add a new runtime/schema/CLI solely for this feature.

---

## 13. ADR triage

Current expectation: **decision-log level may be sufficient**, because the plan extends existing planning/output/prompt behavior without creating a new authority layer or runtime architecture.

However, implementation must run the then-current ADR threshold triage.

Create an ADR only if the actual accepted changes cross that threshold.

Do not use this planning expectation to bypass current governance.

---

## 14. Relationship to Execution Readiness Convergence PR #207

PR #207 remains non-authoritative design evidence and changes only:

- `devlog/notes/execution-readiness-convergence-design.md`

This implementation plan does not require PR #207 to merge first.

The canonical implementation may reuse one narrow principle from that design:

- material Challenge correction requires a fresh Challenge of the revised candidate.

If later canonical implementation of Execution Readiness Convergence overlaps these same files, reconcile the two plans before mutation rather than creating competing edits.

---

## 15. Explicit exclusions

This implementation must **not** create:

- a new repository;
- a central decision database;
- a packet queue;
- a global packet registry;
- automatic archive scanning;
- a packet priority field;
- automatic project promotion;
- a new lifecycle state;
- a second Challenge Gate;
- a new Work Packet type;
- a new Matrix projection;
- Controller/Compute/Watchtower runtime behavior;
- chat transcript archival;
- required artifacts for trivial interactions;
- universal per-project convergence folders.

---

## 16. Falsifiers / stop conditions

Stop or reshape the implementation if:

1. the new prompt cannot work without copying Challenge Gate logic;
2. the Planning Operating Model becomes overloaded enough that a separate owner is actually justified;
3. generated-project prompt distribution causes material unwanted clutter or broken references;
4. the output contract cannot remain host-neutral;
5. owner routing cannot distinguish project-specific from cross-project reference content;
6. Portfolio Operations cannot host the archive without making attention routing noisier;
7. packet creation materially slows ordinary work;
8. the archive starts functioning as a backlog/currentness source;
9. implementation requires a new runtime/service merely to create Markdown;
10. PR #207 or another current lane creates semantic/file collision that cannot be cleanly reconciled.

---

## 17. Challenge result for this implementation plan

Applicable PROGRAMSTART lenses used:

- **B — assumption/evidence validity**
- **C — scope integrity**
- **D — deferred/omitted work**
- **E — blast radius / verification scope**
- **F — decision coherence / reversal**
- **H — methodology / implementation alignment**

Key corrections from the cycle are recorded in §3.

After the final narrowed candidate:

- no new canonical control file is introduced;
- no new repository is introduced;
- no global prompt-standard mandate is introduced;
- no standalone packet template is required initially;
- canonical-before-dependent sequencing is preserved;
- Portfolio Operations remains derived;
- the dedicated prompt composes rather than replaces existing Challenge logic;
- owner-native decision authority remains intact.

**PLAN CONVERGENCE: CLEAR FOR DECLARED IMPLEMENTATION-PLANNING SCOPE.**

---

## 18. GO / NO-GO

### GO

Proceed to the **PROGRAMSTART canonical implementation PR** defined by Gate 1, after a fresh currentness/collision preflight.

### NO-GO

Do not yet:

- create the Portfolio Operations archive before PROGRAMSTART acceptance;
- create a new repository;
- merge PR #207 merely as a prerequisite;
- treat this plan as canonical policy;
- broaden into runtime automation.

---

## 19. Recommended next step

**GO:** authorize Gate 0 + Gate 1 only.

That next execution should:

1. perform fresh currentness/collision checks;
2. implement the minimal PROGRAMSTART canonical deltas;
3. run the exact-candidate Challenge cycle;
4. run repository validation/drift and exact-head CI;
5. stop at the PROGRAMSTART acceptance/merge boundary unless separately authorized to merge.

Only after PROGRAMSTART owner acceptance should the Portfolio Operations archive instantiation begin.
