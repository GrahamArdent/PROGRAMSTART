# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-25
- **Project / repository:** GrahamArdent/decision-lifecycle
- **PROGRAMSTART lesson ID:** proposed `PSL-024`
- **Checkpoint / acceptance surface:** greenfield bootstrap → first stage transition → first generated-repo scaffold PR/CI
- **Classification:** systemic

## What happened

A real Mode-B greenfield project was created with `programstart create` from current PROGRAMSTART authority.

Three separate child-vs-template mismatches then surfaced:

1. Before the first repository baseline commit, stage-transition preflight treated the factory-created future-stage placeholder files as current user changes and rejected them as premature future-step work.
2. The generated child inherited PROGRAMSTART's template self-test `process-guardrails.yml`. Its compatibility matrix attempted to factory-create a web project using `--attachment-source USERJOURNEY`, even though the generated Decision Lifecycle project correctly had no USERJOURNEY attachment. This caused false CI failures.
3. The child inherited the template-oriented `bootstrap-assets` validator as an ongoing CI gate. Adding a legitimate project-specific `.github/workflows/ci.yml` then failed the template inventory check.

A fourth inherited check, CodeQL upload, successfully analyzed the project but failed only because GitHub Code Security is not enabled for this private repository. The child workflow was corrected to retain SARIF locally rather than convert an unavailable paid/platform feature into a code failure.

## Evidence

- repository / PR / commit / run / provider / runtime evidence:
  - Decision Lifecycle bootstrap baseline: `GrahamArdent/decision-lifecycle@1ad60d0`
  - scaffold PR: `GrahamArdent/decision-lifecycle#11`
  - original template-CI failure run: `36092848765` — compatibility jobs failed at factory web create because `USERJOURNEY` was absent
  - second child-profile run: `36093009775` — product checks passed, but `bootstrap-assets` rejected legitimate child workflow `.github/workflows/ci.yml`
  - corrected child-profile run: `36093076167` — Ubuntu/Windows 3.12/3.13 plus compatibility 3.13/3.14 all passed
  - CodeQL run `36093076165` scanned 148/148 Python files and failed only while uploading SARIF because code scanning is not enabled for the private repository
- exact current state relevant to the observation:
  - Decision Lifecycle has a project-specific generated-repo guardrail profile and product CI.
  - PROGRAMSTART main at `947730fa08552d5e94e777e071218a0d325ce324` still materializes the template `templates/github-workflows/process-guardrails.yml` into generated repos unchanged.
  - PROGRAMSTART's own `programstart_factory_smoke.ensure_git_baseline()` already demonstrates that a Git baseline is needed to make change-sensitive validation meaningful.
- verification actually performed:
  - reproduced the stage-transition false positives before baseline commit and observed them disappear after the first baseline commit;
  - inspected the failing CI traceback for missing `USERJOURNEY`;
  - inspected the failing `bootstrap-assets` message for the legitimate child workflow;
  - reran the corrected generated-repo guardrail successfully across the stated OS/Python matrix.
- checks not performed / unavailable:
  - no paid GitHub Code Security enablement was attempted;
  - no PROGRAMSTART methodology implementation change was made as part of this observation.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** correctly created the project authority/scaffold, but handed the child several controls whose semantics still assumed template-self-testing rather than generated-project operation.
- **What helped:** Mode-B evidence reuse, explicit project boundary, stage validators, drift detection, and the generated project methodology files made the mismatches visible early.
- **What created friction or uncertainty:** child state was initially indistinguishable from "all files changed"; generated CI tested template-only capabilities; template inventory checks rejected legitimate child additions.
- **Was existing methodology sufficient?** partially

## Learning decision

- **Existing lesson match:** `PSL-001` covers lean greenfield bootstrap, but not the post-bootstrap child-control/profile boundary. This observation is not merely another proof of lean bootstrap; it exposes a distinct handoff defect between template authority and generated-project operation.
- **Maturity before:** none
- **Maturity after:** candidate
- **Why the evidence changes or does not change maturity:** one real project produced multiple independent failures from the same boundary error, and the failures were mechanically reproduced in CI. A bounded change is now supported, but another real generated repo should validate the eventual fix.
- **PROGRAMSTART change required now:** bounded change owned by bootstrap/adoption/generated-repo control-profile surfaces. The likely change should:
  1. establish or explicitly model the first clean generated-repo baseline before change-sensitive stage preflight relies on git diff;
  2. materialize generated-project CI/validation profiles rather than template self-test workflows;
  3. distinguish immutable/managed bootstrap inventory validation from legitimate post-bootstrap child extensions;
  4. degrade optional provider/platform security checks truthfully when the child lacks the required entitlement, rather than treating unavailable capability as product failure.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next PROGRAMSTART-generated project, especially one without USERJOURNEY and with its own project CI.
- **What evidence would be sufficient:** after valid intake, the first stage transition does not require an undocumented baseline workaround; the first project-specific PR passes inherited/generated guardrails without editing away template-only assumptions; legitimate child workflows do not fail template inventory checks; unavailable optional security features are reported truthfully without blocking unrelated product acceptance.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] If no reusable lesson was found, no unnecessary PROGRAMSTART change was manufactured.
