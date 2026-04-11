---
status: accepted
date: 2026-03-31
deciders: [project owner]
consulted: []
informed: []
---

# 0003. Adopt MADR 4.0 for Architecture Decision Records

## Context and Problem Statement

`PROGRAMBUILD_ADR_TEMPLATE.md` existed but used a minimal bespoke format — no YAML frontmatter, no Decision Drivers section, no Pros/Cons evaluation, no Confirmation step. Decisions recorded in this format lacked the metadata needed to programmatically query status, relate records to each other, or confirm implementation.

## Decision Drivers

- Interoperability with ADR tooling (e.g., `adr-tools`, IDE plugins) that expect MADR YAML frontmatter.
- Status lifecycle (`proposed → accepted → superseded`) makes change tracking unambiguous.
- Confirmation section creates an actionable link between the decision and its verification.
- Structured options and pros/cons improve the quality of reasoning captured.

## Considered Options

- Option A — MADR 4.0 (this decision)
- Option B — Homebrew format (keep existing minimal template)
- Option C — Nygard-style ADRs (flat prose, no frontmatter)
- Option D — Architecture Decision Log in a single file

## Decision Outcome

Chosen option: **Option A (MADR 4.0)**, because it is the most widely adopted Markdown ADR standard with YAML frontmatter, good tooling support, and a clear status lifecycle. The Confirmation section directly ties the decision to a testable assertion.

### Consequences

- Good: Status field enables automated queries for "all accepted decisions" or "all decisions superseded since date X."
- Good: Decision index at `docs/decisions/README.md` provides a single entry point.
- Bad: Slightly more verbose than the prior template — adds setup cost per ADR.
- Neutral: `PROGRAMBUILD_ADR_TEMPLATE.md` is now the authority for MADR format in this system (existing `config/process-registry.json` authority map entry is unchanged).

## Confirmation

`docs/decisions/README.md` MUST be updated whenever a new ADR is added.
`PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` is the canonical source for the template — any format divergence in a decision file is a drift violation.

## Links

- [MADR GitHub](https://adr.github.io/madr/)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
- [docs/decisions/README.md](README.md)
