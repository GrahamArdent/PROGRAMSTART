# Comprehensive decision-derived compiler binding

This source contract implements the paired Matrix P1/P2 and PROGRAMSTART P2 slice
selected by Graham on 2026-10-19. It does not enroll a live project, authorize a
merge/release, or implement initial admission, refresh, delivery or adoption.

An independently authorized packet without a decision-operationalization binding
retains its existing path. A decision-derived binding now requires actual rich
owner evidence; thin positive-current labels alone are not sufficient.

## Owner selection and evidence

The current owner Git declaration (`PROGRAMSTART_AUTHORITY.json` or
`.programstart/authority.json`, exactly one) may select
`decision_operationalization_path`. That regular file has this contract:

```json
{
  "contract_version": "programstart.accepted-operationalization.v1",
  "manifest_path": "plans/accepted-manifest.json",
  "accepted_manifest_sha256": "<canonical JSON SHA256>",
  "owner_decision_ref": "<member of manifest.decision_refs>",
  "readiness_path": "plans/material-readiness.json",
  "reconstruction_path": "evidence/plan-reconstruction.json",
  "root_task_id": "<selected material scope>",
  "projection_ref": "GrahamArdent/ecosystem-matrix@<exact commit>:<path>"
}
```

The existing owner resolver reads those regular files from the exact current
owner Git tree. `resolve_operationalization_binding` also requires an explicitly
provided, trusted read-only Matrix checkout and reads the immutable projection
Git object. It never fetches a caller-selected URL or executes artifact code.
For this bounded source implementation the manifest source_ref must name the exact
current owner file as repository:manifest_path. Other issue/comment acquisition
routes are not enrolled. The accepted owner manifest must be version1.0, ACTIVE, source/owner/decision
matched and complete under the actual PROGRAMSTART manifest schema.

The compiler re-reads this evidence at its readiness boundary. It calls the
Matrix-owned comprehensive reconstruction logic, compares **all recovered
manifest content** and the native projected graph against current owner files,
checks positive currentness/reconciliation, and verifies the owner-retained
receipt's actual recovered content and exact artifact binding. A receipt contains
`record_type=matrix.operationalization_reconstruction.v1`, false execution authority,
the canonical `projection_sha256`, complete `reconstructed_manifest` and its
canonical digest. A coverage/PASS string, a hash, or a previously valid copied
typed binding cannot replace these checks.

A selected declaration cannot downgrade by omitting the binding from its resolved
snapshot. Missing evidence yields machine reconciliation, never false terminality
or a new human permission gate. Changed owner HEAD requires re-read; unrelated
owner edits can reuse unchanged accepted manifest/projection after that re-read.
Acquisition locations are excluded from semantic fingerprints, while actual
repository/commit/ref/content identities remain binding and are mechanically checked.

## Matrix dependency and applicability

`scripts/matrix_projection_dependency/` is a reviewed, pinned source dependency,
not a new semantic owner or runtime adapter.
The exact upstream source is Matrix commit9238ae74d1e1bad052852cd4a7a0464202cf0ed6
(PR49); UPSTREAM.json and byte-pin tests retain custody. Matrix owns both original Python
modules; PROGRAMSTART owns the upstream manifest schema. Pin metadata and tests
retain exact source byte digests. Promotion requires coordinated owner review;
no runtime dependency checkout or private credential is added.

The graph retains material obligations, steps and gates, explicit dependencies,
root source identity and roles. Currentness/reconciliation of the selected root's
actual dependency closure controls readiness. A stale terminal prerequisite may
remain applicable only with owner-sourced `evidence_applicability` containing
`state=APPLICABLE`, a nonempty evidence reference, and matching task source ref
and version. INVALIDATED/UNKNOWN material evidence blocks; unrelated history is
not globally reopened. A label does not authenticate that owner input.

## Trust and limits

As with `RepositoryAuthorityObservation`, the caller must authenticate acquisition
of the intended owner and Matrix repositories. A local Git directory or supplied
repository name is not authentication. Current accepted owner-native declaration
selection is the acceptance basis; hashes establish identity/integrity only.
Raw independently constructed AuthoritySnapshot inputs remain a trusted API, not
an untrusted universal authorization service. Stripping every acquisition/decision
trace and lying about independent authority is outside that existing trusted API
contract, not a certified route. Controller still performs consequence admission.

Temporary-Git composed tests prove this source boundary and cold reconstruction,
not live repository custody, unattended event delivery, restart durability,
deployment, or production acceptance. Completed201/205 and other active lanes
are not re-enrolled or reopened by this source change.
