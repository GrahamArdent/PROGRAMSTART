---
status: superseded by ADR-0013
date: 2026-04-15
deciders: [Solo operator]
consulted: []
informed: []
---

# 0012. Require ADR triage and targeted audit loop for structural hardening checkpoints

<!-- DEC-009 -->

## Context and Problem Statement

PROGRAMSTART hardening work has moved beyond small coverage pushes into structural refactors and workflow-policy changes. Those sessions already end with tests, validation, drift, and typecheck, but the hardening protocol did not explicitly require an ADR decision or a targeted governance review at each checkpoint. Because the broader PROGRAMBUILD audit model concentrates its full audit at Stage 9, strategic hardening sessions could finish technically green while leaving the architecture-history decision implicit.

## Decision Drivers

- Structural hardening checkpoints must remain auditable, not just green.
- ADR discipline must remain active during refactors and workflow-policy changes.
- Authority-sync drift should be checked before a strategic hardening session is considered done.
- Future sessions need a deterministic rule instead of relying on memory.

## Considered Options

- Option A — Keep the current hardening protocol and rely on final audit or reviewer discretion.
- Option B — Add an explicit close-out loop for structural hardening work: ADR triage plus targeted authority/audit checks.
- Option C — Require a full Stage 9-style audit after every hardening phase.

## Decision Outcome

Chosen option: **Option B**, because it adds the missing governance checkpoint without turning every hardening session into a full audit ceremony.

### Approved Decisions

1. **Hardening does not bypass ADR discipline.**
   Structural, workflow-policy, authority, or trust-boundary changes made during hardening must go through explicit ADR triage before the checkpoint is closed.

2. **A targeted close-out loop is required.**
   Before marking an eligible hardening checkpoint complete, run:

   ```powershell
   uv run programstart validate --check adr-coverage
   uv run programstart validate --check authority-sync
   uv run programstart drift
   ```

3. **ADR threshold remains the existing PROGRAMBUILD threshold.**
   The decision to create an ADR is still governed by `PROGRAMBUILD/PROGRAMBUILD.md` and `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md`; this ADR adds timing and enforcement, not a new threshold.

4. **Phase J is always in scope for the loop.**
   Every individual `J-*` item is a dedicated strategic session and must complete the close-out loop before it is marked done.

5. **Checkpoint notes must state the outcome.**
   A hardening checkpoint must record whether ADR triage resulted in a new or updated ADR, or explicitly state that no ADR was required.

### Open Exclusions

- Replacing the PROGRAMBUILD Stage 9 audit with hardening-session checks.
- Requiring a full audit report after every hardening phase.
- Changing the existing ADR threshold criteria.
- Expanding this rule to unrelated feature work outside the hardening protocol.

### Consequences

- Good: Strategic hardening sessions now have an explicit governance checkpoint.
- Good: ADR creation becomes an intentional close-out decision instead of an implicit afterthought.
- Good: Authority-sync drift is checked during structural hardening, not only later.
- Bad: Hardening sessions gain a small amount of extra ceremony.
- Neutral: Some sessions will explicitly conclude that no ADR is needed; that is expected and still useful.

## Pros and Cons of the Options

### Option A

- Good, because it keeps the current hardening flow short.
- Bad, because it leaves ADR need ambiguous at the exact point where structural changes land.

### Option B

- Good, because it closes the governance gap with minimal additional process.
- Good, because it reuses existing validation and drift checks.
- Bad, because it adds another explicit checkpoint to strategic sessions.

### Option C

- Good, because it would maximize audit rigor.
- Bad, because it is too heavy for every hardening checkpoint and would slow the work materially.

## Confirmation

This decision is implemented correctly when all of the following are true:

- The hardening execution prompt requires ADR triage and targeted close-out checks for structural hardening work.
- The hardening gameplan tells operators to perform that loop for every `J-*` item.
- The decision trail links this rule to both the DECISION_LOG and ADR index.
- Future strategic hardening checkpoints record whether an ADR was required.

## Links

- [README.md](README.md)
- [0013-require-governance-close-out-for-durable-operator-checkpoints.md](0013-require-governance-close-out-for-durable-operator-checkpoints.md)
- [DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD.md](../../PROGRAMBUILD/PROGRAMBUILD.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
- [execute-hardening-gameplan.prompt.md](../../.github/prompts/execute-hardening-gameplan.prompt.md)
- [hardeninggameplan.md](../../devlog/gameplans/hardeninggameplan.md)
