# Backbone testing foundation

**27 October 2026 · Candidate 5 · Cross-project audit and testing preparation**

**Status:** `NON_AUTHORITATIVE_REFERENCE` · `OWNER_RECONCILIATION_REQUIRED` · no production test execution or runtime acceptance claimed.

The recommendation is to use **18 journey families**, supported by **84 scenario specifications and six compound failure sequences**. Ten journeys were a useful outline, but too coarse to assign evidence, diagnose gaps or make safe retirement decisions. Eighteen is a coverage baseline, not a maximum and not a prescription to build 84 expensive E2E tests.

The usable starting point is one linked register with four views. Existing owner repositories remain authoritative for implementation and operation. This package is a cross-project reference; it does not add another controller, scheduler, database, master plan or source of execution permission.

## Current Git checkpoint

Repository placement is operator-selected under PROGRAMSTART; see REPOSITORY_PLACEMENT.md. N04 is implemented, locally validated and published on Paths draft PR81. IMPLEMENTATION.md governs the current continuation and preserves the remaining owner/installed proof. Historical pilot records remain evidence rather than fresh runtime status. The original research bytes are retained in a deterministic gzip archive to preserve them through repository text-formatting checks.

## Read this first

- **Open the workbook** to filter scenarios, gaps, owners and candidate savings. Its four operational tabs are Outcomes, Components, Adoption and Lean. Existing tests and Sources are supporting ledgers.
- **Use `data/register.json` as the editable source of this derived package.** CSVs and the workbook are generated views. Spreadsheet edits do not write back; merge a proposed edit into the register and regenerate.
- **Use the execution brief below for the next session.** Start with protected outcomes and independent expected observations; evaluate tests and selectors against those obligations. Reuse the completed Paths pilot described below. No production result has been inferred from a source test name, historical pass count or saved plan.
- **Retain current owner decisions.** Refresh a volatile fact when the next step depends on it. A reference snapshot does not override a newer owner disposition or make an unmerged draft installed.

The bundle contains the complete register, seven CSV views, the workbook, this packet, structural checks, regeneration scripts, evidence of this package's checks, a byte-preserved copy of the earlier research report, the pre-pilot packet/register, and the reproducible Paths pilot with raw evidence. It deliberately excludes duplicate repository source snapshots and creation-time scratch data.

## The four views and their update contract

| View | Question it answers | Record unit and important fields | A legitimate next decision |
|---|---|---|---|
| Components | What belongs to the backbone, who owns it, what actually runs? | Component/surface ID, owner, purpose, candidate boundary, installed identity, observation time/source, next observation | Select a missing runtime observation; identify a possible orphan |
| Outcomes | Can an essential result be achieved and can its failure be detected? | Journey/case ID, stimulus, independent expected result, fault axis, environment, existing test IDs, run evidence and binding gap | Reuse, strengthen or add a specific test at the appropriate layer |
| Adoption | Which useful work exists but has not reached every necessary consumer? | Finding/decision ID, source stage, runtime stage, affected journeys, owner, next action, evidence | Reconcile a qualified change with installer, reader, package and runtime owners |
| Lean | What costs money, time or complexity, and what protection must survive its removal? | Candidate, measurement and unit, baseline/window, protected behavior, disposition, rollback, verified saving | Keep, consolidate, replace or retire a specifically justified item |

Links use stable IDs, never worksheet row numbers. A case points to its journey, boundary, environment, sources and existing tests. A finding or lean candidate points back to affected journeys. A future run points to one fully resolved execution binding and exact evidence. Existing owner decisions are referenced, not recreated here as independent authority.

The boundary register is a **candidate map**, not a claim that every connection is installed. Components include twelve repositories and six operational surfaces: PROGRAMSTART, Autonomous Controller, Compute Spine, Execution Node Control, Paths, Secrets Control Plane, Watchtower, Evidence Spine, Ecosystem Matrix, Mission Control, Ecosystem Lab, Decision Lifecycle; Ubuntu Execution Node, Ubuntu VPS, Windows workstation, GitHub Actions/mailbox, provider identity/webhooks and durable state/backups. Product features, including Resume Creator, are excluded. A product's shared platform dependency can still enter the audit through its backbone owner.

When a connection is discovered, add its owner and producer/consumer contract before assigning test credit. When a component is retired, retain the historical ID and decision, rather than silently removing its evidence. Each new material boundary must acquire a journey/scenario mapping or a reasoned exclusion.

## What the source evidence currently establishes

Three pinned test files were read and their **86 test methods** inventoried: 35 Execution Node diagnostic-boundary methods, 31 Paths controlled-lookup methods, and 20 Compute worker-ingress methods. These are source definitions in three files, **not the ecosystem's test total**. Seventeen of the proposed scenarios have partial links to one or more of those methods. Sixty-seven remain unmapped in this package. All 84 proposed journey scenarios remain NOT_RUN. In the subsequent Paths pilot, the 31 catalogued Paths methods were executed as local fixtures and now reference PILOT01; the remaining 55 catalogued methods were not run. Four additional parity methods and two workflow methods were also run and are recorded in the pilot ledger, outside this original three-file catalog.

The source inventory records exact repository, commit, blob and symbol. For Paths, the pilot establishes selected local fixture scope and a bounded selector matrix. Native CI execution, installed coverage and exhaustive discovery remain open. The remaining catalog entries still need test-tier, selector, skip/quarantine and current-run inspection; no ecosystem-wide test total or duplication claim is made.

The latest retrieved owner evidence matters:

- Compute issue 210 preserves source progress while the independent positive CI verifier and ABA publication-continuity concerns remain open. Its selected Python/JavaScript counts are historical scoped claims, not a current whole-suite run by this audit. Candidate-generated test telemetry cannot authorize publication. [O01]
- PROGRAMSTART issue 256 preserves H2 reference handling as source-only work; preserving a pointer is not proof that material bytes were read or influenced the decision. [O02]
- EN PR 579 and Paths PR 81 were observed as draft, open and unmerged at the pinned heads recorded in the register. Their tests are useful candidates for mapping; their existence does not establish installed enforcement. [T01, T02, L03]
- Mission Control's retrieved README describes an accepted observe-only private application while objective/human-gate writes remain disabled or gated. J18 is therefore conditional, not a reason to turn on a control surface. Matrix's retrieved README describes bounded Compute-135 coverage and currentness; it does not establish complete ecosystem observability. [S01, S02]
- Seven hosted holds recorded by the existing handoff were not freshly observed at runtime in this work. Current inventory, provider state, native behavior and installed identities remain unobserved. [L02]

Do not reopen a repaired morning error using old evidence. Preserve the latest correction and test the remaining invariant. Conversely, a later source fix cannot inherit native, installed or natural-operation credit.

## Completed first pilot: challenge the tests and their selection

The Paths J01 pilot exposed missing regression protection. **All 37 selected existing methods passed locally**, yet the 31 lookup and four parity methods also passed after deliberately removing route availability enforcement or corrupting a returned payload. Two independent outcome probes detected those faults and passed on the unchanged candidate. The existing two workflow tests also passed after each of three disabling edits: removing both lookup suite commands, removing the script path triggers, and disabling the contract job. The added bounded selection checks detected all three.

The unchanged candidate matched **32/32 declared selector scenarios**. This supports a narrow conclusion: its current literal selection settings fit the sampled obligations, but its existing regression checks do not protect those settings. It does not establish exhaustive dependency coverage or native GitHub event semantics. Deliberate fault experiments identify test gaps; they are not evidence that these faults already exist in production.

| Pilot fact | Evidence / scope |
|---|---|
| Exact candidate | Paths PR 81 head `83e22aadbb07f07b39badda1a2b7a914c058dc21`; observed main `3c23450881a1e304d2477d49fbe0f2459a3ffb2a` |
| Requirements | Ten outcome obligations in `pilot/pilot_contract.json`, derived before the experiments from owner contracts and target outcomes |
| Baseline | 31 lookup + 4 parity + 2 workflow methods; two additional probes; local partial source reconstruction |
| Behavioral faults | Six chosen faults; four caught by existing unit checks; two survived unit/parity checks and were caught by the added probes |
| Selection faults | Three disabling workflow edits survived existing workflow tests; bounded matrix caught all three |
| Still unproven | Native Actions dispatch/enablement/required checks, MCP wire and full registry suites, installed consumer, real provider, restart/ledger recovery, independent target readback and owner acceptance |

The current Paths owner checkpoint remains controlling. PR 81 was freshly observed open, draft and unmerged; exact-head Actions listing returned zero runs. Workflow enablement could not be established from the supported fetch route. During that historical pilot, no hosted workflow, runtime, repository or owner record was changed; the later source publication is recorded in IMPLEMENTATION.md.

`pilot/README.md` contains the full interpretation, exact next changes, source pins, limits and reproduction instructions. `pilot/evidence/pilot_results.json` retains commands, timestamps, matrices and log hashes. This pilot is local source evidence, separately recorded as PILOT01; it does not qualify E1 generally or close any proposed E2E case.

The resulting sequence is **obligations → independent expected observations → test adequacy → selector adequacy → admitted native/installed proof**. Mapping actual selectors remains useful, but cannot make those selectors the definition of correctness. Confidence increases because the method found concrete counterexamples; it remains limited to what those experiments tested.

## Why 18 families, and when to add another

The original J01–J09 survive. Original J10 is split into restoration (J10) and retirement (J11), because proving recovery and proving safe removal need different targets, owners and evidence. Seven further families address distinct obligations that were implicit or missing: cancellation, concurrency, adoption, fresh-context continuation, monitoring failure, effect-time authority and durable human decisions.

Every family has a positive useful-work case and at least one falsifier. Denying everything is not success. Cases describe positive, negative, recovery and adversarial behavior; a fault may require several parameterizations and environments before it is qualified.

| ID | Journey / protected outcome | Cases | Earliest wave | Scope |
| --- | --- | --- | --- | --- |
| J01 | Bounded read-only objective — An admitted read returns the correct target result without a target mutation. | 4 | W1 | Core |
| J02 | Intent and material evidence — Current accepted constraints and material evidence affect the correct decision across both successors. | 6 | W1 | Core |
| J03 | Qualification and publication — A valid immutable candidate can publish; invalid or unverified candidates cannot. | 6 | W1 | Core |
| J04 | Original-attempt recovery — Delivery uncertainty recovers the original durable result without repeating its effect. | 4 | W1 | Core |
| J05 | Storm detection and response — A real covered storm reaches a durable receiver acknowledgement and only the authorized response. | 5 | W2 | Core |
| J06 | Package to installed release — The accepted package installs all required artifacts and the actual serving process matches it. | 5 | W2 | Core |
| J07 | Credential lifecycle — An admitted identity gets only its scoped capability and loses it on revocation or expiry. | 5 | W2 | Core |
| J08 | Truthful current-state view — Displayed state is traceable, current and limited to its actual proof scope. | 5 | W1 | Core |
| J09 | Bounded resources and triggers — Valid work progresses within finite execution, retry, publication and workflow-start bounds. | 5 | W1 | Core |
| J10 | State restore and continuity — Restored critical state supports useful work with preserved original-effect identity. | 5 | W2 | Core |
| J11 | Retirement without regression — A selected obsolete component is removed without losing needed work or recovery. | 4 | W4 | Conditional |
| J12 | Cancellation and cleanup — Cancel/deadline terminates only the intended work, preserves its disposition and releases resources. | 4 | W1 | Core |
| J13 | Concurrent ownership and fencing — Concurrent valid workers cannot apply conflicting effects under stale ownership. | 4 | W1 | Core |
| J14 | Decision and contract adoption — An accepted material change reaches every affected consumer or remains explicitly unadopted. | 5 | W1 | Core |
| J15 | Fresh-context continuation — A fresh executor reconstructs the correct current next step without the original chat. | 4 | W0 | Core |
| J16 | Monitoring failure and blind spots — Loss of sensing or delivery becomes visible through a sufficiently independent observation. | 4 | W2 | Core |
| J17 | Authority changes at the effect — Revoked or narrowed authority cannot be used at a later consequential boundary. | 4 | W1 | Core |
| J18 | Human gate wait and resume — A genuine owner gate can wait durably and resume once from the correct decision. | 5 | W3 | Conditional |

These are **journey families**, not 18 implemented browser scripts. E2E means the actual admitted ingress, participating services and durable state through an independently observable target outcome. A stubbed provider, local fixture or in-memory database can prove its narrower contract; it cannot close the real boundary it substitutes.

Add a family when a distinct externally meaningful outcome, authority boundary, recovery obligation or independently governed terminal condition appears. Add a scenario within a family when the same outcome faces another failure mode. Add an environment variant when the same case depends on native OS, database, provider or installation behavior. Merge duplicates only when their outcome, boundaries, failure detection and closure evidence are genuinely equivalent.

The latest coverage correction added explicit cases for untrusted retrieved instructions, unsafe package contents, secret-bearing failures, clock changes/future observations, queue starvation, premature evidence pruning and failed human-gate notification. Cross-tenant/wrong-target input, stale claims, dependency outages, mixed schema versions, rollback and authority revocation are already represented. Network, storage and provider failure need concrete fixture parameterizations when the relevant execution bindings are resolved; the high-level case is not itself that proof.

The six compound sequences challenge interactions rather than merely adding standalone tests:

| ID | Interacting families | Failure sequence | Required observation |
| --- | --- | --- | --- |
| X01 | J03, J04, J13 | Publication succeeds, ack is lost, worker dies, another writer moves ref away and back. | No repeated push or false continuity; valid original result is recovered only with adequate proof. |
| X02 | J02, J15, J17 | A fresh context finds an old prompt while a source restriction has been revoked. | Current owner controls and prior-obligation reconciliation prevent widening. |
| X03 | J05, J09, J16 | Many valid publications arrive while the detector store and normal alert route fail. | Independent finite publication limits hold; coverage outage becomes visible. |
| X04 | J07, J10, J17 | Restore old persisted work with an expired capability and changed owner authority. | Restore does not resurrect permission; observe/reconcile without new effect. |
| X05 | J06, J08, J14 | New source/schema is accepted but one installer omits its validator and the display reads old evidence. | Installed composition and truthful projection expose the partial adoption. |
| X06 | J12, J13, J18 | A valid human resume races duplicate cancellation and a new worker claim. | One current disposition wins; cleanup and target effects remain consistent. |

Use them for convergence after the component contracts are established. Do not run a Cartesian product of every fault on every component. Select cases from dependency impact and preserved invariants; include relevant combinations when their interaction can defeat otherwise green component tests.

## Test layers and evidence rules

| Layer | What it can prove | Evidence needed | What it cannot establish alone |
|---|---|---|---|
| Static/source review | Definition exists; a configuration or import path appears wired | Exact source identity, symbol/selector and dependency map | Execution, native behavior or installed enforcement |
| Isolated component/contract | Bounded logic and producer/consumer behavior | Trusted checker, exact fixtures, expected assertions, discovered/selected/run counts | An unstubbed cross-system outcome |
| Native integration | OS, sockets, processes, systemd, Windows, database and installation semantics | Actual qualified profile, versions, isolation and target observations | Another platform or production release |
| Installed observation | Which artifact/config/process actually serves the admitted endpoint | Installed identity, serving-process readback, current owner and observer | A useful completed transaction merely from liveness |
| Bounded E2E | The actual chain achieves a scoped outcome | Original request/effect IDs, durable result, independent target readback, declared substitutions | All unrelated routes, owners or future versions |
| Recovery/convergence | Invariants survive selected interacting faults | Independent recovery observation, original-effect continuity and cleanup | Universal resilience or release acceptance |

The independent oracle must follow the governing contract, not copy the implementation's answer. For semantic decisions use material-change/irrelevant-change paired inputs with independently expected dispositions. For effects use target state and durable identity, not a self-reported success flag. For publication bind the tested immutable subject and trusted verdict to the actual publishing route. For restoration prove useful resumed work, not only that a process started.

Keep source evidence, run observation and owner acceptance separate. A run may report `PASS_REPORTED`, `FAIL`, `INCONCLUSIVE`, `BLOCKED` or `SKIPPED`; only a fully bound, reviewed receipt can be considered for owner acceptance. This package's cases allow `NOT_RUN` or `RECORDED_UNACCEPTED` and do not auto-promote to accepted. A skipped test is not a pass; an unexpected missing environment is not proof that its behavior is safe.

The local validator is structural lint. It checks IDs, references, known retention, some evidence fields and obvious overclaims. It does not authenticate a person, a tool, a log, a hash origin or an oracle. A fabricated but complete record could pass structural checks. This validator **does not solve the independent positive-verifier problem in Compute issue 210**.

## Environment profiles and execution bindings

| ID | Profile | Required basis | Qualification |
| --- | --- | --- | --- |
| E0 | Nonexecuting source review | Connected exact GitHub/file reads; no executable imports | AVAILABLE_FOR_SOURCE_MAPPING |
| E1 | Isolated offline owner tests | Complete source, trusted checker and actual fixed workload/isolation | UNQUALIFIED |
| E2 | Native Linux and PostgreSQL | Owner-admitted OS/socket/systemd/database requirements and independent limits | UNQUALIFIED |
| E3 | Native Windows and local DC | Current Paths ER033/034 and EN545 actor/effect/target route | UNQUALIFIED |
| E4 | Installed observe-only | Exact installed artifact/config/current owner and admitted observer | UNQUALIFIED |
| E5 | Bounded natural operation | Actual useful task, event limits, original-effect recovery and target readback | UNQUALIFIED |
| E6 | Isolated restore and retirement | Owner selected checkpoint/candidate, disposable target, rollback and cadence | UNQUALIFIED |

E0 is available for connected read-only mapping. E1–E6 are proposed profiles with unresolved admission and qualification. A profile name is not an environment instance. No journey execution binding or run has been added to the register. PILOT01 records a separately scoped local fixture experiment with its own explicit contract and substitutions; it is not general E1 qualification.

Before an ecosystem test is run, resolve a binding containing:

1. Case, current owner/admission reference and exact callable connected tool or accepted native harness; actual arguments, actor, target and effect footprint.
2. Exact source, test, checker, package/config identities and dependency/environment versions. Declare each real versus substituted boundary.
3. Isolation from provider secrets, production sockets, writable control state and unrelated workloads; test data and expected target changes.
4. Finite time, output, storage, retry, concurrency and event/workflow-start limits; independent counters and abort conditions.
5. Original request/attempt/effect identity rules, original-result lookup and same-attempt unknown-result recovery. A mailbox request is a control-plane write even when its eventual effect is a read.
6. Independent expected observation, retained raw evidence destination, cleanup/rollback and the owner who can accept the result.

`templates/execution_binding.json`, `templates/run_receipt.json` and `templates/test_discovery.json` provide unfilled field sets. They are templates, not valid admissions or evidence. Null fields must be resolved; never replace them with invented commands or pretend IDs.

A run receipt preserves source/test/environment identity, timing, original IDs, exact selected workload, discovery/selection/execution accounting, omissions/skips, raw log locator and digest, oracle observation, cleanup outcome, substitutions and independent verifier reference. Native/kernel/database/provider requirements must be explicit. If the output cannot establish them, the result remains incomplete for that scope.

## How to inventory existing tests and remove bloat

For each scoped repository, first establish current owner obligations, externally meaningful outcomes and independently expected observations. Inspect implementations and tests without importing candidate code; identify dependency changes that should require each protection independently of the current filters. Then enumerate tests and map all selectors: push/PR events, path filters, matrices, markers, shards, includes/excludes, scheduled jobs, required checks, skip/xfail/quarantine and retries. Then compare **defined → discovered → selected → executed → asserted → retained**. Record why any item disappears between stages. Challenge test adequacy with bounded behavior faults, and selection adequacy with missed-dependency and disabled-job counterexamples. A green job with zero selected tests is a gap. The Paths pilot demonstrates why merely inventorying existing selectors would be insufficient.

For each test, add its protected contract, incident or unique failure, tier, true dependencies, trusted oracle, environments, owner, selector, runtime/flake evidence and duplicates. Do not infer duplication from similar names or age. A legacy compatibility test can protect an active reader, rollback path, persisted payload or rare recovery task.

Recommended dispositions are KEEP, REPAIR, REPLACE, CONSOLIDATE, QUARANTINE_WITH_OWNER_AND_EXPIRY, or RETIRE_PROPOSED. A flaky test does not gain indefinite quarantine; record cause, affected protection and a real owner decision. New tests should close a specified evidence gap, not merely inflate counts.

Retirement needs a selected candidate and explicit owner decision; consumer/trigger/supervisor discovery; equivalent replacement protection including historical negative controls; representative observation covering rare scheduled and emergency use; disable-before-delete where practical; rollback and post-change observation. A quiet week is not proof that a monthly task is unused. Verify that reboot, installer, timer or workflow cannot resurrect the old path.

The twelve lean controls cover workflow amplification, duplicate tests, orphan services/schedules, retry/polling multiplication, active prompt/history size, unadopted patches, evidence storage, idle host resources, duplicate adapters/stores, unused capabilities, monitoring overhead and native fixture cost. All baselines and savings are currently unknown.

Measure costs per useful outcome and record the window, load and configuration: workflow starts versus jobs versus billed minutes; attempts versus original effects; p50/p95 time where sample size supports it; CPU/RSS/I/O; log growth; flake and quarantine rate; change-to-installed lag. Compare matched baseline and after periods. Do not call missing samples zero or extrapolate dollar savings without a measured unit cost. Do not optimize away independent trust boundaries, recovery or fault detection.

## Proposed sequence

<!-- PLAN_START -->

**Preparation plan — scope: establish an evidence-backed audit baseline; no production activation.**

| Wave | Concrete work and first owners | Exit condition | Work that remains separate |
|---|---|---|---|
| W0 · reconcile and map | Reconcile this reference with current owner truth; refresh only volatile dependencies; derive outcome obligations and independent expected observations, then assess tests and selectors; resolve missing producer/consumer edges; J15 handoff check | Every discovered item has a disposition, owner/reference and next evidence step; no unknown represented as a pass | Native execution, runtime inventory and owner adoption remain distinct |
| W1 · bounded contract proof | Prioritize J01/J17 lookup boundaries, J03/J04 publication and original recovery, J09 bounds, J12 cleanup, J13 fencing; map J02/J08/J14 semantics; use E1 only after a valid binding | Exact selected component/contract cases have trustworthy evidence and explicit exclusions; valid work also progresses | Native, installed, provider and whole-suite claims are unearned |
| W2 · native and installed chain | Qualify actual Linux/PostgreSQL and Windows profiles; observe installed identities; cover J05/J06/J07/J10/J16 and relevant W1 cases across real boundaries | Selected environment and installed boundaries proven or precisely blocked; independent monitor/recovery residuals recorded | Natural production mutations are not implied |
| W3 · bounded E2E and convergence | Select a small risk-driven set of natural operations and compound sequences; include J18 only if current owner permits that gate surface | Useful outcome, target readback, original-effect continuity and required faults verified for declared scope | No universal system acceptance; originating owner gates still control |
| W4 · simplify and verify | Select measured duplicate/legacy candidates; preserve behavior, remove in controlled stages and compare matched cost/reliability evidence | Owner records disposition, rollback and measured result; relevant journeys still hold | No blanket deletion list or unmeasured savings claim |

Waves describe dependencies, not calendar deadlines. Independent read-only mapping can continue while a native or publication gate is blocked. They are proposed sequencing for this audit and do not displace project priorities. First-wave labels in the register mean earliest preparation relevance, not permission to execute all rows.

**Completed bounded work:** PILOT01 establishes the Paths local fixture baseline, two surviving behavioral faults, three undetected selector faults and explicit native/installed gaps. N01 is complete for this scope. Reuse its evidence rather than re-reading unchanged source or rerunning unchanged experiments.

**Prior slice, now implemented:** N04 prepared the smallest owner-local correction: incorporate the unavailable-route and payload fidelity probes; require relevant suite commands, dependency-trigger coverage and runnable/failure-propagating jobs in workflow regression checks; correct the parity suite's stale merged-main wording. Reconcile current Paths owner/head first and preserve the exact evidence invalidated if either changed. Publish or dispatch only under the actual task authorization and current owner scope. The saved audit alone grants neither.

N02/N03 remain independent follow-on mapping for EN and Compute. Refer to IMPLEMENTATION.md before repeating N04; the source correction is complete for its documented scope. Apply the same outcome-first method; do not substitute their existing filters or pass counts for required behavior. Full repository discovery and workflow completeness remain open. Expand outward through required boundaries rather than treating the initial sample as the ecosystem.

**Completion of this pilot:** raw baseline/fault/selection evidence, scoped observations in the register, unchanged E2E status, a reviewable correction proposal and retained continuation. **Completed source correction:** exact owner-local changes and selected validation are linked in IMPLEMENTATION.md. Remaining execution must resolve its actual owner binding; no generic retry handoff where an eligible tool or original-result lookup can resolve the issue. MCP stdio and full-registry command blocks subsequently passed in the source repair; installed target proof remains separately admitted work.

<!-- PLAN_END -->

## Execution brief for the next session

<!-- PROMPT_START -->

Work from the Backbone Testing Foundation dated 2026-10-27 and its linked register as a non-authoritative audit reference. Preserve the existing project execution spines and current owner decisions. PILOT01 is complete for its bounded local scope. N04 source corrections are implemented and locally validated; start with IMPLEMENTATION.md for the exact published subject and remaining native/installed proof; do not infer authorization for runtime effects from this document.

1. Read IMPLEMENTATION.md, REPOSITORY_PLACEMENT.md, the packet's scope, pilot/README.md, PILOT01 evidence and register readiness. N01's bounded pilot is complete; N02/N03 remain follow-on work. Check only owner/source facts whose currentness controls the next action. Preserve repaired findings and all open owner blockers. Distinguish historical existence, current visibility and current access. No result from this reference is owner acceptance.
2. Reuse the pinned inventory and pilot evidence. Establish protected outcomes and independent expected observations before evaluating tests or selectors. Reconcile current Paths owner/head; reuse the implemented outcome, workflow and recovery-applicability corrections and their fault controls. Do not repeat the completed patch slice; refresh only invalidated evidence and qualify remaining owner-scoped proof. For N02/N03, inspect obligations, dependencies, assertions and substituted boundaries before selecting a new experiment. Do not import candidate code during source review. Preserve stable IDs and explicit evidence gaps.
3. Before proposing an actual ecosystem run, resolve its current Paths/owner admission and actor/effect/target scope; exact tool/harness and arguments; complete source/environment; isolated fixture; independent oracle; finite resource/event bounds; cleanup; and result destination. The EN545/Paths fixed probe does not grant arbitrary shell scope. Prefer a narrow typed action when sufficient; any broader Windows/DC/VPS path needs its own current eligible route and accepted semantics. Never invent a tool, widen a read, or use a mailbox write merely because it eventually returns observations.
4. Preserve original request/attempt/effect IDs. Look up the original durable result before any resend. Unknown completion requires same-attempt reconciliation, not a fresh effect. Check eligible equivalent routes when a lookup fails; keep the same admitted scope. If none is callable, name the exact missing capability and continue independent mapping instead of declaring the whole ecosystem unavailable.
5. Execute only a fully bound slice under existing task and owner authorization. If this request remains preparation-only, stop dependent execution after preparing a concrete reviewable binding; keep independent read-only work moving. Record discovered/selected/executed/asserted counts, skips, faults, actual environment, substitutions and independent target readback. Do not promote candidate-controlled test counters to trusted success or native/installed/E2E evidence.
6. Reconcile each result with its real owner. Update the derived register and regenerate views. Keep unknowns explicit. If a new failure mode, consumer or dependency appears, expand the appropriate family/scenario/environment and re-Challenge only the materially changed scope. Do not create another service, queue, priority registry or universal acceptance authority.
7. Finish the bounded slice with exact evidence, remaining obligations, eligible next action and retained result references. A runtime hold blocks only dependent work where current owner authority permits independent progress. Machine-solvable work should not become a human gate. A real owner gate remains controlling even after work is handed to another participant.

<!-- PROMPT_END -->

## Validation and regeneration

Python standard-library checks are sufficient for this package's register and CSVs:

```bash
python3 validate_register.py
python3 -m unittest test_register -v
python3 render_views.py
```

Run the three Python commands from this Git directory. For optional workbook export, the historical original evidence bundle retains `build_workbook.mjs`, which uses `@oai/artifact-tool`; supply a Node environment containing that dependency and run that script with this directory as its input. It regenerates the workbook, renders review previews and checks the summary formulas. It does not run ecosystem code. Do not install or activate backbone components as part of artifact regeneration.

The workbook uses filtered tables and frozen headers, with formula-derived counts. Changing one scenario status, one source mapping and one local-observation state in memory verified all three dependent counts; each was restored. Native Excel was not opened; artifact rendering and exported XLSX structure are the verification scope. A generated workbook is a view of the register revision, not a bidirectional database.

The structural checks include missing pilot evidence and pilot-to-E2E overclaims, missing retention, duplicate/unknown IDs, invented test links, unsupported pass credit, missing positive cases/oracles, fabricated savings, retirement without an owner, absent binding evidence, altered baseline bytes and order-independent keys. Their success applies only to this artifact and the tested controls. The full ecosystem suite and all proposed E2Es remain unexecuted.

## Retention, challenge and owner reconciliation

The known retention inventory contains 40 items: the ten original journey obligations, twelve preliminary findings and eighteen material scope/evidence/authority constraints. Each has a source and target disposition. Original J10 maps to both restoration and retirement. The earlier research report is preserved losslessly in `sources/original_research.md.gz` (decompressed bytes), with SHA-256 `b12369896b8692977330ee432a6df998f1d662b4e4c31de449ca5779179e6da7` and size 53,502 bytes. This is retention of the enumerated known source set, not proof that all historical conversations or tests were discovered.

Byte equality, ID coverage and semantic preservation are separate. The validator catches a removed required retention item and altered baseline bytes; the review separately checked that the final plan/prompt retains owner authority, the source/native/installed distinction, original-effect recovery, useful-work liveness, conditional human-gate scope and retirement protections.

**Convergence result: CLEAR for the declared reference-preparation scope.** This is a same-assistant fresh opposition review, not independent-review provenance or authenticated owner acceptance. Applicable parts were B/C/D/E/F/G/H: evidence/currentness, scope, deferred proof, verification boundaries, decision preservation, dependencies and alignment. No lifecycle stage or feasibility kill criterion was changed or certified.

| Review | Material finding or result | Disposition |
|---|---|---|
| Original ten-journey outline | Recovery and retirement shared one obligation; cancellation, fencing, adoption, fresh context, monitor failure, effect-time authority and human-gate recovery needed explicit coverage | Split/add families; preserve original lineage |
| Expanded draft | Implicit fault coverage and an unmapped provider-identity surface could hide gaps; existing source definitions could be confused with execution | Add seven fault scenarios and B19; preserve source-only credit, unknown selectors and empty runs/bindings |
| Historical candidate-3 opposition review | Challenged false E2E credit, disappearance of verifier/ABA blockers, lost historical protection, stale continuation and archive-as-authority | No new material corrective delta for this reference scope; runtime/adoption conditions remain explicit |
| Historical candidate-3 complete pair review | Checked scope, sequencing, callable routes, original recovery, alternatives, independent readback, continuation and terminal conditions against the corrected pair | No new material corrective delta; no runtime authorization or owner acceptance granted |
| Candidate-4 correction | User challenge exposed circular confidence in existing selectors; fault experiments found two behavior and three selector protection gaps | Reorder obligations before selectors; preserve pilot evidence and narrow source scope; prepare N04 |
| Fresh candidate-4 and complete plan/brief review | Challenge selector self-justification, inflated E2E credit, repeated work, loss of owner constraints and unbounded reproduction | Exact review identities and residuals in evidence/challenge_review.json; same-assistant review only |

The current register identity and candidate-5 review are recorded in `evidence/challenge_review_git.json`; candidate-4 identities in the retained review are historical. `evidence/challenge_review.json` is the retained candidate-4 review; `evidence/challenge_review_git.json` binds the current candidate-5 plan/brief and protocol identities. Candidate-3 review and inputs remain retained as history. All 19 local artifact checks passed, including missing-item, altered-byte and pilot-overclaim controls. The workbook's nine formulas exported without error cells; scenario/mapping/observation dependency changes recalculated and were restored. These results establish package consistency, not backbone correctness.

Historical PILOT01 changed no repository or runtime. The subsequent operator-authorized source correction and Git publication are recorded in IMPLEMENTATION.md. Runtime, hosted-reactivation and owner-acceptance limits remain.


This package is durably captured as a genuine cross-project/operator reference. Operationalization still needs an existing durable machine-addressable record in each affected owner's chosen surface, with the relevant cases, decisions, dependencies, evidence, closure and currentness semantics. PROGRAMSTART's planning model requires that owner reconstruction before claiming cold-resumable operational authority. No such owner adoption is asserted here; the packet does not enter an executable backlog merely by being saved.

**GO:** use this reference and completed pilot for owner reconciliation, outcome-first mapping, a reviewable owner-local correction and preparation of exact bindings. **NO-GO from this packet alone:** production test dispatch, release/merge acceptance, provider/credential changes, enabling write surfaces, storm generation or legacy deletion. Those are distinct actions requiring their actual current scope and owner evidence; ordinary independently authorized work is not globally frozen.

Re-enter the challenge when a material source/owner instruction, case outcome, boundary, environment, evidence basis, admission route, implementation, dependency or completion rule changes. Stable retained research does not need rereading solely because a new session begins; volatile runtime and owner facts must be refreshed where they control the next action.

## Sources and research continuity

The external research basis remains in the preserved original report, including its primary-source links and the limits of each recommendation. This packet operationalizes that research using current connected owner/source observations; it adds no unsupported universal test-coverage threshold, mandatory E2E count or arbitrary retirement age. The register's source hashes identify retrieved text, while Git blobs identify source objects; these are different identities.

| ID | Source | Pinned identity / scope |
| --- | --- | --- |
| P01 | [PROGRAMBUILD_CHALLENGE_GATE.md](https://github.com/GrahamArdent/PROGRAMSTART/blob/main/PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md) | 053d528d0b9f81e41c29276c9c082123842eea11 |
| P02 | [PROGRAMBUILD_PLANNING_OPERATING_MODEL.md](https://github.com/GrahamArdent/PROGRAMSTART/blob/main/PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md) | 8baaa601008efde6c05342ba23e20c9d9abd3952 |
| P03 | [programstart-convergence-packet.prompt.md](https://github.com/GrahamArdent/PROGRAMSTART/blob/main/.github/prompts/programstart-convergence-packet.prompt.md) | 5ee2122f186593d9d69f01905bdf4cc7d9b7a782 |
| T01 | [test_en545_diagnostic_boundaries.py](https://github.com/GrahamArdent/execution-node-control/blob/11b11950e92bfe262b46d861bb7a943ef45a299a/tests/test_en545_diagnostic_boundaries.py) | ce605ad912eb34127e03018119127fc6289edcf8 |
| T02 | [test_controlled_lookup_read.py](https://github.com/GrahamArdent/paths/blob/83e22aadbb07f07b39badda1a2b7a914c058dc21/scripts/test_controlled_lookup_read.py) | 1b1ef3e305b8269db605e0181b7073e1f8757ecf |
| T03 | [test_worker_bridge_local_ingress.py](https://github.com/GrahamArdent/programstart-compute-spine/blob/8723b62a8bac7db131abb12b32d4caed719d996f/tests/test_worker_bridge_local_ingress.py) | 98caf1cbc1cbe127b1c136f26382971e245817f9 |
| S01 | [README.md](https://github.com/GrahamArdent/mission-control/blob/main/README.md) | 42aa2c8cc190a6fce7be1699c9832a76668ac724 |
| S02 | [README.md](https://github.com/GrahamArdent/ecosystem-matrix/blob/main/README.md) | f866c58bc2c9b78dadbcab671fc398ab0c7074c6 |
| L01 | [BACKBONE_ECOSYSTEM_AUDIT_RESEARCH_AND_BLUEPRINT_2026-10-27.md](https://chatgpt.com/library?file_id=libfile_9f478c9f87f08191a3c4b341284df1ed&account_id=personal) | Retrieved record; exact text hash in register |
| L02 | [WATCHTOWER_CI_STORM_OVERNIGHT_HANDOFF_2026-10-24.md](https://chatgpt.com/library?file_id=libfile_e917afaa81f88191babae26f08cff30d&account_id=personal) | Retrieved record; exact text hash in register |
| L03 | [PATHS56_PR81_EN545_LOOKUP_DURABILITY_2026-10-27.md](https://chatgpt.com/library?file_id=libfile_9920a8e706348191b8fac9c201878d6e&account_id=personal) | Retrieved record; exact text hash in register |
| O01 | [https://github.com/GrahamArdent/programstart-compute-spine/issues/210#issuecomment-6449807743](https://github.com/GrahamArdent/programstart-compute-spine/issues/210#issuecomment-6449807743) | Retrieved record; exact text hash in register |
| O02 | [https://github.com/GrahamArdent/PROGRAMSTART/issues/256#issuecomment-6404646890](https://github.com/GrahamArdent/PROGRAMSTART/issues/256#issuecomment-6404646890) | Retrieved record; exact text hash in register |

Current-source records retain exact observed identities and dates in `views/sources.csv` and the register. A URL pointing to `main` is a retrieval location, not an immutable currentness guarantee. Before using it to control an effect, resolve its current owner disposition and compare the relevant identity. The final evidence manifest binds this package's files; it is not a signature or authenticated owner receipt.
