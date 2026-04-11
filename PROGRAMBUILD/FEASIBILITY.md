# FEASIBILITY.md

Purpose: Project viability, kill criteria, and go/no-go decision.
Owner: Product Lead
Last updated: 2026-03-27
Depends on: Program inputs block
Authority: Canonical for project viability

---

## Problem Statement

Describe the problem in one clear paragraph. Do not describe the solution or the stack.

## Primary User Pain

Describe the primary pain, available evidence, and urgency. Reference real signals (support tickets, analytics gaps, user research, competitive loss) when possible.

## Alternatives

| Alternative | Why Insufficient |
|---|---|
| | |
| | |
| | |

## Business Viability Assumptions

- assumption
- assumption
- assumption

## Technical Feasibility Assumptions

State assumptions about the *problem*, not the stack. Technology choices belong in `ARCHITECTURE.md`. Feasibility assumptions should describe what must be true for *any* reasonable implementation to work.

- assumption
- assumption
- assumption

## Top Risks

| Risk | Type | Severity | Notes |
|---|---|---|---|
| | business / technical / legal / delivery | high / medium / low | |
| | | | |
| | | | |

## Kill Criteria

What evidence would stop or materially redirect this project? These should be measurable and observable.

- criterion
- criterion
- criterion

## Rough Cost And Effort Estimate

| Area | Estimate | Confidence | Notes |
|---|---|---|---|
| Development | | | |
| Infrastructure | | | |
| Third-party or vendor cost | | | |
| Ongoing maintenance | | | |

### Estimation Method

Use T-shirt sizing to make estimates visible and challengeable. Bad estimates are better than no estimates — visible estimates get corrected, invisible ones drift.

**Size definitions** (adjust the time ranges per your context):

| Size | Meaning | Typical Solo Range | Typical Small Team Range |
|---|---|---|---|
| XS | Trivial — config, copy, or single-file change | < 1 day | < 1 day |
| S | Small — one well-understood component or integration | 1–3 days | 1–2 days |
| M | Medium — multiple components, some unknowns | 1–2 weeks | 3–5 days |
| L | Large — cross-cutting, multiple integrations, or research needed | 2–4 weeks | 1–2 weeks |
| XL | Very large — architectural, multi-system, or high uncertainty | 4+ weeks | 2–4 weeks |

**Per-area sizing** (fill after requirements are known — revisit at Stage 3):

| Area | Size | Confidence | Assumptions | Risk If Wrong |
|---|---|---|---|---|
| Core product feature set | | high / medium / low | | |
| Auth and identity | | | | |
| Data model and persistence | | | | |
| External integrations | | | | |
| Deployment and infrastructure | | | | |
| Testing and quality | | | | |

**Rules:**
- An estimate with "low" confidence on a P0 area is a risk spike candidate, not a planning input.
- If total estimated effort exceeds the delivery target, record the gap in `DECISION_LOG.md` and decide: cut scope, extend target, or accept the risk.
- Revisit this table at the Stage 3 Challenge Gate (after requirements are defined). Update sizes and confidences with the new information. Record changes.
- Do not treat these estimates as commitments. They are visibility tools. Their purpose is to make the scope-to-capacity relationship explicit so bad surprises happen on paper, not in production.

## Recommendation

Decision: go / limited spike / no-go

Reasoning:

---
