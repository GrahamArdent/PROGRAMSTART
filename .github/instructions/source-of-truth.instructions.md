---
description: "Just-in-Time source-of-truth loading protocol. Use when working on any planning, architecture, implementation, or config task to prevent drift and avoid stale context."
name: "Source-of-Truth JIT Protocol"
applyTo: "{PROGRAMBUILD,USERJOURNEY,config,scripts}/**"
---
# Source-of-Truth JIT Loading Protocol

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

This protocol prevents context drift from accumulating across conversations while also preventing unnecessary full-context reloads and repetitive verification.
You MUST apply it before any task that reads or changes planning documents, config, scripts, or implementation governed by those documents.

## Step 1 — Establish the stage baseline from the registry, not memory

Before opening planning documents, run:

```
programstart guide --system <programbuild|userjourney>
```

The guide output defines the **allowed baseline context** for the current stage or phase. You MUST NOT speculatively open unrelated planning docs or use a previous conversation's memory of what a document said.

The guide output is not an instruction to fully re-read every listed file for every task. For a bounded task, Step 2 narrows that baseline to the smallest authoritative context needed for the current slice.

## Step 2 — Narrow the current task with a work packet when useful

For non-trivial PROGRAMBUILD execution work, use `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` to derive or refresh `CURRENT_WORK_PACKET.md` from the project's authoritative execution spine and current stage.

A work packet MUST:

- name the strategic execution spine or canonical stage that authorizes the work;
- state the bounded objective and explicit non-goals;
- list the exact authority files or sections needed for the slice;
- list specialist/reference material needed only for this task;
- record trusted existing verification evidence that can be reused;
- state what changes would invalidate that evidence;
- define acceptance criteria and targeted verification for the slice.

`CURRENT_WORK_PACKET.md` is derived execution state. It MUST NOT redefine strategy, requirements, architecture, or decision authority. If it conflicts with a canonical owner, correct or regenerate the packet.

For a trivial task, an explicit mental or written slice with the same fields is sufficient; do not create ceremony solely to satisfy the template.

## Step 3 — Know your baseline before changing authority

Before edits that change planning authority, registry/config policy, or other canonical process state, run:

```
programstart drift
```

If that reports violations, you MUST resolve them before adding a new authority change.

For a bounded implementation task that does not change planning authority, use the work packet's trusted evidence and invalidation triggers to decide what must be rechecked. Do not repeat broad validation merely because it ran in a previous slice.

## Step 4 — Canonical before dependent

When an authority change is required:

1. Identify the **authority file** for the concern (use `config/process-registry.json` and the PROGRAMBUILD authority map).
2. You MUST update the authority file first.
3. You MUST derive dependent file changes from the authority content — you MUST NOT invent.
4. You SHOULD use the `/propagate-canonical-change` prompt if the authority change has downstream dependents.
5. If the change alters the current implementation slice, refresh the work packet after the authority change.

## Step 5 — Verify what changed or became at risk

Verification MUST be proportional to the change.

Always ask:

1. What changed?
2. Which contracts, requirements, decisions, or behaviors could that change invalidate?
3. Which existing evidence is still trustworthy because its invalidation trigger did not occur?
4. What is the smallest test/validation set that proves the changed or at-risk surface?

After planning-authority or registry changes, run:

```
programstart validate --check all
programstart drift
```

For implementation slices, run the targeted checks named in the current work packet, plus any broader gate required by the stage or release boundary. A full validation suite is appropriate at convergence points, not automatically after every small slice.

## What to never do

- You MUST NOT assert what a source-of-truth doc says from memory. Read the relevant current section.
- You MUST NOT update a dependent file before its authority file.
- You MUST NOT treat `CURRENT_WORK_PACKET.md`, research, an audit, or a readiness review as a competing master plan.
- You MUST NOT speculatively load every planning document "just in case."
- You MUST NOT repeat broad verification without identifying an invalidation reason or a required convergence gate.
- You MUST NOT add behaviour to downstream docs that the authority docs do not define.
- You MUST NOT carry over assumptions about active stage, active phase, or key decisions between sessions.

## Scope

This protocol applies to all product prompts in `.github/prompts/` and all planning documents.
Internal build prompts in `.github/prompts/internal/` and development logs in `devlog/` are exempt — they are historical PROGRAMSTART development artifacts, not part of the product authority model.

## Quick reference: authority files by concern

| Concern | Authority file |
|---|---|
| Document authority and conflict rules | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` |
| Planning-to-execution separation, proportional rigor, context loading, evidence reuse | `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| Active work-packet structure | `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` |
| Which files are control files | `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` |
| Product architecture and contracts | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements and scope | `PROGRAMBUILD/REQUIREMENTS.md` |
| Product user flows | `PROGRAMBUILD/USER_FLOWS.md` |
| Product decisions and reversals | `PROGRAMBUILD/DECISION_LOG.md` |
| USERJOURNEY execution order | `USERJOURNEY/DELIVERY_GAMEPLAN.md` |
| Route, state, activation rules | `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` |
| Legal and consent behaviour | `USERJOURNEY/LEGAL_AND_CONSENT.md` |
| USERJOURNEY decisions and reversals | `USERJOURNEY/DECISION_LOG.md` |
| Registry of all rules | `config/process-registry.json` |
| Prompt standard | `.github/prompts/PROMPT_STANDARD.md` |

## Product-level JIT during implementation

During active implementation (Stage 7), apply JIT at two levels:

### Stage baseline

Use `programstart guide --system programbuild` to establish the allowed authority surface for implementation.

### Current slice

Use the work packet to identify the exact parts of that authority surface needed now.

- Re-read the applicable contract rows/sections in `PROGRAMBUILD/ARCHITECTURE.md` before changing that contract surface.
- Re-read the requirement IDs and acceptance criteria in `PROGRAMBUILD/REQUIREMENTS.md` that authorize the slice.
- Re-read the relevant user-flow section only when user/state behavior is affected.
- Re-read decision-log entries only for decisions that constrain the current slice.
- Reuse still-valid test or environment evidence when its documented invalidation triggers have not occurred.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first (canonical-before-dependent).
- If you discover a new contract, endpoint, or auth rule not in `ARCHITECTURE.md`, record the decision and update `ARCHITECTURE.md` before implementing the contradiction.
- At periodic convergence points (for example every 3–5 features, a stage transition, or release readiness), run the broader cross-stage/gate checks required by PROGRAMBUILD.

## Temporal semantics

- "MUST outrank" (`PROGRAMBUILD_CANONICAL.md` rule 1) applies **retroactively**: when an existing conflict between validated code and a planning document is discovered, validated behavior is the source of truth and the documentation must be reconciled.
- "MUST update the authority document first" applies **prospectively**: before writing new code that would contradict an authority doc, update the doc first.
- "Before" in canonical-before-dependent means in the same commit or PR, not in a separate change.
- "Never from memory" means re-read the relevant current authority on each new session or after context reset; it does not mean re-read every project document for every small task.
- Existing verification remains usable until a documented invalidation trigger occurs or a required convergence gate demands a broader rerun.
