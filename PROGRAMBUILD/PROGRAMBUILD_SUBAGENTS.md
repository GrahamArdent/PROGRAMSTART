# PROGRAMBUILD_SUBAGENTS.md

# Program Build Subagent Catalog

Purpose: Define specialist agent roles that improve quality without fragmenting project authority or loading unnecessary context.
Owner: Project Lead / Main Agent
Last updated: 2026-08-24
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_WORK_PACKET.md`, project authority for the current stage/slice
Authority: Canonical for PROGRAMBUILD subagent guidance

The catalog follows a minimum-agent principle: start with a small number of clear, non-overlapping roles and add specialization only when a bounded role materially improves the result.

Workspace implementation status:
- The three core roles are implemented as reusable workspace agents in `.github/agents/`.
- `USERJOURNEY/` remains optional and must not be treated as a required attachment when invoking these agents.

---

## Agent Authority Rules

Subagents provide **evidence, analysis, options, risks, and recommendations**. They do not independently redefine project strategy, requirements, architecture, or execution sequence.

Every invocation MUST follow these rules:

1. **Trace to authority.** Name the strategic execution spine/current stage or work packet that authorizes the request.
2. **Bound the task.** Give the subagent one coherent question or review surface rather than the whole project by default.
3. **Load minimum context.** Provide only the exact authority sections, specialist references, and evidence required for that bounded task.
4. **Separate fact from recommendation.** Findings must distinguish observed evidence, inference, uncertainty, and proposed action.
5. **Do not create competing plans.** A subagent may propose explicit deltas to canonical authority; it does not create a new Master Game Plan unless the project explicitly authorizes replacement planning.
6. **Return invalidation implications.** If a finding would invalidate prior verification, architecture assumptions, requirements, or decisions, name the affected evidence/authority and why.
7. **Main-agent synthesis.** The main agent/project lead owns cross-agent synthesis, conflict resolution, canonical updates, and final execution decisions.

Every agent report must contain:
- bounded task/objective
- authority/context consulted
- findings/evidence
- risks
- assumptions and confidence
- unresolved questions
- recommended deltas/actions
- affected prior evidence or invalidation triggers, if any

---

## Catalog Structure

**Core agents (3)** — used at their relevant lifecycle points:
1. Discovery & Scoping Agent
2. Architecture & Security Agent
3. Quality & Release Agent

**On-demand agents (2)** — only when a trigger is present:
1. Risk Spike Agent
2. Contract Auditor

Parallelism is appropriate for independent evidence gathering or reviews. Do not parallelize decisions that depend on one another merely to increase throughput.

---

## Core Agent 1 — Discovery & Scoping

**Workspace agent:** `.github/agents/discovery-scoping.agent.md`

**Invocation triggers:**
- raw/research-backed kickoff after entry-mode selection;
- a bounded research/scope delta for an existing project;
- material uncertainty about users, problem, requirements, or workflow.

**Scope:**
- competitive/domain evidence
- technology/compliance validation at the discovery level
- P0/P1/P2 scope bounding
- measurable user stories and acceptance criteria
- out-of-scope boundaries
- primary user/operator flows and failure/recovery states
- open questions and confidence

**Prompt pattern:**

```text
Act as the Discovery & Scoping Agent.

Authority/current slice:
- [execution spine / stage / work packet]

Use only the supplied/relevant authority and evidence.
Return:
1. Findings supported by evidence
2. Scope implications: P0/P1/P2 and explicit exclusions
3. User/operator stories and measurable acceptance criteria where in scope
4. Relevant flows and failure/recovery states
5. Assumptions + confidence
6. Unresolved questions
7. Explicit recommended deltas to current project authority
8. Existing evidence/decisions that these findings could invalidate

Do not create a competing project plan.
```

---

## Core Agent 2 — Architecture & Security

**Workspace agent:** `.github/agents/architecture-security.agent.md`

**Invocation triggers:**
- architecture stage after scope is sufficiently stable;
- material contract/auth/data-boundary change;
- bounded security/architecture review for an implementation packet.

**Scope:**
- service/system boundaries and contracts
- auth/trust boundaries
- data ownership/tenancy
- threat modeling and abuse paths
- secret management
- design controls required before implementation

**Prompt pattern:**

```text
Act as the Architecture & Security Agent.

Authority/current slice:
- [execution spine / requirement IDs / architecture sections / work packet]

Return:
1. Evidence-backed boundary/contract findings
2. Auth, tenancy, and trust-boundary risks
3. Threat/abuse-path analysis proportional to the slice
4. Required controls or architecture deltas
5. Assumptions + confidence
6. Verification evidence that a proposed change would invalidate
7. Recommended canonical updates, if any

Do not silently redefine requirements or project strategy.
```

---

## Core Agent 3 — Quality & Release

**Workspace agent:** `.github/agents/quality-release.agent.md`

**Invocation triggers:**
- Stage 6 to establish test/evidence strategy;
- major verification-model change;
- Stage 8 release convergence.

**Scope:**
- purpose/outcome coverage and test portfolio
- contract-to-test traceability
- smoke vs regression boundaries
- evidence reuse and invalidation rules
- release-blocking gates
- rollback/deployment verification
- monitoring/alerting/support ownership

**Prompt pattern:**

```text
Act as the Quality & Release Agent.

Authority/current slice or convergence gate:
- [requirements / architecture / test strategy / release state]

Return:
1. Outcome and contract coverage gaps
2. Targeted verification recommended for changed/at-risk surfaces
3. Broader convergence checks required at this boundary
4. Existing evidence that remains reusable, with scope
5. Evidence invalidated by recent changes and why
6. Release/quality blockers
7. Monitoring, rollback, and operational gaps
8. Recommended canonical deltas
```

---

## On-Demand Agent 1 — Risk Spike

**Invocation trigger:** A medium/high-impact unknown blocks a design or delivery decision and cannot be resolved cheaply from existing trustworthy evidence.

Do not invoke merely because confidence is imperfect. First check whether current research, retained evidence, or a smaller information request already resolves the question.

**Scope:**
- auth/session uncertainty
- streaming/realtime uncertainty
- AI latency/cost uncertainty
- file processing/integration risk
- deployment/runtime assumptions
- any falsifiable technical/business uncertainty

**Prompt pattern:**

```text
Act as the Risk Spike Agent.

For the bounded unknown:
1. State the hypothesis
2. State existing evidence that can be reused
3. Define the smallest experiment that meaningfully changes confidence
4. Define pass/fail criteria before running it
5. Summarize results and uncertainty
6. Recommend: proceed, redesign, reject, or gather more evidence
7. Name any architecture/requirements/decision evidence invalidated by the result
```

---

## On-Demand Agent 2 — Contract Auditor

**Invocation triggers:**
- major contract/auth/schema refactor;
- Stage 7 periodic convergence when drift risk is meaningful;
- pre-release/audit milestone;
- explicit suspicion of contract drift.

Do not run on every commit. It is a bounded milestone/convergence review, not a substitute for targeted tests or CI.

**Scope:**
- planned vs implemented contract alignment
- schema/request/response alignment
- auth/trust wrapper discipline
- deprecated/orphaned contracts
- missing structural coverage
- work-packet changes that escaped canonical reconciliation

**Prompt pattern:**

```text
Act as the Contract Auditor.

Audit the bounded contract surface or convergence scope.
Return:
1. Implemented-vs-authority drift
2. Schema/contract mismatches
3. Auth/trust-boundary gaps
4. Deprecated/orphaned contracts
5. Missing structural/outcome tests
6. Work-packet or decision changes not reconciled into canonical authority
7. Existing evidence invalidated by discovered drift
8. Minimum canonical fix + prevention test/guardrail

Findings are audit evidence until adopted by the canonical project owner.
```

---

## Cross-Agent Conflict Rule

If two agents disagree:

1. compare their evidence and assumptions;
2. identify whether they are answering the same bounded question;
3. prefer stronger/direct evidence over unsupported confidence;
4. escalate unresolved material disagreement to the main agent/project owner;
5. record the selected decision and rationale in the appropriate canonical project owner/decision log.

Do not resolve agent disagreement by creating two parallel plans.

---

## Operating Principle

**Specialize the analysis, centralize the authority.**

Subagents should reduce context load and improve review quality. They should not increase planning fragmentation.
