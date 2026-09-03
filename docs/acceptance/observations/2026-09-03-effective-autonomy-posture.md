# Learning Observation — Effective Autonomy Posture

**Date:** 2026-09-03  
**System:** PROGRAMSTART / Autonomous Controller / Compute Spine / Portfolio Operations  
**Classification:** systemic methodology improvement / implemented, real retest pending  
**Candidate lesson:** `PSL-021`  
**Status:** subordinate acceptance evidence; do not treat as validation

## Trigger

The autonomous-development ecosystem crossed a practical threshold where execution capability is improving faster than individual project prompts and plans can reasonably be rewritten.

Live evidence now includes:

- Portfolio Operations automatically advancing Controller work through merge and deriving the next packet until a genuine human security decision was reached;
- Autonomous Controller AC-04 accepting a typed Compute Spine -> Execution Node Codex bridge with bounded verification/recovery;
- AC-05-WP1 accepting deterministic human-gate broker semantics;
- Compute Spine explicitly separating concrete execution-fabric authority from Controller semantic continuation authority;
- Secrets Control Plane proving unattended machine identity for the current synthetic/dev Execution Node baseline;
- Mission-Control becoming the intended human command/exception surface.

The operator's desired end state is that technically automatable, already-authorized work should continue without routine human relay while genuine security/business/physical/consequence decisions remain truthful human gates.

## Problem exposed

Without a reusable rule, every project could require repeated prompt or roadmap edits such as "you may now use Codex automatically" or "you may now keep going between Work Packets."

That would create two failure modes:

1. **under-automation** — projects remain unnecessarily manual even though their existing authority already permits the consequence and the ecosystem can now perform it safely;
2. **authority leakage** — a global statement such as "we have more autonomy now" is misread as permission to cross production, credential, spending, destructive, physical or other stronger project gates.

The missing distinction is between:

- what the project already authorizes; and
- what the current Controller / Compute Spine / worker / identity stack is technically capable of performing.

## Methodology change implemented

PROGRAMSTART PR #88 introduced `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` and wired the rule into the execution checklist.

The core resolver is:

```text
owning-project consequence authority
  ∩ PROGRAMSTART governance
  ∩ current Autonomous Controller capability
  ∩ current Compute Spine / worker capability
  ∩ current identity / secret capability
  ∩ current evidence freshness
  = effective autonomy for this exact action
```

The strongest invariant is:

> **New capability may automate existing permission but must never create new permission.**

Autonomy is consequence-scoped rather than represented by a project-wide `autonomous=true` flag.

Existing Mode-C projects should adopt the rule on natural re-entry rather than through a documentation campaign.

## PROGRAMSTART help / hinder / failure analysis

### What helped

Existing methodology already supplied most required primitives:

- project authority remains above derived runtime state;
- stronger security/destructive/financial/credential/production gates remain independent;
- safe-lane reasoning prevents a narrow gate from freezing unrelated work;
- operator-gate semantics already require exact action/evidence/resume contracts;
- owner-routed learning separates PROGRAMSTART defects from Controller, Compute, worker, Mission-Control and provider defects;
- Portfolio Operations remains derived attention/routing rather than project authority.

These primitives allowed the autonomy change to remain small rather than creating another controller, portfolio roadmap or permission registry.

### What was missing

The existing rules did not explicitly say how a project should consume newly proven execution capability without a project-specific authority rewrite.

That ambiguity becomes material as Controller/Compute capabilities change quickly.

## Local vs systemic

**Systemic.** Any long-lived PROGRAMSTART-managed project can experience capability growth after its project authority was written.

The reusable problem is not specific to Controller, Mission-Control or one product.

## Relationship to existing lessons

- `PSL-020` remains distinct: it governs owner-routed learning and safe promotion of learned behavior.
- This observation concerns **capability/authority composition for autonomous execution**, not ownership of learning.
- `PSL-007` human-gate semantics remain valid and are consumed by this rule.
- `PSL-018` portfolio-attention/execution convergence remains valid; portfolio selection still does not create project permission.

## Evidence maturity

Candidate `PSL-021`: **implemented / not validated**.

The methodology exists and passed PROGRAMSTART's Required PR Gate, including changed-file hooks, base-relative regression comparison, changed-surface drift and strict documentation build.

That proves repository consistency, not real-world effectiveness.

## First real retest condition

Use an existing project whose authority already permits reversible repository implementation and verification.

Success should demonstrate:

1. the project re-enters under current authority without an autonomy-specific roadmap rewrite;
2. the Controller identifies at least three consecutive authorized Work Packets or equivalent bounded continuation steps;
3. newly available Controller/Compute/worker capability is used automatically only for consequence classes the project already permits;
4. exact verification/Challenge requirements remain intact;
5. a stronger consequence class remains gated when reached;
6. unrelated safe work continues when a narrow gate blocks one lane;
7. no generic "proceed" is required between already-authorized packets;
8. human intervention, if any, is classified and routed to the correct owner under the Learning Architecture Gate.

A later L5 retest should additionally prove a genuine human gate survives restart, reaches Mission-Control, receives independently authenticated accepted evidence, and resumes automatically at the declared point.

## Counterevidence / reshape triggers

Narrow or reject the rule if real use shows that:

- consequence classes are too ambiguous to resolve safely;
- projects require substantial autonomy-specific documentation to use the protocol;
- capability evidence becomes a shadow permission registry;
- stale capability declarations cause unsafe or repeated failed execution;
- the rule increases ceremony more than it reduces manual transport;
- automatic capability adoption crosses or weakens a stronger project gate;
- portfolio/controller state begins overriding owning-project truth.

## Does PROGRAMSTART need more change now?

**No.**

Do not add another control file, lifecycle, global autonomy registry or mandatory project artifact before the first real retest.

Let the accepted Controller + Mission-Control work and then a real multi-Work-Packet project benchmark produce the next evidence.

If the retest succeeds, promote candidate `PSL-021` into the concise learning ledger as `validated` or `implemented` with stronger evidence as appropriate. If it fails, correct the protocol first.

## Safety / authority check

- [x] no project authority is stored in this observation;
- [x] no new provider/credential/production/spend permission is created;
- [x] no project-wide autonomy boolean is introduced;
- [x] no global backlog or new execution spine is created;
- [x] capability growth remains subordinate to consequence authority;
- [x] real validation remains open rather than being claimed from documentation alone.
