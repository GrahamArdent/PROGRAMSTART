# REQUIREMENTS.md

Purpose: Functional scope, non-functional targets, user stories, and explicit boundaries.
Owner: Solo operator
Last updated: 2026-04-14
Depends on: FEASIBILITY.md, RESEARCH_SUMMARY.md
Authority: Canonical for scope and requirements

Note: Every P0 requirement must have at least one purpose test in `TEST_STRATEGY.md`. Purpose tests reference the requirement ID (e.g., FR-001). Requirements without purpose tests are not considered covered.

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| FR-001 | Operator can use the unified `programstart` CLI to inspect planning state, query the knowledge base, compare saved workflow snapshots, and restore a prior snapshot only with explicit confirmation. | P0 | Covers `programstart kb search`, `programstart kb ask`, `programstart diff`, and `programstart state rollback`; rollback MUST create a pre-rollback backup. |
| FR-002 | Greenfield bootstrap supplies project-owned, source-bound agent orientation without overwriting local instructions. | P0 | Actual bootstrap/target-command tests; host adoption remains separate. |
| FR-003 | Requirements discovery works backward from outcomes to justified information and complete interactions. | P0 | Semantic protocol and adjudicated acceptance; no claim of automated semantic completeness. |

### Foundation acceptance detail (PROGRAMSTART tooling)

- FR-002 (P0): Both greenfield bootstrap paths create project-specific agent orientation
  with valid canonical links, source identity and truthful methodology commands, without
  replacing existing project-owned instructions. Dry-run creates no files; lean bootstrap
  does not vendor factory runtime, dashboard or tests. A generated file does not certify
  host loading or product readiness.
- FR-003 (P0, semantic protocol): Requirements discovery applies outcome-led information
  and interaction analysis before dependent design through the canonical intake control.
  Explicitly retain unknowns and meaningful final-state assertions. Structural validation
  cannot mechanically certify the quality or completeness of that semantic work.

## Non-Functional Requirements

| ID | Requirement | Measure | Target |
|---|---|---|---|
| NFR-001 | | | |

## User Stories

### Story 1

As a solo operator
I want the unified `programstart` CLI to expose retrieval and workflow-state recovery commands
So that I can inspect architecture knowledge, compare saved state, and recover from bad workflow-state changes without dropping into script-specific entry points

Acceptance criteria:
- `programstart kb search <query>` returns knowledge-base results through the unified CLI.
- `programstart diff` compares the current workflow state with the latest saved snapshot when one exists.
- `programstart state rollback` refuses to run unless `--confirm` is provided and creates a pre-rollback backup before restoring state.

## Out Of Scope

- Networked or multi-user state restoration workflows
- Automatic rollback without an explicit operator confirmation flag

## Assumptions

| Assumption | Risk if wrong | Owner |
|---|---|---|
| Workflow-state snapshots stored locally are sufficient for operator rollback and comparison needs. | Operators may need external snapshot storage or richer recovery tooling. | Solo operator |

---
