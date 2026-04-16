---
status: accepted
date: 2026-04-15
deciders: [Solo operator]
consulted: []
informed: []
---

# 0014. Compose process registry from a manifest and fragments

<!-- DEC-011 -->

## Context and Problem Statement

`config/process-registry.json` had become a large monolithic authority file that mixed workspace asset inventory, workflow guidance, prompt metadata, sync rules, and workflow-state configuration. That structure made high-signal changes unnecessarily risky because unrelated sections shared one edit surface, while scripts and tests across the repo still depended on a single `load_registry()` contract. Phase J-2 needed to reduce that edit blast radius without breaking runtime consumers or generated project repositories.

## Decision Drivers

- Registry changes should be partitioned by concern instead of forcing one large shared JSON edit surface.
- Runtime and tooling consumers must keep a stable merged registry contract.
- Generated project repos must not accidentally inherit PROGRAMSTART-only fragment behavior.
- Schema and pre-commit enforcement must validate the real merged registry, not only the manifest shell.
- Migration must preserve backward compatibility for existing validation, prompt, and workflow-state code.

## Considered Options

- Option A — Keep one monolithic `config/process-registry.json` and continue updating it in place.
- Option B — Introduce a root manifest with fragment includes, load a merged registry in shared code, and stamp generated repos back to a flat registry.
- Option C — Split the registry and require every consumer, including generated repos, to become fragment-aware immediately.

## Decision Outcome

Chosen option: **Option B**, because it fixes the template-repo edit-surface problem while preserving a stable consumer contract and avoiding forced fragment-awareness in downstream generated repos.

### Consequences

- Good: Template registry changes are now localized by concern under `config/registry/`.
- Good: `load_registry()` remains the single stable runtime contract for scripts and tests.
- Good: Schema validation and health tooling now validate the fully composed registry.
- Good: Bootstrapped project repos remain backward-compatible because bootstrap resolves the manifest and writes a flat project registry.
- Bad: Registry composition adds one more abstraction layer that tooling must understand.
- Bad: Bootstrap asset inventory and validation coverage must now include fragment files and schema-check enforcement.
- Neutral: The root `config/process-registry.json` remains the canonical entrypoint, but no longer stores the full payload inline.

## Pros and Cons of the Options

### Option A

- Good, because it avoids migration work.
- Bad, because it keeps one large conflict-prone edit surface.
- Bad, because unrelated governance, workflow, and prompt changes remain tightly coupled.

### Option B

- Good, because it partitions registry concerns while preserving one merged consumer interface.
- Good, because it lets generated repos stay simple and flat after bootstrap.
- Bad, because loaders, tests, and validation hooks need coordinated updates.

### Option C

- Good, because it maximizes consistency between template and generated repos.
- Bad, because it forces fragment-awareness into downstream repos that do not need that complexity.
- Bad, because it would create unnecessary migration churn across bootstrap, attach, and validation flows.

## Confirmation

This decision is implemented correctly when all of the following are true:

- `config/process-registry.json` acts as a manifest entrypoint and loads fragment files through shared registry helpers.
- Scripts and tests that need registry data read the composed registry contract rather than assuming the root file is a complete payload.
- Schema and validation hooks evaluate the merged registry successfully.
- Bootstrapped project repos validate successfully without requiring fragment-aware loading semantics.

## Links

- [0011-separate-workflow-and-operator-prompt-architecture.md](0011-separate-workflow-and-operator-prompt-architecture.md)
- [DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
- [config/process-registry.json](../../config/process-registry.json)
- [scripts/programstart_common.py](../../scripts/programstart_common.py)
- [scripts/programstart_bootstrap.py](../../scripts/programstart_bootstrap.py)
