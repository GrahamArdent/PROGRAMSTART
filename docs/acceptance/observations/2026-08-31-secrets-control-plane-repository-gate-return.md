# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own Secrets & Identity Control Plane scope, execution order, provider configuration, secret values, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-31
- **Project / system:** `GrahamArdent/secrets-control-plane` project-authority bootstrap
- **PROGRAMSTART lesson ID:** `PSL-007` primary supporting retest; `PSL-017` contextual confirmation
- **Checkpoint / acceptance surface:** Operator returned after the exact repository-creation handoff and reported that the repository had been created. The system independently verified the returned state before resuming the declared `RESUME_AT` work.
- **Classification:** positive protocol evidence with failed acceptance condition; no methodology change earned

## Exact prior gate contract

The 2026-08-30 promotion observation declared:

```text
GATE_OWNER: operator
REQUIRED_ACTION: create a new private GitHub repository named `secrets-control-plane` under `GrahamArdent`
SECRET_SAFE_INPUT_BOUNDARY: no secret values are needed for repository creation
RETURN_EVIDENCE: repository exists and is accessible through the connected GitHub tool
ACCEPTANCE: repository metadata resolves as `GrahamArdent/secrets-control-plane`, private, with an initial/default branch usable for commits
INVALIDATION: different repository name/location is intentionally selected, or an existing dedicated repository is discovered
SAFE_WORK_WHILE_WAITING: complete the project bootstrap documents, provider architecture, requirements, decisions, risk/test strategy, implementation work-packet design, and prompt alignment without storing credentials
RESUME_AT: commit the prepared project bootstrap bundle to the dedicated repository on a focused branch, open a PR, verify no secret values are present, then begin the first bounded implementation slice
```

## Returned operator evidence

The operator reported that the requested repository had been created and asked the system to continue.

The system did **not** treat the natural-language completion statement as equivalent to acceptance. It queried live GitHub repository metadata first.

Observed metadata:

- repository: `GrahamArdent/secrets-control-plane`
- repository exists: **yes**
- authenticated access: **admin/push available**
- default branch field: `main`
- repository size: `0`
- visibility: **public**

The declared acceptance required the repository to be **private**.

Therefore the gate is **not accepted yet**.

## Correct execution response

The system stopped before committing the Secrets & Identity Control Plane bootstrap into the public repository.

It continued only secret-safe work that does not widen exposure:

1. verified the bootstrap ZIP contains the full 22-file package;
2. verified all 21 manifest-tracked files match their recorded SHA-256 hashes and byte counts;
3. ran credential-like pattern scans across the full bootstrap package;
4. found no obvious GitHub PAT, OpenAI-style key, AWS access key, Google API key, JWT-like token, private-key block, or environment assignment containing a credential value;
5. verified PROGRAMSTART PR #71 remains open and contains the prior promotion/learning evidence;
6. preserved the project write as blocked only on repository visibility, not on architecture or documentation quality.

No file was written to the public `secrets-control-plane` repository.

## PROGRAMSTART behavior assessed

### What worked

1. **Action completion remained distinct from system acceptance.** The operator had completed a repository-creation action, but live evidence did not satisfy the declared private-repository acceptance criterion.
2. **Returned evidence was independently verified.** The system did not rely on conversational confirmation alone.
3. **The exact gate contract prevented unsafe continuation.** Because `private` was part of acceptance, the visibility mismatch was caught before project authority was published.
4. **The blocker remained narrow.** Secret-safe package validation and methodology reconciliation continued while the repository write remained blocked.
5. **The system preserved the declared resume point.** Once visibility is corrected, the next action remains: commit the bootstrap bundle on a focused branch, open the project PR, verify the committed diff contains no secret values, close M0, and derive the M1 metadata-only inventory packet.

### Friction / limitation

The current connected GitHub write surface does not expose a repository-visibility mutation, so the final correction remains an operator action in GitHub settings.

This is a tooling capability boundary, not evidence that PROGRAMSTART needs a new methodology primitive.

## `PSL-007` retest result

This is strong partial end-to-end evidence for the lesson:

> Operator/manual gates need a secret-safe exact action/evidence/resume contract and must distinguish action completion from system acceptance.

The retest has now proven the most failure-prone branch: **the operator can complete the requested action but return a state that fails acceptance, and PROGRAMSTART must not resume blindly.**

The full open retest condition is not yet complete because the system has not crossed the corrected gate and executed the declared `RESUME_AT` work.

Accordingly:

- `PSL-007` maturity: **unchanged** (`validated` protocol; end-to-end resumption still open)
- methodology change: **none**
- next evidence needed: make the repository private, re-verify live metadata, then resume exactly at the declared project bootstrap commit/PR without broad reorientation

## Safety / authority check

- [x] No raw secret value was requested or persisted.
- [x] No Secrets & Identity Control Plane authority was published to the public repository.
- [x] Returned operator evidence was verified independently.
- [x] Failed acceptance did not become a false success.
- [x] Safe work continued outside the narrow visibility gate.
- [x] Existing PROGRAMSTART primitives were sufficient.
- [x] No new methodology feature was manufactured.
