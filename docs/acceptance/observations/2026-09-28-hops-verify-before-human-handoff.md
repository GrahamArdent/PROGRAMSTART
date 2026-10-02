# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

## Observation identity
- **Date:** 2026-09-28
- **Project:** PROGRAMSTART #158 HOPS convergence
- **Lesson:** PSL-021 strengthening / counterevidence
- **Surface:** P03 dependency -> exact Termius human handoff

## What happened
A genuine root bootstrap boundary required one operator action on the Controller VPS. The session had authoritative VPS inspection capability but crossed unverified machine-observable assumptions into an exact copy/paste handoff twice.

1. **Top-level premise failure:** it supplied `/home/spine-admin/work/programstart-autonomous-controller`, which did not exist. A live filesystem check available to the session would have caught this before operator execution.
2. **Dependency-closure failure:** after staging exact reviewed Controller merge `572a195b78f6980e150c0bf661c418f53aa397aa`, the session verified that the directory and installer existed but did not verify everything the installer consumed. The installer referenced `provisioning/controller/controller_release_update_remote.sh`, an Execution Node repository path absent from the Controller tree, so the second exact handoff also failed.

Controller PR #180 corrected the packaging by making the bootstrap self-contained. Before the third handoff the session verified on the actual VPS: exact staged merge `98fd7f0d6b68b0405f9f815a5ea699130b788281`, installer syntax, local updater syntax, broker compilation, and every `${SRC}/...` dependency referenced by the installer. Dependency closure passed.

## Challenge
The lesson is **not** “never guess.” Hypotheses are legitimate during investigation, and exhaustive verification of every conversational recommendation would add unnecessary ceremony. The unsafe/friction-producing boundary is promotion of an unverified machine-observable hypothesis into an operator action presented as exact.

Verifying only the top-level command/path is also insufficient. Exactness is transitive across the material dependency closure consumed by the action when those dependencies are inspectable with available authoritative tools.

## Learning decision
Strengthen existing **PSL-021**; do not create a synonymous lesson or new state machine.

Before declaring a human gate or emitting an exact copy/paste command/path/identifier/currentness assertion:
- verify every material machine-observable premise available to current authoritative tools;
- verify the material dependency closure consumed by the action on the actual target where practical;
- perform already-authorized machine-safe preparation automatically;
- if a material premise/dependency cannot be verified, label it unresolved rather than presenting the handoff as exact.

## Retest
At the next natural human/manual gate, prove the dominant path catches a stale top-level premise **or a missing/stale consumed dependency** before operator execution, minimizes the human action, and automatically resumes after accepted evidence.

## Safety
No authority expansion, generic privileged surface, secret export, or new project state spine is authorized by this lesson.
