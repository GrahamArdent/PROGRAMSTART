---
status: accepted
date: 2026-04-13
deciders: [Solo operator]
consulted: []
informed: []
---

# 0009. Canonical section alignment in shaping prompts

<!-- DEC-006 -->

## Context and Problem Statement

The seven stage shaping prompts (`shape-research` through `shape-post-launch-review`) cited `PROGRAMBUILD_CANONICAL.md §N` in their Authority Loading section but omitted `PROGRAMBUILD.md §N`. The Protocol Declaration already referenced `PROGRAMBUILD.md §N`, yet without pre-loading that file the AI could proceed without reading the procedural protocol. `PROGRAMBUILD_CANONICAL.md` provides stage boundaries and required output lists; `PROGRAMBUILD.md` provides the procedural protocol for how to do the work. Both are needed for complete authority coverage.

## Decision Drivers

- Authority Loading must pre-load every file referenced in Protocol Declaration.
- `PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD.md` serve complementary roles (what vs. how).
- Seven prompts were affected; consistency across all shaping prompts matters.

## Considered Options

- Option A — Remove `PROGRAMBUILD.md §N` from Protocol Declaration to match Authority Loading.
- Option B — Add `PROGRAMBUILD.md §N` to Authority Loading in all 7 shaping prompts.

## Decision Outcome

Chosen option: **Option B**, because removing the Protocol Declaration reference would weaken protocol clarity. Loading both files ensures the AI has complete authority context before beginning work.

### Consequences

- Good: All 7 stage shaping prompts now pre-load both authority files before beginning work.
- Good: Consistent pattern — Authority Loading always covers Protocol Declaration references.
- Neutral: Slightly more text in each prompt's Authority Loading section.

## Confirmation

Review all `shape-*.prompt.md` files: each Authority Loading section must list both `PROGRAMBUILD_CANONICAL.md §N` and `PROGRAMBUILD.md §N`. `uv run programstart validate --check all` passes with no warnings for DEC-006.

## Links

- DEC-006 in `PROGRAMBUILD/DECISION_LOG.md`
- `.github/prompts/shape-*.prompt.md` — all 7 affected prompts
