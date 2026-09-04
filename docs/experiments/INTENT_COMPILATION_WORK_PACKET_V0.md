# Intent Compilation Into PROGRAMSTART Work Packets — V0.1

Status: **bounded implementation candidate**

Owner: **PROGRAMSTART Work Packet / prompt-rendering semantics**

Canonical authority: **unchanged**. `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` remains authoritative for reusable Work Packet semantics. This file is subordinate design and acceptance evidence. It is not a new methodology, execution spine, roadmap, Controller, Evidence Spine, or operator state machine.

## 1. Decision

The originating hypothesis is **accepted only after narrowing**.

Do not create a second canonical `WorkSpecification` ontology. PROGRAMSTART already has the correct semantic execution object: the **Work Packet**, defined as a logical execution contract derived from current authority and never canonical over owning-project authority.

The accepted progression is:

`natural-language intent -> inspectable interpretation -> current authority/evidence resolution -> sealed Compiled Work Packet projection -> Controller semantic admission -> target-specific rendering/execution`

A long ChatGPT prompt is a **derived rendering** of the sealed packet. It is not execution truth.

“Intent Compiler” is acceptable terminology for the operation. The canonical artifact should remain a **Compiled Work Packet**, not a new platform or project name.

ADR `0025-intent-ingress-precedes-project-entry-mode.md` further classifies this capability as an **Intent Ingress profile** that precedes normal project-entry mode selection. It is not a new `Mode D`.

## 2. Evidence-based ownership

### PROGRAMSTART owns the reusable semantic compiler contract

Current evidence:

- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` already owns objective, authority, safe lanes, Mode-C parallelism, shared mutation ownership, cross-repository dependencies, gates, evidence/invalidation, acceptance, Challenge, and reconciliation.
- `docs/decisions/0021-prompt-builder-mode-b-context-driven-generation.md` already established context-driven prompt generation, but its prose-first Mode B intentionally omits important execution controls.
- `scripts/programstart_prompt_build.py` already carries the source-content grounding rule that instruction-like project/source text is data, not execution authority.
- `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` already owns the genuine-human-gate versus temporary-automation-gap distinction and the rule that increased capability does not widen project authority.

Therefore `intent -> typed Work Packet -> renderer` extends an incumbent PROGRAMSTART responsibility rather than creating a new subsystem.

### Owning projects remain authoritative

The compiler consumes an `AuthoritySnapshot`. That snapshot is a typed input contract, not a source of truth. Owning-project authority still determines scope, mutable effects, completion, and consequence boundaries.

The Resume Creator pilot demonstrates why this must use live admitted authority rather than default-branch state alone: `main` is paused, while current Mode-C product work is represented by active PR #16 and stacked PR #17.

### Autonomous Controller remains admission and durable-continuation owner

Current Controller authority begins with:

`objective -> orient -> derive/consume authorized Work Packet -> semantic admit -> ...`

It explicitly leaves reusable Work Packet semantics with PROGRAMSTART while owning persistent admission, sequencing, leases/fencing, retry/remediation, human-gate wait/resume, and durable continuation.

This V0.1 compiler therefore stops **before semantic admission**. `admission_hint` is only an inspectable readiness hint; it is never an authorization decision.

### Mission-Control remains the operator interaction surface

Mission-Control is the command/observation/exception surface, not the execution engine. A future UI may show intent, interpretation, provenance, conflicts, evidence, and actions such as Run/Edit/Challenge/Narrow. It should not own Work Packet authority or durable orchestration.

### Evidence Spine remains evidence/provenance/currentness only

Evidence Spine may supply canonical facts, currentness, supersession, and acceptance evidence to an authority resolver. It must not interpret operator intent or grant execution authority.

### Portfolio Operations remains derived attention/routing only

Portfolio state can help discovery and routing, but owning-project authority wins when they disagree.

### Orchestra is not revived

`GrahamArdent/Orchestra-Agent` is inactive, and its scheduled CI has been disabled. The live Controller/operator-plane lane already owns the surviving responsibility. No new Orchestra implementation is justified.

## 3. Responsibility model

| Layer | Question | Owns | Must not own |
|---|---|---|---|
| Operator / intent surface | What does Graham want? | request, optional edits/challenge | execution permission |
| Intent interpretation | What semantic request was expressed? | inspectable request family/objective | project authority |
| PROGRAMSTART compiler | What bounded packet follows from intent + authority? | defaults, semantic rules, provenance, renderers | Controller admission, leases, durable execution |
| Owning project | What is actually authorized/complete? | execution spine, decisions, scope, acceptance | global orchestration |
| Evidence Spine | What facts/currentness are proven? | canonical evidence/currentness | intent meaning or execution authority |
| Autonomous Controller | May this packet run now and what happens next? | admission, durable sequencing, leases, recovery, gate resume | reusable methodology |
| Workers/Compute | How is one admitted attempt executed? | concrete attempt/effect | Work Packet continuation decisions |
| Mission-Control/operator plane | What should the human understand/decide? | explanation, awareness, genuine decisions | execution engine or project authority |

## 4. Canonical V0.1 model

Implementation: `scripts/programstart_intent_compile.py`.

### `SurfaceRef`

One typed representation is used for every possible effect surface:

- `repository`;
- `runtime`;
- `provider`;
- `authority`.

A surface has an identifier and an optional `consequential` marker.

This replaces the first implementation's separate repository/runtime/provider collections. The unified representation is smaller and, importantly, lets the same parallel-write protection apply to provider and runtime surfaces instead of only repositories.

### `AuthoritySnapshot`

The smallest currentness/authority input needed by the compiler contains:

- project name and owning repository;
- project authority commit/reference and authority paths;
- PROGRAMSTART methodology commit/reference and execution mode;
- current work references;
- mutable and read-only typed surfaces;
- allowed/prohibited effects;
- genuine human-gate conditions;
- temporary automation-gap conditions;
- evidence requirements;
- acceptance conditions;
- Challenge requirement;
- invalidation and stop conditions;
- active parallel-work protected typed surfaces.

The snapshot rejects any surface that is simultaneously declared mutable and read-only.

Production authority resolution should use exact immutable references. Test fixtures use shortened public commit references to avoid the repository secret scanner classifying full SHA strings in JSON fixtures as high-entropy secrets.

### `IntentInterpretation`

Contains:

- raw request;
- normalized request;
- semantic intent family;
- interpreted objective;
- untrusted project hint;
- explicit narrowing/non-interference constraints;
- unresolved material ambiguity.

The deterministic V0.1 interpreter selects only a small transformation family. It never derives permissions, spend, destructive consequences, or project ownership from wording. Unknown intent fails narrow.

### `CompiledWorkPacket`

Contains:

- schema/compiler versions;
- deterministic intent and specification IDs;
- SHA-256 semantic integrity digest;
- interpreted intent;
- resolved project owner and execution mode;
- exact authority snapshot supplied to compilation;
- bounded typed surface access and effects;
- human gates versus temporary automation gaps;
- parallel-work conflicts and typed expected write set;
- evidence/currentness binding;
- acceptance, Challenge, invalidation, and stop conditions;
- operator interaction policy;
- applied transformation-rule IDs;
- field-level provenance;
- non-authoritative admission hint.

### Deliberately omitted from semantic identity

A generation timestamp is not part of the canonical semantic object. Identical intent + identical authority + identical compiler rules should produce the same semantic packet. Currentness is instead bound to authority references/fingerprint and invalidation triggers. Operational systems may record receipt/compile time outside the semantic digest.

## 5. Explicit versus inferred field model

| Meaning | Origin | Rule |
|---|---|---|
| raw intent | `explicit_user` | never rewritten away |
| explicit non-interference | `explicit_user` | narrows scope only |
| intent family/objective | `interpreted_intent` | inspectable; unknown fails narrow |
| owning project/repository | `project_authority` | project hint cannot override it |
| mutable/effect boundaries | `project_authority` | never inferred from broad wording |
| execution mode | `methodology_default` + resolved authority | current rule, not historical hard-code |
| genuine human gates | current project/consequence policy | renderer cannot add/remove them silently |
| temporary automation gaps | `evidence_inference` | remain distinct from human judgment |
| parallel protection/conflicts | `evidence_inference` | current active-lane evidence |
| Challenge requirement | current methodology/project risk posture | inherited automatically |
| recommendations | `recommendation` | non-authoritative until reconciled |
| material ambiguity | `unresolved` | exposed; mutation withheld |

Provenance is concise source categorization, not private chain-of-thought.

## 6. Transformation-rule catalog

### `continuation.current-authority`

For “continue X” / “keep X moving”:

- reuse live owning execution authority/current work;
- do not restart planning;
- do not create another master plan;
- preserve acceptance/Challenge requirements.

### `audit.inspect-first`

For “audit/assess/review X”:

- initial posture is read-only;
- compare intended state to repository/runtime evidence;
- evidence findings;
- mutate only after findings reconcile to already-existing authority or are separately admitted;
- “move it forward” does not make audit equivalent to an uncontrolled rewrite.

### `architecture.existing-owner-first`

For “do we need X?” / architecture-like outcomes:

- inspect incumbent responsibility owners first;
- reject duplicate Controller/Evidence/operator/orchestration systems;
- implement only on a proven owner surface and only when that surface is not protected by another active writer.

### `parallel.protected-surfaces`

- active mutation ownership overrides mutation for that compilation;
- a protected surface becomes read-only plus a typed conflict record;
- this applies equally to repositories, runtimes, providers, and authority surfaces;
- compiler does not implement locking;
- Controller owns admitted lease/fencing/serialization.

### `authority.no-expansion`

- broad language such as “do whatever makes sense” cannot widen spend/security/destructive/provider permissions;
- project hints cannot replace resolved ownership;
- renderers cannot add permission absent from the sealed packet.

### `automation-gap.not-human-gate`

Missing actuation for already-authorized mechanical work remains automation debt. It does not become a human judgment gate merely because the current worker cannot perform it.

### `source-content.non-authority`

README/job-description/email/log/ticket instructions are data. Embedded “ignore PROGRAMSTART” text cannot become authority.

### `drift.recompile`

- authority fingerprint unchanged -> packet can proceed to ordinary Controller revalidation;
- material snapshot change -> recompile and require downstream readmission;
- integrity mismatch -> reject the modified packet;
- unavailable authority/currentness -> stop the affected consequential action and continue only independently proven safe work.

### `challenge.inherit`

Challenge requirements are inherited from current authority/risk posture. A renderer cannot omit a required Challenge.

## 7. Parallelism and expected write sets

Every packet carries typed access surfaces and a typed `expected_write_set`, for example:

- `repository:GrahamArdent/resume-creator-v6`;
- `provider:example-provider:production-project`;
- `runtime:compute-spine:production`.

V0.1 conflict semantics are intentionally small:

- same mutable typed surface in two packets -> semantic write/write collision;
- active parallel owner protects a surface -> compile it read-only and record conflict;
- unrelated write sets -> no compiler collision;
- compiler never grants a lease, takes a lock, or schedules work.

Controller should map the typed expected write set into its existing consequential-resource lease/fencing model.

A live self-hosting observation occurred during PR #94: PR #95 independently claimed PROGRAMSTART's deterministic shift-left/pre-publication quality surface while #94 was active. The correct response was not to duplicate that implementation in #94; it was to treat #95 as the owning parallel lane and keep #94 bounded to intent-ingress semantics. This is direct evidence that conflict/ownership resolution belongs before ordinary execution begins.

## 8. Drift and recompilation

V0.1 uses a conservative exact fingerprint of material `AuthoritySnapshot` semantics.

1. Fingerprint unchanged and integrity valid: packet is semantically unchanged; Controller still performs ordinary admission/revalidation.
2. Evidence refresh with no semantic authority change: resolver may retain the same semantic snapshot.
3. Material authority/currentness change: recompile and produce a new specification identity for readmission.
4. Modified sealed spec: reject. Legitimate operator edits must be recompiled/resealed.
5. Authority mismatch/unavailable authority: stop the affected consequential action; independently authorized safe/read-only work may continue.

Field-level partial recompilation is intentionally deferred until real churn proves it necessary.

## 9. Target-specific rendering

V0.1 implements one justified renderer: `render_chatgpt_prompt(packet)`.

It carries only conversational-worker-relevant semantics:

- mission;
- authority/currentness references;
- source-data grounding;
- transformation rules;
- mutable/read-only typed surfaces;
- allowed/prohibited effects;
- parallel conflicts;
- human gates versus automation gaps;
- evidence/acceptance;
- Challenge;
- invalidation/stop conditions;
- explicit admission disclaimer.

The prompt includes the sealed Work Packet ID/digest and states that it grants no authority.

No Controller wire envelope is implemented here because the active Controller lane owns that API/versioning contract.

The standalone compiler CLI remains a developer/contract harness in V0.1. Do not promote it to a polished operator command until a trusted authority/currentness resolver can provide `AuthoritySnapshot` automatically. Requiring the operator to hand-author that snapshot would merely move prompt boilerplate into JSON boilerplate.

## 10. Real pilots

### A — Resume Creator parallel-safe continuation

Input:

`Continue Resume Creator, but don't interfere with the infrastructure work happening in parallel.`

Expected:

- owner remains Resume Creator V6;
- only Resume Creator is writable;
- shared autonomy infrastructure is read-only/protected;
- application submission, new spend, and destructive security/provider consequences remain genuine gates;
- exact-head CI, realistic product acceptance, and Challenge remain completion requirements.

### B — Watchtower audit with live collision

Input:

`Watchtower seems behind. Audit how it's being used and move it forward.`

The fixture binds Watchtower V0.2 authority and declares the parallel Watchtower lane as active mutation owner.

Expected:

- resolve as audit;
- start read-only;
- compile Watchtower repository mutation to read-only because of active ownership;
- record a parallel write-ownership conflict;
- do not create a lock manager or competing Watchtower roadmap.

### C — Durable backend continuation architecture

Input:

`I think ChatGPT shouldn't have to stay open for autonomous work. Make the system keep working in the backend.`

Expected:

- resolve as architecture evaluation;
- incumbent owner is existing Autonomous Controller, not Orchestra or a new orchestrator;
- Controller/Mission-Control/Evidence/Compute surfaces remain protected by the active parallel lane;
- output is bounded analysis/integration handoff, not competing implementation.

## 11. Post-implementation Challenge

The first implementation and first CI run produced useful findings instead of being treated as closure.

### Finding C1 — parallel protection was repository-centric

The initial model had separate repository/runtime/provider collections and only fully applied active parallel-write protection to repositories. A protected runtime/provider surface could therefore have been represented too permissively.

**Remediation:** replace those separate collections with typed `SurfaceRef` objects for repository/runtime/provider/authority. The same protection algorithm now applies to every surface type. Add an adversarial provider-surface test proving a provider declared mutable by project authority but protected by active parallel work compiles read-only and is removed from the expected write set.

### Finding C2 — contradictory authority snapshot could hide resolver defects

The initial snapshot did not reject the same surface appearing both mutable and read-only.

**Remediation:** `AuthoritySnapshot` now rejects contradictory declarations before compilation. A focused test covers the failure.

### Finding C3 — real commit SHAs triggered repository secret scanning

Full public Git commit SHAs embedded in JSON fixtures were flagged as high-entropy strings by `detect-secrets`.

**Remediation:** fixtures use short public refs while the design record retains the exact inspected commits. Production resolution remains responsible for exact immutable authority references.

### Finding C4 — formatting gate stopped before behavior tests

First PR validation failed changed-file hooks for trailing whitespace, line length/formatting, and the fixture SHA false positives. Pyright itself passed.

**Remediation:** code/tests were normalized with the repository's exact Ruff toolchain and the temporary branch-only formatter workflow was removed immediately afterward. No permanent CI-side source auto-commit mechanism remains. The systemic connector/pre-publication quality gap is owned separately by PR #95 and is not duplicated here.

### Finding C5 — mode terminology was overloaded

Project-entry Mode C and Prompt Builder's Mode A/Mode B describe different axes. Adding an `Intent Compiler Mode D` would make the API harder to reason about and would incorrectly imply a new project lifecycle.

**Remediation:** ADR 0025 defines **Intent Ingress** as an orthogonal pre-entry profile. It resolves or consumes current authority first and then hands work into the existing project-entry/execution mode.

### Finding C6 — polished CLI exposure would be premature

The unified `programstart` CLI could technically add an `intent-compile` subcommand now, but V0.1 still requires a resolved authority snapshot.

**Remediation:** keep the standalone module CLI as a developer/contract harness. The operator-facing command/API should be added only when authority/currentness resolution can make ordinary-language ingress real instead of requiring hand-authored authority JSON.

### Remaining trust-boundary finding

`AuthoritySnapshot` resolution is the most consequential upstream trust boundary. If a resolver incorrectly declares a provider/runtime mutation authorized, the compiler must not independently manufacture a correction. Production integration should version/validate the resolver contract and bind its fields to owning-project/current evidence. This V0.1 intentionally does not build a second discovery/resolution service inside PROGRAMSTART.

## 12. Controller integration handoff

The active Controller/operator lane should consume, not reimplement, these semantics:

1. accept a sealed packet or lossless mapping;
2. verify schema/compiler version, integrity digest, and authority fingerprint;
3. re-resolve/revalidate current project + PROGRAMSTART authority before consequential admission;
4. reject digest/version mismatch;
5. map typed `expected_write_set` into existing Controller lease/fencing semantics;
6. use compiler conflicts as admission evidence, not as another lock primitive;
7. preserve human-gate versus automation-gap classification;
8. require recompile/readmission on material authority drift;
9. expose provenance without private reasoning;
10. never treat `admission_hint` as an admission decision.

The active Controller lane owns the exact API/model adaptation. This PROGRAMSTART branch does not mutate Controller code.

## 13. Operator-plane handoff

A future Mission-Control/operator surface can show:

- original request;
- interpreted objective/intent family;
- resolved project owner;
- methodology/project authority refs;
- mutable/read-only surfaces;
- human gates and automation gaps;
- parallel conflicts;
- evidence/acceptance/Challenge;
- provenance;
- unresolved ambiguity;
- Run / Edit / Challenge / Narrow Scope / Inspect Evidence.

Editing creates a newly compiled/sealed packet. Low-risk unambiguous packets do not require mandatory review when current policy permits autonomous admission.

## 14. Evidence Spine handoff

Evidence Spine may eventually provide:

- canonical authority/currentness evidence references;
- invalidation/supersession signals;
- exact evidence IDs bound to acceptance requirements.

It must not become project authority, intent interpreter, or Controller admission service.

## 15. Success metrics

A measured rollout should track:

- manual prompt-boilerplate reduction;
- required PROGRAMSTART semantic-constraint coverage;
- unsupported authority added: target **zero**;
- genuine-human-gate versus automation-gap errors;
- typed write-surface collision detection;
- renderer semantic-boundary regressions;
- unnecessary clarification rate;
- operator edits before admission;
- semantic object size versus rendered prompt size;
- reproducibility from the same intent + authority state;
- stale-authority packets rejected before consequential execution.

Prompt brevity alone is not a success metric.

## 16. Live implementation checklist

- [x] current ownership determined;
- [x] historical/manual prompt pattern inspected;
- [x] responsibility boundary proven;
- [x] canonical representation narrowed to a Compiled Work Packet projection;
- [x] explicit vs inferred provenance model implemented;
- [x] current-methodology/project inheritance represented through authority snapshot + rule catalog;
- [x] typed parallel-work/write-surface representation implemented;
- [x] ChatGPT renderer implemented as a derived artifact;
- [x] three real short-intent -> structured fixtures added;
- [x] Work Packet -> long-form prompt rendering tested;
- [x] semantic integrity boundary tested;
- [x] adversarial cases encoded;
- [x] Controller integration point defined without Controller mutation;
- [x] operator-plane integration point defined without Mission-Control mutation;
- [x] Evidence Spine currentness role defined without overloading it;
- [x] stale-authority/recompile policy defined;
- [x] real-world pilot fixtures use current Resume Creator, Watchtower, and Controller evidence;
- [x] Intent Ingress vs project-entry mode distinction proven and documented;
- [x] PR #95 parallel ownership detected and respected rather than duplicated;
- [ ] exact-head CI green after Challenge remediations;
- [ ] post-implementation Challenge clear after final CI/patch review;
- [ ] owning PR/checklist reconciled after final Challenge;
- [x] reusable learning disposition defined.

## 17. Learning disposition

### PROGRAMSTART

- Existing Work Packet semantics are the right canonical contract; do not create a parallel Work Specification system.
- Intent Ingress is an orthogonal pre-entry profile, not Mode D.
- Prompt Builder Mode B is useful evidence, but prose-first rendering should become a renderer over structured semantics where practical.
- Repeated prompt clauses map to reusable semantic rules: continuation/current-authority, audit/inspect-first, parallel protected surfaces, no authority expansion, human-gate/automation-gap distinction, source-data non-authority, drift/recompile, and Challenge inheritance.
- Mutation surfaces should be typed uniformly across repository/runtime/provider/authority domains.
- Do not expose a polished operator command before authority/currentness resolution can supply its inputs automatically.
- Connector-only mutation can lack a candidate workspace for deterministic pre-publication formatting; that systemic quality concern belongs to PR #95 rather than this compiler lane.

### Autonomous Controller

- consume compiled write sets/conflicts as admission/lease inputs;
- verify integrity/currentness before execution;
- do not duplicate interpretation/default rules already owned by PROGRAMSTART.

### Mission-Control/operator plane

- expose interpretation/provenance/edit/challenge affordances;
- do not require review for every low-risk packet;
- edits produce a new sealed packet.

### Evidence Spine

- supply canonical currentness/invalidation evidence when integration is earned;
- do not accept/authorize work on behalf of owning projects.

### Portfolio Operations

- discovery/attention hints may assist authority resolution;
- owning-project authority always wins;
- captured conversation intent is not execution authority by itself.

## 18. Remaining gaps

1. **AuthoritySnapshot resolver integration:** V0.1 requires an already-resolved snapshot. The active Controller/operator/Evidence lane should determine the least-duplicative producer.
2. **Field-level drift optimization:** any material snapshot fingerprint change currently forces recompile. More selective reconciliation should wait for real evidence of costly churn.
3. **Additional renderers:** Codex/worker/API/GitHub-issue renderers are deferred until a real consumer contract exists.
4. **Prompt Builder self-adoption:** after the PR is green/Challenge-clear, PROGRAMSTART can decide whether existing `prompt-build --mode context` should route through structured compilation or remain a legacy/simple renderer. Do not conflate this renderer-local mode with project-entry modes.
5. **Operator-facing intent command/API:** defer until authority/currentness resolution can eliminate hand-authored `AuthoritySnapshot` input.
6. **Measured Controller admission pilot:** semantic compilation is proven here; end-to-end Controller admission belongs to the active Controller lane after it accepts the handoff.

## 19. V0.1 success statement

If exact-head CI and final Challenge clear, this bounded implementation proves:

> A short natural-language request plus a current resolved authority snapshot can be deterministically transformed into an inspectable sealed PROGRAMSTART Work Packet projection that preserves operator intent, adds no new execution authority, inherits current methodology/project constraints, represents typed parallel-write ownership, distinguishes human gates from automation gaps, detects stale/tampered semantics, and renders a conversational worker prompt as a derived artifact.

It does **not** claim arbitrary natural language alone can discover truth or authority. Authority resolution remains an explicit upstream trust boundary, and semantic admission remains a Controller responsibility.
