# PROGRAMSTART Learning Observation — Acceptance Learning Loop Self-Hosting

Status: **subordinate / non-canonical evidence**.

## Observation identity

- **Date:** 2026-08-27
- **Project / repository:** `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** `PSL-013`
- **Checkpoint / acceptance surface:** organization of cross-project learning after PRs #56/#57/#59 and Resume Creator acceptance PR #58
- **Classification:** systemic / self-hosting implementation evidence

## What happened

Real PROGRAMSTART acceptance work had begun updating `docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md`, including Calendar Bridge, Email Bridge, GCRM, Dedication, LinkedIn Generator, and Resume Creator V6. The evidence proved the ledger was useful, but also exposed two structural gaps:

1. normal PROGRAMSTART orchestration did not mechanically require a Learning Gate, so updates depended on an agent deliberately remembering to treat a session as acceptance work;
2. one document was serving both as detailed chronological evidence and as a maturity rollup, making it progressively harder to scan and update safely.

PR #60 implements a conditional Learning Gate and separates append-only observations from the concise maturity ledger.

## Evidence

- Pre-loop detailed ledger blob `1f81c091d0c81561c65ca0212cec324945b9c70b` is preserved unchanged at `docs/acceptance/PROGRAMSTART_ACCEPTANCE_HISTORY_THROUGH_2026-08-27.md`.
- Resume Creator V6 previously added real acceptance evidence through PROGRAMSTART PR #58, proving cross-project learning was already useful even before the formal loop.
- GCRM/PROGRAMSTART PR #59 produced the first observation under `docs/acceptance/observations/`, proving the evidence/rollup split is usable.
- PR #60 adds `docs/PROGRAMSTART_LEARNING_LOOP.md`, the observation template, orchestration prompt v2.5 Learning Gate behavior, checklist updates, authority/index registration, compact maturity ledger, and root changelog reconciliation.
- No product repository was mutated to implement the learning mechanism.
- No local pytest/Ruff/Pyright/`programstart drift`/`nox -s ci` result is claimed in this connected-only environment.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** converted an ad-hoc but useful acceptance practice into an explicit meaningful-checkpoint Learning Gate with conditional persistence and future-retest routing.
- **What helped:** preserved old evidence exactly, reduced the main ledger to a scannable maturity view, and made `no reusable lesson` a first-class result so normal projects are not forced to generate methodology noise.
- **What created friction or uncertainty:** before PR #60, the acceptance checklist said to update the ledger, but the main orchestration prompt did not require that evaluation and there was no evidence/rollup split.
- **Was existing methodology sufficient?** partially; the practice existed but was not reliably routed or organized.

## Learning decision

- **Existing lesson match:** built-in PROGRAMSTART acceptance-learning loop.
- **Maturity before:** candidate / design gap identified from real usage.
- **Maturity after:** implemented.
- **Why maturity changed:** PR #60 implements the protocol and self-hosts the new observation structure, but a future normal product checkpoint has not yet naturally exercised v2.5 and demonstrated the full conditional record/no-record decision in ordinary use.
- **PROGRAMSTART change required now:** PR #60 only; do not add a background daemon, central product registry, or automatic methodology mutation engine.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next meaningful checkpoint in a real PROGRAMSTART-assisted product project after PR #60 merges.
- **What evidence would be sufficient:** PROGRAMSTART automatically evaluates the Learning Gate; either (a) returns `no reusable lesson` without creating noise, or (b) creates/updates a focused observation and maturity rollup when evidence warrants it, while product authority/completion remain independent.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The lesson remains `implemented`, not falsely `validated`, until a future real product checkpoint exercises it.
