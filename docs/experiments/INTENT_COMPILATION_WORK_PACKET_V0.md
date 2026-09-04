# Intent Compilation / Intent Ingress — V0.1

Status: **COMPLETE / MERGED — integration frontier active**

Owner: **PROGRAMSTART Work Packet semantics**

Canonical authority is unchanged. `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` remains authoritative for reusable Work Packet semantics. ADR `0025-intent-ingress-precedes-project-entry-mode.md` owns the Intent Ingress architecture decision. This file is subordinate implementation/acceptance evidence only.

## 1. Decision

The original hypothesis is accepted with narrowing:

`operator intent -> trusted semantic interpretation -> current authority/currentness -> sealed Compiled Work Packet -> existing project mode -> Controller admission -> execution/rendering`

Key decisions:

- the canonical semantic object remains the existing PROGRAMSTART **Work Packet**, not a new `WorkSpecification` ontology;
- Intent Ingress is a **pre-entry profile**, not Mode D;
- natural-language interpretation and deterministic compilation are separate trust boundaries;
- long prompts are derived renderings, not execution truth;
- owning-project authority remains authoritative;
- Controller remains the admission/durable-continuation owner.

## 2. Compact PROGRAMSTART packet for this scaffold

```text
OBJECTIVE:
Scaffold the smallest useful Intent Ingress boundary before normal PROGRAMSTART project-mode execution.

WHY_NOW / AUTHORITY:
ADR 0025 + existing Work Packet semantics + merged PR #94 implementation evidence.

BLOCKER_SCOPE:
none for repository scaffold; production interpretation/authority resolution remain future integration boundaries.

SAFE_EXECUTION_LANE:
Lane B — reversible PROGRAMSTART repository implementation only.

CLOSURE_CONTROL:
PR #94 merged as 89d36a396532b0afc678f5b9d0994652f1ce6f2e after synchronization with current main and Required PR Gate #116.

COORDINATED_MODE_C_LANES:
PR #95 formerly owned shift-left/pre-publication quality work and is merged into main.

SELECTED_LANE:
Intent Ingress semantics only.

LANE_INDEPENDENCE_EVIDENCE:
PR #94 did not duplicate PR #95 quality-gate implementation; both have converged into current main.

LANE_CONFLICTS:
none for the completed V0.1 repository scaffold.

IN_SCOPE:
- deterministic interpretation/authority boundary;
- stateless ingress adapter;
- Work Packet compilation handoff;
- focused adversarial tests;
- current ADR/acceptance reconciliation.

OUT_OF_SCOPE:
- LLM/interpreter service;
- authority/currentness resolver;
- database/queue/persistent ingress state;
- new Controller/orchestrator;
- top-level polished operator CLI;
- Mission-Control/Evidence Spine/Controller implementation changes.

REQUIRED_CONTEXT:
ADR 0025, PROGRAMBUILD Work Packet semantics, merged PR #94, current main including merged PR #95.

ACCEPTANCE_CRITERIA:
- compiler performs no keyword/phrase interpretation of English;
- missing/ambiguous interpretation fails narrow;
- missing authority is represented explicitly;
- resolved inputs compile immediately without another workflow engine;
- authority and parallel-work protections remain unchanged;
- audit packets begin genuinely read-only with no expected write set;
- exact synchronized-head PR gate green;
- final Challenge finds no material authority widening or duplicated owner.

TARGETED_VERIFICATION:
Focused intent/compiler/audit-scope tests + repository Required PR Gate.

DURABLE_UPDATES_IF_NEEDED:
ADR 0025 + this compact acceptance record + PR body only.
```

## 3. Minimal implementation

### `scripts/programstart_intent_compile.py`

Owns deterministic compilation of typed semantics into a sealed Work Packet projection.

It consumes:

- `IntentInterpretation`;
- `AuthoritySnapshot`.

It does **not** interpret natural language, discover project authority, grant admission, lock resources, schedule work, persist state, or execute effects.

`compile_interpreted_work_packet()` is the semantic compiler boundary. The older `compile_work_packet()` shape remains only as a developer convenience wrapper for explicitly supplied interpretation fields.

Audit compilation is inspect-first: an `AUDIT` packet exposes declared project mutation surfaces as read-only for that initial packet and therefore has no expected write set. If findings justify already-authorized implementation, derive/recompile a bounded implementation packet rather than silently converting the audit packet into a writer.

### `scripts/programstart_intent_ingress.py`

A deliberately stateless adapter with three possible results:

`needs_interpretation -> needs_authority -> compiled`

These are return states, not persisted lifecycle states.

The adapter:

- preserves raw intent;
- rejects an interpretation that describes different raw intent;
- refuses compilation while semantic ambiguity remains;
- exposes missing authority instead of guessing it;
- immediately invokes the existing compiler once both trusted inputs exist.

It adds no database, queue, background worker, durable state machine, LLM client, authority resolver, Controller, or operator-facing product command.

### Tests

Existing tests continue to cover:

- authority broadening;
- source/prompt injection;
- stale authority;
- tampered packet integrity;
- renderer privilege expansion;
- repository/provider/runtime parallel protection;
- human-gate versus temporary-automation-gap separation;
- write-set collision semantics;
- three real ecosystem pilots.

Ingress tests prove:

- raw request alone returns `needs_interpretation`;
- trusted interpretation without authority returns `needs_authority`;
- resolved inputs compile immediately;
- unresolved semantic ambiguity never falls through to compilation;
- English phrases such as `don't interfere` are not lexically parsed by the compiler;
- trusted explicit constraints are preserved without expanding authority;
- interpretation/raw-request mismatch is rejected.

Audit-scope regression tests additionally prove:

- an uncontested audit of a generally writable project has no mutable surface or expected write set;
- the same project authority remains writable when compiled as an explicitly bounded execution packet.

## 4. Real pilot semantics retained

### Resume Creator continuation

Short intent resolves to the existing Resume Creator authority. Shared autonomy infrastructure remains protected/read-only; existing product acceptance and Challenge requirements remain inherited.

### Watchtower audit

Audit begins read-only regardless of general project write authority. Active parallel Watchtower mutation ownership is retained as conflict/currentness evidence rather than creating another execution lane. Any later implementation requires a separately reconciled/recompiled bounded packet.

### Durable backend autonomy

Architecture intent resolves to the incumbent Autonomous Controller responsibility rather than reviving Orchestra or inventing a second orchestrator.

## 5. Critical trust boundaries

### Semantic interpretation producer

The compiler cannot know whether an upstream interpretation correctly captured objective, explicit constraints, or ambiguity. V0.1 therefore treats interpretation as a typed trusted input and fails narrow when it is unknown/incomplete.

Do not invent a production interpreter/provenance protocol until a real consumer is selected. The eventual integration should identify the interpretation producer/version and preserve operator-visible provenance.

### Authority/currentness resolver

`AuthoritySnapshot` is an input contract, not authority itself. A bad resolver can still supply incorrect project/provider/runtime permissions. Production integration must bind snapshot fields to owning-project/current evidence.

### Controller admission

A valid compiled packet is not permission to execute. Controller still owns currentness revalidation, semantic admission, leases/fencing, sequencing, retry/resume, and human-gate handling.

## 6. Post-implementation Challenge findings

The implementation changed materially because Challenge findings were treated as work, not commentary.

1. **Repository-centric parallel protection** — replaced separate surface collections with typed repository/runtime/provider/authority surfaces.
2. **Contradictory authority snapshots** — overlapping mutable/read-only declarations now fail validation.
3. **Public commit SHAs tripped secret scanning** — fixtures use short public refs; production resolution still requires exact immutable evidence.
4. **Connector-created candidates reached CI with deterministic formatting debt** — branch debt was corrected; merged PR #95 owns the systemic publication-gate improvement.
5. **Mode terminology was overloaded** — rejected Mode D; ADR 0025 defines orthogonal Intent Ingress.
6. **Polished CLI exposure was premature** — standalone compiler remains a developer harness until authority resolution is real.
7. **Keyword intent classification was a semantic shortcut** — removed from the deterministic compiler. Raw English without trusted semantic kind fails narrow.
8. **Lexical explicit-constraint extraction had the same flaw** — removed. Explicit constraints must be supplied by the trusted interpretation layer.
9. **A persistent ingress state machine would duplicate orchestration** — rejected. V0.1 uses only stateless result states.
10. **The experiment record itself had become too large** — compressed to this bounded implementation/acceptance record rather than allowing subordinate documentation to become another specification.
11. **Inspect-first audit posture still advertised a write set** — fixed. Initial audit packets now force mutable project surfaces read-only while preserving relevant parallel-work evidence; a focused regression proves bounded execution remains writable.

No remaining V0.1 Challenge finding requires wider authority, a new service, a new schema family, or cross-repository mutation.

## 7. What remains intentionally unbuilt

Only real integration evidence should justify these next steps:

1. **Semantic interpretation producer contract** — choose the actual LLM/operator interpretation surface and its provenance/version shape.
2. **Authority/currentness resolver** — produce `AuthoritySnapshot` from current owning-project authority, admitted work, parallel ownership and accepted evidence.
3. **Controller admission pilot** — consume the sealed packet without reimplementing PROGRAMSTART semantics.
4. **Operator product surface** — expose ordinary-language ingress only when the first three steps can work without hand-authored authority JSON.
5. **Additional renderers** — add only for real consumers.

Do not add these merely to make the architecture look complete.

## 8. Acceptance / closure

Current acceptance checklist:

- [x] canonical Work Packet ownership preserved;
- [x] Intent Ingress separated from project-entry mode;
- [x] deterministic compiler separated from natural-language understanding;
- [x] lexical kind/constraint parsing removed;
- [x] stateless ingress scaffold implemented;
- [x] parallel surface/conflict semantics retained;
- [x] human-gate/automation-gap distinction retained;
- [x] focused ingress/adversarial tests added;
- [x] inspect-first audit packet has empty expected write set;
- [x] bounded execution remains writable under the same authority;
- [x] no new service/database/queue/orchestrator/operator CLI added;
- [x] current ADR reconciled;
- [x] subordinate experiment documentation compressed;
- [x] synchronized head `858b50c062100a315113999eb1c69bce29b339ea` passed Required PR Gate run #116 against current main;
- [x] final behavioral patch Challenge clear for the V0.1 repository scaffold;
- [x] PR #94 merged as `89d36a396532b0afc678f5b9d0994652f1ce6f2e`; owning-state reconciliation recorded here.

## 9. Learning disposition

The reusable PROGRAMSTART lesson is narrower than “build an intent compiler”:

> Use natural-language Intent Ingress to obtain typed semantic intent and current authority, then hand deterministic Work Packet semantics into the existing project mode and Controller. Keep missing inputs explicit, keep the ingress stateless, make inspect-first intents truly non-writing, and add product/runtime machinery only when a real integration requires it.

High strategic value earns attention, not execution authority. More automation must reduce operator boilerplate without creating a second methodology or hiding trust boundaries.
