# Objective preservation and outcome proof

Owner: PROGRAMSTART #241, applying existing #132/#127 objective-convergence semantics
and #113 Challenge/currentness. A successful slice cannot silently become overall
completion. This is not a new controller, scheduler or backlog.

## Records and authority

PROGRAMBUILD/OBJECTIVES.json projects owner-accepted purpose, objective IDs, outcomes,
observable success criteria and selected proof_workflow. PROGRAMBUILD/OUTCOME_PROOF.json
traces every ID to requirements, implementation, composed scenario, environment and
evidence file SHA256 bindings. Incomplete rows retain status, reason and resume_when.
Full and lean bootstrap create deliberately unaccepted discovery records if absent;
force bootstrap preserves existing records. Bootstrap cannot accept user objectives.

The owner must be an issue in the same repository. Authenticated native owner metadata,
not copied JSON, establishes acceptance. Immutable owner issue comments start with
`PROGRAMSTART_OBJECTIVE_ACCEPTANCE_V1` plus a newline, then exactly these JSON fields:

```json
{
  "claim": "baseline",
  "result": "accepted",
  "contract_sha256": "canonical-contract-sha256",
  "previous_contract_sha256": null,
  "scope_change_reason": "",
  "head_sha": null,
  "proof_sha256": null,
  "run_id": null
}
```

Use scripts.programstart_objective_proof.digest for canonical JSON SHA256. Later
baselines reference the previous accepted digest and give a scope-change reason.
An enrolled target's owner cannot be redirected by candidate edits. Removing goals
requires explicit owner-native change, not editing a candidate manifest. Append
rejection/acceptance instead of editing history; latest applicable disposition controls.

Full completion additionally needs claim=completion, exact candidate head_sha, current
contract/proof digests and positive native Actions run_id. Provider run metadata must
show the same head/repository, selected workflow path, completed status and success.
The workflow must match accepted target bytes; a candidate cannot replace it to certify
itself. Candidate PASS/run JSON is not accepted as provider evidence.

This is repository-owner acceptance, not guaranteed independent or human review.
App-delegated owner identity may act within its granted scope; custody/separation still
matter. A valid workflow run cannot establish oracle adequacy. The owner must review
criteria, composed scenarios and actual proof. This gate cannot discover every unstated
objective, prove physical facts, or stop an authorized owner approving a wrong claim.

## Actual consumers

| Consumer | Enforcement |
|---|---|
| Advance / state CLI | Accepted trace at intake and requirements/design/scaffold/test transitions; full proof leaving implementation/release/audit/postlaunch or any final PROGRAMBUILD step |
| Dashboard advance | Same verifier; recheck actual state under its mutation lock |
| validate --check objective-proof | Full-completion verification; missing records fail |
| closeout | Default explicitly checkpoint/objective_complete=false; --objective-complete invokes full gate |
| Existing merge adapter | Enrolled candidate cannot drop goals/coverage; slice merge cannot imply overall completion; full claim requires native owner/run evidence; snapshot rechecks bind objective authority |
| Required PR Gate | Loads policy and API adapter from accepted base, never candidate code; enrolled objective claims are checked with read-only native API access; first policy introduction cannot self-certify enrollment |

Skip-preflight, skip-gate-check, dry-run and caller Challenge clear cannot bypass the
objective gate. Deferral remains available because it does not claim completion.
Missing auth/API/evidence fails closed. No candidate-defined executable runs in this
verifier. Regular committed safe-path file hashes bind evidence; changes invalidate it.
Unregistered legacy merge snapshots explicitly report UNENROLLED/objective_complete=false;
workflow full completion does not grandfather missing records. Deliberate enrollment
is necessary; do not invent a project's whole goal from the current PR.

## Verification and limits

Run tests/test_programstart_objective_proof.py and existing workflow/dashboard/closeout/
bootstrap/merge regressions. Card Vault O1–O6 stay visible while O2/O3/O4 remain pending:
a green auditor must not close them. Positive adapter fixtures use explicitly synthetic
native metadata, not live acceptance or actual product evidence.

Raw state edits, direct GitHub issue closure/merge endpoints, uninstrumented release
consumers and deployments that have not adopted the verifier are not intercepted.
Merge adapter retains its non-atomic comment/admission race and never grants activation.
PROGRAMSTART branch metadata reports protected=true, Required PR Gate bound to App15368,
enforcement_level=everyone. The full administrative protection endpoint returns403;
other bypass/admin configuration is not established. The required workflow runs the
accepted-base objective policy after adoption. This does not establish coverage on
other repositories or unregistered projects.

Use accepted methodology source. Merge adapter verifies its own code and this verifier
against accepted PROGRAMSTART main; candidate code cannot self-install to approve itself.
Source/CI acceptance, project enrollment and installed operational proof are distinct.
No new credential, daemon or paid service is introduced.
