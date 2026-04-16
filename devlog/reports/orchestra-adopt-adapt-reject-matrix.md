# Orchestra Agent Adopt / Adapt / Reject Matrix

Purpose: Convert the Orchestra Agent review into a direct reuse matrix with priority, effort, rationale, and transferability.
Status: Analysis backlog. This is not an approved implementation plan.
Basis: Derived from the code review captured in `devlog/reports/orchestrareport.md`.
Last updated: 2026-04-16

---

## Executive Summary

The strongest Orchestra Agent material is reusable **scaffolding**. The weakest material is its attempt to use a broad prompt-driven loop as an operational control plane.

That leads to a simple rule:

- Adopt the parts that increase evidence, boundedness, and observability.
- Adapt the parts that are structurally useful but currently too loose.
- Reject the parts that collapse analysis and action into one high-permission prompt loop.

Priority uses this meaning:

- `P1`: highest leverage or highest risk reduction.
- `P2`: useful, but not the next thing to do.
- `P3`: optional or portfolio-scale enhancement.

Effort uses this meaning:

- `Low`: limited surface, low policy complexity.
- `Medium`: moderate design and integration work.
- `High`: requires architectural reshaping or a new trust model.

---

## Adopt

| Pattern | Priority | Effort | Why adopt it | Why it travels well |
| --- | --- | --- | --- | --- |
| Tool-call audit logging | P1 | Low | Durable tool traces are one of the fastest ways to make automation inspectable and debuggable. | Any agent, assistant, or workflow runner benefits from knowing what happened, when, and with what result. |
| Pre-execution guardrails | P1 | Medium | Guardrails reduce dependence on prompt obedience and create explicit policy boundaries before action. | This pattern works in coding agents, deployment helpers, review bots, and workflow systems. |
| Hook lifecycle around actions | P2 | Medium | Pre/post hooks keep the core execution path lean while allowing evidence capture, notifications, or local policy enforcement. | Cross-cutting concerns exist in almost every automation system. |
| Operational telemetry by tool or step | P2 | Low | Latency, failure rates, and usage concentration help identify weak operational surfaces quickly. | Telemetry is generic infrastructure with low conceptual risk. |
| Multi-project registry shell | P3 | Medium | Portfolio visibility is useful when one operator manages many repos or workflows. | Repo portfolios are common; a simple registry becomes more valuable over time. |

### Why these are adopt candidates

These patterns are useful because they improve **operational truthfulness** without requiring trust in open-ended model judgment. They make systems easier to inspect, easier to debug, and easier to bound.

---

## Adapt

| Pattern | Priority | Effort | What is good about it | Why it cannot be reused as-is |
| --- | --- | --- | --- | --- |
| Playbooks | P1 | High | Repeated tasks do benefit from named reusable flows. | Prompt chains are too loose; they need typed steps, expected outputs, and stop conditions. |
| Scheduling | P1 | High | Recurrence is valuable for audits, reminders, and status production. | Scheduling prompts is not a trustworthy primitive; schedules should target named operations. |
| Memory | P1 | High | Persistent context can improve continuity. | Freeform embedding recall is too weak unless memories are classified, verified, and aged. |
| Project detection | P2 | High | Automatic context seeding does reduce cold-start cost. | Marker-file inference is too shallow for serious planning or architecture advice. |
| Session persistence | P2 | Medium | History continuity helps users pick up where they left off. | Chat history alone is not enough; decision records need their own structure and lifecycle. |

### How these should be adapted

The common fix is the same across all five items: replace prompt-era looseness with typed structures.

- Playbooks should become typed workflows.
- Scheduling should target declared operations.
- Memory should distinguish verified facts from tentative notes.
- Project detection should produce explicit context bundles.
- Sessions should preserve decision records, not only messages.

These are good ideas trapped in weak shapes.

---

## Reject

| Pattern | Priority | Effort | Why reject it as a model |
| --- | --- | --- | --- |
| Prompt-led core orchestration | P1 | N/A | The control plane becomes too ambiguous, too hard to reason about, and too dependent on changing model behavior. |
| Prompt-scheduled unattended jobs | P1 | N/A | Recurring prompts are not stable enough to serve as trustworthy operational units. |
| Auto-commit as a default path | P1 | N/A | It blurs advice and action, creates repo-mutation risk, and weakens review discipline. |
| Broad generic tool surface as product identity | P1 | N/A | A huge mixed tool surface makes policy harder, trust lower, and product purpose fuzzier. |
| Naive JSON vector memory as trusted context | P1 | N/A | Similarity recall over unclassified notes is not a durable basis for high-quality decisions. |

### Why these are reject candidates

These patterns do not merely need polish. They are misaligned with trustworthy decision support because they expand action power faster than they expand evidence, policy, or determinism.

---

## Priority View

### First things worth borrowing

1. Tool-call audit logging.
2. Pre-execution guardrails.
3. Typed replacement for playbooks.
4. Operation scheduling instead of prompt scheduling.

### First things worth refusing

1. Prompt-led control as the system center.
2. Auto-commit as a normal path.
3. Broad unrestricted tool exposure.

This ordering is deliberate. The first list raises trust quickly. The second list prevents predictable category mistakes.

---

## Why These Choices Generalize Beyond PROGRAMSTART

The conclusions are not repo-specific. They apply to many agent systems because the same tradeoff repeats across products:

- Evidence-producing scaffolding usually transfers well.
- Typed workflows transfer better than prompt chains.
- Policies outside the model transfer better than prompt warnings.
- Open-ended control loops transfer poorly unless the target domain already tolerates ambiguity.

The portable lesson is not "copy this repo." It is "separate the reusable safety scaffolding from the product-specific orchestration model."

---

## Bottom Line

If Orchestra Agent is mined for reusable value, treat it like a source of **operational patterns**, not a source of **governing architecture**.

Adopt what increases visibility.
Adapt what needs typed structure.
Reject what makes authority too model-dependent.
