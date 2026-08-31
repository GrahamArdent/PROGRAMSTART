# PROGRAMSTART Learning Observation — External Change Maintenance Loop

Date: 2026-08-31  
Related lesson: `PSL-019` — External change monitoring should terminate in governed maintenance rather than routine operator relay  
Classification: systemic workflow friction / implementation  
Maturity effect: **implemented on this methodology branch; real autonomous maintenance retest remains open**

## Trigger

A scheduled OpenAI/Codex/MCP watch was already successfully detecting meaningful upstream changes such as model retirement, pricing/plan changes, Remote capability changes, and MCP integration changes.

The operator then identified the actual workflow defect: when a detected change objectively requires PROGRAMSTART maintenance, the system still ends by notifying the operator and waiting for the operator to tell PROGRAMSTART to make the resulting change.

That creates unnecessary human relay work precisely where the correct response may already be deterministic.

The operator explicitly authorized the recommendation to evolve PROGRAMSTART so relevant external changes can be verified, classified, maintained, tested, and routed automatically while preserving stronger human gates for real decisions.

## Live authority/evidence review

The current PROGRAMSTART repository already provides most of the required primitives:

- evidence reuse/invalidation and freshness discipline;
- Adaptive Decision Router for genuine uncertainty/consequence;
- decision-scoped Cost Governance;
- repository-boundary rules;
- Mode-C authority preservation;
- Work Packet and verification economy;
- risk-triggered post-implementation Challenge Gate;
- an evidence-driven Learning Loop;
- selective PROGRAMSTART control propagation;
- manual full convergence when broad validation is warranted.

The gap is not another lifecycle. It is a missing external-change routing policy that says what an upstream signal should cause after it is verified.

## Watchtower review

Live `GrahamArdent/repo-watchtower` authority was inspected before defining the integration.

Watchtower V0.2 is explicitly **read-only portfolio observability**. Its current milestone authority forbids repository mutation, repair PR creation, workflow reruns, auto-merge, and infrastructure mutation. That boundary must remain intact.

Watchtower's longer-term architecture nevertheless already contains the natural future companion capabilities:

- authenticated intake and signal normalization;
- incident classification and durable evidence;
- repository policy;
- automation planning;
- isolated runners;
- `notify_only`, PR-only, and eventual auto-merge trust levels;
- validation evidence and circuit breakers.

The correct integration is therefore role separation, not duplication:

- Watchtower can become a sensor/incident/evidence plane and later an execution substrate when its own authority earns that capability;
- PROGRAMSTART remains responsible for authority-aware maintenance classification and composition of decision/cost/challenge/verification rules;
- each target project remains authoritative for its own implementation, architecture, release, and repository policy.

This avoids prematurely expanding Watchtower V0.2 while preserving a clean future interface.

## Implemented correction

This branch adds `docs/PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md` and wires it into always-on repository instructions.

The protocol routes verified upstream changes to:

- `no_effect`;
- `evidence_refresh`;
- `deterministic_maintenance`;
- `bounded_behavioral_maintenance`;
- `material_decision`;
- `automation_failed`.

It separates automatic PR creation from auto-merge and requires explicit repository policy plus actually enforced/green validation before auto-merge is allowed.

Material architecture, security/privacy/legal, billing/spending, migration/data, destructive, release, project-scope/sequencing, secret, and other hard-to-reverse changes preserve their stronger authority gates.

For changes affecting multiple projects, every project receives its own Mode-C delta and repository PR boundary; one provider update cannot become an implicit portfolio-wide mutation transaction.

## Immediate operational limitation

PROGRAMSTART currently has a manual-only full convergence workflow and does not currently enforce protected `main` status checks. Therefore this implementation deliberately does **not** claim that scheduled maintenance should begin auto-merging PROGRAMSTART changes immediately.

The safe current trust level is:

**detect/verify/classify → automatically prepare focused maintenance PR when authorized → run whatever truthful validation is available → escalate only when required.**

Auto-merge should be enabled only after the target repository has an explicit maintenance policy and an enforced validation path capable of proving the relevant change.

This is a safety property, not unfinished product ceremony.

## Anti-bloat / adversarial review

The design was challenged against these failure modes:

1. external news becoming architecture authority;
2. provider monitoring creating a stale central vendor catalogue;
3. every upstream announcement creating repository churn;
4. deterministic maintenance being blocked on unnecessary human relay;
5. automatic PR creation being conflated with permission to auto-merge;
6. one upstream event mutating many projects as a portfolio transaction;
7. Watchtower receiving repair authority before its own V0.2 boundary permits it;
8. price/security/destructive changes bypassing existing stronger gates;
9. failed automation retrying indefinitely or hiding unresolved exposure.

The protocol addresses each with evidence verification, bounded classification, project-specific authority, separate PR/merge trust levels, Watchtower role separation, existing Cost/Challenge/Decision composition, and circuit breakers.

## Retest

`PSL-019` should remain **implemented**, not validated, until a natural external change is handled end to end.

A strong real retest is the next verified upstream change that objectively invalidates a PROGRAMSTART model/command/configuration/reference and has one unambiguous safe replacement.

Validation should demonstrate that the system:

- detects and verifies the change without operator prompting;
- finds the live affected PROGRAMSTART surface;
- classifies it as deterministic maintenance rather than a material decision;
- prepares the focused change/PR automatically;
- produces truthful validation evidence;
- does not request operator involvement when none is required;
- does not auto-merge unless the repository's explicit policy and enforced gates permit it;
- leaves useful audit evidence and avoids notification noise after successful routine handling.
