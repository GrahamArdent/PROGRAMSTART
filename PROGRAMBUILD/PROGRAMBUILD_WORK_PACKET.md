# PROGRAMBUILD_WORK_PACKET.md

# Program Build Work Packet

Purpose: Define the smallest useful current-slice planning structure without creating a competing game plan or unnecessary documentation ceremony.
Owner: Project Lead / Operator
Last updated: 2026-09-09
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md`, the project's strategic execution spine, relevant requirements/architecture/decisions
Authority: Canonical for work-packet semantics, including accepted-recommendation resolution evidence, checklist completeness, bounded exploration/human-gate readiness, and bounded cross-system test envelopes. A filled packet is derived execution context and is never canonical over project authority.

---

## 1. Core Rule

A **work packet is a logical execution contract**, not necessarily a file.

It answers:

- what are we doing now?
- why is it authorized/next?
- if this follows an accepted recommendation, what did generic acceptance actually authorize under current project authority?
- does the accepted recommendation execute inside current authority, require authority reconciliation before/with execution, or remain deferred without resequencing?
- does a stronger approval/manual/security/cost/privacy/legal/release gate remain unsatisfied despite generic acceptance?
- what exact action is blocked, if any, and how narrowly is that blocker scoped?
- what safe execution lane remains available, if any?
- when one Mode-C spine legitimately exposes more than one current lane, which lanes matter now and which single packet is selected for this invocation?
- what proves that selected packet is independent enough to proceed, what surfaces conflict, and where must the lanes converge again?
- when coordinated lanes share one consequential mutable runtime/provider/device/deployment resource, which exact lane owns mutation now and what releases or transfers that ownership?
- if another repository is a real dependency, which repository owns which meaning/mechanics and what is the current dependency state?
- what cross-repository evidence is reusable, what invalidates it, and what external/manual boundary remains?
- when a proposed concept is materially uncertain, repeatedly failing, consequential, or approaching a human gate, what smallest evidence supports or falsifies that premise and what bounds further exploration?
- if an operator/manual action is the actual next gate, is the procedure technically ready, what exactly remains human-only, who must do exactly what, what evidence must come back, and where does execution resume?
- what is in and out of scope?
- which current authority/evidence matters?
- what evidence can be reused?
- what could invalidate that evidence?
- what proves completion?
- is omission risk high enough, or is there an applicable durable checklist, such that checklist completeness should be active?
- if a checklist is active, which already-authorized obligations remain satisfied / not applicable / blocked / authority-permitted deferred?
- does the actual completed change trigger PROGRAMBUILD's post-implementation adversarial Challenge Gate before merge-ready/closure?
- what durable project state must be reconciled afterward?

A work packet is **not**:

- a new master plan;
- a cross-project or portfolio master plan;
- a parallel backlog or scheduler;
- a second requirements/architecture document;
- a running diary;
- a place to copy the whole repository;
- a credential/secret store;
- a recommendation registry or hidden future-work queue;
- a retry ledger or concept registry;
- a checklist that can invent scope;
- mandatory paperwork for trivial or single-step work.

---

## 2. Choose Compact Or Extended

### Compact packet — default

Use for ordinary coherent work that can be executed and reviewed without a durable packet file.

The compact packet may live in:

- the task/issue/PR description;
- the agent's current task state;
- a concise planning block in the active session.

Required fields:

```text
OBJECTIVE:
WHY_NOW / AUTHORITY:
BLOCKER_SCOPE: [none | row_only | merge_gate | mutation_gate | milestone | release | unresolved]
SAFE_EXECUTION_LANE: [A | B | C | none] + why it is actually allowed
CLOSURE_CONTROL:
COORDINATED_MODE_C_LANES: [none | current lane names/descriptions]
SELECTED_LANE:
LANE_INDEPENDENCE_EVIDENCE:
LANE_CONFLICTS:
LANE_CONVERGENCE:
RELATED_REPOSITORY_DEPENDENCY: [none | repository + relationship type + authority owner]
DEPENDENCY_STATE: [unknown | unsatisfied | partial | satisfied]
DEPENDENCY_EVIDENCE:
DEPENDENCY_INVALIDATION:
MANUAL_BOUNDARY: [none | concise summary]
OPERATOR_GATE: [none | active]
GATE_OWNER:
REQUIRED_ACTION:
SENSITIVE_INPUT_HANDLING:
RETURN_EVIDENCE:
EVIDENCE_ACCEPTANCE:
GATE_INVALIDATION:
RESUME_AT:
SAFE_WHILE_WAITING:
IN_SCOPE:
OUT_OF_SCOPE:
REQUIRED_CONTEXT:
REUSABLE_EVIDENCE:
INVALIDATION_TRIGGERS:
ACCEPTANCE_CRITERIA:
TARGETED_VERIFICATION:
DURABLE_UPDATES_IF_NEEDED:
```

Conditional concept-viability fields — include only when the chosen mechanism is materially uncertain, repeatedly failing, consequential enough to justify premise testing, or approaching a human gate with unresolved viability:

```text
CONCEPT:
WHY_IT_SHOULD_WORK:
MINIMUM_FALSIFICATION_TEST:
FALSIFICATION_CONDITION:
CONCEPT_STATUS: [untested | supported | inconclusive | falsified]
ALTERNATIVE_CONCEPTS:
EXPLORATION_BUDGET:
LAST_ATTEMPT_DELTA:
```

These fields bound reasoning; they are not a new lifecycle or retry registry. `EXPLORATION_BUDGET` describes a proportional evidence/effort boundary, not a mandatory numeric retry count. `LAST_ATTEMPT_DELTA` is required only when another materially similar attempt is being considered and must state what changed and why that change could alter the result.

Conditional human-gate readiness fields — include when `OPERATOR_GATE: active` and an operator handoff is being prepared:

```text
GATE_CLASSIFICATION: [genuine_human_gate | temporary_automation_gap]
GATE_READINESS: [not_ready | ready]
GATE_READINESS_EVIDENCE:
HUMAN_ONLY_REMAINDER:
```

`GATE_READINESS: ready` is admissible only when machine-obtainable uncertainty material to the requested human action has been resolved to the level warranted by its consequence, the procedure itself has been validated, and the exact human-only authority/evidence remainder is known. An automation failure count by itself can never make a gate ready.

Conditional shared-mutation ownership fields — include only when coordinated/current lanes can mutate the same consequential external/runtime/provider/device/deployment resource:

```text
SHARED_MUTATION_RESOURCE:
MUTATION_OWNER: [lane/packet + exact candidate/ref when relevant]
RELEASE_OR_TRANSFER_CONDITION:
```

These fields are a conflict-control lease, not a new project authority or broad mutation permission. They may be omitted when no consequential shared mutable resource exists.

Conditional accepted-recommendation fields — include only when the current invocation actually follows generic acceptance of a concrete prior recommendation:

```text
ACCEPTED_RECOMMENDATION:
RECOMMENDATION_DISPOSITION: [execute_current_authority | reconcile_authority_then_execute | defer_without_resequencing]
AUTHORITY_RECONCILIATION_BEFORE_EXECUTION: [none | exact owning artifact/decision change]
STRONGER_GATE_OVERLAY: [none | preserved + owner/condition]
```

Conditional checklist fields — include only when checklist completeness is actually activated by omission risk or an applicable durable checklist:

```text
COMPLETENESS_CHECKLIST: [inline | referenced] + source/reason
CHECKLIST_RECONCILIATION: [pending | complete | blocked] + unresolved items if any
```

Conditional closure field — include only when risk is already known to trigger it:

```text
ADVERSARIAL_CLOSURE: required + trigger reason
```

Do not add `ADVERSARIAL_CLOSURE: not_triggered` as routine paperwork. Even when the field was absent at packet creation, closure must still inspect the **actual completed change** and apply the trigger in `PROGRAMBUILD_CHALLENGE_GATE.md`.

When the slice was directly requested or already selected by current authority, omit the accepted-recommendation fields entirely. Do not manufacture a recommendation-resolution event or record `none` fields for every task.

When generic operator acceptance follows a prior recommendation, resolve exactly one `RECOMMENDATION_DISPOSITION` under `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`:

- `execute_current_authority` — execute the bounded work without strategic-plan churn;
- `reconcile_authority_then_execute` — update the existing owning authority/decision before or atomically with dependent implementation;
- `defer_without_resequencing` — preserve the future direction only where warranted, do not execute it now, and return to the actual current slice.

`STRONGER_GATE_OVERLAY` is independent of disposition. Generic `proceed` does not erase an explicit security/destructive/financial/credential/production/privacy/legal/release/operator gate. Conversely, do not invent a stronger gate when current project authority does not require one.

`SAFE_EXECUTION_LANE` is the A/B/C **safety class** for the selected packet. It is not the same thing as a named coordinated Mode-C lane and is not an automatic permission. It must be supported by the project's own authority, dependency state, and safety rules.

`COORDINATED_MODE_C_LANES` may be `none`. Populate it only when the current project authority genuinely exposes two or more relevant current lanes, such as one blocked closure-control row plus an independent reversible preparation row. Visibility does not authorize execution of every listed lane.

Cross-repository fields may be `none` when the packet has no real companion dependency. Do not manufacture a relationship merely because two repositories are related historically or organizationally.

Operator-gate fields may be `none` when the current slice can proceed in the available environment. A manual gate does **not** require a cross-repository dependency; credentials, provider-console actions, physical-device checks, human review, approvals, or other operator-only actions can be single-project gates.

Do not activate concept-viability fields for routine deterministic work that already has sufficient evidence and a well-understood mechanism. Their purpose is to prevent premise lock-in and low-information loops, not to create ceremony.

When checklist completeness is not active, omit the checklist fields entirely rather than recording `not_needed`. When it is active, use `inline` or `referenced`; checklist items must come from current authority/acceptance/risk obligations and cannot silently create scope.

If implementation introduces a material trust/security, persistence/idempotency/retry/concurrency, schema/migration, destructive/external-side-effect, production runtime/deployment, or other high-impact/hard-to-reverse boundary, activate the conditional field and run the existing Challenge Gate before declaring merge-ready/complete.

### Extended persisted packet — only when useful

Persist `CURRENT_WORK_PACKET.md` when one or more of these materially benefits execution:

- the slice spans sessions;
- multiple agents/people must share the same active context;
- dependencies or blockers make resumption non-obvious;
- concurrent Mode-C lanes create a real coordination/conflict boundary;
- the slice is high-risk or has meaningful blast radius;
- the evidence/invalidation model is non-trivial;
- the task is likely to pause and resume;
- the work is complex enough that a durable packet reduces, rather than adds, coordination cost.

Do **not** persist a file merely because the work is labelled "non-trivial."

A project MAY keep at most one active replaceable `CURRENT_WORK_PACKET.md` unless its own authority explicitly defines a different mechanism.

---

## 3. Compact Packet Lifecycle

1. **Derive** from the current strategic execution spine/stage and live project state.
2. **Resolve accepted recommendation when relevant** — if the operator generically accepted a prior recommendation, derive `execute_current_authority`, `reconcile_authority_then_execute`, or `defer_without_resequencing`; preserve any stronger gate overlay. Do not ask the operator to restate this classification when current authority is sufficient to derive it.
3. **Reconcile authority before dependent execution when required** — for `reconcile_authority_then_execute`, update the existing owner of durable scope/sequencing/architecture/decision/acceptance truth before or atomically with implementation. Do not intentionally leave authority describing the superseded design.
4. **Resolve bounded cross-repository dependencies when relevant** — identify the companion repository, relationship type, authority owner, dependency state/evidence, invalidation conditions, and manual boundary. Keep each repository's execution spine separate.
5. **Classify blockers** — if the closure-control row is blocked, identify the exact blocked action and classify the narrowest truthful scope before treating work as stopped.
6. **Scan safe lanes** — consider Lane A read-only/analysis, Lane B reversible repository/preparation work, and Lane C live/irreversible/external work under the project's own dependency and safety rules. A blocker label never automatically authorizes Lane C.
7. **Coordinate Mode-C lanes when the spine exposes more than one current lane** — keep closure-control unchanged, list only the current lanes needed for the decision, record independence/conflict/convergence evidence, select exactly one current executable packet for this invocation, and establish exclusive shared-mutation ownership when those lanes can touch the same consequential mutable resource.
8. **Challenge concept viability when useful** — before materially investing in an uncertain/repeatedly failing/consequential approach or escalating it to a human gate, state the premise, use the smallest discriminating evidence/falsification test, bound further exploration, and pivot rather than forcing a falsified concept. Another attempt must add a material delta and reason it could change the result.
9. **Resolve an operator/manual gate when needed** — classify the gate, search bounded alternative actuation when it is a temporary automation gap, and prepare a handoff only after `GATE_READINESS: ready`. If readiness is not established, continue machine-side validation/research or pivot instead of making the operator debug the procedure.
10. **Narrow** to one coherent objective with explicit non-goals. If disposition is `defer_without_resequencing`, the accepted future recommendation is not the execution objective; derive the real current slice instead.
11. **Reference** only the exact authority sections/evidence needed now.
12. **Reuse** trustworthy evidence whose invalidation conditions have not occurred, including valid evidence from a companion repository or prior operator action.
13. **Activate checklist completeness when useful** — use an inline/referenced checklist when omission risk is meaningful or an applicable durable checklist exists; omit checklist fields entirely for trivial work rather than adding `not_needed` ceremony.
14. **Execute** only the selected packet without silently widening scope or treating recommendation acceptance, a dependency graph, coordinated-lane view, shared-mutation ownership, concept status, checklist, or handoff as broader mutation authority.
15. **Verify** the changed/at-risk surface with the smallest sufficient check set.
16. **Challenge closure when the actual risk surface requires it** — before merge-ready/accepted/complete status, inspect the completed implementation/config/runtime behavior and run the existing `PROGRAMBUILD_CHALLENGE_GATE.md` post-implementation adversarial review when triggered. Do not use green current tests or eventual success as a substitute for constructing a realistic failure sequence or reviewing a materially poor execution trajectory.
17. **Reconcile checklist completeness when active** — every applicable item must be satisfied, not applicable with reason, blocked with exact gate, or deferred only when authority permits. A forgotten/unresolved required item prevents truthful closure.
18. **Reconcile durable state** — material decisions/scope/architecture/status belong in the repository that owns each concern. If execution disproved the accepted recommendation's premise or the selected concept, reconcile actual evidence rather than forcing the original recommendation/concept through.
19. **Close or hand off** the packet and derive the next slice from the newly current state.

If the packet needs its own backlog, milestones, or independent sequencing, it is too large. Split it.

### 3.1 Cross-repository dependency rule

A cross-repository relationship is a **derived, task-scoped authority/dependency graph**. It is canonical for nothing.

For a bounded relationship, identify only what the current decision needs:

- **primary/implementation repository** — the repository whose current slice is being orchestrated;
- **related repository** — the repository that owns a product meaning, contract, runtime boundary, or other prerequisite relevant to the slice;
- **relationship type** — for example product contract, runtime contract, companion dependency, or another explicitly described relation;
- **authority owner** — the exact concern the related repository owns;
- **dependency state** — `unknown`, `unsatisfied`, `partial`, or `satisfied`;
- **dependency evidence** — the exact repository/runtime/test evidence supporting that state;
- **invalidation conditions** — what would make that evidence unsafe to reuse;
- **manual boundary** — credential, physical-device, provider, operator, or other external action still required;
- **closure control** — the project/slice that still controls closure after reusable companion evidence is considered.

`partial` is intentionally first-class. A dependency may be satisfied on one plane and still open on another, such as a hosted runtime contract already deployed while companion repository convergence or real provider acceptance remains incomplete.

A derived graph MAY support:

- read;
- orient;
- classify;
- plan;
- verify;
- reuse still-valid cross-repository evidence.

It MUST NOT by itself authorize PROGRAMSTART to:

- advance both projects;
- close both projects;
- merge companion PRs;
- edit multiple execution spines as one transaction;
- turn the relationship into a portfolio Master.

Independent work in the primary repository may proceed only when that repository's own authority proves the work does not assume an unsatisfied part of the dependency.

### 3.2 Operator / manual gate handoff rule

An operator/manual gate is a **derived, bounded handoff**, not a new project state machine or authority layer. Use it when the actual next action genuinely needs operator/provider/physical evidence or when a mechanical action is already authorized but no bounded alternative actuator survives the Effective Autonomy checks.

Before the handoff becomes active for operator notification, classify it under `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` and require:

```text
GATE_CLASSIFICATION: [genuine_human_gate | temporary_automation_gap]
GATE_READINESS: ready
GATE_READINESS_EVIDENCE:
HUMAN_ONLY_REMAINDER:
```

`GATE_READINESS` is **not** a retry counter. It proves that the system has done the work that can reasonably be done before consuming human attention.

For a non-trivial gate, `GATE_READINESS_EVIDENCE` should retain only the evidence needed to show, where applicable:

- the concept/mechanism remains sufficiently supported for the requested consequence;
- current documentation/runtime/provider evidence supports the procedure;
- the relevant shell/tool/version/target is known;
- syntax, quoting, formatting, paths, typed arguments, config shape, or equivalent procedure details have been validated;
- harmless/dummy/non-secret portions were exercised where practical and useful;
- the consumer, destination, scope, owner/permission requirements, and secret-sensitive boundary are known;
- the post-action system verification is already defined;
- rollback/removal/recovery is understood when consequence/persistence warrants it;
- `HUMAN_ONLY_REMAINDER` truly identifies the authority, secret possession, MFA, provider approval, physical action, judgment, or evidence that cannot be supplied mechanically.

If material readiness evidence is still missing, set `GATE_READINESS: not_ready` in current task state and **do not notify the operator simply to debug the instructions**. Continue bounded research/validation, select a better-supported concept, or stop truthfully at the unresolved non-human boundary.

A useful ready handoff MUST state:

- **gate owner** — the person, provider console, physical device, reviewer, approver, or other boundary that can perform the action;
- **required action** — one concrete next action or tightly coupled action set; avoid vague instructions such as "finish setup";
- **sensitive input handling** — where credentials/secrets must be entered or stored, if relevant; name secret/config keys when useful, but never ask the operator to paste secret values into the packet/chat when a secure owning surface exists;
- **return evidence** — the non-secret evidence PROGRAMSTART needs back, such as resource identifiers, provider status, workflow outcome, screenshot/result summary, device behavior, or a bounded smoke result;
- **evidence acceptance** — what makes that returned evidence sufficient for the blocked decision/closure-control step;
- **gate invalidation** — what change would make the handoff or returned evidence stale/unsafe to reuse;
- **resume point** — the exact project row/slice/check to continue from after acceptable evidence returns;
- **safe while waiting** — any independently authorized Lane A/B work that may continue without bypassing the gate, or `none`.

Handoff rules:

1. Do not ask the operator to restate facts or evidence already available from project/repository/runtime authority.
2. Do not ask for raw secrets, refresh tokens, private keys, service-role keys, passwords, or similarly sensitive values in ordinary handoff evidence. Point to the secure provider/deployment/device surface that owns them.
3. Distinguish **operator action completed** from **system acceptance verified**. A console click or credential entry is not itself proof that the dependent runtime behavior works.
4. Request the smallest non-secret return evidence that can close the uncertainty. Do not demand broad screenshots/log dumps when a resource ID, status/result, or narrow smoke outcome is enough.
5. When evidence returns, reuse prior valid evidence and re-check only surfaces invalidated by the operator action. Do not restart the project or repeat broad research by default.
6. If returned evidence satisfies `EVIDENCE_ACCEPTANCE`, that accepted evidence is itself the resume signal unless the handoff explicitly declares a separate post-evidence approval. Do not require a redundant `proceed`, `go ahead`, or equivalent acknowledgement merely to continue already-authorized work.
7. Resume at the declared `RESUME_AT` point. A handoff does not silently advance or close the project's execution spine.
8. If the operator action changes a cross-repository dependency, reconcile each repository independently under its own authority rather than treating the handoff as a multi-project transaction.
9. Generic acceptance of the recommendation that led to the gate does not automatically satisfy the gate itself. Preserve the exact action/evidence boundary until it is actually crossed.
10. A concept that becomes falsified before the operator acts invalidates the handoff. Withdraw/rebuild the handoff rather than consuming human action to rescue the stale premise.
11. If the operator must correct command formatting, syntax, path, destination, permission, or another material machine-resolvable detail after handoff, treat that as counterevidence to `GATE_READINESS: ready`, correct the procedure, and route reusable learning to the behavior owner.

A generic statement such as `manual action required` is insufficient when the next action can be specified truthfully.

### 3.3 Concurrent Mode-C lane coordination rule

A coordinated lane view is **derived current execution context inside one existing project spine**. It is not a second execution spine, parallel backlog, scheduler, multi-agent launch plan, or permission to execute every visible lane.

Use it only in Mode C when the project's own current authority shows that more than one lane materially matters now. A common shape is:

- one **closure-control lane** that still governs milestone/release closure but is blocked or waiting;
- one or more **independent preparation/analysis lanes** that the same spine explicitly permits to proceed without bypassing closure order.

For the current invocation:

1. keep the project's existing `CLOSURE_CONTROL` unchanged;
2. list only the relevant current lanes, not every future row or idea;
3. select exactly one `SELECTED_LANE` as the current executable packet;
4. record `LANE_INDEPENDENCE_EVIDENCE` showing why that selected packet does not assume the blocked/unfinished portion of another lane;
5. record `LANE_CONFLICTS` for shared mutable files, providers, secrets, contracts, migrations, branches, installed releases, deployment slots, devices, or other surfaces that prevent unsafe overlap; use `none known` only when current evidence supports that statement;
6. record `LANE_CONVERGENCE` describing where context/verification must widen again before milestone/release closure or consequential mutation;
7. when two or more current lanes can mutate the same consequential resource, record the exact `SHARED_MUTATION_RESOURCE`, one `MUTATION_OWNER`, and the `RELEASE_OR_TRANSFER_CONDITION` before any lane crosses that mutation boundary;
8. immediately before consequential mutation, re-check the current resource state, selected lane/candidate, and mutation owner; stale ownership evidence is not permission to proceed;
9. transfer mutation ownership only after the previous owner is explicitly released/complete/superseded and the new owner is reconciled against current resource/repository/runtime state.

Coordination rules:

- The A/B/C `SAFE_EXECUTION_LANE` classification still applies to the **selected packet**. A named coordinated lane is not a new safety class.
- Visibility is not permission. A listed blocked closure-control lane remains blocked.
- PROGRAMSTART MUST NOT infer that multiple Lane C or overlapping mutation packets may run concurrently. Consequential overlap requires explicit project authority and conflict evidence.
- When current lanes share one consequential mutable resource, **at most one lane may own mutation of that resource at a time across invocations/sessions**. Other lanes MAY continue only with work proven unable to mutate that resource, such as read-only analysis or repository-only preparation.
- Mutation ownership is a narrow conflict-control lease, not project authority, priority, or permission to widen the owning packet.
- PROGRAMSTART MUST NOT auto-launch several agents/branches/PRs merely because several lanes are visible.
- One invocation returns one selected executable packet. A later invocation may select another lane after reorientation/reconciliation, but it MUST NOT silently seize an active shared-mutation lease.
- Each completed packet reconciles its durable state through the one existing project spine. Do not maintain a hidden PROGRAMSTART lane backlog.
- Before a shared convergence/closure point, widen context/verification enough to ensure the lanes did not invalidate each other's assumptions.

**Reference acceptance shape:** GCRM R4 keeps R4-02 as closure-control while its Master explicitly permits independent reversible R4-04 inventory/procedure preparation. Selecting R4-04 does not advance or close R4-02 and does not authorize live credential/provider mutation. Execution Node Stage 4 further shows that sibling repository lanes may remain active while one exact lane/SHA owns a single privileged installed-release boundary; another lane must not replace that release until ownership is released or transferred.

### 3.4 Checklist completeness rule

A checklist is a **derived completion inventory**, not a source of scope or sequencing.

Use checklist form when omission risk is meaningful or an applicable durable checklist already exists for the current boundary. Prefer the smallest useful surface:

- inline in the active session/work packet;
- PR/task/issue description;
- referenced existing durable checklist;
- persisted file only when multi-session/multi-person/resumption value justifies it.

For material checklist items, record or retain enough source context to show which authority/acceptance/risk obligation produced the item.

Closure statuses:

- **satisfied** — evidence proves the obligation is met;
- **not applicable** — current authority/risk proves the item does not apply; state why when non-obvious;
- **blocked** — exact gate/action/owner is known and closure remains truthful;
- **deferred** — only when the project's current authority explicitly permits deferral without invalidating closure.

#### Accepted-recommendation obligation coverage

When checklist completeness is active for a concrete accepted recommendation that is stable and materially multi-part, and omission or cross-owner risk is meaningful, atomize **only its material independently dispositionable obligations** into the existing checklist/Work Packet. Do not activate this rule for trivial recommendations or turn a simple recommendation into mandatory bureaucracy.

For each such obligation, retain enough bounded context to preserve:

- the obligation itself;
- its durable owner;
- any dependency that affects truthful closure;
- the evidence and acceptance condition needed to dispose it;
- the invalidation condition for that evidence/acceptance;
- exactly one terminal recommendation-accountability disposition: `implemented_and_accepted`, `rejected_with_evidence`, `superseded_by_accepted_solution`, or `explicitly_deferred_to_owner`.

`implemented_and_accepted` requires evidence sufficient for the owning acceptance authority; code presence or PR merge alone is not acceptance when runtime/provider/human proof remains stronger. `explicitly_deferred_to_owner` closes the **originating recommendation-accountability obligation only**: it does not assert that the receiving owner implemented or accepted the work, and it does not unblock an originating product/release dependency when current authority still requires the foreign outcome. Rejected or superseded obligations retain enough evidence to prevent silent resurrection/re-analysis.

This coverage stays inside the existing derived checklist/Work Packet and is reconciled or discarded with it. Do not create a global obligation registry, recommendation ledger, parallel backlog, or new lifecycle for this purpose.

An unchecked/forgotten required item is not equivalent to `not applicable` or `deferred`.

Do not create a universal persisted checklist registry. Do not convert checklists into a second Master. Reuse existing checklists when applicable and discard/close derived slice checklists with the packet.

### 3.5 Material cross-system test envelope

Use this section only when one behavioral proposition materially crosses repository, service, runtime, provider, device, human, or authority boundaries and ownership could otherwise become ambiguous. Ordinary unit/component tests do not need this envelope.

A material cross-system test has **exactly one `TEST_AUTHORITY` for each behavioral proposition**. The Test Authority owns the proposition being tested, the START/STOP boundary, and the verdict criteria. A parent system scenario may contain narrower participant-local tests, but each proposition still has one behavioral owner.

The authority roles are deliberately separate:

- **Goal authority** owns the desired product/system outcome.
- **TEST_AUTHORITY does not grant execution authority**. Test ownership cannot authorize provider, runtime, repository, secret, production, destructive, financial, privacy, legal, or other consequences.
- **Execution authority** decides which effects may occur while exercising the test.
- **Evidence authority validates evidence** provenance, integrity, binding, currentness, and sufficiency for its stated evidence purpose; it cannot mint approval or execution scope merely because the evidence is coherent.
- **Acceptance authority** decides whether verified evidence satisfies the declared behavioral/system claim.
- A **participant** supplies an input/output/evidence contract inside its own authority. **Participation does not transfer backlog, closure, or execution ownership** to that participant.

When useful, include this conditional envelope:

```text
TEST_ID:
BEHAVIOR_UNDER_TEST:
TEST_AUTHORITY:
GOAL_AUTHORITY:
EXECUTION_AUTHORITY:
PARTICIPATING_SYSTEMS:
START_CONDITION:
PRECONDITIONS:
AUTHORIZED_TEST_EFFECTS:
PROHIBITED_TEST_EFFECTS:
OBSERVABLE_SUCCESS:
OBSERVABLE_FAILURE:
EVIDENCE_PRODUCERS:
EVIDENCE_AUTHORITY:
ACCEPTANCE_AUTHORITY:
STOP_CONDITION:
CLEANUP_OWNER:
INVALIDATION_TRIGGERS:
OWNER_HANDOFFS:
```

Test-envelope rules:

1. `START_CONDITION` must identify when the proposition begins to be evaluated; `STOP_CONDITION` must identify when the verdict is terminal enough to end the scenario. Work before START or after STOP is not silently part of the test.
2. `AUTHORIZED_TEST_EFFECTS` must trace to real execution authority. A test plan is not permission to create credentials, deploy, spend, mutate providers, or widen access.
3. `PROHIBITED_TEST_EFFECTS` should make high-risk non-goals explicit when scope confusion is plausible.
4. `EVIDENCE_PRODUCERS` may span systems; that does not make the evidence collector the behavioral owner.
5. A test may consume Evidence Spine currentness/provenance as evidence without making Evidence Spine the Test Authority or Acceptance Authority for another system's behavior.
6. A genuine external dependency may still block the originating project's closure when the originating project's own current product/release authority explicitly requires that dependency. **Mere participation or observation is not a closure dependency.**
7. Do not turn the envelope into a test backlog, orchestration engine, global registry, or mandatory artifact. It is bounded derived context inside the existing Work Packet/PR/task/issue surface.

#### Cross-owner test finding / handoff rule

When a test exposes a defect, debt, or missing behavior owned by another repository/system, preserve a durable handoff to the real owner rather than absorbing foreign work into the originating project's strategy.

A useful handoff may retain:

```text
HANDOFF:
OWNER:
OBSERVED_GAP:
EVIDENCE:
REQUIRED_CONDITION:
```

If the foreign work is not itself an explicit originating-project acceptance dependency, it **must not remain as an unchecked foreign-owner closure item** merely because it was discovered during the test. The originating project may retain the observation/reference after its own scope closes. The receiving owner determines whether/how to promote and execute the work under its own authority.

#### Chat-detachment claims

When the behavioral proposition claims backend continuation independent of ChatGPT or another operator UI, the test envelope must make false success difficult:

- durable admission must satisfy `START_CONDITION` **before** the chat/UI detaches;
- after START, no ChatGPT-carried command, state, polling result, lane relay, `proceed`, or manual reconstruction may be required for the claimed continuation;
- Controller/worker/provider state used by the verdict must come from durable machine evidence, not conversation memory;
- later ChatGPT use may inspect the result only after the backend path has independently reached its declared STOP/recovery condition;
- an external job merely continuing after a chat closes is not proof of semantic continuation unless the behavioral owner had durably admitted the objective before detachment.

---

## 4. Extended `CURRENT_WORK_PACKET.md` Template

Use this only when persistence is justified. Omit conditional sections that do not apply; a persisted packet is not a reason to fill `none`/`not_needed` ceremony.

```markdown
# CURRENT_WORK_PACKET.md

PACKET_ID:
STATUS: [ready | active | blocked | complete | superseded]
PROJECT:
CURRENT_STAGE_OR_MILESTONE:
AUTHORITY_SPINE:
AUTHORITY_VERSION_OR_COMMIT:

## Accepted Recommendation Resolution — omit unless this packet follows generic acceptance
ACCEPTED_RECOMMENDATION:
RECOMMENDATION_DISPOSITION: [execute_current_authority | reconcile_authority_then_execute | defer_without_resequencing]
AUTHORITY_RECONCILIATION_BEFORE_EXECUTION:
STRONGER_GATE_OVERLAY:

BLOCKER_SCOPE: [none | row_only | merge_gate | mutation_gate | milestone | release | unresolved]
SAFE_EXECUTION_LANE: [A | B | C | none]
BLOCKED_ACTION:
CLOSURE_CONTROL:

## Concept Viability / Bounded Exploration — omit unless materially useful
CONCEPT:
WHY_IT_SHOULD_WORK:
MINIMUM_FALSIFICATION_TEST:
FALSIFICATION_CONDITION:
CONCEPT_STATUS: [untested | supported | inconclusive | falsified]
ALTERNATIVE_CONCEPTS:
EXPLORATION_BUDGET:
LAST_ATTEMPT_DELTA:

## Concurrent Mode-C Lane Coordination
COORDINATED_MODE_C_LANES: [none | current lane names/descriptions]
SELECTED_LANE:
LANE_INDEPENDENCE_EVIDENCE:
LANE_CONFLICTS:
LANE_CONVERGENCE:
SHARED_MUTATION_RESOURCE: [omit when no consequential shared mutable resource exists]
MUTATION_OWNER: [omit when no shared mutation lease is active]
RELEASE_OR_TRANSFER_CONDITION: [omit when no shared mutation lease is active]

## Cross-Repository Dependency
RELATED_REPOSITORY: [none | repository]
RELATIONSHIP_TYPE: [product_contract | runtime_contract | companion | other]
RELATED_AUTHORITY_OWNER:
RELATED_EXECUTION_SPINE:
DEPENDENCY_STATE: [unknown | unsatisfied | partial | satisfied]
DEPENDENCY_EVIDENCE:
DEPENDENCY_INVALIDATION:
MANUAL_BOUNDARY:

## Operator / Manual Gate Handoff
OPERATOR_GATE: [none | active]
GATE_CLASSIFICATION: [genuine_human_gate | temporary_automation_gap]
GATE_READINESS: [not_ready | ready]
GATE_READINESS_EVIDENCE:
HUMAN_ONLY_REMAINDER:
GATE_OWNER:
REQUIRED_ACTION:
SENSITIVE_INPUT_HANDLING:
RETURN_EVIDENCE:
EVIDENCE_ACCEPTANCE:
GATE_INVALIDATION:
RESUME_AT:
SAFE_WHILE_WAITING:

## Material Cross-System Test Envelope — omit unless ownership/boundaries are materially cross-system
TEST_ID:
BEHAVIOR_UNDER_TEST:
TEST_AUTHORITY:
GOAL_AUTHORITY:
EXECUTION_AUTHORITY:
PARTICIPATING_SYSTEMS:
START_CONDITION:
PRECONDITIONS:
AUTHORIZED_TEST_EFFECTS:
PROHIBITED_TEST_EFFECTS:
OBSERVABLE_SUCCESS:
OBSERVABLE_FAILURE:
EVIDENCE_PRODUCERS:
EVIDENCE_AUTHORITY:
ACCEPTANCE_AUTHORITY:
STOP_CONDITION:
CLEANUP_OWNER:
INVALIDATION_TRIGGERS:
OWNER_HANDOFFS:

## Objective
One concrete outcome.

## Why This Is Next
Trace to the execution spine, accepted-recommendation disposition, dependency order, blocker resolution, concept viability, coordinated-lane selection, safe-lane preparation, ready operator gate, or current stage.

## Scope
### In
- item

### Out
- item

## Required Context
- exact authority file/section/ID
- specialist evidence only when triggered

## Trusted Evidence + Invalidation
| Evidence | Why reusable | Invalidated by |
|---|---|---|
| | | |

When an external resource is involved, preserve **historical existence** separately from **current visibility/accessibility**. A resource that is currently missing or inaccessible is not automatically proven never to have existed or to have been deleted.

For concept viability, preserve only the evidence/falsification result and attempt delta needed to justify the next action. A later contradictory observation invalidates `supported`; do not retain success-by-inertia.

For coordinated lanes, preserve the independence/conflict/convergence evidence that made the selected packet safe. If another lane changes a shared assumption or mutable surface, re-evaluate only the affected coordination decision rather than replaying the whole project. If a shared-mutation lease exists, any mutation of that resource by another lane invalidates the lease evidence and dependent physical/runtime acceptance until ownership and current state are reconciled again.

For cross-repository evidence, preserve the repository/runtime/test source and the exact invalidation condition. Do not collapse a partially satisfied dependency into a boolean green state.

For operator-returned evidence, retain non-secret provenance and the exact acceptance/invalidation condition. Do not persist credentials merely to make the handoff durable. A change that falsifies the concept, procedure, target, consumer, permissions, or secret destination invalidates gate readiness before the human action is requested.

For a material cross-system test, retain only the authority roles, bounded START/STOP conditions, authorized/prohibited effects, and evidence/verdict references needed to prevent ownership confusion. Do not copy participant backlogs into the packet.

## Assumptions / Unknowns
| Item | Confidence | Action |
|---|---|---|
| | high / medium / low | reuse / verify / spike / decide |

## Acceptance Criteria
- [ ] criterion

## Completeness Checklist — omit unless activated
MODE: [inline | referenced]
SOURCE_OR_REASON:
- [ ] already-authorized obligation → source reference

At closure, resolve every applicable item as satisfied / not applicable with reason / blocked with exact gate / authority-permitted deferred.

## Verification
| Changed / at-risk surface | Check | Result |
|---|---|---|
| | | pending |

## Post-Implementation Adversarial Closure
TRIGGER: [not_triggered | required] + actual changed-surface reason
CHALLENGED_INVARIANT:
FAILURE_SEQUENCE:
RESULT: [clear | warning | blocked]
TARGETED_PROOF_OR_FIX:

Use `PROGRAMBUILD_CHALLENGE_GATE.md`; do not invent a second review protocol here.

## Stop / Escalation Conditions
- condition

## Durable Updates On Completion
- execution spine/status:
- decision log / ADR:
- requirements:
- architecture:
- tests / registry:
- release / operations:
- companion repository, only if that repository's own authority requires an update:

## Close-Out
OUTCOME:
VERIFICATION_SUMMARY:
CHECKLIST_RECONCILIATION:
ADVERSARIAL_CLOSURE_RESULT:
EVIDENCE_INVALIDATED_OR_REUSED:
AUTHORITY_RECONCILED:
REMAINING_BLOCKERS:
NEXT_RECOMMENDED_SLICE:
```

---

## 5. Context-Minimization Rule

Reference authority instead of copying it.

Prefer:

```text
ARCHITECTURE.md §4.2
Requirement FR-017
Decision DEC-021
```

Do not paste pages of authoritative text into a packet unless the task genuinely needs that text inline.

For accepted recommendations, reference the prior recommendation and only the authority needed to determine its disposition. Do not copy an entire conversation into the packet.

For concept viability/bounded exploration, keep the smallest discriminating premise/evidence/falsification/attempt-delta state; do not accumulate an exhaustive retry diary.

For checklist items, reference the owning requirement/gate/acceptance source rather than copying broad documents. The checklist should reduce omission risk without increasing context unnecessarily.

For coordinated Mode-C lanes, load only the source rows/constraints and shared surfaces needed to prove independence/conflict/convergence and any active shared-mutation ownership. Do not load the whole future milestone map just to list candidate lanes.

For a companion repository, load only the authority/evidence needed to resolve the declared dependency. Do not load its entire planning hierarchy merely because a cross-repository edge exists.

For an operator gate, name secure secret/config surfaces, readiness evidence, human-only remainder, and required non-secret return evidence rather than copying secret values, broad provider-console state, or unrelated logs into the packet.

The packet should make context **smaller**.

---

## 6. Evidence-Reuse Rule

For each verification concern, ask in this order:

1. Has this already been proven?
2. Is the evidence still in scope?
3. Did this slice trigger an invalidation condition?
4. What is the narrowest check that closes the remaining uncertainty?

Do not repeat broad verification by habit.
Do not reuse evidence after a relevant invalidation trigger.
Age/session change alone is not invalidation unless the underlying fact is genuinely time-sensitive.

For provider/runtime resources, keep these facts distinct:

- verified historical existence;
- current visibility/accessibility;
- current operational state;
- cause of any discrepancy, when actually known.

`not visible` or `inaccessible` MUST NOT silently rewrite verified historical existence to `never existed` or `deleted`.

For concept viability, `supported` remains reusable only while the evidence, mechanism, environment, requirements, and falsification conditions that justified it still hold. A materially contradictory result must lower/reclassify the concept rather than be buried under more retries. A successful end state does not erase a materially defective trajectory when deciding whether to standardize/reuse the path.

For coordinated Mode-C lanes, reuse the authority/evidence that proves a packet independent until a selected or sibling lane changes a shared dependency, mutable surface, closure assumption, or active shared-mutation resource. A lane label alone is not evidence of independence. If the consequential resource changes under another lane, exact-source/runtime/provider acceptance that depended on the prior resource state is invalid until current ownership/state is reconciled.

For cross-repository dependencies, evidence remains reusable only while its declared assumptions and invalidation conditions still hold. Repository merge state, head changes, contract/runtime changes, provider state, credential state, or directly conflicting evidence may invalidate only the relevant portion rather than forcing a full re-audit of both repositories.

For operator gates, record the returned **outcome/evidence**, not the secret material used to produce it. An operator's statement that an action was performed may satisfy an action-completion fact, but runtime/device/provider acceptance still requires the evidence defined by `EVIDENCE_ACCEPTANCE`. Human-gate readiness is invalidated when the concept, procedure, target, consumer, version, permission model, secret destination, or post-check changes materially before the operator acts.

For accepted recommendations, current execution/runtime evidence can invalidate the recommendation's premise. Generic operator acceptance does not override contradictory evidence discovered during implementation; reconcile actual truth and derive a new slice instead of forcing the original recommendation through.

A green current test suite is reusable evidence, but it is not by itself evidence that an activated post-implementation adversarial closure review occurred. When `PROGRAMBUILD_CHALLENGE_GATE.md` is triggered, challenge the actual completed implementation using the smallest relevant failure-sequence lens and retain only the resulting bounded evidence.

---

## 7. Existing-Project / Research Rule

For an existing repository:

- read its current instructions and strategic execution spine first;
- use the packet only as the current execution lens;
- keep research/audits as evidence;
- convert useful findings into explicit deltas to current authority;
- when a generic operator acceptance follows a recommendation, derive the recommendation disposition from current authority before executing;
- do not rewrite the Master for normal implementation detail;
- do not let an accepted future idea resequence current work;
- preserve stronger explicit approval/operator gates independently from generic acceptance;
- if another repository is a real prerequisite, inspect only enough of its authority/evidence to classify the dependency while preserving both execution spines;
- if the active closure row is blocked, classify blocker scope and scan safe lanes before concluding the project must wait;
- when several current lanes legitimately coexist under the one spine, keep closure-control explicit and select one independently authorized packet for the current invocation;
- when those lanes share a consequential mutable external/runtime/provider/device/deployment resource, preserve one explicit mutation owner across invocations and keep sibling lanes non-mutating on that resource until release/transfer;
- when the chosen mechanism is materially uncertain, repeatedly failing, consequential, or approaching a human gate, test/falsify the concept and bound exploration instead of exhaustively perturbing one implementation;
- another materially similar attempt must state the attempt delta and why it could change the result;
- if the next action is operator-only, classify the gate and require gate readiness before returning the exact handoff; do not make the operator debug unvalidated instructions;
- when operator evidence returns, reorient only enough to confirm acceptance/invalidation and resume the existing spine;
- use an applicable checklist when omission risk warrants it, and reconcile its required items before closure;
- inspect both the actual completed change and any materially suspect execution trajectory for a risk-triggered post-implementation Challenge Gate before merge-ready/closure;
- reconcile accepted changes back into the repository that owns the relevant canonical artifact;
- close/replace the packet after the slice.

A newer packet, recommendation-resolution result, concept status, coordinated-lane view, shared-mutation lease, checklist, research report, cross-repository graph, operator handoff, or adversarial-review result never outranks established project authority merely because it is newer.

---

## 8. Completion Rule

A packet is complete when:

- the scoped outcome is done or explicitly stopped;
- any accepted-recommendation disposition was honored without over-authorizing generic acceptance;
- `reconcile_authority_then_execute` work has its durable authority/decision truth reconciled rather than leaving known stale authority behind;
- `defer_without_resequencing` did not silently execute/reorder the deferred recommendation and the real current slice remains truthful;
- any stronger gate overlay remains preserved until its actual action/evidence requirement is satisfied;
- if concept viability/bounded exploration was activated, its status/evidence truthfully supports the final action or records the falsification/pivot; a falsified concept was not silently rescued through operator effort;
- no repeated-attempt sequence used substantially identical attempts as evidence of progress without a material attempt delta;
- acceptance criteria are resolved;
- required targeted verification is complete;
- if a checklist was active, every applicable required item is resolved as satisfied / not applicable with reason / blocked with exact gate / authority-permitted deferred;
- when accepted-recommendation obligation coverage was activated, every material independently dispositionable obligation has one terminal recommendation-accountability disposition, and `explicitly_deferred_to_owner` is never treated as proof that the receiving owner's implementation is complete;
- checklist fields were omitted when checklist completeness was not active rather than adding `not_needed` ceremony;
- any post-implementation adversarial Challenge Gate required by the actual changed risk surface or materially suspect trajectory is `clear` or the packet remains truthfully blocked/warning rather than being declared merge-ready/complete;
- material durable decisions/state are reconciled;
- remaining blockers are durably tracked with their narrowest truthful scope;
- if coordinated Mode-C lanes are present, closure-control stayed unchanged, one packet was selected for this invocation, independence/conflict evidence stayed valid, and the convergence point remains explicit;
- if a shared-mutation lease was active, the owning packet remained the sole mutator of that resource and completion leaves ownership explicitly released, transferred, or still active with a truthful reason/gate;
- any cross-repository dependency state is supported by current evidence and does not overstate partial satisfaction;
- any remaining external/manual boundary is exact;
- if stopped at an operator gate, `GATE_READINESS: ready`, readiness evidence, human-only remainder, the handoff, safe-while-waiting rule, and exact resume point are explicit and project closure is not falsely claimed;
- if a material cross-system test envelope was active, the declared START/STOP and authority roles remained valid, test effects stayed inside execution authority, and foreign findings were handed to their real owners unless the originating project's own authority explicitly made them closure dependencies;
- the next executable safe slice, or the exact reason no safe slice exists, can be derived from current project state without relying on the old packet/checklist as authority.

**Success test:** the packet reduced execution ambiguity, premise lock-in, avoidable human debugging, and omission risk more than it increased documentation work.
