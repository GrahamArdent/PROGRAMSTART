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

## 9. Human gates, alternative actuation, and notifications

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

This search is a reasoning obligation, not a requirement to build new infrastructure for every blocked action. It should be fast for simple cases and deeper only when the consequence, recurrence or operator burden warrants it.

> **Tool creativity is mandatory before human transport. Be creative in mechanism and conservative in authority.**

Examples of valid creative composition include an existing typed endpoint invoking an exact accepted runtime that safely refreshes its own fixed implementation path, or a connected API plus repository automation replacing a manual copy/paste step. Examples of invalid composition include disguising a broader action as a safer allow-listed action, adding arbitrary shell execution only to avoid an operator relay, broadening credentials without approval, or routing around a real legal/security/production gate.

When an action truly requires the operator:

- persist the exact gate and resume point;
- continue unaffected safe lanes where permitted;
- notify the operator through an awareness-only surface;
- authenticate consequential operator responses independently of notification delivery;
- resume automatically after accepted evidence;
- do not require a redundant generic `proceed` after the declared evidence has been accepted.

Every human intervention should retain enough structured reason/outcome evidence to determine whether it was:

- genuinely required and should remain human;
- temporarily required because a capability is missing;
- avoidable methodology friction;
- avoidable Controller/Compute/worker friction;
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
- an operator relay is declared before existing bounded tools/capabilities are composed and challenged.

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
4. execute/verify/reconcile if permitted;
5. if execution appears blocked only by tooling/transport, run the alternative-actuation search before classifying an operator relay;
6. stop at the narrowest real gate;
7. continue other projects/safe lanes when capacity and authority permit;
8. surface only meaningful human actions.

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
- temporary automation gaps resolved without operator relay;
- safe-lane continuation while another lane is gated;
- first-pass verification success;
- retry/remediation/recovery outcomes;
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
- run the alternative-actuation search before escalating a mechanical tooling/transport limitation to the operator;
- record a project-specific decision only when real ambiguity or consequence warrants it.

The methodology change should reduce manual coordination, not create a new documentation campaign across every repository.

---

## 14. Invariants

- Capability is not authority.
- A project-wide `autonomous=true` flag is insufficient for consequential systems.
- New execution capability may automate existing permission but never create new permission.
- Tool creativity is mandatory before human transport for an already-authorized mechanical action.
- Be creative in mechanism and conservative in authority.
- An alternative-actuation search may compose trusted capabilities but must not disguise, bypass, or weaken a stronger gate.
- Human-gate notifications are awareness, not acceptance.
- Learned success never grants broader authority.
- Project authority remains the source of project scope/sequence/consequence truth.
- Controller semantic state remains subordinate to project/PROGRAMSTART authority.
- Compute Spine remains concrete execution fabric, not semantic project authority.
- Portfolio state remains derived attention/routing evidence.
- Safe automation should continue until a real boundary is reached; a narrow gate should not unnecessarily freeze unrelated authorized work.
