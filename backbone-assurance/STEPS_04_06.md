# Steps 4–6 — source enforcement, native observations and boundary audit

Observed 28 October 2026 UTC / 27 October America/Toronto. This is derived audit evidence under the [ten-step plan](TEN_STEP_PLAN.md), not component authority or a release grant.

## Status against the actual finish lines

| Step | Completed work | Remaining finish-line obligation |
|---|---|---|
| 4 — PR review/checks | Separate-context review of Paths81 and PROGRAMSTART257; automatic audit discovery, generated-view freshness and discovery-omission protection implemented; local verification below | Both original PRs remain draft. Exact-head hosted checks are absent; current Paths56 and EN572 records retain the account billing/spending hold and owner/installed admission. Accepted source/merge is not earned. |
| 5 — installed Paths journey | Three fresh, narrowly admitted native requests returned independently read results; observed current EN release, enrolled fixed route and actual Windows-probe failure | Actual first-call guard consumer, private target readback and durable original-effect cold replay remain unproven. The fixed EN545 probe is not a guard consumer or general machine runner. |
| 6 — EN/Compute outcome-first audit | Obligations and independent observations below, selected source/test inspection, identified gaps; a reproduced Compute recovery defect repaired in draft PR215 | This scoped audit is complete as a map of obligations and gaps. Source repair still needs full owner/hosted/integration acceptance and installation; exhaustive suite mapping belongs to step7. |

## Step 4 — protection that actually runs

The reviewer confirmed that the previous `testpaths=["tests"]` omitted the audit. Default discovery now includes `backbone-assurance`: the 19 retained artifact checks plus a new generated-view freshness test run through the existing pytest/Nox/PR path. A guard in the always-selected `tests` directory invokes real default collection and requires named audit protections. No new workflow, scheduler or service was added.

The guard is registered in existing bootstrap assets. Registry role distinguishes the template owner from generated project repositories: generated projects do not inherit the populated audit or its selection obligation. The first broader validation exposed missing bootstrap registration; it was corrected rather than waived. Faults in temporary copies demonstrate that duplicate register cases and stale CSV content fail assertions. Temporarily removing the audit selector makes the always-selected discovery guard fail. Production source, coverage scope/floor and screenshot tolerances are unchanged.

The scope of these checks remains audit artifact integrity and selection. They do not authenticate component acceptance, prove a semantic oracle or execute the 84 ecosystem scenarios.

## Step 5 — actual machine evidence

Current Paths ER-033 admits the fixed probe to the ChatGPT GitHub actor. ER-034 general operator access belongs to a separate actor; no generic command was inferred. Current EN545 owner comments retain the pinned SSH/client route, finite diagnostics and separate reboot/reinstall obligations.

| Original request | Actual observed result | Interpretation |
|---|---|---|
| `req-backbone-audit-status-20261028t004506121z` | SUCCEEDED / NOT_EVALUATED; node execution-node, installed control `97e67a5faecfaca46733c6e643b5c7f9cc2bc99e` | Real bounded node status, not whole-node acceptance |
| `req-backbone-localdc-status-20261028t004705723z` | SUCCEEDED / NOT_EVALUATED; ENROLLED, access_proven=false; same installed commit, client `96f9772e5677aaa77adf603a460f7d43a343cc7ad585e94ade531ded31dfdbab` | Historical enrollment/current client identity, not Windows READY |
| `req-backbone-localdc-probe-20261028t004859611z` | FAILED / FAIL; diagnostic schema1, MCP_INITIALIZE / TIMEOUT, access_proven=false | Finite observed failure; root cause unknown |

Results remain in the EN owner's `results/<original-id>/result.json`; LIVE01/LIVE02 in the register pin exact blobs and returned-byte hashes. The intermediate status result blob is `1f1237c780dba56c9b18a3f2fb2dd826a3856665`. No request was blindly reissued; no service, key, configuration, release, reboot or credential was changed. The failed probe is not credited as a successful backbone journey.

The root status also reports unresolved host-health observations: seven failed units/scopes, inactive generic ssh.service, and 65 H2C events in its 60-second sample. Dedicated accepted SSH listeners and temporary scope ownership require owner-specific interpretation; these facts neither diagnose the MCP timeout nor authorize broad cleanup. Whole-node health remains unaccepted. One unattributed owner-intake staging item is also reported. Preserve and route findings through EN's existing operations owner.

Current EN572 fixed private JoyHub consumer is draft `c34bd1e8be4d8cc3d6ceae3529f94d8b6ae305ee`, with no dispatcher registration, installed admission or live invocation. Its required hosted jobs are blocked by the recorded GitHub account payment/spending restriction. Connected GitHub reads are callable, but do not exercise the installed first-call guard. Neither a local guard fixture nor a native fixed Windows status can substitute for that missing consumer boundary. No broader actor, credential, runner or alternate release path was invented.

## Step 6 — obligations before tests

Source review snapshots: EN `49efccaf0544e2bd8ae472bd52ab7da2cc9e21fe`; Compute `444cf89485220bfd8ac73ae0d2562d9e48794d26`. Admission and installed release are checked separately; mailbox commits do not make repository HEAD the installed source. Owners are EN's EXECUTION_NODE_STABILIZATION/ACCEPTANCE and Compute's COMPUTE_SPINE_EXECUTION/TEST_STRATEGY, plus current action-specific authority.

| Boundary | Required outcome and independent expected observation | Selected source/test evidence | Gap or disposition |
|---|---|---|---|
| EN admission | Unsupported action/args/risk, expired request or wrong release produces zero transport/provider calls | protocol.py; test_protocol.py; Windows stage denial tests | Native account/sudo/key custody still separate |
| EN target | Fresh expected node/release/host and actual marker/package read | windows_local_dc.py; pinned vps_client.py; client identity/SSH tests | Actual probe failed at MCP initialize. Outer EN seam lacks contradictory-proof negatives; pinned client currently constructs proof facts. Owner-scoped seam hardening remains a candidate |
| EN bounds | Fixed actions, finite deadlines/bytes, no selector expansion or secret output; cleanup after failure | windows_local_dc.py dispatch and stage tests; client tests | No general MCP authority; clean reinstall and physical reboot remain open |
| EN completion | Exact request/digest, durable terminal result, failed operation never PASS | agent.py; protocol/agent negatives | Real returned status and failure retained; whole-node and useful guard journey not established |
| EN recovery | STARTED never blindly executes again; pending publication repeats only publication; changed digest rejects | agent.py; test_agent.py seeded-state/dispatch counters | Fixture recovery is not actual cold consumer restart; owner requires native original-ID proof |
| Compute admission | Actual admitted Controller peer and bounded envelope before worker work; rejected peer has zero processing calls | worker_bridge_local_ingress.py; local-ingress peer tests | Peer UID is mocked in selected rejection test; live UID/socket DAC/service admission needed |
| Compute target | Parent bytes bind immutable child, expected EN action/node/release and receipt digest | worker_bridge_agent.py target validator; selected digest/cross-carrier tests | Local-ingress suite does not exercise real target validator or worker; no cross-credit |
| Compute bounds | Frame/result ceilings, bounded concurrency and finite waits; excess connections never execute | local-ingress contention/saturation/listener tests | Selected file lacks several partial/malformed/oversize frame negatives; not an exhaustive suite absence claim. Two real AF_UNIX fixtures are unavailable in this sandbox |
| Compute completion | Terminal result persisted before completion marker, immutable original receipt across carriers | agent completion code; cross-carrier/missing-result tests | Cross-carrier fixture replaces parent processing; proves cache mechanics, not useful execution or owner acceptance |
| Compute recovery | Existing corrupt/unreadable state blocks without rewrite or new child/gate; process replacement preserves refusal | strict durable reader repair; six new tests including real subprocess | Draft PR215 addresses demonstrated encoding/shape corruption, not comprehensive state-dictionary semantics or installed power-loss durability |

### Reproduced recovery defect and repair

Compute's permissive JSON reader returned None both for absence and malformed/oversized/nonobject/unreadable state. Original code reached fresh-child construction with a corrupt saved record; corrupt terminal evidence could also be overwritten. The repair adds a strict durable reader at state load, terminal load and terminal store; ordinary observation polling stays permissive. Existing invalid bytes are preserved and a finite integrity error blocks resumption.

[Compute draft PR215](https://github.com/GrahamArdent/programstart-compute-spine/pull/215), commit `8c2431d99d94693cf8b48e6d553dc4ba885c87cd`, owns the source fix and raw red/green logs. The original implementation fails seven subcases. Review found the terminal-store hole, which was separately reproduced and corrected; fresh review of the complete corrected candidate found no further material issue in scope. Six new methods and selected existing agent/expiry/Codex/private suites pass: **95 methods**. Compilation passes. This uses a pinned selected-source fixture and stdlib-only environment, not a full repository checkout. Initial missing fixture dependencies were repaired. The local-ingress suite still has two real socket-permission errors, not suppressed passes. PR147 source overlap and PR209/214 dependencies require integration qualification before acceptance; no shared runtime was changed.

### Authority and evidence gaps

Compute's early global stage/transport text and AGENTS/TEST_STRATEGY retain Stage0.5/status-only framing while later accepted-release appendices and README describe real typed execution. Reconcile those existing owners before a new consequential action; neither stale broad restrictions nor later observed capability grants a new effect. EN's acceptance owner explicitly separates capability acceptance from whole-node acceptance and retains physical reboot requirements. This audit identifies the conflicts without replacing either project's spine.

## Remaining continuation

Keep steps4/5 open. The non-delegable hosted account condition must be resolved by its owner; retain required checks and holds. Then require exact-head checks/owner acceptance, compatible consumer admission, guarded source adoption, actual protected target readback and cold original-ID recovery with no repeated effect. Do not repeat the new source fixes as unfinished implementation, or rerun failed native requests to manufacture a PASS. Follow step7 for broader selector/skip/flakiness mapping after this bounded checkpoint.

## Local validation checkpoint

The corrected full `gate_safe` command passes all selected sessions in `/tmp/programstart-validation-20261027`: **3,148 pytest cases, zero skips, two expected warnings; 100% configured production coverage, zero missing statements/branches**. The 20 audit cases are included in that total; seven CSV subtests are not additional top-level methods. Initial full-gate failures were three missing-bootstrap-asset assertions plus lint; registration was corrected and the whole gate rerun. Register/source observation updates then passed the artifact checks again. Tracked-only artifact qualification then confirmed the audit checks do not depend on ignored workbook export intermediates; final lint/docs preparation follows before publication.

[Raw local validation and fault logs](evidence/steps456-local-validation.log.gz) retain the failed and successful attempts. Decompressed bytes: 140260; SHA-256 `0eb6b9535af4ca9a22fa6912b77aef7b2720f83a88cda3320d5234290e25f1d9`. Compute repair logs remain owner-local in PR215. Actual native records remain owner-local at the original EN request/result paths.
