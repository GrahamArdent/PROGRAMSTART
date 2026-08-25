---
status: accepted
date: 2026-08-25
deciders: [solo operator]
consulted: []
informed: []
---

# 0024. Rank Current Product Authority over Legacy Repository Evidence in Mode C

## Context and Problem Statement

A real-world Mode-C acceptance test exposed an authority ambiguity in PROGRAMBUILD.

The existing-project rules correctly said to preserve the project's execution spine and reuse repository evidence, but they did not explicitly define what to do when historical repository artifacts conflict with newer product intent.

In the acceptance test, a legacy `README.md` described the repository as a Streamlit application and included a runnable Streamlit command. Because repository state had been treated broadly as authoritative, that historical implementation description was incorrectly elevated into rebuild direction even though newer project work had moved beyond the prototype.

This is a reusable methodology defect. The same failure could occur with any legacy README, framework, dependency, UI prototype, database choice, API style, architecture artifact, or run command.

## Decision Drivers

- Preserve existing-project product intent rather than accidentally resurrecting obsolete implementation choices.
- Keep repository state authoritative for current technical reality without confusing reality with strategic intent.
- Prevent README files and legacy code from silently becoming requirements.
- Make Mode-C orientation deterministic when evidence conflicts.
- Preserve useful historical implementation evidence for migration and salvage decisions.
- Avoid forcing operators to restate decisions that are already persisted in higher-authority project artifacts.

## Considered Options

1. **Keep repository state broadly authoritative.** Let agents infer rebuild direction from the strongest visible repository signals.
2. **Ignore legacy implementation evidence.** Treat old code, README files, and dependencies as untrusted and rebuild only from planning documents.
3. **Define explicit Mode-C authority precedence.** Separate product-intent authority from implementation evidence and require reconciliation before deriving rebuild direction.

## Decision Outcome

Chosen option: **3 — explicit Mode-C authority precedence with a legacy-evidence guard**.

For product intent, Mode C SHOULD rank evidence in this order unless the project defines a more specific hierarchy:

1. current explicit operator/user decisions;
2. the project's designated execution spine or canonical strategic authority;
3. accepted and persisted product decisions, requirements, architecture, and decision records;
4. current implementation and tests as evidence of actual behavior;
5. descriptive documentation such as `README.md`;
6. legacy code, historical frameworks, archived artifacts, and obsolete dependencies as migration/history evidence.

Repository state remains authoritative for **what currently exists and behaves**. It is not automatically authoritative for **what the product has been decided to become**.

A README, dependency, framework, prototype UI, historical run command, or legacy implementation MUST NOT by itself become a rebuild requirement or strategic direction.

Before selecting or implementing a Mode-C rebuild slice, the agent MUST reconcile apparent repository behavior with current product authority. If they conflict, the conflict must be named and the higher-ranked current authority followed. Lower-ranked artifacts remain useful migration, salvage, compatibility, and historical evidence unless the project deliberately re-adopts them.

### Consequences

- Good: Existing-project rebuilds are less likely to resurrect obsolete stacks or prototype shapes.
- Good: Repository evidence remains useful for understanding current behavior and migration cost.
- Good: README files keep their descriptive role without silently becoming strategic authority.
- Good: Mode-C agents have a deterministic conflict-resolution rule before implementation begins.
- Good: Previously accepted product decisions can be reused without unnecessary operator repetition.
- Bad: Agents must spend a small amount of effort identifying whether an artifact describes current intent or only historical implementation.
- Bad: Projects with no clear strategic authority may expose ambiguity that must be resolved before a large rebuild decision.
- Neutral: This does not prohibit retaining a legacy framework; it requires an explicit current reason to retain it.

## Confirmation

This decision is implemented when:

- the Mode-C `shape-idea` prompt distinguishes current technical reality from current product intent;
- the prompt contains an explicit authority-precedence rule;
- README/framework/prototype evidence is explicitly prevented from becoming rebuild direction by itself;
- Mode-C orientation requires reconciliation before the first rebuild slice is selected;
- regression coverage fails if those safeguards are removed;
- future existing-project adoption work treats legacy artifacts as evidence rather than implicit requirements.

## Links

- [Planning operating model](../../PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md)
- [Idea intake protocol](../../PROGRAMBUILD/PROGRAMBUILD_IDEA_INTAKE.md)
- [Mode-C shape prompt](../../.github/prompts/shape-idea.prompt.md)
- [Strategic execution spine decision](0023-use-one-strategic-execution-spine-with-bounded-work-packets.md)
