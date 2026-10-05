# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-10-05
- **Project / repository:** isolated Codex Workbench A / `graham-workbench`
- **PROGRAMSTART lesson ID:** `PSL-008`
- **Checkpoint / acceptance surface:** EXP-009 typed-dispatch implementation reconciliation after concurrent-writer detection
- **Classification:** systemic / real retest / validation

## What happened

A bounded Codex implementation session was launched against the Workbench repository. The remote control surface later issued a force-termination action and the controlling lane treated the session as stopped. The tracked wrapper ended, but a Codex sandbox/test descendant survived, was reparented to PID 1, and retained the ability to mutate the same repository.

A later lane passed its initial repository currentness check and began bounded EXP-009 work. Before committing or overwriting the discovered implementation, its shared-mutation/collision check detected staged files and a live mutation-capable descendant that did not belong to the current lane. Mutation stopped, provenance was reconciled, the orphan tree was terminated, the competing partial implementation was removed, and one canonical implementation was preserved.

## Evidence

- The surviving Codex descendant was observed reparented to PID 1 after the control/session termination.
- Repository/index evidence showed an independently staged EXP-009 implementation while the later lane was active.
- The later lane stopped mutation rather than treating its own clean-start observation as perpetual permission.
- Reconciliation preserved the canonical implementation and removed only the competing partial implementation.
- After reconciliation, focused EXP-009 tests passed **17/17** and the inherited EXP-008 durable-runner suite passed **12/12**.
- The EXP-009 socket returned to the intended state: socket active/listening, receiver inactive between requests.
- No scheduler, global lock service, portfolio registry, new lifecycle, or new authority plane was required.

## PROGRAMSTART behavior

- **What helped:** PSL-008's single shared-mutation-owner rule and immediate pre-mutation collision/currentness reasoning prevented a second writer from being silently accepted.
- **What failed:** release semantics were underspecified. A control-surface/session termination acknowledgement was treated as equivalent to termination of the mutation-capable execution tree.
- **Why this matters:** mutation ownership protects the resource, not the transport session. Detached or reparented descendants can outlive the surface that launched them.

## Learning decision

- **Existing lesson match:** `PSL-008` — exclusive mutation ownership for a shared consequential resource.
- **Maturity before:** implemented.
- **Maturity after:** validated.
- **Why:** this is the real cross-invocation/shared-resource retest named by PSL-008. The existing owner rule changed behavior as intended by stopping the later lane, while the incident exposed one bounded release-condition ambiguity.
- **PROGRAMSTART change earned:** clarify the existing Work Packet rule so mutation ownership is not released merely because a transport/session exits, disconnects, times out, acknowledges cancellation, or receives a termination request. Release/transfer requires positive evidence that the prior execution can no longer mutate the protected resource. When that cannot be established, fail closed and keep competing work non-mutating.

## Rejected expansions

This evidence does **not** earn:

- a global process registry;
- a new scheduler/orchestrator;
- a universal PID/cgroup database;
- a new lifecycle state machine;
- a second Controller;
- a mandatory process implementation for every execution surface.

Process group, cgroup, systemd unit, child enumeration, provider job identity, or another owner-native mechanism may supply termination proof. The methodology owns the required outcome, not one implementation.

## Retest

Continue normal use. Record counterevidence if positive release proof creates material false deadlock/ceremony, fails to cover a mutation-capable execution form, or if an owner-native execution surface can safely prove release with a weaker condition.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new execution authority was created.
- [x] No secret/private payload was persisted.
- [x] The change extends PSL-008 rather than creating a synonym lesson.
- [x] Detailed runtime evidence remains with the owning Workbench experiment; this record retains only the methodology-relevant result.
