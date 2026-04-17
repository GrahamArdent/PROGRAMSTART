---
status: accepted
date: 2026-04-18
deciders: [Solo operator]
consulted: []
informed: []
---

# 0019. Typed Pydantic Models for Process Registry

<!-- DEC-016 -->

## Context and Problem Statement

`load_registry()` returns an untyped `dict[str, Any]`. Every consumer must do manual key access, hope the key exists, and hope the value has the expected type. This defeats the purpose of having a structured registry and creates silent failures when the registry evolves.

## Decision Drivers

- Type safety: IDEs and pyright should catch key/type errors at edit time, not runtime.
- Backward compatibility: the existing `dict[str, Any]` API is used in 10+ scripts; breaking it would be high-risk.
- Schema evolution: the registry gains new keys every few sessions; models must tolerate additions.
- Import weight: Pydantic is an optional dependency for some consumers; models must not force a hard import at module load time.

## Considered Options

- Option A — Replace `load_registry()` return type with a Pydantic model
- Option B — Add a parallel `load_validated_registry()` that returns a Pydantic model alongside the existing dict API
- Option C — Use TypedDict instead of Pydantic

## Decision Outcome

Chosen: **Option B** — parallel `load_validated_registry()` alongside existing `load_registry()`.

### Consequences

- Good: full Pydantic validation, IDE autocomplete, pyright enforcement — all opt-in.
- Good: existing dict API unchanged; zero migration required.
- Good: lazy import pattern (`from .programstart_models import ProcessRegistry` inside the function body) avoids hard Pydantic dependency at module-load time.
- Good: `model_config = {"extra": "allow"}` on evolution-prone models tolerates new registry keys without model updates.
- Neutral: consumers must explicitly call `load_validated_registry()` to get typed access.
- Bad: two loading functions to maintain — but the validated one is a thin wrapper.

## Implementation Notes

- 17 model classes added to `scripts/programstart_models.py`: `SyncRule`, `MetadataRules`, `ValidationPolicy`, `RepoBoundaryDoc`, `RepoBoundaryPolicy`, `StageOrderEntry`, `StageGuidance`, `WorkflowGuidance`, `WorkflowStateConfig`, `SystemDefinition`, `PlanningReferenceRules`, `PromptRegistryConfig`, `ManagedStagePrompt`, `PromptGenerationConfig`, `GeneratedRepoPromptPolicy`, `WorkspaceConfig`, `OperatorGameplanEntry`, `ExemptGameplanEntry`, `GameplanPromptPolicy`, `AdrPolicy`, `ManifestCollectionConfig`, `BaselineEntry`, `IntegrityConfig`, `ProcessRegistry` (root model).
- `load_validated_registry()` added to `scripts/programstart_common.py` with `TYPE_CHECKING` guard for pyright and lazy runtime import.
- Round-trip property: `ProcessRegistry.model_validate(load_registry()).model_dump()` produces a valid dict indistinguishable from the original.

## Confirmation

- All 1752 tests pass.
- pyright clean on both modified files.
- Pre-commit all-files clean.
