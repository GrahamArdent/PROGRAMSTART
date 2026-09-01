# PROGRAMSTART Learning Architecture

Purpose: define when software should be designed to learn from real operation, how learning evidence is routed to the system that owns the behavior, and how learned changes are evaluated, promoted, rolled back, and prevented from silently broadening authority.

Status: **PROGRAMSTART operational protocol / subordinate to project authority**.

This protocol is distinct from `docs/PROGRAMSTART_LEARNING_LOOP.md`.

- `PROGRAMSTART_LEARNING_LOOP.md` asks whether real project execution should improve PROGRAMSTART methodology.
- This protocol asks whether the software or system being built should itself improve from real operational evidence, and how those lessons are routed to the correct owner.

Learning capability is conditional. It is not a mandatory subsystem, document set, model-training pipeline, or autonomous self-modification mechanism for every project.

---

## 1. Core Principle

During planning and architecture, ask:

> **Would this system materially benefit from learning from real operation, outcomes, failures, human corrections, usage patterns, repeated decisions, cost/performance evidence, or environmental change?**

If **no**, do not add learning ceremony.

If **yes**, activate a bounded **Learning Architecture Gate** and define only the learning machinery justified by the actual product/system.

The governing rule is:

> **Learn from evidence. Route lessons to the owner. Promote changes deliberately. Never let learning silently expand authority.**

Learning may improve behavior, defaults, routing, ranking, prompts, policies, retry strategies, resource selection, UX, recommendations, or models. It does not automatically imply machine learning or model training.

---

## 2. Learning Architecture Gate — Activation

Activate the gate when one or more of these are materially true:

- repeated real-world outcomes can reveal better/worse choices;
- operator or user corrections contain reusable signal;
- executor/provider/worker choice affects quality, latency, reliability, or cost;
- retry/recovery outcomes can improve future failure handling;
- ranking, recommendation, personalization, scheduling, routing, or prioritization can improve from observed results;
- recurring human gates may become safely automatable with evidence;
- system behavior depends on changing external conditions;
- drift, degradation, or changing usage patterns must be detected;
- the product intentionally adapts over time;
- future model fine-tuning or policy optimization is a credible requirement.

Do not activate merely because telemetry exists, AI is used, or learning sounds desirable.

---

## 3. Required Learning Decisions

When the gate is active, resolve the minimum necessary decisions below in the project's existing authority surfaces.

### 3.1 Learning target

What behavior or outcome is intended to improve?

Examples:

- executor selection;
- retry strategy;
- task routing;
- recommendation quality;
- ranking relevance;
- cost efficiency;
- human-intervention rate;
- recovery success;
- UX completion rate;
- prompt effectiveness.

### 3.2 Signal

What evidence indicates better, worse, success, failure, regression, or uncertainty?

Prefer observable outcomes over self-reported model confidence.

### 3.3 Owner

Which system owns the behavior being learned?

A lesson MUST be routed to the authority owner of the behavior rather than automatically to PROGRAMSTART.

Possible owners include:

- PROGRAMSTART methodology;
- Compute Spine or another execution/control system;
- worker/execution-node infrastructure;
- the current product repository;
- a dedicated service or model component;
- external provider limitation/evidence;
- Mission Control or another operator surface.

### 3.4 Collection

What telemetry/evidence is retained, at what granularity, and for how long?

Collect the smallest evidence set that can support the intended decision and verification.

### 3.5 Privacy and security

Define what MUST NOT become learning data, including secrets, unnecessary personal data, private content, raw credentials, sensitive prompts, or provider payloads when bounded references/outcomes are sufficient.

### 3.6 Evaluation

How is a candidate learned improvement tested before it becomes trusted behavior?

Examples include:

- offline replay;
- deterministic tests;
- shadow evaluation;
- canary trial;
- A/B test;
- bounded experiment;
- independent adversarial review;
- manual acceptance for high-consequence changes.

### 3.7 Promotion

What evidence and authority are required before the candidate becomes active behavior?

Learning evidence is advisory until the current owner authorizes promotion under its normal project/operational rules.

### 3.8 Rollback

How is a harmful or degraded learned change reversed quickly and safely?

### 3.9 Drift and counterevidence

How can later evidence weaken, narrow, reject, or supersede a prior learned conclusion?

A learning system must be able to unlearn or retire bad conclusions rather than only accumulate positive evidence.

### 3.10 Human corrections

When humans correct or override the system, decide whether the correction is:

- one-off/local;
- a candidate reusable signal;
- a policy/authority decision rather than training evidence;
- evidence that an unnecessary human gate exists;
- evidence that a human gate must remain.

Do not treat every human action as ground truth.

---

## 4. Owner-Routed Learning

The default routing loop is:

**REAL EVENT / OUTCOME → OBSERVATION → OWNER CLASSIFICATION → OWNER-SPECIFIC EVALUATION → CHANGE, IF EARNED → REAL RETEST**

Before creating a reusable lesson, determine:

1. What actually happened?
2. Which behavior produced or failed to prevent the outcome?
3. Which repository/system owns that behavior?
4. Is the observation local, systemic, confirmation, counterevidence, or an external limitation?
5. Does the owner already have a mechanism/roadmap item that covers it?
6. Is a change justified now, or should the observation only be retained for a future retest?

A single event may produce evidence relevant to multiple owners, but remediation and authority remain separate.

Example:

- PROGRAMSTART created an unnecessary gate → PROGRAMSTART methodology learning.
- Compute Spine lost retry state after restart → Compute Spine capability learning.
- Mission Control presented an approval poorly on mobile → Mission Control product learning.
- A provider API refused a supported operation → external limitation/evidence unless local handling was defective.

---

## 5. Authority Boundary

Learning MAY change behavior only within already-authorized boundaries.

Learning MUST NOT automatically:

- grant broader repository permissions;
- expose new secrets;
- increase spending authority;
- create production access;
- remove a required human/consequence gate;
- expand deployment scope;
- bypass branch/release/security rules;
- modify another repository's authority;
- promote itself to project or portfolio authority;
- self-approve an authority expansion because previous behavior performed well.

A learned proposal that requires broader authority must go through the normal authority/decision/approval path as if it had been proposed manually.

---

## 6. Deterministic Before Adaptive

Do not use adaptive/LLM/ML learning when deterministic rules can solve the problem reliably and cheaply.

Prefer deterministic mechanisms for:

- permission enforcement;
- retry counters and hard limits;
- budget ceilings;
- leases and locks;
- idempotency;
- schema validation;
- cryptographic/authentication checks;
- safety invariants;
- required approval boundaries.

Use learned/adaptive behavior where evidence can legitimately improve a choice within those fixed guardrails.

---

## 7. Project Artifact Rule

The Learning Architecture Gate does **not** create a mandatory `LEARNING_PLAN.md` or learning ledger for every project.

Record decisions in the existing authority that already owns the concern:

- `REQUIREMENTS.md` — desired learning outcomes and product constraints;
- `ARCHITECTURE.md` — telemetry, feedback path, ownership, data/privacy boundaries, promotion path;
- `TEST_STRATEGY.md` — evaluation, comparison, regression, drift, and acceptance evidence;
- `DECISION_LOG.md` / ADR — durable policy or architecture decisions;
- strategic execution spine — sequencing when learning capability is actual project work;
- Work Packet — bounded implementation/evaluation slice;
- `POST_LAUNCH_REVIEW.md` — real outcome evidence and follow-up.

Create a dedicated product/system learning ledger only when the amount of retained lesson state, experimentation, or operational routing is large enough that existing surfaces become unclear or expensive to reconstruct.

Such a ledger remains subordinate to the owning system's authority and MUST NOT become a shadow backlog or autonomous policy authority.

---

## 8. Relationship to PROGRAMSTART Learning

After a meaningful project checkpoint, two independent questions may apply:

### Methodology question

Did PROGRAMSTART materially help, hinder, or fail in a reusable way?

Use `docs/PROGRAMSTART_LEARNING_LOOP.md`.

### Product/system-learning question

Did real evidence reveal a potentially reusable improvement to the software/system itself?

Use this protocol and route the observation to the behavior owner.

One event may answer both questions, but the records and changes should remain owner-specific.

---

## 9. Learning-Capable Infrastructure Systems

Execution/control systems such as Compute Spine are strong candidates for this gate because real operation can improve:

- executor/model routing;
- worker/resource routing;
- retry/recovery selection;
- failure classification;
- scheduling/queue policy within fixed safety constraints;
- cost/latency tradeoffs;
- unnecessary human-gate identification;
- recovery playbooks;
- anomaly/degradation detection.

They MUST still preserve deterministic authority, permission, budget, safety, and concurrency guardrails.

---

## 10. Suggested Evidence Metrics

Select only metrics that affect real decisions. Candidate measures include:

- success rate by task/executor/resource class;
- first-pass verification rate;
- retry frequency and cause;
- successful automatic recovery rate;
- false-success/incorrect-closure rate;
- rollback rate;
- human interventions per completed Work Packet;
- human intervention time;
- avoidable human-gate rate;
- queue/wait time;
- worker utilization;
- latency to completion;
- cost per successful outcome;
- drift/regression rate;
- promotion rollback frequency.

Metrics MUST NOT be optimized in a way that hides failures, weakens verification, or makes autonomy appear higher than reality.

---

## 11. Change Promotion Pattern

For a non-trivial learned change:

1. retain the observation and evidence;
2. classify the owning system;
3. verify current authority/implementation does not already solve it;
4. define the smallest candidate change;
5. define acceptance and rollback before activation;
6. test in the narrowest safe environment;
7. require normal owner-specific review/approval where applicable;
8. activate within existing authority;
9. monitor for regression/counterevidence;
10. retain or revert based on evidence.

High-consequence learned behavior should use stronger independent review and staged rollout.

---

## 12. Success Test

The learning architecture is working when:

- learning is activated only where real value exists;
- observations are routed to the system that owns the behavior;
- product/system learning does not flood PROGRAMSTART's methodology ledger;
- candidate improvements are evaluated before promotion;
- safety/permission/authority boundaries remain deterministic and independently governed;
- bad learned changes can be rolled back or rejected;
- later evidence can narrow or reverse earlier conclusions;
- real operation measurably improves useful outcomes without creating shadow authority or uncontrolled self-modification.
