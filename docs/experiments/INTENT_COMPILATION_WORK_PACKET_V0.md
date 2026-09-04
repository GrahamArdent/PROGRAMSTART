# Intent Compilation Into PROGRAMSTART Work Packets — V0.1

Status: **bounded implementation candidate**  
Owner: **PROGRAMSTART Work Packet / prompt-rendering semantics**  
Canonical authority: **unchanged** — `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` remains authoritative for reusable Work Packet semantics.  
This document is subordinate design/acceptance evidence. It is not a new methodology, execution spine, project roadmap, Controller, Evidence Spine, or operator state machine.

## 1. Decision

The original hypothesis is **partly accepted and materially narrowed**.

Natural-language intent should not compile into a second canonical `WorkSpecification` ontology. PROGRAMSTART already has the correct semantic execution object: the **Work Packet**, explicitly defined as a logical execution contract derived from current authority and never canonical over owning-project authority.

The accepted progression is therefore:

`natural-language intent -> inspectable interpretation -> current authority/evidence resolution -> sealed Compiled Work Packet projection -> Controller semantic admission -> target-specific renderer/executor`

A long ChatGPT prompt is a **derived rendering** of that sealed packet. It is not execution truth.

The user-facing capability may reasonably be called **Intent Compiler** because it describes the operation. The canonical artifact should be called **Compiled Work Packet**, not `PROGRAMSTART Compiler`, `Work Specification Generator`, or another new platform name.

## 2. Evidence-based ownership decision

### PROGRAMSTART owns the semantic compiler contract

Current evidence:

- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` already defines the logical execution contract and includes objective, authority, blockers/safe lanes, Mode-C parallelism, shared mutation ownership, cross-repository dependencies, operator gates, evidence/invalidation, acceptance, Challenge, and reconciliation.
- `docs/decisions/0021-prompt-builder-mode-b-context-driven-generation.md` already established a context-driven prompt-generation precursor. Its admitted limitation is that Mode B directly renders prose and intentionally omits important execution controls such as sync rules, kill criteria, and stage gating.
- `scripts/programstart_prompt_build.py` already contains the reusable source-content grounding rule needed to prevent instruction-like project/source text from becoming execution authority.
- `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` already owns the distinction between genuine human gates and temporary automation gaps, and the rule that capability growth may increase execution of existing permission but may not increase project authority.

Conclusion: evolving PROGRAMSTART from `context -> prompt` toward `intent -> typed Work Packet -> renderer` is an extension of an incumbent responsibility, not a new subsystem.

### Owning projects remain authoritative

The compiler consumes an exact `AuthoritySnapshot`. The snapshot is a typed input contract, not a new source of truth. Owning-project authority still determines scope, mutable effects, completion, and consequence boundaries.

The Resume Creator pilot proves why this matters: default-branch `main` is paused, while the current admitted Mode-C work is represented by open PR #16 and stacked PR #17. A compiler that treated default-branch state as sufficient authority would be wrong.

### Autonomous Controller remains the admission and durable-continuation owner

Current Controller authority states the target loop as:

`objective -> orient -> derive/consume authorized Work Packet -> semantic admit -> ...`

and explicitly assigns reusable Work Packet semantics to PROGRAMSTART while assigning persistent semantic admission, sequencing, leases/fencing, retry/remediation, human-gate wait/resume, and durable continuation to Controller.

Therefore this V0.1 compiler stops **before semantic admission**. `admission_hint` is only an operator-facing readiness hint; it is never an authorization decision.

### Mission-Control remains the operator interaction surface

Mission-Control is the command/observation/exception surface, not an execution engine. The latest Controller lane has also retained Mission-Control as the operator interaction plane while absorbing durable decision state into Controller.

A future operator UI may show the interpreted packet, provenance, conflicts, evidence, and actions such as Run/Edit/Challenge/Narrow. That UI should not own Work Packet authority or durable orchestration.

### Evidence Spine remains evidence/provenance/currentness only

Evidence Spine canonically captures facts and scoped acceptances while explicitly refusing to grant unrelated execution authority. It is a natural future source for authority/currentness evidence and invalidation signals used by the snapshot resolver, but it does not interpret user intent or admit work.

### Portfolio Operations remains derived attention/routing only

Portfolio Operations may help resolve plausible project ownership or active attention, but it is explicitly stale when it disagrees with an owning project. It must not become the compiler's execution authority.

### Orchestra is not revived

`GrahamArdent/Orchestra-Agent` is inactive and its scheduled CI has been disabled since 2026-08-22. The live Controller/operator-plane lane has already dispositioned the remaining useful orchestration/interaction concepts. No new Orchestra implementation is justified.

## 3. Responsibility model

| Layer | Question it answers | Owns | Must not own |
|---|---|---|---|
| Operator / intent surface | What does Graham want? | natural-language request, optional edits/challenge | execution permission |
| Intent interpretation | What semantic request family/objective was expressed? | explicit inspectable interpretation | project authority |
| PROGRAMSTART intent compiler | What bounded Work Packet follows from intent + current authority? | reusable transformation/default rules, provenance, prompt rendering | Controller admission, leases, durable execution |
| Owning project | What is actually authorized and complete? | execution spine, decisions, scope, acceptance | global orchestration |
| Evidence Spine | What facts/currentness/provenance are proven? | canonical evidence and scoped acceptance facts | intent meaning or execution authority |
| Autonomous Controller | May this compiled packet run now, and what happens next? | semantic admission, durable sequencing, leases, recovery, gate wait/resume | reusable methodology, worker fabric |
| Compute/worker layer | How is an admitted bounded attempt executed? | concrete attempts/effect identity/runtime execution | Work Packet continuation decisions |
| Mission-Control/operator plane | What should the human understand or decide? | explanation, awareness, genuine human decision return | execution engine or project authority |

## 4. Canonical V0.1 model

Implementation: `scripts/programstart_intent_compile.py`.

### `AuthoritySnapshot`

The smallest currentness/authority input needed to compile without making the compiler a discovery engine:

- project name and owning repository;
- exact project authority commit and authority paths;
- exact PROGRAMSTART methodology commit and execution mode;
- current work references;
- mutable/read-only repositories;
- explicitly authorized runtime/provider mutation surfaces, when any;
- allowed/prohibited effects;
- genuine human-gate conditions;
- temporary automation-gap conditions;
- evidence requirements;
- acceptance conditions;
- Challenge requirement;
- invalidation and stop conditions;
- active parallel-work protected surfaces.

The resolver that produces this object must prefer current owning authority/current admitted work over stale summaries. This V0.1 does not create a second repository-discovery service.

### `IntentInterpretation`

Contains:

- raw request;
- normalized request;
- semantic intent family;
- interpreted objective;
- untrusted project hint if supplied;
- explicit narrowing/non-interference constraints;
- unresolved material ambiguity.

The deterministic V0.1 interpreter only selects a small transformation family. It never derives permissions, spend, destructive consequences, or project ownership from wording. Unknown intent fails narrow.

### `CompiledWorkPacket`

Contains:

- schema/compiler versions;
- deterministic `intent_id`;
- deterministic `specification_id`;
- SHA-256 semantic integrity digest;
- interpreted intent;
- resolved project owner and execution mode;
- exact authority snapshot;
- bounded surface access and effects;
- human gates vs temporary automation gaps;
- parallel-work conflicts and expected write set;
- evidence/currentness binding;
- acceptance, Challenge, invalidation and stop conditions;
- operator interaction policy;
- applied transformation-rule IDs;
- field-level provenance;
- non-authoritative admission hint.

### Deliberately omitted from semantic identity

`generated_timestamp` is not part of the canonical semantic object. A timestamp would make identical intent + identical authority appear different and weaken idempotency. Currentness is instead bound to exact authority commits/fingerprint and invalidation triggers. A UI/event store may record receipt/compile time as operational metadata outside the semantic digest.

## 5. Explicit versus inferred field model

| Field/meaning | Origin | Rule |
|---|---|---|
| raw intent | `explicit_user` | never rewritten away |
| explicit non-interference clause | `explicit_user` | narrows scope only |
| intent family/objective | `interpreted_intent` | inspectable; unknown fails narrow |
| owning project/repository | `project_authority` | project hint cannot override it |
| mutable/effect boundaries | `project_authority` | never inferred from broad wording |
| current execution mode | `methodology_default` + resolved authority | current rule, not historical hard-code |
| genuine human gates | `project_authority` / current consequence policy | no renderer may add/remove them silently |
| temporary automation gaps | `evidence_inference` | remain distinct from human judgment |
| parallel protection/conflicts | `evidence_inference` | current active-lane evidence |
| Challenge requirement | `methodology_default` / project risk posture | inherited automatically |
| recommendations | `recommendation` | non-authoritative until reconciled |
| material ambiguity | `unresolved` | exposed; mutation withheld |

No provenance field exposes private chain-of-thought. It records only inspectable source category and concise reason.

## 6. Transformation-rule catalog

The implementation encodes reusable semantic rules rather than treating a long prompt as the rule source.

### Project continuation — `continuation.current-authority`

Input class: "continue X", "keep X moving".

Derivation:

- reuse current owning execution spine/work packet;
- inspect current admitted work rather than restart planning;
- do not create another roadmap/master plan;
- preserve current acceptance/Challenge rules.

### Audit — `audit.inspect-first`

Input class: "audit/assess/review X".

Derivation:

- initial posture is read-only;
- compare intended authority to actual repository/runtime evidence;
- evidence findings;
- mutate only after a finding reconciles into already-existing authority or an authority-gap process admits it;
- "move it forward" does not turn the first audit step into an uncontrolled rewrite.

### Architecture evaluation — `architecture.existing-owner-first`

Input class: "do we need X?", "make the system keep working in the backend".

Derivation:

- inspect existing responsibility owners first;
- reject duplicate Controller/Evidence/operator/orchestration systems;
- implement only on the proven owner surface and only when that surface is not currently protected by another writer.

### Parallel work — `parallel.protected-surfaces`

- declared active mutation ownership overrides mutation for that compilation;
- protected overlap becomes read-only plus a typed `parallel_write_ownership` conflict;
- compiler detects the semantic conflict but does not implement a distributed lock;
- Controller owns admitted leases/fencing/serialization.

### Authority — `authority.no-expansion`

- "do whatever makes sense" cannot widen spend/security/destructive/provider permissions;
- project hints cannot replace resolved project ownership;
- renderer cannot add permissions absent from the sealed packet.

### Human/automation boundary — `automation-gap.not-human-gate`

- missing actuator for already-authorized mechanical work remains automation debt;
- only genuine judgment/consequence/physical/secret/legal/business boundaries become human gates.

### Source trust — `source-content.non-authority`

- README/job-description/email/log/ticket text is data;
- embedded "ignore PROGRAMSTART" instructions never become authority.

### Drift — `drift.recompile`

- exact authority fingerprint unchanged -> packet may continue to Controller revalidation;
- semantic snapshot changed -> recompile and require downstream readmission before new consequential work;
- packet integrity mismatch -> reject/stop the affected action;
- authority/currentness cannot be established -> stop consequential action and continue only independently proven safe/read-only work.

### Challenge — `challenge.inherit`

- current project/methodology risk posture decides whether Challenge is mandatory;
- renderer cannot omit a required Challenge.

## 7. Parallelism and write-surface representation

Every packet carries typed surfaces and an `expected_write_set`.

V0.1 conflict semantics are intentionally small:

- mutable + mutable same semantic surface -> write/write collision;
- active parallel owner protects a surface -> compile that surface read-only and record conflict;
- unrelated write sets -> no compiler-level collision;
- compiler never grants a lease, takes a lock, or schedules work.

Controller integration should map `expected_write_set` / protected surfaces into its existing consequential-resource lease/fencing semantics rather than introduce another lock service.

## 8. Drift and recompilation policy

V0.1 uses a conservative exact fingerprint of material `AuthoritySnapshot` inputs.

1. **Continue unchanged:** fingerprint unchanged and packet integrity valid. Controller still performs ordinary admission/revalidation.
2. **Evidence refresh with no semantic authority change:** resolver may retain the same semantic snapshot; no new packet identity is required.
3. **Material authority/currentness change:** recompile. The new semantic digest/specification ID must be readmitted by Controller.
4. **Modified compiled spec after sealing:** integrity mismatch; reject rather than silently execute edits. A legitimate operator edit must produce a newly compiled/sealed packet.
5. **Authority mismatch/unavailable authority:** stop the affected consequential action; safe independent read-only work may continue when independently authorized.

A future field-level drift optimizer may distinguish "reconcile one field" from full recompile, but V0.1 deliberately prefers conservative recompile over stale execution.

## 9. Target-specific rendering

V0.1 implements one justified renderer: `render_chatgpt_prompt(packet)`.

It includes only conversational-worker-relevant semantics:

- mission;
- exact authority/currentness references;
- source-data grounding;
- transformation rules;
- mutable/read-only scope;
- allowed/prohibited effects;
- parallel conflicts;
- human gates versus automation gaps;
- evidence/acceptance;
- Challenge;
- invalidation/stop conditions;
- admission disclaimer.

The prompt carries the sealed Work Packet ID/digest and explicitly says it grants no authority.

No Controller-specific wire envelope is implemented here because the Controller lane owns its admission API/versioning. The integration handoff below defines semantics, not a competing Controller contract.

## 10. Real pilots

### A — Resume Creator parallel-safe continuation

Input:

`Continue Resume Creator, but don't interfere with the infrastructure work happening in parallel.`

Current authority evidence used by fixture:

- active Resume Creator PR #17 head `d0ab72d19aab65110e9c48c6b8fb0cd4b26ae729`;
- current owning game plan `docs/PRODUCTION_READINESS_GAMEPLAN_2026-03-24.md` reconciled in PR #16/#17;
- shared autonomy repositories supplied as read-only/protected parallel surfaces.

Expected semantic result:

- owner remains Resume Creator V6;
- Resume Creator is the only writable repository;
- Controller/Evidence/PROGRAMSTART/Compute/Execution Node/Secrets/Watchtower/Portfolio/Mission-Control/Orchestra surfaces are read-only;
- application submission/spend/destructive-security consequences remain genuine gates;
- exact-head CI + realistic product acceptance + Challenge remain completion requirements.

### B — Watchtower audit with live collision

Input:

`Watchtower seems behind. Audit how it's being used and move it forward.`

Current fixture binds Watchtower V0.2 authority at `d86eab90c8985f355f54f10555ecdc59633270bd` and its primary execution spine `docs/WATCHTOWER_V0_2_EXECUTION.md`.

Because a parallel Watchtower live-integration lane is declared as mutation owner, the compiler:

- resolves the request as an audit;
- begins read-only;
- converts Watchtower repository mutation to read-only for this packet;
- records a parallel write-ownership conflict;
- does not build a lock manager or competing Watchtower plan.

### C — Durable backend continuation architecture

Input:

`I think ChatGPT shouldn't have to stay open for autonomous work. Make the system keep working in the backend.`

Current fixture binds the existing Autonomous Controller authority at `7a168cfd1304af5f389fc088ea920d05efff81c2`.

Expected semantic result:

- intent class is architecture evaluation;
- incumbent owner is the existing Controller, not Orchestra or a new orchestrator;
- Controller/Mission-Control/Evidence/Compute surfaces remain protected by their active parallel lane;
- output is a bounded integration/analysis handoff rather than competing implementation.

## 11. Adversarial Challenge

Implemented tests cover:

- source prompt injection;
- ambiguous/broad natural language failing narrow;
- fake project hint losing to resolved authority;
- stale methodology/authority requiring recompile;
- parallel mutation collision becoming read-only/conflict;
- duplicate intent producing identical IDs/spec;
- modified sealed spec failing integrity;
- renderer preserving semantic digest and critical boundaries;
- renderer not adding a mutable repository absent from the spec;
- human spend/security gates surviving broad execution language;
- temporary automation gaps not being relabeled as human gates;
- write/write collision detection without claiming lock ownership.

Challenge finding retained for follow-up integration review:

- **AuthoritySnapshot resolution is the most important trust boundary.** If a resolver incorrectly labels a provider/runtime surface as mutation-authorized, the compiler must not independently guess that correction. Production integration should version/validate the resolver contract and make consequence capability explicit, ideally consuming owning-project/Evidence-Spine currentness and Controller consequence vocabulary. V0.1 intentionally does not build that resolver inside PROGRAMSTART.

## 12. Controller integration handoff

The durable Controller/operator lane should consume, not reimplement, these semantics:

1. accept a sealed compiled packet or a lossless mapping of it;
2. verify `schema_version`, `compiler_version`, integrity digest and exact authority fingerprint;
3. re-resolve/revalidate current project + PROGRAMSTART authority before consequential admission;
4. reject a modified digest/version mismatch;
5. map `expected_write_set` to the Controller's existing semantic consequential-resource lease/fencing layer;
6. use `dependencies.conflicts` as admission evidence, not as a new lock primitive;
7. preserve human-gate vs automation-gap distinction;
8. on material authority drift, require recompile/readmission rather than continue from a stale rendered prompt;
9. store/render Work Packet provenance without private reasoning;
10. never treat `admission_hint` as an admission decision.

The active Controller lane owns the exact API/model adaptation. This PROGRAMSTART branch intentionally does not mutate Controller code.

## 13. Operator-plane integration handoff

A future Mission-Control/operator surface can safely show:

- original request;
- interpreted objective/intent family;
- resolved project owner;
- exact methodology/project authority refs;
- mutable/read-only surfaces;
- human gates and automation gaps;
- parallel conflicts;
- evidence/acceptance/Challenge;
- field provenance;
- unresolved ambiguity;
- Run / Edit / Challenge / Narrow Scope / Inspect Evidence.

Editing must recompile/reseal; the UI must not modify an already-admitted packet in place. Low-risk unambiguous packets do not require mandatory operator review when current policy permits autonomous admission.

## 14. Evidence Spine integration handoff

Evidence Spine may eventually provide:

- canonical authority/currentness evidence references;
- invalidation/supersession events;
- exact evidence IDs bound to required acceptance conditions.

It must not become project authority, intent interpreter, or Controller admission service.

## 15. Success metrics for a future measured rollout

Track at minimum:

- manual prompt-boilerplate reduction;
- required PROGRAMSTART semantic-constraint coverage;
- unsupported authority added (**target: zero**);
- genuine-human-gate versus automation-gap classification errors;
- write-surface collision detection;
- renderer semantic-boundary regressions;
- unnecessary clarification rate;
- operator edits before admission;
- semantic object size versus rendered prompt size;
- reproducibility for same intent + same authority state;
- stale-authority packets rejected before consequential execution.

Prompt brevity alone is not a success metric.

## 16. Live implementation checklist

- [x] current ownership determined;
- [x] historical/manual prompt pattern inspected via current PROGRAMSTART Prompt Builder Mode B plus preserved real work prompts/context;
- [x] responsibility boundary proven against PROGRAMSTART, Controller, Mission-Control, Evidence Spine, Portfolio and inactive Orchestra;
- [x] canonical representation narrowed to a sealed **Compiled Work Packet projection**, not a second Work Specification ontology;
- [x] explicit vs inferred provenance model implemented;
- [x] PROGRAMSTART inheritance/default rules represented through exact authority snapshot + rule catalog;
- [x] parallel-work/write-surface representation implemented;
- [x] ChatGPT prompt renderer implemented as a derived artifact;
- [x] three real short-intent -> structured fixtures added;
- [x] work-spec -> long-form prompt rendering covered by tests;
- [x] semantic integrity/equivalence boundary covered;
- [x] adversarial cases encoded;
- [x] Controller integration point defined without Controller mutation;
- [x] operator-plane integration point defined without Mission-Control mutation;
- [x] Evidence Spine currentness role defined without overloading it;
- [x] stale-authority/recompile policy defined;
- [x] real-world pilot fixtures use current Resume Creator, Watchtower, and Controller evidence;
- [ ] exact-head CI green;
- [ ] post-implementation Challenge clear after CI and patch review;
- [ ] owning authority/PR reconciled after Challenge;
- [x] reusable learning disposition defined below.

## 17. Learning disposition

Reusable findings route to existing owners:

### PROGRAMSTART

- Work Packet semantics are already the right canonical contract; avoid a parallel `WorkSpecification` system.
- Prompt Builder Mode B is useful evidence but its direct-context-to-prose architecture should become a renderer path over structured semantics where practical.
- Frequently repeated long-prompt clauses map to existing reusable rules: continuation/current-authority, audit/inspect-first, parallel protected surfaces, no authority expansion, human-gate/automation-gap distinction, source-data non-authority, drift/recompile, Challenge inheritance.

### Autonomous Controller

- use compiled write sets/conflicts as admission/lease inputs;
- verify spec integrity/currentness before execution;
- do not duplicate interpretation/default rules already owned by PROGRAMSTART.

### Mission-Control/operator plane

- expose interpretation/provenance/edit/challenge affordances;
- do not require review for every low-risk packet;
- edits produce a new sealed packet.

### Evidence Spine

- supply canonical currentness/invalidation evidence when integration is earned;
- do not accept/authorize work on behalf of owning projects.

### Portfolio Operations

- project discovery/attention hints may help a resolver, but owning authority always wins;
- conversation-derived intent is not execution authority merely because it was captured.

## 18. Remaining gaps

1. **AuthoritySnapshot resolver integration:** V0.1 requires an already-resolved exact snapshot. The active Controller/operator/Evidence lane should determine the least-duplicative producer using its current contracts.
2. **Field-level drift optimization:** current implementation deliberately recompiles on any material snapshot fingerprint change. More selective reconciliation should be added only if real churn makes this costly.
3. **Additional worker renderers:** Codex/worker/API/GitHub-issue renderers are not implemented until a real consumer contract exists; semantic packet remains reusable.
4. **Methodology self-adoption:** after this PR proves green/Challenge-clear, PROGRAMSTART may decide whether to connect the existing `prompt-build --mode context` path to structured compilation or preserve backward compatibility as a legacy/simple mode.
5. **Measured live admission:** these pilots prove deterministic semantic compilation; a full Controller admission pilot belongs to the active Controller lane after its API contract accepts this handoff.

## 19. V0.1 success statement

If exact-head CI and Challenge clear, this bounded implementation proves the narrower target:

> A short natural-language request plus an exact current authority snapshot can be deterministically transformed into an inspectable sealed PROGRAMSTART Work Packet projection that preserves operator intent, adds no new execution authority, inherits current methodology/project constraints, represents parallel write ownership, distinguishes human gates from automation gaps, detects stale/tampered semantics, and renders a conversational worker prompt as a derived artifact.

It does **not** claim that arbitrary natural language alone is sufficient to discover truth or authority. Authority resolution remains an explicit upstream trust boundary, and semantic admission remains a Controller responsibility.
