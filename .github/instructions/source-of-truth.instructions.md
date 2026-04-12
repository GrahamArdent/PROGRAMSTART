---
description: "Just-in-Time source-of-truth loading protocol. Use when working on any planning, architecture, implementation, or config task to prevent drift and avoid stale context."
name: "Source-of-Truth JIT Protocol"
applyTo: "{PROGRAMBUILD,USERJOURNEY,config,scripts}/**"
---
# Source-of-Truth JIT Loading Protocol

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

This protocol prevents context drift from accumulating across conversations.
You MUST apply it before any task that reads or changes planning documents, config, or scripts.

## Step 1 — Derive context from the registry, not memory

Before opening any document, run:

```
programstart guide --system <programbuild|userjourney>
```

You MUST load only the files it returns. You MUST NOT speculatively open additional docs.
You MUST NOT use a previous conversation's memory of what a doc said — re-read it.

## Step 2 — Know your baseline before changing anything

Before any edit that touches a planning doc, run:

```
programstart drift
```

If that reports violations, you MUST stop and resolve them before adding new changes.
A clean baseline is required.

## Step 3 — Canonical before dependent

When a change is required:

1. Identify the **authority file** for the concern (use `config/process-registry.json` `sync_rules` to find it).
2. You MUST update the authority file first.
3. You MUST derive dependent file changes from the authority content — you MUST NOT invent.
4. You SHOULD use the `/propagate-canonical-change` prompt if the authority change has downstream dependents.

## Step 4 — Verify after every change set

After any set of edits, run both:

```
programstart validate --check all
programstart drift
```

Both MUST pass before moving on.

## What to never do

- You MUST NOT assert what a source-of-truth doc says from memory. Read it.
- You MUST NOT update a dependent file before its authority file.
- You MUST NOT skip `programstart drift` before editing because "it's probably fine."
- You MUST NOT add behaviour to downstream docs that the authority docs do not define.
- You MUST NOT carry over assumptions about active stage, active phase, or key decisions between sessions.

## Quick reference: authority files by concern

| Concern | Authority file |
|---|---|
| Stage order and gates | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` |
| Which files are control files | `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` |
| Product architecture and contracts | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements and scope | `PROGRAMBUILD/REQUIREMENTS.md` |
| Product user flows | `PROGRAMBUILD/USER_FLOWS.md` |
| USERJOURNEY execution order | `USERJOURNEY/DELIVERY_GAMEPLAN.md` |
| Route, state, activation rules | `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` |
| Legal and consent behaviour | `USERJOURNEY/LEGAL_AND_CONSENT.md` |
| Decisions and reversals | `USERJOURNEY/DECISION_LOG.md` |
| Registry of all rules | `config/process-registry.json` |

## Product-level JIT during implementation

The protocol above applies to process/planning tasks. During active implementation (Stage 7),
you MUST also apply JIT to *product* authority docs:

- Before writing code for a feature, re-read the applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md`.
- Before writing code for a feature, re-read the relevant requirement in `PROGRAMBUILD/REQUIREMENTS.md`.
- You MUST NOT implement from memory. Re-read the actual doc.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first (canonical-before-dependent).
- If you discover a new contract, endpoint, or auth rule not in `ARCHITECTURE.md`, record it in `DECISION_LOG.md` and update `ARCHITECTURE.md` in the same commit.
- Every 3–5 features, re-read the full contracts section of `ARCHITECTURE.md` to catch silent drift.

## Temporal semantics

- "MUST outrank" (`PROGRAMBUILD_CANONICAL.md` rule 1) applies **retroactively**: when an existing conflict between validated code and a planning document is discovered, code is the source of truth.
- "MUST update the authority document first" applies **prospectively**: before writing new code that would contradict an authority doc, update the doc first.
- "Before" in canonical-before-dependent means in the same commit or PR, not in a separate change.
- "Never from memory" means re-read on each new session or after context window reset, not just across conversations.
