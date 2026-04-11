---
status: accepted
date: 2026-03-27
deciders: [project owner]
consulted: []
informed: []
---

# 0001. Use PROGRAMBUILD Workflow System as Repository Scaffold

## Context and Problem Statement

Starting a software project from a blank slate means repeatedly hand-crafting the same planning structure — stage gates, file inventories, authority maps, drift detection, and validation tooling — across every project. Without a reusable scaffold, these artifacts drift, lack consistency, and are often missing entirely.

## Decision Drivers

- Need for a repeatable, auditable delivery infrastructure across projects.
- Desire to automate drift detection and authority-chain enforcement rather than relying on human memory.
- Template-first approach enables faster project kickoff without sacrificing rigor.

## Considered Options

- Option A — PROGRAMBUILD repo scaffold (this system)
- Option B — Plain README + backlog in a project management tool
- Option C — Adopt an existing OSS planning framework (OpenAgile, SAFe, etc.)

## Decision Outcome

Chosen option: **Option A (PROGRAMBUILD)**, because it provides machine-readable stage gates, drift detection, schema-validated state files, and reusable prompt workflows while remaining lightweight enough for solo/small team use.

### Consequences

- Good: Consistent planning structure across projects; automated validation.
- Good: Canonical authority chain prevents conflicting sources of truth.
- Bad: Adds repo infrastructure overhead that small throw-away experiments may not need.
- Neutral: Projects using this scaffold must follow the canonical update protocol when changing stage order or file inventory.

## Confirmation

`scripts/programstart_validate.py --check all` must pass on every commit that touches `PROGRAMBUILD/`, `USERJOURNEY/`, `config/`, or `scripts/`.

## Links

- [PROGRAMBUILD_CANONICAL.md](../../PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md)
- [PROGRAMBUILD_FILE_INDEX.md](../../PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md)
