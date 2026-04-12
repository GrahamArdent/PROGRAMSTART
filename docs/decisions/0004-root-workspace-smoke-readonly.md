---
status: accepted
date: 2026-04-11
deciders: [solo operator]
consulted: []
informed: []
---

# 0004. Root-Workspace Smoke Must Be Read-Only

## Context and Problem Statement

The dashboard smoke script (`scripts/programstart_dashboard_smoke.py`) exercises 4 POST routes: `uj-phase`, `uj-slice`, `workflow-signoff`, and `workflow-advance`. Three of these perform real filesystem writes — `uj-phase` and `uj-slice` write to `USERJOURNEY/IMPLEMENTATION_TRACKER.md`, and `workflow-signoff` appends timestamped entries to STATE.json's `signoff_history` array. Only `workflow-advance` has dry-run protection. Running dashboard smoke against the live workspace therefore mutates tracked files, producing artifacts that accumulate over repeated runs.

## Decision Drivers

- Operators must trust that orientation tools (guide, drift, dashboard) do not silently change state.
- Repeated smoke runs against the root workspace should be safe to run any time.
- Smoke isolation is the simplest trust boundary to reason about.

## Considered Options

- Option A — Split smoke into read-only and isolated-write scripts (this decision)
- Option B — Add `dry_run` to all POST routes and trust the flag
- Option C — Environment variable guard on server to reject POST routes

## Decision Outcome

Chosen option: **Option A (split scripts)**, because separate trust boundaries are easier to reason about and harder to misuse. Read-only smoke runs against the root workspace using only GET endpoints. Mutating smoke runs only in bootstrapped temporary workspaces.

### Consequences

- Good: Root-workspace smoke is guaranteed non-mutating. Operators can run it freely.
- Good: CI continues running mutating smoke in bootstrapped workspaces, preserving write-path coverage.
- Bad: Two smoke scripts to maintain instead of one.
- Neutral: `PROGRAMSTART_READONLY=1` environment variable was also added as defense-in-depth, blocking POST routes at the server level.

## Confirmation

- `scripts/programstart_dashboard_smoke_readonly.py` performs only GET requests.
- `nox -s smoke_readonly` runs against the root workspace.
- `nox -s smoke_isolated` runs mutations in a temporary bootstrapped workspace.
- `PROGRAMSTART_READONLY=1` causes the server to reject all POST routes with 405.

## Links

- [DEC-001 in DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
