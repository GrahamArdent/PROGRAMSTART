# PROGRAMSTART Effective Autonomy Posture

Purpose: define how a PROGRAMSTART-managed project can safely benefit from increasing autonomous execution capability without requiring every project to be manually rewritten whenever the Controller, Compute Spine, workers, or credential paths improve.

Status: **PROGRAMSTART operational protocol / subordinate to owning-project authority**.

This protocol does not create a new controller, portfolio authority, scheduler, backlog, or permission source.

---

## 1. Core principle

The amount of work that may progress autonomously at any moment is the intersection of:

1. **owning-project authority** — what consequences the project currently permits;
2. **PROGRAMSTART governance** — what methodology/gates/verification apply;
3. **Autonomous Controller capability** — what semantic continuation, recovery, gate handling and sequencing are currently proven;
4. **Compute Spine / worker capability** — what concrete execution can currently be performed safely;
5. **identity / secret capability** — what authenticated machine/provider access is actually available;
6. **current evidence** — whether authority, code, dependencies, environment and required verification are still valid.

Call this intersection the project's **effective autonomy posture**.

> **Capability growth may increase how much already-authorized work can execute automatically. It must never increase what the project is authorized to do.**

---

## 2. Why this exists

PROGRAMSTART-managed projects can outlive individual execution mechanisms.

A project may authorize reversible repository-local implementation while the ecosystem initially has only manual transport. Later, the Autonomous Controller may gain persistent multi-packet continuation and Compute Spine may gain a safe Codex worker path.

The project should not need a roadmap rewrite merely because implementation capability improved.

Likewise, a newly available capability must not silently convert a previously gated consequence into autonomous permission.

The methodology therefore separates:

- **permission / consequence posture** — owned by the project; from
- **available execution capability** — owned by Controller / Compute Spine / workers / identity systems.

Effective autonomy is computed from both.

---

## 3. Autonomy posture is not one percentage

Do not label a project simply `AUTONOMOUS=true`.

A project may be autonomous for one consequence class and human-gated for another.

Examples:

- read/orient/analyze — automatic;
- repository branch edits — automatic;
- tests/CI/Challenge — automatic;
- bounded remediation — automatic;
- merge — policy-dependent;
- provider setup — gated;
- production deployment — gated;
- destructive migration — gated;
- material recurring spend — gated;
- physical-device acceptance — human/physical gate.

Represent posture at the smallest useful consequence-class granularity rather than one misleading project-wide autonomy flag.

---

## 4. Recommended consequence classes

Projects MAY use their own stronger taxonomy, but the reusable resolver should be able to reason about at least:

- `READ_ONLY` — repository/provider/operational observation with no mutation;
- `REPOSITORY_REVERSIBLE` — branch/worktree code, tests, docs and reviewable repository-only changes;
- `REPOSITORY_INTEGRATION` — merge/auto-merge or default-branch integration under repository policy;
- `RUNTIME_REVERSIBLE` — bounded non-production runtime/test environment effects with explicit cleanup/recovery;
- `EXTERNAL_MUTATION` — provider/account/system mutation outside the repository;
- `PRODUCTION_DEPLOYMENT` — release/deployment to production or production-like user-impacting environments;
- `DESTRUCTIVE_OR_IRREVERSIBLE` — deletion, destructive migration, irreversible data/resource change;
- `SPEND_OR_QUOTA` — material recurring/variable spend or quota consumption;
- `SECRET_OR_PERMISSION_EXPANSION` — new/rotated secrets, broader scopes, new identities or materially broader permissions;
- `PHYSICAL_OR_HUMAN_ACCEPTANCE` — physical-device, legal/business/security judgment, or other genuinely human evidence.

The exact labels are less important than preserving consequence separation.

---

## 5. Project-side posture

The owning project may state reusable autonomy preferences/constraints in the existing authority that owns the consequence.

Examples:

- `READ_ONLY`: auto-continue;
- `REPOSITORY_REVERSIBLE`: auto-continue with deterministic verification;
- `REPOSITORY_INTEGRATION`: follow enforced repository merge policy;
- `EXTERNAL_MUTATION`: require explicit gate;
- `PRODUCTION_DEPLOYMENT`: require explicit gate;
- `SPEND_OR_QUOTA`: require Cost Governance / explicit approval;
- `SECRET_OR_PERMISSION_EXPANSION`: require explicit security/permission gate.

Do not require a dedicated `AUTONOMY_PLAN.md`.

Use existing requirements, architecture, strategic spine, decision log, repository policy, Work Packet or release authority wherever that truth already belongs.

If no explicit project posture exists for a consequential class, fail closed rather than inventing permission from global capability.

---

## 6. Runtime capability declaration

The Autonomous Controller and execution infrastructure should expose machine-readable **capability evidence**, not global project permission.

Examples:

- can persist semantic run state;
- can chain authorized Work Packets;
- can dispatch read-only Codex work;
- can dispatch workspace-write Codex work;
- can verify exact repository/worktree identity;
- can survive restart;
- can pause on human gate;
- can authenticate accepted human evidence;
- can resume automatically;
- can access a provider with a given bounded machine identity;
- can deploy to a specific environment;
- can incur a bounded cost under an already-authorized envelope.

Capability declarations must be derived from actual accepted implementation/runtime evidence and may be invalidated when health, identity, version or environment changes.

A capability declaration is never permission to use that capability against every project.

---

## 7. Effective autonomy resolution

Before autonomous mutation/continuation, resolve:

```text
project authority
  ∩ PROGRAMSTART gate/verification rules
  ∩ Controller semantic capability
  ∩ Compute Spine / worker execution capability
  ∩ identity/secret capability
  ∩ current evidence freshness
  = effective autonomy for this exact action
```

If the intersection permits the action, autonomous continuation MAY proceed.

If the action exceeds any boundary, stop only the affected consequence/lane and continue unrelated safe work when current authority permits it.

Never weaken the strongest applicable boundary merely to preserve autonomous flow.

---

## 8. Automatic capability adoption

When the ecosystem gains a new proven capability, projects MAY begin using it automatically only when all of the following are true:

1. the owning project's existing authority already permits the consequence class;
2. the new capability does not require broader permission, secrets, spend, public exposure or project-scope change;
3. the Controller/Compute/worker capability is accepted and current;
4. required deterministic verification/Challenge/recovery semantics remain satisfied;
5. the change is implementation-mechanism substitution rather than a semantic authority expansion.

Examples:

- manual branch editing -> Codex workspace-write may be adopted automatically when repository-reversible work was already authorized;
- manual test execution -> remote worker CI may be adopted automatically when tests were already authorized;
- session-bound continuation -> persistent Controller continuation may be adopted automatically when the same Work-Packet sequence was already authorized.

Counterexamples requiring a gate/decision:

- new production credentials;
- new provider write scope;
- auto-merge where project policy previously required review;
- production deployment where only staging was authorized;
- increased spending authority;
- removing a human gate because automation has recently performed well.

---

## 8.1 Concept viability and bounded exploration

Autonomy MUST NOT turn persistence into an obligation to rescue a bad premise.

Before investing materially in a non-trivial, uncertain, repeatedly failing, consequential, or human-gated approach, PROGRAMSTART must challenge the **concept being attempted**, not only its current implementation.

Use the smallest useful viability record, in current task/Work-Packet state when needed:

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

This is conditional reasoning state, not a mandatory new project artifact or global registry.

Rules:

1. **Test the premise early.** Prefer the smallest experiment or current authoritative research capable of discriminating whether the proposed mechanism can satisfy the required outcome.
2. `supported` means current evidence is strong enough to justify the next bounded investment for the consequence at hand. It is not a universal or permanent proof.
3. `inconclusive` means obtain a more discriminating observation, research result, prototype, or materially different mechanism. Do not convert uncertainty into repetitive execution.
4. `falsified` means stop trying to force that concept. Preserve the evidence, pivot to a materially different viable concept, or truthfully stop. Do not ask a human to rescue a falsified premise merely because human action is available.
5. A repeated attempt is justified only when **something material changed** — evidence, mechanism, configuration, environment, hypothesis, implementation, or diagnostic discrimination — and there is a concrete reason that change could alter the result. Rewording the same command or repeating substantially identical attempts without new information is not progress.
6. Exploration is bounded by expected information value and consequence, not by a universal retry count. Spend more evidence-gathering effort when the decision is high-value, uncertain, hard to reverse, recurrent, or likely to create repeated operator burden; spend less when the action is cheap, reversible, and well understood.
7. Stop or pivot when additional attempts have low expected information gain, when the premise is contradicted, when a materially better concept is supported, or when further exploration would consume disproportionate time/cost/operator attention relative to the decision.
8. Evaluate **trajectory as well as outcome**. A correct final result reached through stale evidence, unnecessary operator relays, repeated indistinguishable attempts, unsafe shortcuts, or accidental success is not evidence that the path itself is good enough to standardize.
9. For predictable, deterministic work, prefer the simplest reliable workflow. Add agentic/compositional complexity only when current evaluation evidence shows it improves the required outcome.

The goal is neither "never give up" nor "fail fast". The goal is **bounded evidence-seeking that can falsify its own premise**.

---

## 9. Human-gate classification: genuine_human_gate vs temporary_automation_gap, readiness, alternative actuation, and notifications

A mature autonomy posture aims for **zero human transport work**, not zero human judgment.

Before declaring a human gate, classify the boundary origin:

- **`genuine_human_gate`** — the intended authority, safety, or evidence model requires human judgment, authorization, physical action, secret entry, legal/business acceptance, or equivalent human evidence;
- **`temporary_automation_gap`** — the action is mechanical and already authorized, but the current Controller, Compute Spine, worker, identity, or tool surface lacks a proven actuator or transport path.

**Current-environment inability alone is never evidence of a genuine human gate.** A temporary automation gap is removable implementation debt, not permanent project architecture.

Before requesting operator transport for a `temporary_automation_gap`, PROGRAMSTART MUST perform an **alternative-actuation search** proportional to the consequence and urgency:

1. restate the exact already-authorized consequence and preserve the strongest applicable gate;
2. inspect the capability graph beyond the first obvious tool surface, including connected APIs/connectors, provider-native APIs, CLI tools, repository automation, accepted runtimes, local agents, scheduled tasks, authenticated machine identities, existing control queues, custom/bounded API composition, and other already-trusted execution mechanisms that are actually available;
3. generate bounded compositions of those capabilities rather than assuming one tool must perform the whole action end-to-end;
4. prefer reuse of an existing trusted bridge, exact accepted artifact, fixed target/path, typed arguments, reversible behavior, and independently verifiable result over a new broad actuator;
5. Challenge candidate mechanisms for authority expansion, secret/identity widening, arbitrary command execution, destructive/external effects, spend, privacy, persistence and recovery risk;
6. use the safest viable composition that remains inside current authority; route any durable capability debt to its real owner;
7. request a short operator relay only when no bounded alternative survives the authority/capability/Challenge checks or when the boundary is genuinely human.

This search is a reasoning obligation, not a requirement to build new infrastructure for every blocked action. It should be fast for simple cases and deeper only when the consequence, recurrence or operator burden warrants it. It is also **not an instruction to exhaust every imaginable implementation**: apply Section 8.1 and abandon or pivot from falsified/low-information concepts.

> **Tool creativity is mandatory before human transport. Concept loyalty is not. Be creative in mechanism and conservative in authority.**

Examples of valid creative composition include an existing typed endpoint invoking an exact accepted runtime that safely refreshes its own fixed implementation path, or a connected API plus repository automation replacing a manual copy/paste step. Examples of invalid composition include disguising a broader action as a safer allow-listed action, adding arbitrary shell execution only to avoid an operator relay, broadening credentials without approval, routing around a real legal/security/production gate, or repeatedly perturbing syntax after the underlying mechanism has lost evidentiary support.

### Human-gate readiness

A human gate is **not ready** merely because automation is blocked or because several attempts failed.

Before consuming operator attention, the executor must resolve every machine-obtainable uncertainty that is material to the requested human action and establish that the proposed handoff procedure is sufficiently validated for its risk. Where applicable, this includes:

- the concept/mechanism is `supported`, not `falsified`; an `inconclusive` concept may reach the operator only when the unresolved fact itself genuinely requires human evidence and cannot be resolved safely beforehand;
- current authoritative/provider/runtime documentation or direct evidence supports the proposed mechanism;
- the exact runtime/shell/tool/version and target identity relevant to the instruction are known;
- command syntax, quoting, formatting, typed arguments, paths, configuration shape, or equivalent procedure details are validated before the operator is asked to execute them;
- non-secret portions are exercised with harmless/dummy inputs where practical and materially useful;
- the exact consumer, destination, scope, ownership/permission requirements, and secret-sensitive boundary are known when credentials are involved;
- the post-human verification is already defined and can verify the desired system effect without exposing the secret;
- rollback/removal/recovery is understood when the human action is consequential or creates persistent state;
- the **human-only remainder** is named precisely: the authority, secret possession, MFA, provider approval, physical action, judgment, or other evidence that only the human can supply.

When these conditions are met, the gate may be represented as:

```text
GATE_READINESS: ready
GATE_READINESS_EVIDENCE: <bounded references/results>
HUMAN_ONLY_REMAINDER: <exact human-only input/action>
```

If material readiness evidence is missing:

```text
GATE_READINESS: not_ready
```

and the system MUST NOT notify the operator merely to debug the proposed instructions. It must continue bounded research/validation, choose a better supported concept, or truthfully stop at the unresolved non-human boundary.

> **Human attention is a protected resource. The human supplies authority or uniquely human evidence; the human is not the debugger of unvalidated machine instructions.**

When an action truly requires the operator and gate readiness is established:

- persist the exact gate and resume point;
- continue unaffected safe lanes where permitted;
- notify the operator through an awareness-only surface;
- provide one precise bounded action or tightly coupled action set, with exact context sufficient to perform it correctly;
- authenticate consequential operator responses independently of notification delivery;
- resume automatically after accepted evidence;
- run the already-defined post-human acceptance check rather than treating action completion as proof;
- do not require a redundant generic `proceed` after the declared evidence has been accepted.

Every human intervention should retain enough structured reason/outcome evidence to determine whether it was:

- genuinely required and should remain human;
- temporarily required because a capability is missing;
- avoidable methodology friction;
- avoidable Controller/Compute/worker friction;
- caused by an unvalidated or falsified concept/procedure;
- external-provider limitation.

Route resulting learning to the behavior owner under `PROGRAMSTART_LEARNING_ARCHITECTURE.md`.

---

## 10. Autonomy learning

PROGRAMSTART SHOULD learn about autonomy only from reusable methodology evidence.

Examples that may belong to PROGRAMSTART:

- projects repeatedly cannot express safe auto-continuation without ad-hoc prompts;
- consequence classes are ambiguous across projects;
- a global rule causes unnecessary human gates;
- project posture is routinely mistaken for infrastructure capability;
- capability adoption repeatedly widens authority accidentally;
- an operator relay is declared before existing bounded tools/capabilities are composed and challenged;
- an operator is asked to debug syntax, formatting, paths, permissions, configuration or another machine-resolvable uncertainty that should have been validated before the handoff;
- automation repeatedly retries one implementation while evidence increasingly contradicts the underlying concept;
- final success hides a poor trajectory that would be unsafe, costly, brittle, or operator-heavy if standardized.

Examples that do not automatically belong to PROGRAMSTART:

- Codex fails a particular task class -> Controller/executor learning;
- worker resource pressure -> Compute Spine/worker learning;
- passkey UX friction -> Mission-Control learning;
- provider auth outage -> provider/local integration evidence.

The target is not to maximize autonomy as a vanity metric. The target is to reduce **justified human work** without weakening correctness, safety, verification, cost control, recoverability or authority.

---

## 11. Portfolio behavior

A portfolio/autonomous controller may periodically evaluate projects for available safe progress, but it must not become project authority.

For each candidate project:

1. re-read owning authority;
2. identify current Work Packet/frontier or derive the next bounded packet under PROGRAMSTART;
3. resolve exact effective autonomy for the proposed action;
4. when the approach is non-trivial, uncertain, repeatedly failing, consequential, or approaching a human gate, apply concept viability/bounded exploration before investing further;
5. execute/verify/reconcile if permitted;
6. if execution appears blocked only by tooling/transport, run the alternative-actuation search before classifying an operator relay;
7. before notifying the operator, require human-gate readiness and identify the exact human-only remainder;
8. stop at the narrowest real gate;
9. continue other projects/safe lanes when capacity and authority permit;
10. surface only meaningful, technically ready human actions.

A stale portfolio registry or old chat instruction must never substitute for current project authority.

---

## 12. Metrics

Where useful, measure:

- autonomous Work-Packet completion rate;
- consecutive Work Packets completed without human transport;
- human interventions per completed Work Packet;
- human intervention minutes;
- intervention reason/owner;
- avoidable vs required gate rate;
- human gates rejected as `not_ready` before operator notification;
- operator actions that required instruction correction after handoff;
- temporary automation gaps resolved without operator relay;
- concepts falsified/pivoted before consequential or human investment;
- repeated attempts with vs without a material attempt delta;
- safe-lane continuation while another lane is gated;
- first-pass verification success;
- retry/remediation/recovery outcomes;
- trajectory defects hidden by eventual final success;
- false-success/incorrect-closure rate;
- cost per successful outcome;
- capability adoption regressions.

A technically automatable and already-authorized action that still requires the operator to relay routine information is an autonomy gap.

A legitimate security/business/physical consequence that still requires human judgment is not automatically an autonomy failure.

---

## 13. Adoption rule

For existing Mode-C projects, do not restart planning or create a new autonomy roadmap merely because this protocol is introduced.

On the next natural orientation/Work-Packet derivation:

- use existing authority to infer only consequence classes that are already explicit enough;
- keep ambiguous consequential classes gated;
- use current Controller/Compute/worker capability evidence;
- allow already-authorized safe work to benefit from newly proven execution capabilities;
- apply concept viability/bounded exploration only when uncertainty, repeated failure, consequence, recurrence, or operator burden makes it useful;
- run the alternative-actuation search before escalating a mechanical tooling/transport limitation to the operator;
- require human-gate readiness before requesting operator action;
- record a project-specific decision only when real ambiguity or consequence warrants it.

The methodology change should reduce manual coordination, not create a new documentation campaign across every repository.

---

## 14. Invariants

- Capability is not authority.
- A project-wide `autonomous=true` flag is insufficient for consequential systems.
- New execution capability may automate existing permission but never create new permission.
- Test the concept before spending heavily on implementations of it when viability is materially uncertain.
- A falsified concept must be abandoned or replaced, not rescued through operator effort merely because a human is available.
- A repeated attempt must add material evidence, mechanism, configuration, hypothesis, environment, implementation, or diagnostic discrimination with a reason it could change the result.
- Exploration is bounded by expected information value and consequence, not by a universal retry count or an obligation to exhaust every possibility.
- Evaluate trajectory as well as final outcome before standardizing an autonomous path.
- Tool creativity is mandatory before human transport for an already-authorized mechanical action.
- Concept loyalty is not mandatory; pivot when evidence falsifies or materially weakens the premise.
- Be creative in mechanism and conservative in authority.
- An alternative-actuation search may compose trusted capabilities but must not disguise, bypass, or weaken a stronger gate.
- A human gate is not admissible merely because automation is blocked; the handoff procedure must be technically ready and the human-only remainder explicit.
- Human attention must not be used to debug machine-resolvable uncertainty or unvalidated instructions.
- Human-gate notifications are awareness, not acceptance.
- Learned success never grants broader authority.
- Project authority remains the source of project scope/sequence/consequence truth.
- Controller semantic state remains subordinate to project/PROGRAMSTART authority.
- Compute Spine remains concrete execution fabric, not semantic project authority.
- Portfolio state remains derived attention/routing evidence.
- Safe automation should continue until a real boundary is reached; a narrow gate should not unnecessarily freeze unrelated authorized work.
