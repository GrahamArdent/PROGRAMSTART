# DECISION_LOG.md

Purpose: Running record of material project decisions, reversals, and rationale.
Owner: Solo operator
Last updated: 2026-04-11
Depends on: FEASIBILITY.md, RESEARCH_SUMMARY.md, ARCHITECTURE.md
Authority: Canonical for project decision history

---

## Status Vocabulary

| Status | Meaning |
|---|---|
| PROPOSED | Decision is under consideration — not yet committed |
| ACTIVE | Decision is committed and in force |
| REVERSED | This row replaces an earlier decision. The `Replaces` column points to the original ID. |
| SUPERSEDED | This original decision has been overridden. See the `Replaces` column of the REVERSED entry. |

**Reversal rule:** When a decision is overridden, add a new REVERSED row and update the original row's status to SUPERSEDED. Both rows must exist — do not delete the original. See `PROGRAMBUILD_CHALLENGE_GATE.md` Part F for the enforcement rules.

---

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-04-11 | inputs_and_mode_selection | Root-workspace smoke MUST be read-only; mutating dashboard smoke MUST run only in isolated temp workspaces | ACTIVE | — | Solo operator | noxfile.py, scripts/programstart_dashboard_smoke.py |

## Decision Details

### DEC-001

- Context: Dashboard smoke script exercises 3 POST routes that mutate the live workspace (uj-phase, uj-slice, workflow-signoff). Only workflow-advance uses dry_run. The signoff route is accumulative — each run adds a new history entry to STATE.json.
- Decision: Read-only smoke for root workspace. Mutating smoke isolated to bootstrapped temp workspaces only.
- Why: Trust boundary. Operators must trust that orientation tools (guide, drift, dashboard) do not silently change state. Repeated smoke runs must not leave artifacts.
- Alternatives considered: (1) Add dry_run to all POST routes — still requires trusting the flag. (2) Environment variable guard on server — smoke-level isolation is simpler to reason about.
- Consequences: Dashboard smoke split into read-only script and existing mutating script. CI continues running mutating smoke in bootstrapped workspaces. Root-workspace smoke is guaranteed non-mutating.
- Follow-up: Phase 1.5 may add route-level read-only guard for defense-in-depth.

---
