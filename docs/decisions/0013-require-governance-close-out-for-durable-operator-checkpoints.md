---
status: accepted
date: 2026-04-15
deciders: [Solo operator]
consulted: []
informed: []
---

# 0013. Require governance close-out loop for durable operator checkpoints

<!-- DEC-010 -->

## Context and Problem Statement

ADR-0012 closed a real gap for hardening: strategic structural work could finish green while leaving the ADR decision implicit. That fix revealed the broader architecture issue. PROGRAMSTART now uses several long-form operator execution prompts, and they can all land durable structural or policy changes. The operator standard, however, did not yet require a governance close-out loop or truthful direct-command verification, which meant the same ambiguity could reappear outside hardening.

## Decision Drivers

- Durable operator checkpoints must remain auditable, not just green.
- The governance rule should live at the operator-prompt layer rather than as a hardening-only exception.
- Operator prompts should verify against the truthful direct command surface.
- Failure diagnosis should not depend on truncated output.

## Considered Options

- Option A — Keep ADR-0012 as a hardening-only rule and rely on discretion elsewhere.
- Option B — Generalize the rule to long-form operator execution prompts that can land durable structural or policy changes.
- Option C — Require a full Stage 9-style audit after every operator phase.

## Decision Outcome

Chosen option: **Option B**, because it lifts the lesson to the correct abstraction layer without forcing every operator checkpoint into a full audit ceremony.

### Approved Decisions

1. **Governance close-out is an operator-prompt rule for durable checkpoints.**
   Long-form operator execution prompts that can land durable structural, workflow-policy, authority, or trust-boundary changes must require a governance close-out loop before the checkpoint is marked complete.

2. **The minimum close-out commands are fixed.**
   The governance close-out loop must include:

   ```powershell
   uv run programstart validate --check adr-coverage
   uv run programstart validate --check authority-sync
   uv run programstart drift
   ```

3. **ADR threshold remains unchanged.**
   The decision to create or update an ADR is still governed by `PROGRAMBUILD/PROGRAMBUILD.md` and `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md`.

4. **Truthful direct-command verification is mandatory.**
   Long-form operator prompts must use the truthful direct command surface for their verification steps and must not instruct operators to diagnose failures from truncated output.

5. **Checkpoint evidence must record the ADR outcome.**
   A durable operator checkpoint must state whether ADR triage produced a new or updated ADR, or explicitly record that no ADR was required.

6. **Short-form utility prompts are excluded.**
   Diagnostic utility prompts that cannot close a durable change checkpoint are not required to carry the governance close-out loop.

### Consequences

- Good: The lesson from hardening is now captured at the operator architecture layer.
- Good: Enhancement, gate-repair, hardening, and prompt-architecture remediation prompts can share one governance pattern.
- Good: Verification instructions become more truthful and less brittle.
- Bad: Long-form operator prompts gain extra ceremony.
- Neutral: ADR-0012 remains a valid historical waypoint but is now superseded by the broader operator rule.

## Pros and Cons of the Options

### Option A

- Good, because it minimizes churn.
- Bad, because it leaves the same governance gap in other operator prompts.

### Option B

- Good, because it fixes the root issue at the operator-prompt layer.
- Good, because it keeps the rule reusable and consistent.
- Bad, because it requires touching several prompt surfaces and standards.

### Option C

- Good, because it maximizes audit rigor.
- Bad, because it is too heavy for every operator checkpoint and would slow routine maintenance materially.

## Confirmation

This decision is implemented correctly when all of the following are true:

- The operator prompt standard requires governance close-out for durable checkpoints.
- Long-form operator execution prompts that can land durable policy or structural changes carry the governance close-out loop.
- Those prompts use the truthful direct command surface and avoid truncated diagnosis guidance.
- The decision trail links the broader rule from the DECISION_LOG to the ADR index.

## Links

- [0012-require-hardening-adr-triage-and-audit-loop.md](0012-require-hardening-adr-triage-and-audit-loop.md)
- [README.md](README.md)
- [DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD.md](../../PROGRAMBUILD/PROGRAMBUILD.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
- [OPERATOR_PROMPT_STANDARD.md](../../.github/prompts/OPERATOR_PROMPT_STANDARD.md)
- [execute-hardening-gameplan.prompt.md](../../.github/prompts/execute-hardening-gameplan.prompt.md)
- [execute-enhancement-gameplan.prompt.md](../../.github/prompts/execute-enhancement-gameplan.prompt.md)
- [execute-gate-gameplan.prompt.md](../../.github/prompts/execute-gate-gameplan.prompt.md)
- [execute-prompt-architecture-remediation-gameplan.prompt.md](../../.github/prompts/execute-prompt-architecture-remediation-gameplan.prompt.md)