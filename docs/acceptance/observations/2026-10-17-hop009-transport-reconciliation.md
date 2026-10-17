# HOP009 transport evidence reconciliation — 2026-10-17

Mode C; operator selected P0/P1 of PATHS-HOP-PLAN-20261017. Credential architecture and Mission-Control remain excluded. This is owner-derived acceptance evidence, not a new execution spine or standing queue.

## Outcome
Compute75 owner reconciliation: https://github.com/GrahamArdent/programstart-compute-spine/issues/75#issuecomment-6229049004.
HOP009's bounded transport instance is accepted from original retained proof, current authenticated reconciliation, natural fallback, restored normal selection, independent recovery and the installed startup-prerequisite correction. Proposed canonical count: 25 proven / 12 partial / 0 unproven. All 37 rows remain; no other HOP changes.

## Original evidence recovered
Retained VPS state and parent-results contain fixed01, normal02, recovery01 and baseline2. Complete directory scans covered 26,976 state entries and 26,905 result entries; only four HOP009 matches in each were returned. The first 16,384-entry sample was incomplete and was not used as absence proof.
- fixed01 parent SHA256: 84401ae04e609691a1a368d57103de77a946a71bb9958d680cdf3a4374fa5414.
- normal02 parent SHA256: a76c2a5409a042bd41c88c553b8fc1f507d364ca48a2800808e4e4a6df6b844c.
- recovery01 parent SHA256: 5835d49af2a56240ece5f7e719db2cea32da53f584c29843de39aec54d97226c.
The fixed01 child is req-spine-641e9bb749672a001112-status, request digest0fc22920206148c5330979d992515c17f7aff0c30ff743ec619a257ccfa66f71, original EN result commit395d16fc68f2ac7103835fd36075c696f465ef61. Native fallback-request commitaf540d462b89b9dbc543b6605fdbe391bd57866a is retained in state.

[Authenticated original terminal reconciliation](https://github.com/GrahamArdent/execution-node-control/blob/3a236d063560a068c76e6c7a159980dd4c397fee/runtime_results/req-hop009-service-context-reconcile-20261017t031329901z/result.json): each exact original ID/digest returned its saved result twice under actual installed Controller UID997 and existing supplementary ingress group. Wrong digests returned CONFLICT/request_identity_conflict. State/result bytes stayed unchanged. Bridge service actual start2026-10-16T23:05:08Z is later than the September29 receipts. This establishes retention and terminal readback across an actual process restart, not host-crash survival or a new autonomous semantic invocation.

## Current failure and repair
Fresh status req-vps-worker-hop009-current02-20261017t031559353z, digest e954fd4e086006a11bdce639e645c51f08e54ca7759490b771b765b21d49b2ba, naturally encountered private-normal availability failure and completed through the same immutable child/digest via Git fallback. EN child req-spine-3d0b3c07cc92ec0e56b0-status/digest962a31af3dd049a0cf1574b5cbcc352b14eef70bd2c27744f988872d2e638261; result commita542b5b987a0b2e2565850ccd1a412d42fe98ecb. No old acceptance experiment was recreated.

Fixed metadata found both dedicated listeners auto-restarting; fixed sshd -t returned255 solely Missing privilege separation directory. /run/sshd was absent. No credential or Tailscale failure was established.
[Runtime restoration](https://github.com/GrahamArdent/execution-node-control/blob/ce5fb26321c84820fa809fb81241d4f3f6c84bd0/runtime_results/req-hop009-restore-sshd-runtime-20261017t032050562z/result.json) created only /run/sshd root:root0755 after exact preconditions; both configs then passed0 and existing listener retry policies recovered both units. No manual service restart, SSH configuration/key/address/port/policy change or credential operation.

[Post-repair normal transaction](https://github.com/GrahamArdent/programstart-compute-spine/blob/c6ec3254857a402f8c973c237d573d8141336689/control/worker-results/req-vps-worker-hop009-postrepair-20261017t032145462z/result.json) returned SUCCEEDED/transport_acceptance PASS via private-normal2223 compute-spine-normal; fallback=false, Git execution=false, recovery identity reuse=false.
[Independent current recovery](https://github.com/GrahamArdent/execution-node-control/blob/2937e78851697c233da7f042213c7fa138bdc382/runtime_results/req-hop009-recovery-bounded-reconcile-20261017t032747734z/result.json) retained the original request req-vps-worker-hop009-recovery-20261017t032438041z and digest793b81aea74cbd67c53d17f2c04b75f838d5952ee4de0e8b0f9958a9d7488e42 across retryable BUSY. Fixed control_health_probe SUCCEEDED/transport_acceptance PASS on2222 compute-spine-recovery, Git=false and caller host/port/command selectors=false. Its application acceptance remains NOT_EVALUATED; do not relabel it as a broader product PASS.

## Startup correction and adoption
[EN502](https://github.com/GrahamArdent/execution-node-control/pull/502) merged760c6b73897274b16cf33b65d9a13ad4e6a4d737 from exact f359bd4789d97136f0e75c90e5c71341f607c674 after Control Plane CI38998589754 SUCCESS and actual-diff Challenge6229010633.
Three source unit copies add only /usr/bin/install -d -o root -g root -m0755 /run/sshd before the existing sshd -t. No RuntimeDirectory cleanup owner is introduced.
[Two isolated cold-/run proofs](https://github.com/GrahamArdent/execution-node-control/blob/6054d6951ffb906a3409a6de06b9eab7a35d7373/runtime_results/req-hop009-isolated-startup-proof-20261017t032319478z/result.json) independently reproduce missing-directory255 then corrected0 for both configs. Real host runtime-directory inode/mode/ownership unchanged; no listener started and no host reboot.

[Exact live unit configuration adoption](https://github.com/GrahamArdent/execution-node-control/blob/3f0deecc48163f9e2d8832ee197f559267937393/runtime_results/req-hop009-corrected-unit-adoption-20261017t032825007z/result.json) verifies root-owned old source/FragmentPath and running state, retains root-only rollback, writes only the two accepted external unit artifacts atomically and reloads systemd without service restart.
- Normal unit installed SHA256: 4be7b6de50f1bd05ae26bfeb7992c217ce3bd49a6a8007c301cf3d289904a12d.
- Recovery unit installed SHA256: 9b057f7ac665dbb551bc357af8bde976117574849f17a5d7491207da4be1bccc.
Both loaded prestart chains contain two commands and both services remain active. This is distinct from an EN dispatcher executable release: EN7661c99bcaa5ed00ecaff38bfaab9155761e6b34 and Compute7d1db8065baa8d6f517bb3c271a0b4b27b622435 remain unchanged. Controller source authority was freshly observed7d4e91fc913626ca0c156548a681ae2d6e77ec78. Installed normal client bytes exactly match accepted original source; bridge/ingress evolved, so current native reconciliation was independently checked.

## Preserved failures and corrections
- First observer used an incorrect release-directory path; its absence was not interpreted as missing installation. Correct installed path was read from the owner installer.
- Initial retained scan reached its bound; later complete scan supersedes only the absence inference.
- Plain sudo-u omitted installed supplementary groups and failed PermissionError. Read actual Controller service context before using existing group membership; no group/account grant changed.
- First fresh status had expected_acceptance longer than256 and was rejected before admission. It is retained. A contemplated serialized submission also re-encoded JSON; it was rejected before creating state and is not same-byte proof. The corrected existing published request was already IN_PROGRESS and was reconciled without redispatch.
- Original recovery attempts returned BUSY; bounded original-ID reconcile eventually submitted once from confirmed NOT_FOUND and succeeded.
- First unit adoption failed its loaded-command check and rolled back. The observer had collapsed repeated ExecStartPre properties; correction retains every occurrence. Independent rollback readback confirmed exact old hashes and active services before retry. Corrected adoption passed with two loaded commands, not a weakened source test.
- Temporary diagnostic, configuration, isolated test and maintenance SSH invocations remain BOOTSTRAP_DEBT. They are not promoted to a new reusable carrier. Cross-host maintenance used existing pinned public fallback; this is not fully private-carriage proof.

## Challenge, verification and completeness
Protocol blobs: Challenge Gate 053d528d0b9f81e41c29276c9c082123842eea11; Planning Operating Model8baaa601008efde6c05342ba23e20c9d9abd3952; convergence promptb71bc3e787d624845c678419b92f54c651441be4. Existing plan/prompt pair31d9367d54e9ac2b27633657af1aa9bbfc4624a18cbcd5aa356fc75123dcf8cd governs the selected HOP slice; user explicitly parked credential research. No strategic reversal or new transport.
Same-assistant fresh opposition, not independent model/human/native semantic Challenge-consumer acceptance. Relevant B/C/D/E/F/H lenses: stale issue closure versus raw proof; missed multi-command metadata; availability failure versus trust downgrade; startup/stop lifecycle; false mkdir success; immutable-ID retry; shared failure domains; source/installed distinctions; one-row-only canonical reconciliation. Corrected observer review6229042319 and owner disposition6229049004 retain the material corrections.
The exact code source CI and native negative/positive/cold/configuration checks support this bounded defect closure. Canonical contract/matrix checks and exact-head hosted acceptance must pass before status promotion merges. Local candidate preparation: parity generator --write/--check PASS; all-contract validation PASS (inherited stale-KB warnings); drift PASS; 30 focused parity tests PASS; documented changed-file CI hook profile PASS, including secret scan and formatting. The unskipped strict precommit validator fails on ten unchanged April27 KB freshness warnings; those are retained, not fixed by invented review dates. The repository's own PR workflow explicitly skips that strict hook and performs its separate authoritative checks. Preserve all other classifications.

## Residuals and invalidation
Normal/recovery still share the physical EN, kernel/network, SSH implementation and /run/sshd. Later root removal, global SSH lifecycle cleanup, credential/key/config/listener changes or normal/recovery regression invalidate affected currentness. No host reboot, crash injection or independent-host recovery was tested; isolated cold runtime proof is explicitly narrower.
No all37-HOP or detached objective completion. No new provider identities, credentials, network policy, recurring scheduler or background execution. Credential renewal failures remain separate; restoring this prerequisite does not resolve them.
Learning: a live control agent and Git fallback can hide simultaneous normal/recovery failure. Check useful transactions and shared prerequisites. No new general framework is required.
