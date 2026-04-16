---
status: accepted
date: 2026-04-16
deciders: [Solo operator]
consulted: []
informed: []
---

# 0015. Reuse external agent systems by pattern, not wholesale

<!-- DEC-012 -->

## Context and Problem Statement

PROGRAMSTART reviewed Orchestra Agent as a possible source of reusable orchestration ideas. The review found several useful operational patterns, including audit logging, pre-execution guardrails, hook lifecycles, telemetry, and multi-project registry concepts. It also found that Orchestra Agent's core trust model is a broad prompt-centered control loop with mixed analysis and action powers, which is a poor fit for PROGRAMSTART-style governance and for other systems that rely on explicit authority surfaces.

## Decision Drivers

- Reuse should favor patterns that improve evidence, boundedness, and inspectability.
- PROGRAMSTART and future generated systems need explicit authority surfaces rather than model-led control planes.
- Useful external ideas should not be discarded solely because the source repo's overall architecture is not a good fit.
- Decision support should stay distinct from high-permission automation unless the action path is explicitly bounded.
- The repo needs a durable reuse rule for future evaluations of external agent systems.

## Considered Options

- Option A — Adopt an external prompt-led agent framework directly when it appears feature-rich.
- Option B — Reuse selected operational patterns from external agent systems while rejecting prompt-led control planes as the governing architecture.
- Option C — Reject external agent systems entirely and avoid borrowing any of their patterns.

## Decision Outcome

Chosen option: **Option B**, because it preserves the best reusable scaffolding from external agent systems without importing a trust model that is too ambiguous for governance-heavy work.

### Consequences

- Good: Future evaluations now have a durable rule to separate transferable scaffolding from non-transferable orchestration models.
- Good: Evidence-first patterns such as audit logging, guardrails, hooks, and typed workflows remain available for reuse.
- Good: PROGRAMSTART and similar systems keep explicit authority documents, validation, and state as the control plane.
- Bad: Reuse becomes slower because external systems must be decomposed and judged pattern by pattern.
- Bad: Feature-rich agent frameworks may look attractive in the short term but still require disciplined rejection of their core control model.
- Neutral: Exploratory agent shells remain useful as advisory tools, but they are not promoted to governing architecture by default.

## Pros and Cons of the Options

### Option A

- Good, because it can deliver many capabilities quickly.
- Bad, because feature breadth does not guarantee a trustworthy control model.
- Bad, because prompt-led orchestration blurs analysis, action, and authority.

### Option B

- Good, because it captures reusable safety and observability patterns.
- Good, because it preserves explicit authority and validation as the governing mechanism.
- Bad, because it requires more architectural judgment than wholesale adoption.

### Option C

- Good, because it avoids importing a weak trust model.
- Bad, because it throws away legitimately useful patterns that can benefit multiple programs.
- Bad, because it turns a nuanced evaluation problem into a blanket refusal rule.

## Confirmation

This decision is being followed correctly when all of the following are true:

- External agent evaluations explicitly classify findings into adopt, adapt, and reject groups.
- Borrowed features are bounded scaffolding such as evidence capture, policy enforcement, or typed workflow support rather than prompt-led governing loops.
- Governance-heavy systems keep state, validation, and authority documents as the control plane.
- New roadmaps or backlogs distinguish decision support from action-taking behavior.

## Links

- [DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [orchestrareport.md](../../devlog/reports/orchestrareport.md)
- [orchestra-adopt-adapt-reject-matrix.md](../../devlog/reports/orchestra-adopt-adapt-reject-matrix.md)
- [orchestra-trustworthy-decision-support-roadmap.md](../../devlog/reports/orchestra-trustworthy-decision-support-roadmap.md)
- [orchestration-model-comparison.md](../../devlog/reports/orchestration-model-comparison.md)
