# Paths lookup pilot — 27 October 2026

The outcome-first approach found specific missing regression protections. It did not establish that the current selector configuration is wrong or that the ecosystem is qualified. This is the historical pre-repair pilot. Its resulting changes were subsequently published on Paths PR81; see [the current implementation checkpoint](../IMPLEMENTATION.md). The observations and next-change section below describe the original pilot subject, not the repaired head.

## Question and expected observations

For J01, an admitted read must return the right target result without widening authority or repeating an uncertain effect. Requirements were written in `pilot_contract.json` before the experiments, using current Paths owner contracts rather than taking existing test assertions or workflow filters as the requirements. PO01–PO10 cover current admission, actor/effect/target matching, route eligibility, clean current source, eligible fallback, denial, original pending identity, payload fidelity and independent readback, evidence scope, and selection of relevant checks.

The selected subject is [Paths PR 81](https://github.com/GrahamArdent/paths/pull/81), head `83e22aadbb07f07b39badda1a2b7a914c058dc21`; observed main was `3c23450881a1e304d2477d49fbe0f2459a3ffb2a`. PR 81 was open, draft and unmerged. The [current Paths 56 checkpoint](https://github.com/GrahamArdent/paths/issues/56#issuecomment-6445270947) preserves installed/native proof gaps and NO-GO for merge activation. This pilot does not override it.

## Results

| Experiment | Existing checks | Independent observation | Conclusion |
|---|---|---|---|
| Unchanged selected source | 31 lookup + 4 gate-parity + 2 workflow tests passed | Two added outcome probes also passed | Local fixture baseline only |
| Remove quota exclusion | Unit suite failed | Assertion failures | Existing protection detected the fault |
| Remove target matching | Unit suite failed | Assertion failure | Existing protection detected the fault |
| Remove admission recheck | Unit suite failed | Assertion failures | Existing protection detected the fault |
| Continue after pending result | Unit suite failed | Assertion failure | Existing protection detected the fault |
| Allow an unavailable route | All 31 lookup + 4 parity tests passed | Added probe observed a forbidden callback and failed | Missing regression protection |
| Replace the returned payload | All 31 lookup + 4 parity tests passed | Added probe observed payload corruption and failed | Missing regression protection |
| Remove lookup and parity suite commands from workflow | Existing workflow tests passed | Independent selection matrix found 28 mismatches | Missing selector regression protection |
| Remove the MCP workflow's `scripts/**` triggers | Existing workflow tests passed | Independent selection matrix found 14 mismatches | Missing dependency-trigger protection |
| Disable the MCP contract job with literal `false` | Existing workflow tests passed | Independent selection matrix found 28 mismatches | Missing runnable-job protection |

All faults were introduced only into disposable local copies. Unchanged source bytes were verified against their Git blob IDs. The faults are deliberate experiments, **not claims of existing production defects**. The two payload/availability probes supply expectations independently of the mutated implementation, but reuse the existing environment fixture; they are not independently operated or authenticated acceptance verifiers.

The unchanged candidate matched **32 of 32 declared selection scenarios**: fourteen representative dependency paths on pull requests and main pushes, plus four negative event/path cases. The scenario set was derived from the protected obligations and implementation dependency edges, not merely copied from the configured filters. It remains a sample, not proof of exhaustive dependency discovery.

## What ran and what remains open

The environment was CaaS Python 3.12.14 and Git, with nine exact fetched files in a partial source reconstruction. Children had a scrubbed environment and finite wall, CPU, memory and file-size limits. No network client was imported by these selected suites; no production/provider/host action or GitHub workflow dispatch occurred. Original sources were unchanged. This is a scoped local source observation, not qualification of the general E1 environment.

The 31 unit methods use synthetic gates and in-memory callbacks. Four parity methods execute pinned gate scripts but substitute composition/recipe dependencies. The two workflow tests inspect text. Their check of event settings and command strings is insufficient to detect the three demonstrated disabling edits. The independent matrix uses a deliberately bounded evaluator for these literal workflows; it is **not GitHub's native event, diff, expression or required-check engine**.

Exact-head Actions listing returned zero runs. Workflow enabled/disabled status could not be retrieved with the available supported fetch route and remains unknown. Branch protection, actual GitHub discovery/selection, merge-queue behavior and native job execution have not been proven. Main omits these new guard suites because the candidate guard work remains unmerged; that difference is not independently classified as a main regression.

The ten MCP wire fixture cases, full registry suite, full repository tests, installed consumer, real provider, durable original-effect ledger, restart recovery and independent target readback were **not executed**. A provider callback's value remains `VERIFIED_READ_RESULT_REQUIRES_OWNER_READBACK`; local payload fidelity cannot establish that the provider read the intended real target. All 84 journey scenarios therefore remain `NOT_RUN` in the foundation. No independent positive release verifier or owner acceptance is established.

One small provenance issue was also observed: the parity test's module documentation describes its gates as matching merged main, while its continuation-gate blob is candidate-specific. Its actual blob assertion remains precise. Correct the wording with the owner patch rather than treating the sentence as installed proof.

## Concrete next change

1. Reconcile the current Paths owner disposition and head. Prepare an owner-local patch incorporating the two probes in `challenge_probes.py`; preserve the existing useful tests and denial/recovery protections.
2. Strengthen workflow regression checks to require the guard and parity commands, relevant dependency-trigger coverage, runnable jobs, failure propagation, and nonzero discovered tests. Retain checks of exact-head execution and bounds. Use a small declared change/event matrix; reject unsupported configurations instead of silently guessing.
3. Correct the parity provenance wording. Run the selected exact-candidate suites and the same fault controls in the appropriately admitted owner environment. Then qualify MCP wire/full-registry coverage and the missing installed chain separately. Do not infer merge, publication or native dispatch permission from this report.
4. Expand to EN and Compute after this bounded pattern is reconciled. Start each slice with its protected outcomes and independent observations, then evaluate tests and selectors. Keep eighteen journey families as a revisable coverage baseline, not a fixed E2E budget.

## Evidence and reproduction

`evidence/pilot_results.json` records command arguments, timing, exit status, test counts, mutation identities, the full selector matrices and raw-log hashes. `evidence/result_review.json` checks source preservation and that detected faults failed assertions rather than setup/import. `evidence/source_integrity.json` lists exact source hashes, imports and method inventory. Owner/PR/tree observations are retained separately.

`run_pilot.py` and `challenge_probes.py` in the retained [original evidence bundle](https://chatgpt.com/library?file_id=libfile_b5e74c3e3cc481919c9797590d274633&account_id=personal) reproduce the bounded experiment. This Git area retains its historical evidence; reusable experimental implementations remain an Ecosystem Lab concern. Repository-backed source copies are intentionally not included in this artifact bundle. To reproduce, retrieve every file in `evidence/fetched_files.json` at the pinned commit into `pilot/source/<path>`, verify its Git blob and SHA-256 against `source_integrity.json`, and inspect the sources before execution. Use Python 3.12 with Git and PyYAML in an isolated Linux environment. Run `python3 pilot/run_pilot.py` from an extracted **working copy**; it writes new evidence and would replace that working copy's prior logs. Do not rerun into the preserved evidence directory. This reproduction recipe is not authorization for a production or hosted runner.

Within the existing 86-method catalog, ET036–ET066 now reference PILOT01 as `LOCAL_FIXTURE_RUN_OBSERVED`. The four parity and two workflow methods are recorded here and in the pilot ledger; they are not silently added to the earlier three-file catalog. The original candidate-3 register and packet are retained for comparison. All source observations, local executions, proposed journey cases and owner acceptance remain separate.
