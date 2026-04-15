---
status: superseded by ADR-0011
date: 2026-04-12
deciders: [Solo operator]
consulted: []
informed: []
---

# 0008. Cross-cutting prompts registered at workflow_guidance level

<!-- DEC-005 -->

## Context and Problem Statement

Stage guide prompts such as `programstart-stage-guide` and `programstart-stage-transition` apply to every stage. Registering them individually in each stage's `prompts` array creates N duplicate entries and a maintenance burden whenever a cross-cutting prompt is added or renamed.

## Decision Drivers

- Avoid polluting every stage's prompts array with identical entries.
- Provide a single registration point for prompts that span all stages.
- Keep `programstart_step_guide.py` display logic simple — merge at render time.

## Considered Options

- Option A — Add cross-cutting prompts to every stage's `prompts` array.
- Option B — Register them once in a `cross_cutting_prompts` array at the `workflow_guidance` level and merge at display time.

## Decision Outcome

Chosen option: **Option B**, because it eliminates duplication and gives a single place to manage prompts that apply everywhere.

### Consequences

- Good: Single registration point; `programstart guide` shows cross-cutting prompts at every stage without per-stage edits.
- Good: Adding a new cross-cutting prompt requires one line in `process-registry.json`.
- Bad: `programstart_step_guide.py` must know to merge the array — minor code complexity.

## Confirmation

`uv run programstart guide` lists cross-cutting prompts at every stage. `uv run programstart validate --check all` passes with no warnings for DEC-005.

## Links

- DEC-005 in `PROGRAMBUILD/DECISION_LOG.md`
- `config/process-registry.json` — `workflow_guidance.cross_cutting_prompts`
- `scripts/programstart_step_guide.py` — merge logic
