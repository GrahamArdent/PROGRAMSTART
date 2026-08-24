---
description: "Just-in-Time source-of-truth protocol for planning, architecture, implementation, and config work."
name: "Source-of-Truth JIT Protocol"
applyTo: "{PROGRAMBUILD,USERJOURNEY,config,scripts}/**"
---
# Source-of-Truth JIT Protocol

This protocol exists to prevent two opposite failures:

- acting from stale conversational memory;
- loading/rechecking the whole project for every small task.

Use the smallest current authority/evidence set that safely supports the task.

## 1. Establish live orientation

At a new task/session, use current machine state rather than memory:

```text
programstart status
programstart guide --system <programbuild|userjourney>
```

The guide defines the **allowed baseline authority surface**, not a requirement to fully read every listed file.

## 2. Narrow to the current slice

For PROGRAMBUILD work, define a work packet using `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`.

A work packet is a logical execution contract. Use the compact form by default. Persist `CURRENT_WORK_PACKET.md` only when multi-session/multi-agent coordination, risk, dependency complexity, blockers, or resumability make the file useful.

The current slice must identify:

- objective and non-goals;
- strategic authority/stage that permits it;
- exact authority sections/IDs needed now;
- reusable evidence;
- invalidation triggers;
- acceptance criteria;
- targeted verification.

A work packet never redefines strategy, requirements, architecture, or decision authority.

## 3. Canonical before dependent

When changing planning authority, registry/config policy, or another canonical process concern:

1. identify the concern owner from current registry/authority guidance;
2. check relevant baseline drift before making the authority change;
3. update the canonical owner first;
4. derive dependent changes from that authority;
5. refresh the current slice if the authority change affects it.

Use `programstart drift` when authority/registry drift is relevant. Do not run it reflexively for unrelated implementation slices.

## 4. Verify what changed or became at risk

Always ask:

1. What changed?
2. What can that change invalidate?
3. Which existing evidence remains trustworthy?
4. What is the smallest sufficient check that closes the remaining uncertainty?
5. Is this a convergence boundary that requires wider verification?

For planning-authority/registry changes, use the repository's required validation + drift gate.

For bounded implementation, use targeted checks plus any broader checks triggered by invalidation, shared-contract impact, stage transition, release readiness, or another meaningful convergence condition.

Do not repeat broad verification just because a session changed.

## 5. Reconcile durable state

After the slice:

- record material decisions in the correct durable authority;
- update requirements/architecture/status only when the result actually changes them;
- record verification evidence once;
- close/replace the packet instead of accumulating a second planning hierarchy.

## 6. Never do these

- assert current authority from memory without reading the relevant current section;
- update a dependent before its authority;
- treat a work packet/research/audit/readiness review as a competing master plan;
- speculatively load every planning file “just in case”;
- rerun broad checks without an invalidation/convergence reason;
- create persistent work-packet paperwork when a compact task/PR representation is sufficient;
- use a fixed feature count or calendar cadence as proof that convergence is required.

## Authority quick reference

| Concern | Canonical owner |
|---|---|
| Document authority/conflict rules | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` |
| Planning/JIT/evidence/proportional rigor | `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| Work-packet semantics | `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` |
| Stage sequencing | `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md` |
| Gate selection/convergence | `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` |
| Product architecture/contracts | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements/scope | `PROGRAMBUILD/REQUIREMENTS.md` |
| Product decisions/reversals | `PROGRAMBUILD/DECISION_LOG.md` |
| USERJOURNEY execution order | `USERJOURNEY/DELIVERY_GAMEPLAN.md` |
| Registry | `config/process-registry.json` |
| Prompt standard | `.github/prompts/PROMPT_STANDARD.md` |

## Temporal semantics

- Validated behavior may reveal that planning documentation is stale; reconcile stale authority when discovered.
- Before intentionally creating new behavior that contradicts current authority, update the authority in the same coherent change first.
- “Never from memory” means re-read the relevant current authority after session/context reset; it does **not** mean re-read the repository.
- Existing verification remains usable until a documented invalidation trigger occurs or a required convergence boundary calls for broader proof.
