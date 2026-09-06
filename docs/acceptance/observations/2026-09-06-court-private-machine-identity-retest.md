# Learning Observation — Court Case private machine identity retest

**Date:** 2026-09-06  
**System:** PROGRAMSTART Effective Autonomy / Execution Node / Court Case lawyer-portal recovery  
**Classification:** confirmation + owner-routed operational correction  
**Lesson:** `PSL-021`  
**Maturity result:** remains **validated**

## Trigger

Court Case lawyer-portal recovery needed a bounded read-only observation of a Graham-controlled private VPS from the Graham-controlled Execution Node.

An initial observation attempt used `bootstrap_exec_v0` while relying on an operator-host SSH identity. Host-key verification succeeded, but authentication failed because the control-agent container correctly reported:

- `operator_host_filesystem_access=false`;
- `operator_ssh_identity_access=false`.

The first operational conclusion treated this substrate-local identity absence as if the private VPS were generally unreachable and began compensating with increasingly indirect diagnostics.

The operator challenged that conclusion and required the private-machine situation to be rectified before using PROGRAMSTART as the learning/reconciliation layer.

## What current authority already said

`docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` already requires:

- distinction between `genuine_human_gate` and `temporary_automation_gap`;
- alternative-actuation search before operator transport;
- inspection of authenticated machine identities and existing trusted runtimes/queues;
- composition of bounded existing capabilities;
- conservative authority even when mechanism selection is creative.

The existing `PSL-021` Court Evidence retest already names machine identities as part of that search.

Therefore this incident did **not** expose a missing PROGRAMSTART concept or justify another autonomy framework.

## Live correction

Fresh Execution Node inspection found an already-accepted typed action, `controller_release_update`, that fixes a private VPS target, `spine-admin` account, dedicated machine-local SSH key, pinned known-hosts file, strict key-only authentication, and caller-nonselectable remote behavior.

The missing fact was not private connectivity. It was capability/identity selection.

A one-time bounded `BOOTSTRAP_EXEC_V0` retest then used that already-existing dedicated machine identity solely to prove the path and observe a minimized Court Case operational surface.

Request:

`req-court-vps-observe-bootstrap-20260906-0708`

Execution Node result commit:

`24d0531818877b442209238daa93e6ecd9d87263`

The operation completed successfully while the carrier continued to report `operator_host_filesystem_access=false`. This proves that absence of the operator identity was independent of availability of the dedicated machine identity.

The result emitted no evidence content, credential content, or private-key content and performed no remote mutation.

The lawyer VPS observation showed no lawyer deployment or public edge at the observation time, allowing the owning Court Case recovery to classify the remote state as `NO_PUBLIC_MUTATION` rather than `UNKNOWN_BLOCKED`.

## PROGRAMSTART help / hinder / failure analysis

### What helped

`PSL-021` and Effective Autonomy already contained the correct governing behavior. Once applied to the full capability graph, they led directly to the existing machine identity rather than a human SSH relay or weaker security boundary.

### What failed operationally

The first pass stopped too early at a property of one execution substrate:

`this container cannot access Graham's operator SSH identity`

and allowed that to become an ecosystem-level inference:

`the Execution Node cannot authenticate to the private VPS`.

Those statements are not equivalent.

The reusable execution discipline is:

1. test **transport reachability**;
2. resolve which **machine/service identity** is available on an authorized substrate;
3. resolve the exact **operation authority** granted to that identity/capability;
4. preserve separate evidence/audit and project-data authority boundaries.

A failure in one layer must not silently imply failure in the others.

## Learning disposition

No new PROGRAMSTART lesson ID is earned.

No new controller, generic remote shell, secrets system, capability registry mandate, or lifecycle is earned.

No core PROGRAMSTART methodology change is required by this observation because the existing Effective Autonomy protocol and `PSL-021` already explicitly require the alternative-actuation search that would have prevented the false human/transport conclusion.

The primary durable change belongs to the **Execution Node execution-fabric owner**: preserve discoverable evidence that the private VPS machine identity/transport exists, keep operator credentials out of project/control containers, and expose future project needs through narrow typed operations rather than rediscovering identity paths or normalizing `BOOTSTRAP_EXEC_V0`.

Execution Node PR #102 records that owner-specific evidence.

## Methodology implication

This incident strengthens the interpretation of `PSL-021`:

> **Do not promote a substrate-local missing identity into an ecosystem-level human gate. Resolve transport, identity, and authority independently before escalating mechanical work.**

That sentence is an interpretation of the existing rule, not a new authority or feature.

If future cases repeatedly show agents failing to perform this decomposition despite the current Effective Autonomy text, then a deterministic capability-discovery/checklist enforcement change may be earned. One incident after the existing PSL-021 implementation is not enough evidence to add another methodology mechanism.

## Safety / Challenge result

The correction did not:

- expose Graham's personal SSH key;
- mount an operator home directory into the control-agent container;
- create arbitrary project shell authority;
- broaden the remote VPS account or SSH policy;
- expose Court Case evidence or lawyer credentials;
- mutate the VPS during observation;
- weaken host-key verification;
- convert infrastructure access into evidence-content authority.

The retained bootstrap carrier remains explicit debt and is not reclassified as normal execution merely because this bounded retest succeeded.
