# Automation Gap Audit

Purpose: Identify what is and is not automated across every PROGRAMBUILD stage and USERJOURNEY phase, with source-of-truth references, specific mapping changes, and critical assessment.
Last updated: 2026-04-13 (stage6gameplan Phases A–E: validate_risk_spike_resolution, UJ phase_0 engineering-ready gate, cross-stage validation refs in all prompts, sync_rules citations in PB prompts, PRODUCT_SHAPE whitelist + USER_FLOWS section check + test-coverage rename)
Method: Full codebase audit against `config/process-registry.json`, `scripts/`, `.github/prompts/`, `tests/`, `.github/workflows/`, `noxfile.py`, `schemas/`, `.pre-commit-config.yaml`, `PROGRAMBUILD_CANONICAL.md`, `source-of-truth.instructions.md`, and all canonical authority docs.

**Companion document**: `promptaudit.md` audits the same system from the prompt & source-of-truth reference angle. Findings here are cross-referenced with PA-* IDs from that audit where they overlap.

**Implementation plan**: `stage3gameplan.md` defines the phased implementation order (Phases A-I) for all AUTOMATE-tier findings and all CRITICAL/HIGH promptaudit findings. Execution prompt: `.github/prompts/implement-protocol-alignment.prompt.md`.

---

## Reading Guide

Each finding includes:

- **Source of truth**: Where the authority docs define this requirement
- **Current state**: What exists today in code/config
- **Suggested mapping**: Specific code, config, or prompt changes needed
- **Reason**: Why this automation matters (or why it may not)
- **Critical note**: Whether this is worth doing at all

Verdicts per finding: **AUTOMATE** (clear value), **CONSIDER** (value depends on context), **SKIP** (low value or intentionally deferred).

---

## PROGRAMBUILD Stages (0–10)

---

### Stage 0: inputs_and_mode_selection

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-idea.prompt.md` — AI-led 7-question interview |
| Stage-gate validation | ✅ | `validate --check intake-complete` — 6 KICKOFF_PACKET + 5 IDEA_INTAKE + 3 NOT_BUILDING + 3 KILL_SIGNAL |
| Preflight dispatch | ✅ | `preflight_problems()` → `run_stage_gate_check("intake-complete")` at `workflow_state.py:136` |
| Tests | ✅ | `test_programstart_validate_intake.py` (9 tests) |
| Registry guidance | ✅ | `workflow_guidance.programbuild.inputs_and_mode_selection.prompts` includes `shape-idea.prompt.md` |

#### Finding 0-A: No PRODUCT_SHAPE whitelist validation

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD/PROGRAMBUILD.md` Section 3 defines valid shapes: `web-app`, `mobile-app`, `API-service`, `CLI-tool`, `data-pipeline`, `browser-extension`, `desktop-app`, `library/SDK`, `platform/marketplace`, `AI-agent/assistant`. The exact list is in the "Decide which shape" conditionals table.
- **Current state**: `validate_intake_complete()` at `validate.py:69` checks `PRODUCT_SHAPE` is non-empty but accepts any value. Strip logic exists for hint text only.
- **Suggested mapping**: Add a `VALID_PRODUCT_SHAPES` set to `validate.py`. After the non-empty check for `PRODUCT_SHAPE` (~line 93), add: `if value not in VALID_PRODUCT_SHAPES: problems.append(...)`. Source the list from PROGRAMBUILD.md or add it to `process-registry.json` as `programbuild.valid_product_shapes`.
- **Reason**: A typo like `web app` (no hyphen) or `webapp` would silently pass intake and cause downstream PRODUCT_SHAPE-conditional logic (scaffold, test strategy, architecture prompts) to fall through to defaults.
- **Critical note**: Low risk today because PRODUCT_SHAPE is only consumed by prompts, not by conditional code paths in scripts. Value increases if scaffold or test strategy automation branches on PRODUCT_SHAPE. See also PA-2 in `promptaudit.md` — prompts hardcode protocol instead of loading PROGRAMBUILD.md, so PRODUCT_SHAPE conditioning rules are duplicated in prompts rather than derived.

#### Finding 0-B: `programstart recommend` not auto-triggered during advance

- **Verdict: SKIP**
- **Source of truth**: `workflow_guidance.kickoff.scripts` lists `programstart_recommend.py`. It is a guidance tool, not a gate.
- **Current state**: `recommend` is a standalone CLI command. Not called during `advance`.
- **Reason**: Recommend outputs variant advice. By the time you advance past Stage 0, the variant is already chosen. Triggering recommend during advance is too late — it should run *before* filling the kickoff packet, which is what `shape-idea.prompt.md` already guides.
- **Critical note**: No automation needed. The prompt covers this. Adding recommend to advance would be redundant and confusing.

#### Finding 0-C: No DECISION_LOG.md entry enforcement at Stage 0

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 0 step 5: "Record all three decisions in DECISION_LOG.md." The three decisions are PRODUCT_SHAPE, variant choice, and USERJOURNEY decision. `PROGRAMBUILD_CHECKLIST.md` Section 1 item: "create DECISION_LOG.md".
- **Current state**: No check that DECISION_LOG.md exists or has entries when advancing past Stage 0. `validate_intake_complete()` does not inspect DECISION_LOG.md at all.
- **Suggested mapping**: In `validate_intake_complete()`, add a check: (1) `PROGRAMBUILD/DECISION_LOG.md` exists, (2) it has at least one non-header row in its decision table. This mirrors the pattern in `validate_feasibility_criteria()` which already parses markdown sections.
- **Reason**: The GAMEPLAN mandates three decisions be logged before leaving Stage 0. Without enforcement, the decision log starts empty and downstream stages inherit undocumented assumptions.

---

### Stage 1: feasibility

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-feasibility.prompt.md` — kill criteria structuring + go/no-go |
| Stage-gate validation | ✅ | `validate --check feasibility-criteria` at `validate.py:138` — kill criteria format, ≥3 criteria, go/no-go |
| Preflight dispatch | ✅ | `preflight_problems()` → `run_stage_gate_check("feasibility-criteria")` at `workflow_state.py:137` |
| Tests | ✅ | `test_programstart_validate_feasibility.py` (10 tests) |
| Registry guidance | ✅ | `workflow_guidance.programbuild.feasibility.prompts` includes `shape-feasibility.prompt.md` |

#### Finding 1-A: No DECISION_LOG.md cross-reference for feasibility decision

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 1 step 3: "Record the recommendation in DECISION_LOG.md". `PROGRAMBUILD_CHECKLIST.md` Section 2: "record the decision in DECISION_LOG.md". `sync_rules[3]` (`programbuild_feasibility_cascade`): FEASIBILITY.md is authority for DECISION_LOG.md.
- **Current state**: `validate_feasibility_criteria()` at `validate.py:138` checks FEASIBILITY.md content (kill criteria format, count, go/no-go) but never inspects DECISION_LOG.md.
- **Suggested mapping**: At the end of `validate_feasibility_criteria()`, add: read DECISION_LOG.md, parse its table, check that at least one row references "feasibility" or "go/no-go" or "kill" in its Decision column. Pattern: `if not any(keyword in row.get("Decision","").lower() for keyword in ("feasibility","go/no-go","kill"))`.
- **Reason**: Two authority docs (GAMEPLAN, CHECKLIST) mandate this. The sync_rule confirms FEASIBILITY.md → DECISION_LOG.md is a tracked dependency. An unrecorded feasibility decision means Stage 2+ operates on an undocumented assumption.
- **Critical note**: The check should be lenient (keyword match, not exact format) because DECISION_LOG entries are prose.

#### Finding 1-B: Challenge gate log entry is advisory-only, not blocking

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD_CHALLENGE_GATE.md` says "Run this checklist before starting any new stage. It is not optional." `PROGRAMBUILD_GAMEPLAN.md` lists "Challenge Gate: Run PROGRAMBUILD_CHALLENGE_GATE.md" as the first item at every stage. `PROGRAMBUILD_CHECKLIST.md` lists "run Challenge Gate" at every stage transition.
- **Current state**: `_check_challenge_gate_log()` at `workflow_state.py:77-116` scans for a matching `| From Stage` row. If missing, it prints a **yellow warning** at `workflow_state.py:412-414`. The `--skip-gate-check` flag suppresses the warning entirely. Advance is **never blocked** by a missing gate log entry.
- **Suggested mapping**: Two options: (A) Make the warning blocking by default, add `--force-no-gate` to override (breaking change). (B) Add a `strict_challenge_gate` boolean to `process-registry.json` `workflow_state.programbuild` — when true, missing gate log entry returns an error in `preflight_problems()` rather than a post-preflight warning.
- **Reason**: The CHALLENGE_GATE doc uses RFC 2119 language implying this is mandatory ("It is not optional"). But enforcing it as a hard block would require the operator to fill in the gate log table before every advance, which is friction for solo operators.
- **Critical note**: The current advisory approach is probably correct for solo operators (per user's preference for solo-friendly defaults). Could become blocking for `enterprise` variant only. Consider making this variant-conditional. See also PA-3 in `promptaudit.md` which rates this as CRITICAL from the kill-criteria-evaporation angle — the Challenge Gate is the *only* mechanism that re-reads kill criteria, and its advisory status means kill criteria structurally evaporate after Stage 1.

#### Finding 1-C: No RISK_SPIKES.md seeding validation

- **Verdict: SKIP**
- **Source of truth**: `shape-feasibility.prompt.md` mentions seeding risk spikes. But `PROGRAMBUILD_FILE_INDEX.md` lists RISK_SPIKES.md as a Stage 4 output. `workflow_state.step_files.feasibility` does not include RISK_SPIKES.md — only FEASIBILITY.md and DECISION_LOG.md.
- **Current state**: No script checks whether RISK_SPIKES.md is seeded at Stage 1.
- **Reason**: RISK_SPIKES.md is canonically a Stage 4 deliverable. Seeding it at Stage 1 is a nice-to-have encouraged by the prompt but not a structural requirement. Validating it here would create a false dependency.
- **Critical note**: Skip. The top 3 risks captured in FEASIBILITY.md's risk section serve as the bridge.

---

### Stage 2: research

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-research.prompt.md` — structured research protocol |
| Stage-gate validation | ❌ | No content validation — by design |
| Preflight dispatch | ❌ | No entry in `stage_checks` dict at `workflow_state.py:136` |
| Registry guidance | ✅ | `workflow_guidance.programbuild.research.prompts` includes `shape-research.prompt.md` |

#### Finding 2-A: No `validate --check research-complete`

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 2 Cross-Stage Validation has 4 checks: (1) no research finding contradicts feasibility assumption, (2) no tech recommendation contradicts a known constraint, (3) competitor that fully solves problem → re-evaluate, (4) low-confidence decisions recorded in DECISION_LOG. `PROGRAMBUILD_CHECKLIST.md` Section 3 has 6 items including "validate stack maturity" and "record low-confidence decisions in DECISION_LOG.md".
- **Current state**: No validation function exists. `stage_checks` dict at `workflow_state.py:136` has no entry for `research`. Research quality is enforced by Challenge Gate alone (and that's advisory-only per Finding 1-B).
- **Suggested mapping**: Create `validate_research_complete()` in `validate.py`. Minimum viable check: (1) RESEARCH_SUMMARY.md exists and has non-template content (check for sections like "## Findings", "## Alternatives", "## Decisions"), (2) DECISION_LOG.md has at least one entry dated at or after research stage start. Add `"research": "research-complete"` to `stage_checks` dict. Add `"research-complete": validate_research_complete` to `run_stage_gate_check()` dispatch. Add `research-complete` to argparse choices.
- **Reason**: Research is the only early stage (0–4) with a shaping prompt but no content gate. The GAMEPLAN defines explicit cross-stage validation items. Without any check, an empty or template-only RESEARCH_SUMMARY.md passes advance silently.
- **Critical note**: The original gameplan (stage2gameplan.md Q3) intentionally deferred this because research quality is hard to validate structurally. A minimal existence-and-sections check is a reasonable middle ground — it catches "forgot to do research" without trying to assess research quality.

#### Finding 2-B: No RESEARCH_SUMMARY.md modification check

- **Verdict: SKIP**
- **Source of truth**: None. No authority doc requires a file-modification timestamp check.
- **Current state**: `validate_required_files()` checks the file exists. `validate_metadata()` checks metadata block.
- **Reason**: Checking file modification time is fragile (git operations, file copies change mtime). The existence+sections check in Finding 2-A is more reliable.
- **Critical note**: Skip. If Finding 2-A is implemented, this becomes redundant.

---

### Stage 3: requirements_and_ux

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-requirements.prompt.md` |
| Stage-gate validation | ✅ | `validate --check requirements-complete` at `validate.py:204` |
| Preflight dispatch | ✅ | `workflow_state.py:138` |
| Tests | ✅ | `test_programstart_validate_requirements.py` (9 tests) |

#### Finding 3-A: Cross-reference substring bug (`FR-1` matches `FR-10`)

- **Verdict: AUTOMATE**
- **Source of truth**: `validate_requirements_complete()` at `validate.py:261`: `if req_id and req_id not in flow_text`. This is a Python `in` operator on strings, which is substring matching.
- **Current state**: `FR-1 not in flow_text` returns False if `flow_text` contains `FR-10`, `FR-100`, or `FR-1a`. The validator incorrectly reports that `FR-1` is referenced when only `FR-10` is.
- **Suggested mapping**: Change the substring check to a word-boundary regex: `if req_id and not re.search(rf"\b{re.escape(req_id)}\b", flow_text)`. This ensures `FR-1` matches only `FR-1`, not `FR-10`.
- **Reason**: This is a latent correctness bug. It silently passes validation when a requirement is actually unreferenced in USER_FLOWS.md. The GAMEPLAN Stage 3 Cross-Stage Validation item 4 says "User flows reference users identified in the inputs block" — false cross-references undermine this.
- **Critical note**: Low risk today if all requirement IDs use 3-digit format (FR-001). Becomes a real bug the moment someone uses short IDs. Fix is trivial (one line change).

#### Finding 3-B: No P0 minimum count enforcement

- **Verdict: SKIP**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 3 Cross-Stage Validation: "The success metric from the inputs block is achievable by the P0 requirements alone." This is a semantic check, not a count check.
- **Current state**: `validate_requirements_complete()` validates that each row has a valid priority but does not enforce a minimum number of P0 requirements.
- **Reason**: What constitutes "enough P0s" is project-dependent. A CLI tool might have 2 P0s. Enforcing a count would produce false positives for legitimate small-scope projects.
- **Critical note**: Skip. The semantic check ("are P0s sufficient for the success metric?") cannot be automated structurally. The prompt `shape-requirements.prompt.md` already challenges weak requirements during the interactive session.

#### Finding 3-C: No USER_FLOWS.md structural validation

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 3: "Produce USER_FLOWS.md with step-by-step journeys." `PROGRAMBUILD_CHECKLIST.md` Section 4: "create USER_FLOWS.md", "define loading, empty, error, and retry states."
- **Current state**: `validate_requirements_complete()` checks that USER_FLOWS.md exists and that requirement IDs appear in it, but does not validate its internal structure (no check for flow definitions, state coverage).
- **Suggested mapping**: Add to `validate_requirements_complete()`: check that USER_FLOWS.md has at least one `## Flow` or `### Flow` section header with step content beneath it. Optionally check for "loading", "empty", "error" keywords if the PRODUCT_SHAPE warrants user-facing states.
- **Reason**: USER_FLOWS.md could be a stub with just requirement IDs pasted in, passing the cross-reference check without containing any actual flow definitions.
- **Critical note**: Marginal value. A section-header check catches empty stubs, but the real quality check is in the shape-requirements prompt session. CONSIDER only if adding value beyond what the prompt already enforces.

---

### Stage 4: architecture_and_risk_spikes

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-architecture.prompt.md` (upgraded Phase D, 2026-04-12) |
| Stage-gate validation | ✅ | `validate --check architecture-contracts` + `validate --check risk-spikes` + `validate --check risk-spikes-resolved` (Phase E+F stage6, 2026-04-13) |
| Preflight dispatch | ✅ | `stage_checks["architecture_and_risk_spikes"] = ["architecture-contracts", "risk-spikes", "risk-spikes-resolved"]` (2026-04-13) |
| Tests | ✅ | `test_programstart_validate_architecture.py` (9 tests), `test_programstart_validate_risk_spikes.py` (6 tests), `test_programstart_validate_risk_spike_resolution.py` (5 tests) |

#### Finding 4-A: No RISK_SPIKES.md resolution check at Stage 4→5 transition

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 7 entry_criteria[0]: "ARCHITECTURE.md is complete and all spikes in RISK_SPIKES.md are resolved or explicitly deferred with a decision." `process-registry.json` `implementation_loop.entry_criteria[0]` repeats this verbatim. `PROGRAMBUILD_CHECKLIST.md` Section 5: "run risk spikes for unknowns."
- **Current state**: `validate_architecture_contracts()` at `validate.py:269` checks ARCHITECTURE.md sections but never reads RISK_SPIKES.md. No function validates spike resolution status. See also PA-7 in `promptaudit.md` — RISK_SPIKES.md is referenced by 4 prompts but has no validator or dedicated tests.
- **Suggested mapping**: Create `validate_risk_spike_resolution()` in `validate.py`. Parse RISK_SPIKES.md for a status table (look for columns like "Status", "Outcome", "Resolution"). Check that each row has a status of `resolved`, `deferred`, or `accepted` — not `open` or `in-progress`. Wire this into `run_stage_gate_check("architecture-contracts")` as an additional call, or create a separate `"risk-spikes-resolved"` check dispatched for Stage 4.
- **Reason**: Unresolved risk spikes flowing into scaffold and implementation is one of the three failure modes the Challenge Gate was designed to catch (assumption rot). The GAMEPLAN is explicit that spikes must be resolved or deferred-with-decision before implementation starts.
- **Critical note**: High value. This is the gap between "architecture is documented" and "architecture is validated." The current gate only checks architecture document structure, not whether the associated risks were actually resolved. See also PA-7 in `promptaudit.md` — RISK_SPIKES.md is referenced by 4 prompts but has no validator or dedicated tests.

#### Finding 4-B: No DECISION_LOG.md cross-reference for architecture decisions

- **Verdict: AUTOMATE**
- **Source of truth**: `sync_rules[15]` (`architecture_decision_alignment`): "When ARCHITECTURE.md contracts change, DECISION_LOG.md should be reviewed for a corresponding entry." `PROGRAMBUILD_GAMEPLAN.md` Stage 4 step 5: "Record spike outcomes and decisions." `PROGRAMBUILD_CHECKLIST.md` Section 5: "promote material architecture decisions into ADRs if needed."
- **Current state**: `validate_architecture_contracts()` does not inspect DECISION_LOG.md. The sync_rule exists but `require_authority_when_dependents_change` is `false` (soft guidance only).
- **Suggested mapping**: At the end of `validate_architecture_contracts()`, add a check similar to Finding 1-A: DECISION_LOG.md should have at least one entry. This is minimal — we're not checking content alignment, just that the log has been touched during the architecture stage.
- **Reason**: The sync rule explicitly calls this out. Architecture decisions without decision log entries create undocumented technical commitments.
- **Critical note**: Keep it minimal (existence check, not content matching). Architecture decisions are varied and hard to match structurally. See also PA-5 in `promptaudit.md` — DECISION_LOG.md is conditional in 4/5 shaping prompts while the GAMEPLAN mandates it at every stage.

- **Verdict: SKIP**
- **Source of truth**: `PROGRAMBUILD.md` Section 11 defines contract structure per PRODUCT_SHAPE (endpoints have endpoint + auth + schema + errors for web-apps; commands have flag + validation + exit codes for CLI tools).
- **Current state**: `validate_architecture_contracts()` checks for section existence (Data Model, Contracts/Command Surface, System Topology, Technology Decision Table) but not per-contract completeness.
- **Reason**: Contract structure varies dramatically by PRODUCT_SHAPE. A web-app contract has endpoint/auth/schema/errors. A CLI tool has command/flags/validation/exit-codes. Validating per-contract completeness requires PRODUCT_SHAPE-aware parsing logic that is complex and brittle.
- **Critical note**: Skip. The `shape-architecture.prompt.md` already enforces this during the interactive session. Structural validation of variable-format contracts has high maintenance cost and low marginal value over the prompt.

---

### Stage 5: scaffold_and_guardrails

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-scaffold.prompt.md` (Phase H, 2026-04-12) |
| Stage-gate validation | ✅ | `validate --check scaffold-complete` at `validate.py:392` (Phase G, 2026-04-12) |
| Preflight dispatch | ✅ | `stage_checks["scaffold_and_guardrails"] = "scaffold-complete"` (2026-04-12) |
| Registry guidance | ✅ | `workflow_guidance.programbuild.scaffold_and_guardrails.prompts` includes `shape-scaffold.prompt.md` |

#### Finding 5-A: No `shape-scaffold.prompt.md`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 12 defines a detailed scaffold protocol: create contract layer, boundary helper, structural tests, CI with timeouts. `PROGRAMBUILD_GAMEPLAN.md` Stage 5 defines 6 steps and 3 cross-stage validation checks. `PROGRAMBUILD_CHECKLIST.md` Section 6 has 10 items. `workflow_guidance.programbuild.scaffold_and_guardrails.prompts` contains only `programstart-stage-guide.prompt.md` and `programstart-stage-transition.prompt.md` — no stage-specific shaping prompt.
- **Suggested mapping**: Create `.github/prompts/shape-scaffold.prompt.md`. Content should codify PROGRAMBUILD.md Section 12 steps: (1) Load ARCHITECTURE.md contracts and PRODUCT_SHAPE, (2) Create contract layer adapted to shape (routes for web-app, commands for CLI, etc.), (3) Create boundary helper, (4) Add structural tests (alignment, reverse alignment, auth matrix, no-hardcoded-identifiers), (5) Create CI with explicit timeouts. Add the prompt to `workflow_guidance.programbuild.scaffold_and_guardrails.prompts` in `process-registry.json`. Add the prompt to `bootstrap_assets`.
- **Reason**: Stages 0–4 each have a dedicated shaping prompt that codifies their section of PROGRAMBUILD.md. Stage 5 has a 10-item checklist and detailed protocol in PROGRAMBUILD.md Section 12 but no prompt to guide execution. The operator must read PROGRAMBUILD.md manually and translate it into action.
- **Critical note**: High value. Scaffold is the first stage where code is produced. Getting the contract layer and structural tests right is foundational. A prompt that loads ARCHITECTURE.md and applies PRODUCT_SHAPE-specific scaffold rules would significantly reduce implementation errors. **Canonical note**: Per `PROGRAMBUILD_CANONICAL.md` Rule 5, adding a new prompt requires: (1) add to `PROGRAMBUILD_FILE_INDEX.md` Tooling table, (2) add to the CANONICAL authority map if the prompt becomes the authority for a concern, (3) add to `workflow_guidance.programbuild.scaffold_and_guardrails.prompts` in `process-registry.json`, (4) add to `bootstrap_assets`.

#### Finding 5-B: No `validate --check scaffold-complete`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 12 gate: "Feature work starts only after every structural test is green." `PROGRAMBUILD_GAMEPLAN.md` Stage 5 Cross-Stage Validation: (1) every contract traces to ARCHITECTURE.md, (2) structural tests cover alignment/auth/no-hardcoded-ids, (3) scaffold does not implement product features. `PROGRAMBUILD_CHECKLIST.md` Section 6: "create CI with timeouts" + 4 structural test types.
- **Current state**: No `scaffold-complete` check exists. The `scaffold_and_guardrails` stage has no entry in `stage_checks` and no validation function.
- **Suggested mapping**: Create `validate_scaffold_complete()` in `validate.py`. Minimum viable checks: (1) At least one CI workflow file exists (`.github/workflows/*.yml` glob), (2) At least one test file exists in the project (test glob), (3) `ARCHITECTURE.md` exists (already checked, but confirms it survived scaffold). Add `"scaffold_and_guardrails": "scaffold-complete"` to `stage_checks` at `workflow_state.py:136`. Add `"scaffold-complete": validate_scaffold_complete` to dispatch dict. Add `scaffold-complete` to argparse choices.
- **Reason**: The PROGRAMBUILD.md gate is explicit: "Feature work starts only after every structural test is green." But PROGRAMSTART is a template repo — it cannot run the *project's* tests. The check should validate that the scaffolding artifacts exist, not that they pass.
- **Critical note**: The validation is necessarily weaker than for Stages 0–4 because the scaffold outputs (CI config, test files, code structure) live in the *generated project repo*, not in PROGRAMSTART. PROGRAMSTART can only check that PROGRAMBUILD docs reference these artifacts, not verify their content. This inherent limitation means the check is a "did you do the work?" gate, not a "did you do it correctly?" gate. Still worth having.

#### Finding 5-C: No validation that `programstart_starter_scaffold.py` output matches architecture

- **Verdict: SKIP**
- **Source of truth**: `programstart_starter_scaffold.py` generates a project skeleton at `programstart create` time. It runs *before* ARCHITECTURE.md exists (it's part of bootstrap, not Stage 5).
- **Current state**: The scaffold script generates a generic project structure based on templates, not architecture decisions.
- **Reason**: The scaffold script and the Stage 5 scaffold are different things. The script generates an initial project structure. Stage 5 builds the *architecture-informed* contract layer. Comparing them is a category error.
- **Critical note**: Skip. This finding was inaccurate — the scaffold script and Stage 5 scaffold are not the same artifact.

---

### Stage 6: test_strategy

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-test-strategy.prompt.md` (Phase H, 2026-04-12) |
| Stage-gate validation | ✅ | `validate --check test-strategy-complete` at `validate.py:368` (Phase G, 2026-04-12) |
| Preflight dispatch | ✅ | `stage_checks["test_strategy"] = "test-strategy-complete"` (2026-04-12) |
| Existing check | ⚠️ | `validate --check test-coverage` counts test files only (misleading name; see Finding 6-C) |
| Registry guidance | ✅ | `workflow_guidance.programbuild.test_strategy.prompts` includes `shape-test-strategy.prompt.md` |

#### Finding 6-A: No `shape-test-strategy.prompt.md`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 13 defines a complete test strategy protocol: purpose test rules ("If this test fails, does a real user lose a real capability?"), auth test rules, golden test policy, endpoint-to-test registry, requirements-to-test traceability matrix. `PROGRAMBUILD_GAMEPLAN.md` Stage 6 defines 5 steps and 4 cross-stage validation checks. `PROGRAMBUILD_CHECKLIST.md` Section 7 has 8 items including traceability matrix and endpoint-to-test registry.
- **Current state**: `workflow_guidance.programbuild.test_strategy.prompts` has only the generic stage-guide and stage-transition prompts. No prompt codifies the Section 13 protocol.
- **Suggested mapping**: Create `.github/prompts/shape-test-strategy.prompt.md`. Content: (1) Load REQUIREMENTS.md P0 requirements + ARCHITECTURE.md contracts + PRODUCT_SHAPE, (2) Apply PRODUCT_SHAPE testing checklist from PROGRAMBUILD.md, (3) Define purpose test litmus for each P0, (4) Create requirements-to-test traceability matrix, (5) Create endpoint-to-test registry from ARCHITECTURE.md contracts, (6) Define golden test policy adapted to shape. Add to `workflow_guidance.programbuild.test_strategy.prompts` and `bootstrap_assets`.
- **Reason**: Same pattern as Finding 5-A. PROGRAMBUILD.md Section 13 has a rich protocol. Without a prompt, the operator must manually extract and apply the rules.
- **Critical note**: High value. Test strategy directly determines implementation quality at Stage 7. The traceability matrix (P0 → test) and endpoint-to-test registry are structural artifacts that a prompt can guide well. **Canonical note**: Same Rule 5 housekeeping as Finding 5-A — new prompt must be added to FILE_INDEX.md, registry guidance, and bootstrap_assets. See also PA-4 in `promptaudit.md` — TEST_STRATEGY.md has zero prompt + zero validator + zero tests.

#### Finding 6-B: No `validate --check test-strategy-complete`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 6 Cross-Stage Validation: (1) every P0 in REQUIREMENTS.md appears in traceability matrix, (2) every contract from ARCHITECTURE.md in endpoint-to-test registry. `process-registry.json` `implementation_loop.entry_criteria[1]`: "TEST_STRATEGY.md is complete with a requirements-to-test traceability matrix covering all P0 requirements." `implementation_loop.entry_criteria[2]`: "Every P0 requirement in REQUIREMENTS.md has at least one named purpose test."
- **Current state**: `validate --check test-coverage` (at `validate.py`) only counts test files in the workspace — it does not inspect TEST_STRATEGY.md content at all. No function validates traceability matrix or endpoint registry.
- **Suggested mapping**: Create `validate_test_strategy_complete()` in `validate.py`. Checks: (1) TEST_STRATEGY.md exists with non-template content, (2) a "Traceability" or "Requirements" table/section exists, (3) P0 requirement IDs from REQUIREMENTS.md appear in TEST_STRATEGY.md (cross-reference similar to requirements→USER_FLOWS check), (4) an "Endpoint" or "Contract" or "Registry" section exists. Add `"test_strategy": "test-strategy-complete"` to `stage_checks`. Add to dispatch and argparse.
- **Reason**: This directly enforces two of the four `implementation_loop.entry_criteria` that are currently documented-but-not-enforced (per Finding 7-A). Building it at Stage 6 means the entry criteria check at Stage 7 can delegate to it.
- **Critical note**: High value. P0-to-test traceability is the single most impactful quality check that is missing. The cross-reference pattern already exists in `validate_requirements_complete()` (requirement IDs in USER_FLOWS.md) — the same pattern applies here.

#### Finding 6-C: `test-coverage` check is meaningless for content validation

- **Verdict: CONSIDER**
- **Source of truth**: `validate_test_coverage()` is listed as a warning-only check. It counts `tests/test_*.py` files.
- **Current state**: This check validates the PROGRAMSTART template repo's own test count, not the generated project's. It has no relationship to TEST_STRATEGY.md content.
- **Suggested mapping**: If Finding 6-B is implemented, consider deprecating `test-coverage` or renaming it to `template-test-coverage` to avoid confusion with `test-strategy-complete`.
- **Reason**: The name `test-coverage` implies it validates test strategy coverage, but it only counts files. This creates a false sense of safety.
- **Critical note**: Low priority. The warning-only nature limits the damage, but the naming is misleading.

---

### Stage 7: implementation_loop

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `implement-gameplan-phase*.prompt.md` (8 files) + `product-jit-check.prompt.md` — surfaced via `programstart guide` (Phase B, 2026-04-12) |
| Stage-gate validation | ✅ | `validate --check implementation-entry` at `validate.py:425` — delegates to architecture-contracts + risk-spikes + test-strategy-complete (Phase G, 2026-04-12) |
| Preflight dispatch | ✅ | `stage_checks["implementation_loop"] = "implementation-entry"` (2026-04-12) |
| Entry criteria | ✅ | `validate_implementation_entry_criteria()` enforces all 4 `registry.implementation_loop.entry_criteria` items |
| Checklist tracking | ✅ | `programstart_checklist_progress.py` |
| Registry guidance | ✅ | `workflow_guidance.programbuild.implementation_loop.prompts` includes all 8 phase prompts + `product-jit-check.prompt.md` |

#### Finding 7-A: Entry criteria documented but not enforced

- **Verdict: AUTOMATE**
- **Source of truth**: `process-registry.json` `workflow_guidance.programbuild.implementation_loop.entry_criteria`:
  1. "ARCHITECTURE.md is complete and all spikes in RISK_SPIKES.md are resolved or explicitly deferred with a decision."
  2. "TEST_STRATEGY.md is complete with a requirements-to-test traceability matrix covering all P0 requirements."
  3. "Every P0 requirement in REQUIREMENTS.md has at least one named purpose test."
  4. "DECISION_LOG.md is current — no decisions made since the last stage that are not recorded."
- **Current state**: These are stored as informational strings in the registry. No script reads or enforces them. `preflight_problems()` at `workflow_state.py:117` (function def), with `stage_checks` dict at line 136, has no `"implementation_loop"` entry. See also PA-1 in `promptaudit.md` — the JIT protocol is entirely absent from the prompt layer, amplifying the impact of unenforced entry criteria.
- **Suggested mapping**: Create `validate_implementation_entry()` in `validate.py` that delegates to: (1) `validate_architecture_contracts()` (already exists — covers entry_criteria[0] partially), (2) `validate_risk_spike_resolution()` (from Finding 4-A — covers the spike part), (3) `validate_test_strategy_complete()` (from Finding 6-B — covers entry_criteria[1] and [2]), (4) DECISION_LOG.md has entries (minimal existence check — covers entry_criteria[3]). Add `"implementation_loop": "implementation-entry"` to `stage_checks`. Wire dispatch.
- **Reason**: These are the most explicitly documented gate criteria in the entire system. They exist as structured data in the registry. They were designed to be enforced. Not enforcing them is a system design gap, not an intentional omission.
- **Critical note**: This is the highest-value single automation in this audit. Implementation without validated architecture, test strategy, and spike resolution is the exact failure mode the PROGRAMBUILD system was designed to prevent. The entry_criteria array exists specifically to be read programmatically — it has no other purpose. **Schema note**: `process-registry.schema.json` defines `workflow_guidance` as a bare `type: "object"` with no inner structure — the entry_criteria array format, prompt lists, and script references are entirely unconstrained by the schema. A malformed or empty entry_criteria array passes schema validation silently.

#### Finding 7-B: `implement-gameplan-phase*.prompt.md` not surfaced by `programstart guide`

- **Verdict: AUTOMATE**
- **Source of truth**: `process-registry.json` `workflow_guidance.programbuild.implementation_loop.prompts` contains only `["programstart-stage-guide.prompt.md", "programstart-stage-transition.prompt.md"]`. The 8 `implement-gameplan-phase*.prompt.md` files are listed only in `bootstrap_assets`, not in `implementation_loop.prompts`.
- **Current state**: `programstart guide --system programbuild` at Stage 7 returns the generic stage-guide and stage-transition prompts. It does not surface the implementation gameplan prompts. `product-jit-check.prompt.md` is also absent.
- **Suggested mapping**: Add to `implementation_loop.prompts` in `process-registry.json`:
  ```json
  ".github/prompts/product-jit-check.prompt.md",
  ".github/prompts/implement-gameplan-phase1.prompt.md",
  ".github/prompts/implement-gameplan-phase2.prompt.md",
  ".github/prompts/implement-gameplan-phase3.prompt.md",
  ".github/prompts/implement-gameplan-phase4.prompt.md",
  ".github/prompts/implement-gameplan-phase7.prompt.md",
  ".github/prompts/implement-gameplan-phase8.prompt.md",
  ".github/prompts/implement-gameplan-phase9.prompt.md",
  ".github/prompts/implement-gameplan-phase10.prompt.md"
  ```
- **Reason**: The guide system is the JIT-protocol-compliant way to discover applicable prompts. If Stage 7 prompts are not in the guidance, the JIT protocol (`source-of-truth.instructions.md` Step 1: "derive context now — run `programstart guide`; read only those files") actively prevents the operator from discovering them. This is a direct violation of **JIT Step 1**: the protocol says derive-from-registry, and the registry omits these prompts.
- **Critical note**: This is a registry configuration bug, not a feature request. The prompts exist, they're meant for Stage 7, and the registry guidance system is designed to surface them. Fix is a config-only change with no code needed. Per the **source-of-truth temporal semantics**, an operator following JIT Step 1 is instructed to "treat everything else as tentative" — meaning these implementation prompts are effectively invisible to a compliant operator.

#### Finding 7-C: No test-pass validation before advance

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD.md` Section 14 definition of done includes "structural tests green." `PROGRAMBUILD_GAMEPLAN.md` Stage 8 Cross-Stage Validation: "Every P0 requirement from REQUIREMENTS.md is implemented, tested, and passing." Implementation is in the *generated project repo*, not PROGRAMSTART.
- **Current state**: `preflight_problems()` runs file-existence, metadata, authority-sync, drift, and stage-gate content checks. It does not run `pytest` or check CI status.
- **Suggested mapping**: For PROGRAMSTART itself, `nox -s tests` or `pytest` could be invoked during preflight for `implementation_loop` stage. However, for generated projects, PROGRAMSTART cannot know the test command. Option: add an optional `test_command` field to `workflow_state.programbuild` state that the operator can set, and `preflight_problems()` invokes it if present.
- **Reason**: Running tests before advancing ensures the implementation actually passes its own quality bar. But this crosses the boundary between PROGRAMSTART (template repo) and the generated project.
- **Critical note**: For PROGRAMSTART's own development, tests already run via CI and nox. For generated projects, PROGRAMSTART shouldn't assume the test runner. CONSIDER adding as an opt-in config, not a default.

---

### Stage 8: release_readiness

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-release-readiness.prompt.md` (Phase H, 2026-04-12) |
| Stage-gate validation | ✅ | `validate --check release-ready` at `validate.py:434` (Phase G, 2026-04-12) |
| Preflight dispatch | ✅ | `stage_checks["release_readiness"] = "release-ready"` (2026-04-12) |
| Registry guidance | ✅ | `workflow_guidance.programbuild.release_readiness.prompts` includes `shape-release-readiness.prompt.md` |

#### Finding 8-A: No `shape-release-readiness.prompt.md`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 15 defines 5 minimum gate items: deployment validated, rollback validated, secrets verified, smoke tests pass, monitoring active. `PROGRAMBUILD_GAMEPLAN.md` Stage 8 defines 3 steps and 6 cross-stage validation checks including a final kill-criteria re-check and dependency health check. `PROGRAMBUILD_CHECKLIST.md` Section 9 has 10 items including "verify rollback plan", "verify monitoring and alerting", "verify SLO and SLI targets".
- **Current state**: No prompt exists. `workflow_guidance.programbuild.release_readiness.prompts` has only generic prompts.
- **Suggested mapping**: Create `.github/prompts/shape-release-readiness.prompt.md`. Content: (1) Load ARCHITECTURE.md, TEST_STRATEGY.md, REQUIREMENTS.md, FEASIBILITY.md kill criteria, (2) Produce RELEASE_READINESS.md with deployment plan, rollback plan, secrets audit, smoke test results, monitoring config, (3) Re-check all kill criteria from FEASIBILITY.md, (4) Verify all P0 requirements are implemented and passing, (5) Run final dependency health check. Add to registry and bootstrap_assets.
- **Reason**: Release readiness is a critical gate. The PROGRAMBUILD.md minimum gate is explicit and structured. A prompt codifying this prevents release decisions based on "feels done."
- **Critical note**: High value. This is the last quality gate before code reaches users. **Canonical note**: Same Rule 5 housekeeping as Finding 5-A — new prompt must be added to FILE_INDEX.md, registry guidance, and bootstrap_assets.

#### Finding 8-B: No `validate --check release-ready`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 15 minimum gate (5 items). `PROGRAMBUILD_GAMEPLAN.md` Stage 8 Cross-Stage Validation (6 checks). `PROGRAMBUILD_CHECKLIST.md` Section 9 (10 items).
- **Current state**: No validation function. Stage 8 has no entry in `stage_checks`.
- **Suggested mapping**: Create `validate_release_ready()` in `validate.py`. Checks: (1) RELEASE_READINESS.md exists with non-template content, (2) Required sections exist: "Deployment", "Rollback", "Monitoring" (section-header check), (3) A go/no-go decision exists (similar to feasibility recommendation check), (4) Kill criteria from FEASIBILITY.md are re-checked (cross-reference: look for kill-criteria keywords in RELEASE_READINESS.md or a "Kill Criteria" section). Add `"release_readiness": "release-ready"` to `stage_checks`. Wire dispatch and argparse.
- **Reason**: Without this check, the operator can advance past release readiness with an empty or template-only RELEASE_READINESS.md. The PROGRAMBUILD.md gate items are explicitly "minimum" — they are non-negotiable.
- **Critical note**: The check necessarily validates document structure, not operational reality (PROGRAMSTART can't verify that monitoring is actually active). But catching an empty release readiness doc is still high value.

#### Finding 8-C: No security scan gate

- **Verdict: SKIP**
- **Source of truth**: No authority doc mandates a security scan as a release gate. `PROGRAMBUILD.md` Section 15 mentions "secrets and config verified" but not automated scanning.
- **Current state**: `noxfile.py` has a `security` session (runs `bandit` and `pip-audit`) but it's a separate nox session, not wired into advance.
- **Reason**: Security scanning is a CI concern, not a PROGRAMSTART workflow state concern. The nox `security` session and CI gate already handle this. Wiring it into advance would duplicate the CI gate.
- **Critical note**: Skip. Already covered by `nox -s ci` and GitHub Actions.

---

### Stage 9: audit_and_drift_control

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `audit-process-drift.prompt.md` |
| Stage-gate validation | ✅ | `validate --check audit-complete` at `validate.py:468` (Phase G, 2026-04-12) |
| Preflight dispatch | ✅ | `stage_checks["audit_and_drift_control"] = "audit-complete"` (2026-04-12) |
| Drift check | ✅ | `programstart drift` runs at any stage in preflight |

#### Finding 9-A: No `validate --check audit-complete`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 16 gate: "All critical and high findings must have owners, fixes, or explicit acceptance before release." `PROGRAMBUILD_GAMEPLAN.md` Stage 9: "Produce AUDIT_REPORT.md with severity, category, evidence, impact, fix, and prevention. All critical and high findings must have owners." `PROGRAMBUILD_CHECKLIST.md` Section 10: "assign owners for critical and high findings", "record any explicit residual-risk acceptance."
- **Current state**: No validation function. Stage 9 has no entry in `stage_checks`.
- **Suggested mapping**: Create `validate_audit_complete()` in `validate.py`. Checks: (1) AUDIT_REPORT.md exists with non-template content, (2) A findings table exists (look for `| Severity` or `| Category` table header), (3) If findings table has rows with "Critical" or "High" severity, check that "Owner" or "Assigned" column is non-empty. Add `"audit_and_drift_control": "audit-complete"` to `stage_checks`. Wire dispatch and argparse.
- **Reason**: The PROGRAMBUILD.md gate is explicit about ownership of critical/high findings. Without this check, an audit report with unassigned critical findings can advance to post-launch.
- **Critical note**: Medium-high value. The table-parsing pattern already exists in `validate_requirements_complete()` (using `parse_markdown_table`). Reuse that pattern for audit findings.

#### Finding 9-B: Drift check is general-purpose, not Stage 9 specific

- **Verdict: SKIP**
- **Source of truth**: `programstart drift` runs in `preflight_problems()` at `workflow_state.py:129-132` for *every* advance, not just Stage 9.
- **Current state**: Drift detection runs at every stage transition. Stage 9 adds the `audit-process-drift.prompt.md` for a comprehensive review.
- **Reason**: Making drift "Stage 9 only" would be a regression. The current behavior (drift runs everywhere, plus a dedicated audit prompt at Stage 9) is correct.
- **Critical note**: Skip. This is correctly designed. The gap is not "drift should be gated to Stage 9" — it's that AUDIT_REPORT.md content isn't validated (Finding 9-A).

---

### Stage 10: post_launch_review

| Capability | Status | Detail |
|---|---|---|
| Shaping prompt | ✅ | `shape-post-launch-review.prompt.md` (Phase H, 2026-04-12) |
| Stage-gate validation | ❌ | Terminal stage — no advance gate needed |
| Preflight dispatch | ❌ | Terminal stage — no advance gate needed |
| Registry guidance | ✅ | `workflow_guidance.programbuild.post_launch_review.prompts` includes `shape-post-launch-review.prompt.md` |

#### Finding 10-A: No `shape-post-launch-review.prompt.md`

- **Verdict: AUTOMATE**
- **Source of truth**: `PROGRAMBUILD.md` Section 17 defines required content: success metric comparison, decision validation/reversal review, incident/gap review, follow-up assignments with owners, Template Improvement Review (7-row proposal table). `PROGRAMBUILD_GAMEPLAN.md` Stage 10 defines 5 steps, 5 cross-stage validation checks, and a full Template Improvement Review protocol. `PROGRAMBUILD_CHECKLIST.md` Section 11 has 7 items including "run Template Improvement Review."
- **Current state**: No prompt. The Template Improvement Review is the most structured protocol in PROGRAMBUILD.md Section 17 and has no automated guidance.
- **Suggested mapping**: Create `.github/prompts/shape-post-launch-review.prompt.md`. Content: (1) Load KICKOFF_PACKET (SUCCESS_METRIC), FEASIBILITY.md (kill criteria), DECISION_LOG.md (reversals), (2) Produce POST_LAUNCH_REVIEW.md: metric comparison, kill criteria final review, lessons learned, follow-up owners, (3) Run Template Improvement Review: for each lesson, assess "systemic?" and propose PROGRAMBUILD template update if yes. Add to registry and bootstrap_assets.
- **Reason**: The Template Improvement Review is the feedback loop that improves PROGRAMBUILD across projects. Without a prompt guiding it, the review is likely to be skipped or done superficially.
- **Critical note**: Medium value. Stage 10 is a terminal stage — there's no "advance to check." The value is in process improvement, not gate enforcement. But the Template Improvement Review is unique and valuable enough to warrant dedicated prompt guidance. **Canonical note**: Same Rule 5 housekeeping as Finding 5-A — new prompt must be added to FILE_INDEX.md, registry guidance, and bootstrap_assets.

#### Finding 10-B: No success metric comparison automation

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD_GAMEPLAN.md` Stage 10 step 2: "Compare actual metrics to the success metric from the inputs block." Cross-Stage Validation: "The success metric comparison uses the exact metric from the inputs block, not a reframed version."
- **Current state**: No script reads SUCCESS_METRIC from KICKOFF_PACKET and checks whether POST_LAUNCH_REVIEW.md references it.
- **Suggested mapping**: In a `validate_post_launch_complete()` function, read SUCCESS_METRIC from KICKOFF_PACKET, then check that POST_LAUNCH_REVIEW.md contains the metric text or a section that references it. Pattern: extract SUCCESS_METRIC value, check `metric_text in post_launch_text`.
- **Reason**: Prevents the common failure of "we launched, here are some numbers" without connecting back to the original success metric. The GAMEPLAN cross-stage validation explicitly warns against "a reframed version."
- **Critical note**: A text-matching check is fragile (metric wording may evolve). More robust: check for a "Success Metric" section header in POST_LAUNCH_REVIEW.md. That's sufficient to confirm the comparison was attempted.

---

## USERJOURNEY Phases (0–8)

### Cross-cutting Assessment

- **Source of truth**: `USERJOURNEY/DELIVERY_GAMEPLAN.md` defines a Source of Truth Matrix (10 rows), Operating Rule, and procedural Delivery Steps. `userjourney.instructions.md` mandates treating `first_value_achieved` as the canonical activation event. `process-registry.json` `workflow_guidance.userjourney` defines files, scripts, and prompts for each phase — all phases share the same two generic prompts.
- **Current state**: `preflight_problems()` at `workflow_state.py:123-126` runs `validate_required_files`, `validate_metadata`, and `validate_workflow_state` for userjourney but NO content checks. `stage_checks` dict has a `system == "programbuild"` guard at line 135 — userjourney is entirely excluded from content validation. `validate_engineering_ready()` exists but is gated by `enforce_engineering_ready_in_all` which is `false` in `process-registry.json`.
- **Critical note**: USERJOURNEY is a **project attachment** (`packaging: "project_attachment"`, `optional: true`). It is not part of the reusable template system per `PROGRAMBUILD_CANONICAL.md` Rule 7. This means USERJOURNEY automation has lower priority than PROGRAMBUILD automation — it's project-specific, not structural.

#### Finding UJ-A: No phase-specific shaping prompts

- **Verdict: CONSIDER**
- **Source of truth**: `workflow_guidance.userjourney.phase_0` through `phase_8` all list the same two prompts: `userjourney-next-slice.prompt.md` + `programstart-stage-guide.prompt.md`. The DELIVERY_GAMEPLAN defines 9 distinct phases with different deliverables and concerns per phase.
- **Current state**: All phases use the same generic guidance. No phase-specific protocol exists.
- **Suggested mapping**: For highest-value phases, create dedicated prompts:
  - `shape-uj-product-freeze.prompt.md` (Phase 0): Load OPEN_QUESTIONS.md, resolve all items, produce decision freeze.
  - `shape-uj-legal-drafts.prompt.md` (Phase 1): Load LEGAL_AND_CONSENT.md, produce TOS/Privacy drafts against consent rules.
  - `shape-uj-state-routing.prompt.md` (Phase 3): Load ROUTE_AND_STATE_FREEZE.md + STATES_AND_RULES.md, produce state machine design.
  Add each to the corresponding phase in `workflow_guidance.userjourney` and to `userjourney_bootstrap_assets` or `bootstrap_assets`.
- **Reason**: Phases 0, 1, and 3 have the most structured deliverables (decision freeze, legal drafts, state machine) and would benefit most from dedicated prompts. Other phases (5: implementation, 6: QA) are execution-focused and well-served by the generic slice prompt.
- **Critical note**: Lower priority than PROGRAMBUILD prompts. The USERJOURNEY is project-specific. Creating 9 phase-specific prompts is over-engineering. Create prompts only for phases with structured, repeatable deliverables (0, 1, 3 at most).

#### Finding UJ-B: No USERJOURNEY content gate checks

- **Verdict: CONSIDER**
- **Source of truth**: `workflow_state.py:135`: `if system == "programbuild" and active_step:` — hard-coded programbuild-only guard. DELIVERY_GAMEPLAN.md Operating Rule: "Do not update code-planning documents independently." The DELIVERY_GAMEPLAN defines per-phase deliverables but no explicit gate criteria.
- **Current state**: USERJOURNEY advance runs file-existence, metadata, and workflow-state checks only. No content validation for any phase.
- **Suggested mapping**: For highest-value phases, create content validators:
  - Phase 0: `validate_uj_decision_freeze()` — check OPEN_QUESTIONS.md has 0 unresolved items (reuse `validate_engineering_ready()` logic which already does this at `validate.py:585`).
  - Phase 1: `validate_uj_legal_drafts()` — check TERMS_OF_SERVICE_DRAFT.md and PRIVACY_POLICY_DRAFT.md exist with non-template content.
  - Phase 3: `validate_uj_state_freeze()` — check ROUTE_AND_STATE_FREEZE.md has route definitions (table with `| Route` header or equivalent).
  Extend the `stage_checks` dict to support userjourney by removing the `system == "programbuild"` guard and adding phase-specific entries.
- **Reason**: The engineering-ready check already validates OPEN_QUESTIONS.md resolution — but it's disabled by default. Phase 0 is essentially "resolve all open questions," which is exactly what `validate_engineering_ready()` checks. This is the lowest-friction automation: the code exists, it just needs to be wired in.
- **Critical note**: Phase 0 (decision freeze) has the clearest, most automatable gate: "are all open questions resolved?" For other phases, the deliverables are harder to validate structurally because USERJOURNEY docs are prose-heavy project-specific content. Recommend automating Phase 0 first, then evaluating if others justify the effort.

#### Finding UJ-C: `engineering-ready` check disabled by default

- **Verdict: AUTOMATE**
- **Source of truth**: `process-registry.json` line 190: `"enforce_engineering_ready_in_all": false`. `validate.py:585`: `validate_engineering_ready()` checks OPEN_QUESTIONS.md for unresolved items under "Remaining Operational And Legal Decisions". The `all` composite check at `validate.py:1002` conditionally includes it only when the flag is true.
- **Current state**: The check exists, works, and is tested — but never runs in normal validation because the flag is false.
- **Suggested mapping**: Two options: (A) Change `enforce_engineering_ready_in_all` to `true` in `process-registry.json`. This is a one-line config change. (B) Wire it into Phase 0 advance only (not `all`) — add `"phase_0": "engineering-ready"` to a userjourney section of `stage_checks`.
- **Reason**: The check was built, tested, and deployed. It validates the single most important USERJOURNEY gate: "are all blocking questions resolved before implementation?" Having it disabled by default means it never runs.
- **Critical note**: Option B (Phase 0 only) is preferred. Running it in `all` means it blocks `validate --check all` at every stage even when the USERJOURNEY hasn't reached Phase 0 yet.

#### Finding UJ-D: No `first_value_achieved` activation event validation

- **Verdict: SKIP**
- **Source of truth**: `userjourney.instructions.md`: "MUST treat `first_value_achieved` as the canonical activation event." `process-registry.json` `systems.userjourney.activation_event: "first_value_achieved"`.
- **Current state**: The activation event is defined in config but consumed only by prompts and human processes. No script validates that the concept appears in ANALYTICS_AND_OUTCOMES.md or implementation code.
- **Reason**: Validating that "first_value_achieved" appears in docs is trivial but low value — it's a string match that doesn't confirm the concept is correctly implemented. Validating it in code requires running the generated project's tests, which is out of PROGRAMSTART's scope.
- **Critical note**: Skip. The instruction file and config define it. The prompt system surfaces it. Structural validation adds no real safety.

---

## Cross-Cutting Infrastructure

### What IS Automated

| Area | Tool | Source of Truth |
|---|---|---|
| File existence | `validate --check required-files` | `systems.*.control_files + output_files + core_files` in registry |
| Metadata blocks | `validate --check metadata` | `systems.*.metadata_required` + `metadata_rules.required_prefixes` in registry |
| Authority sync | `validate --check authority-sync` | `sync_rules[]` in registry + `PROGRAMBUILD_CANONICAL.md` lists |
| Drift detection | `programstart drift` | `sync_rules[]` + git changed-files |
| Bootstrap assets | `validate --check bootstrap-assets` | `workspace.bootstrap_assets` in registry |
| Repo boundary | `validate --check repo-boundary` | `repo_boundary_policy` in registry |
| ADR coverage | `validate --check adr-coverage` | `docs/decisions/README.md` |
| KB freshness | `validate --check kb-freshness` | `config/knowledge-base.json` |
| Workflow state (manual) | `validate --check workflow-state` | `process-registry.json` stage_order + manual checks in `validate_workflow_state()` |
| Workflow state (schema) | Pre-commit + Nox `lint` via `check-jsonschema` | `schemas/programbuild-state.schema.json`, `schemas/userjourney-state.schema.json` |
| Registry schema | Pre-commit + Nox `lint` via `check-jsonschema` | `schemas/process-registry.schema.json` |
| Planning references | `validate --check planning-references` | `planning_reference_rules` in registry |
| Rule enforcement | `validate --check rule-enforcement` | `sync_rules[]` in registry |
| Test file count | `validate --check test-coverage` | `tests/test_*.py` glob |
| CI gate | `nox -s ci` / GitHub Actions | `noxfile.py` + `.github/workflows/` |
| Challenge gate log | `_check_challenge_gate_log()` | `PROGRAMBUILD_CHALLENGE_GATE.md` gate log table |
| Dashboard | `programstart serve` | State files (stage-agnostic display) |
| Sign-off log | `programstart log` | State file `signoff_history` |

### Cross-Cutting Gaps

#### Finding X-A: No test-pass as precondition for any advance

- **Verdict: CONSIDER**
- **Source of truth**: `PROGRAMBUILD.md` Section 12: "Feature work starts only after every structural test is green." Section 14 definition of done: "structural tests green." `PROGRAMBUILD_GAMEPLAN.md` Stage 8 Cross-Stage Validation: "Every P0 requirement is implemented, tested, and passing."
- **Current state**: `preflight_problems()` at `workflow_state.py:121-145` does not invoke any test runner.
- **Suggested mapping**: Add an optional `preflight_test_command` to `workflow_state.programbuild` config. If set, `preflight_problems()` invokes it before advance. Default: not set (no change in behavior). For PROGRAMSTART itself, could be `["uv", "run", "pytest", "--tb=line", "-q"]`.
- **Reason**: For PROGRAMSTART's own development, tests already run via CI. For generated projects, PROGRAMSTART doesn't know the test command. The value is in making it configurable, not mandatory.
- **Critical note**: Low priority. CI already catches this for PROGRAMSTART. For generated projects, this is opt-in configuration, not a structural gap.

#### Finding X-B: Dashboard is stage-agnostic (no stage-specific guidance)

- **Verdict: SKIP**
- **Source of truth**: No authority doc defines dashboard content requirements per stage.
- **Current state**: `programstart serve` renders a web dashboard showing current state, sign-off history, and validation status. It does not show stage-specific guidance, recommended prompts, or next actions.
- **Reason**: `programstart guide` already provides stage-specific guidance. The dashboard is a state viewer, not a guidance tool. Duplicating guide output in the dashboard would create a maintenance burden and a second source of truth for stage guidance.
- **Critical note**: Skip. The dashboard and guide have different responsibilities. Merging them violates the single-responsibility principle already established by the toolchain design.

#### Finding X-C: No automated backlog prioritization engine

- **Verdict: SKIP**
- **Source of truth**: None. No authority doc defines automated prioritization.
- **Current state**: Requirements priorities (P0/P1/P2) are assigned manually during Stage 3.
- **Reason**: Prioritization is a product decision, not a process automation. PROGRAMSTART validates priorities exist and are valid; it should not assign them.
- **Critical note**: Skip. Out of scope for a planning template system.

---

## Summary: Prioritized Gap List

Findings sorted by automation value:

### Tier 1 — AUTOMATE (clear value, source-of-truth backed)

| ID | Finding | Stage | Effort | Key Source of Truth | Status |
|---|---|---|---|---|---|
| 7-A | Entry criteria not enforced | 7 | Medium | `registry.implementation_loop.entry_criteria` (4 items) | ✅ DONE (Phase G) |
| 7-B | Implementation prompts not in guide | 7 | Trivial | `registry.workflow_guidance.implementation_loop.prompts` | ✅ DONE (Phase B) |
| 5-A | No shape-scaffold prompt | 5 | Medium | `PROGRAMBUILD.md` Section 12 (scaffold protocol) | ✅ DONE (Phase H) |
| 6-A | No shape-test-strategy prompt | 6 | Medium | `PROGRAMBUILD.md` Section 13 (test strategy protocol) | ✅ DONE (Phase H) |
| 6-B | No test-strategy-complete validation | 6 | Medium | `GAMEPLAN.md` Stage 6 + `registry.entry_criteria[1-2]` | ✅ DONE (Phase G) |
| 8-A | No shape-release-readiness prompt | 8 | Medium | `PROGRAMBUILD.md` Section 15 (5 minimum gate items) | ✅ DONE (Phase H) |
| 8-B | No release-ready validation | 8 | Medium | `PROGRAMBUILD.md` Section 15 gate | ✅ DONE (Phase G) |
| 4-A | No RISK_SPIKES resolution check | 4→5 | Medium | `GAMEPLAN.md` Stage 7 entry_criteria[0] | ✅ DONE (Phase F + stage_checks) |
| 9-A | No audit-complete validation | 9 | Medium | `PROGRAMBUILD.md` Section 16 gate | ✅ DONE (Phase G) |
| 10-A | No shape-post-launch-review prompt | 10 | Medium | `PROGRAMBUILD.md` Section 17 + Template Improvement Review | ✅ DONE (Phase H) |
| 3-A | Cross-reference substring bug | 3 | Trivial | `validate.py:261` — one-line regex fix | ✅ DONE (Phase B) |
| 0-C | No DECISION_LOG entry at Stage 0 | 0 | Small | `GAMEPLAN.md` Stage 0 step 5 | ✅ DONE (Phase E) |
| 1-A | No DECISION_LOG cross-ref at Stage 1 | 1 | Small | `GAMEPLAN.md` Stage 1 step 3 + sync_rule | ✅ DONE (Phase E) |
| 4-B | No DECISION_LOG cross-ref at Stage 4 | 4 | Small | sync_rule `architecture_decision_alignment` | ✅ DONE (Phase E) |
| UJ-C | engineering-ready check disabled | UJ | Trivial | `registry.enforce_engineering_ready_in_all` | ✅ DONE (Phase B stage6 — wired into UJ phase_0 preflight at `workflow_state.py`) |

### Tier 2 — CONSIDER (value depends on context)

| ID | Finding | Stage | Effort | Key Source of Truth | Status |
|---|---|---|---|---|---|
| 2-A | No research-complete validation | 2 | Medium | `GAMEPLAN.md` Stage 2 cross-stage + CHECKLIST | |
| 5-B | No scaffold-complete validation | 5 | Medium | `PROGRAMBUILD.md` Section 12 gate | |
| 1-B | Challenge gate advisory-only | All | Medium | `CHALLENGE_GATE.md` "not optional" | |
| 0-A | No PRODUCT_SHAPE whitelist | 0 | Small | `PROGRAMBUILD.md` Section 3 (shapes table) | ✅ DONE (Phase E stage6) |
| 3-C | No USER_FLOWS structural validation | 3 | Small | `GAMEPLAN.md` Stage 3 + CHECKLIST | ✅ DONE (Phase E stage6) |
| 7-C | No test-pass before advance | 7 | Medium | `PROGRAMBUILD.md` Sections 12, 14 | |
| 10-B | No success metric comparison | 10 | Small | `GAMEPLAN.md` Stage 10 step 2 | |
| UJ-A | No phase-specific prompts | UJ | Large | `DELIVERY_GAMEPLAN.md` phase definitions | |
| UJ-B | No USERJOURNEY content gates | UJ | Large | `DELIVERY_GAMEPLAN.md` + instruction files | |
| X-A | No test-pass precondition | All | Medium | `PROGRAMBUILD.md` Sections 12, 14 | |
| 6-C | test-coverage check misleading | 6 | Trivial | `validate.py` naming | ✅ DONE (Phase E stage6) |
| SCH-A | Runtime validator skips JSON schema | All | Small | `.pre-commit-config.yaml` + `validate.py:907` | |
| SCH-B | Registry schema unconstrained inner structure | All | Medium | `schemas/process-registry.schema.json` | |

### Tier 3 — SKIP (low value or intentionally deferred)

| ID | Finding | Stage | Reason |
|---|---|---|---|
| 0-B | recommend not auto-triggered | 0 | Prompt already covers this; recommend at advance is too late |
| 1-C | No RISK_SPIKES seeding at Stage 1 | 1 | RISK_SPIKES is a Stage 4 deliverable; seeding is optional |
| 2-B | No file-modification check | 2 | Fragile; superseded by Finding 2-A |
| 3-B | No P0 minimum count | 3 | Project-dependent; semantic check can't be automated |
| 4-C | No per-contract completeness | 4 | PRODUCT_SHAPE-variable structure; high maintenance, low value |
| 5-C | Scaffold script vs Stage 5 mismatch | 5 | Category error — different artifacts |
| 8-C | No security scan gate | 8 | Already covered by nox + CI |
| 9-B | Drift not Stage-9-specific | 9 | Current design is correct (drift runs everywhere) |
| UJ-D | No first_value_achieved validation | UJ | String match adds no real safety |
| X-B | Dashboard stage-agnostic | All | Guide handles stage guidance; dashboard is state viewer |
| X-C | No backlog prioritization | All | Product decision, not process automation |
| SCH-C | Schema signoff.decision unconstrained | All | Manual validator already catches this; earlier detection is marginal |

---

## Schema, Canonical, and Source-of-Truth Audit

This section assesses whether the findings above properly account for three structural dimensions: **JSON schema enforcement**, **PROGRAMBUILD_CANONICAL.md authority rules**, and the **JIT source-of-truth protocol** from `source-of-truth.instructions.md`.

### Schema Enforcement Model

The three JSON schemas in `schemas/` are enforced at **two layers**:

| Layer | Tool | When | What it catches |
|---|---|---|---|
| Pre-commit | `check-jsonschema` hooks (`.pre-commit-config.yaml` lines 47–65) | On every commit | Structural violations of all 3 schemas |
| CI / Nox | `nox -s lint` → `check-jsonschema` runs (`noxfile.py` lines 72–87) | CI gate, on-demand | Same structural violations |
| Runtime | `validate_workflow_state()` at `validate.py:907–960` | `programstart validate` / `programstart advance` | Manual checks that **partially overlap** with schemas but are stricter in some areas |

**Key gap**: `programstart validate --check workflow-state` and `programstart advance` call `validate_workflow_state()`, which does NOT invoke `check-jsonschema` or the `jsonschema` library. It performs manual checks. An operator who edits a state file and runs `programstart advance` without committing first **skips schema validation entirely**.

### Schema Permissiveness Analysis

| Schema | Required fields enforced | What is NOT constrained |
|---|---|---|
| `process-registry.schema.json` | 7 top-level keys (version, workspace, systems, sync_rules, metadata_rules, workflow_guidance, workflow_state) | `workflow_guidance` and `workflow_state` are bare `type: "object"` — no inner structure. Entry criteria, prompt lists, script references, stage names are all unconstrained. `additionalProperties: true` everywhere. |
| `programbuild-state.schema.json` | system (const "programbuild"), active_stage, stages, variant. Per stage: status (enum 4 values), signoff (requires decision, date, notes) | Stage key names (any string accepted). `signoff.decision` is `type: "string"` — no value constraint. `signoff.date` is `type: "string"` — no format constraint. |
| `userjourney-state.schema.json` | system (const "userjourney"), active_phase, phases. Per phase: same as above | Same as programbuild: phase key names unconstrained, signoff.decision/date unconstrained. |

### Schema vs. Manual Validator Divergence

`validate_workflow_state()` and the state schemas overlap but diverge:

| Check | Schema | Manual validator (`validate_workflow_state()`) |
|---|---|---|
| Status enum (planned/in_progress/completed/blocked) | ✅ enforced | ✅ enforced |
| Signoff requires decision, date, notes | ✅ enforced | ⚠️ checks decision and date only (notes not checked) |
| Signoff decision value (approved/go/accepted) | ❌ any string | ✅ enforced |
| Signoff date format (YYYY-MM-DD) | ❌ any string | ✅ enforced |
| Stage/phase names match registry | ❌ any key | ✅ enforced (checks against `workflow_steps()`) |
| Ordering (before active = completed) | ❌ not modeled | ✅ enforced |
| Exactly one in_progress step | ❌ not modeled | ✅ enforced |
| `variant` field required | ✅ (programbuild only) | ❌ not checked |
| `system` const value | ✅ enforced | ❌ not checked |

#### Finding SCH-A: `validate_workflow_state()` does not delegate to JSON schemas at runtime

- **Verdict: CONSIDER**
- **Source of truth**: Pre-commit hooks at `.pre-commit-config.yaml:47–65` and Nox lint session at `noxfile.py:72–87` enforce all 3 schemas at commit/CI time. `validate_workflow_state()` at `validate.py:907` reimplements a **subset** of schema checks manually and adds runtime-specific checks (ordering, decision values, date format) that schemas don't cover.
- **Current state**: Schema validation and runtime validation are **independent systems** that partially overlap. Neither is a superset of the other. The `variant` field requirement (schema-only) and `system` const check (schema-only) are never verified at runtime. Conversely, decision value constraints and ordering checks are never verified by schema.
- **Suggested mapping**: Two options: (A) Add `jsonschema` as a runtime dependency, import the schema files in `validate_workflow_state()`, and run `jsonschema.validate()` before the manual checks — catches structural issues that manual checks miss (variant, system const). (B) Add the 2 missing manual checks (variant non-empty, system matches expected const) to `validate_workflow_state()` — avoids a new dependency. Option B is preferred for a planning-tools repo.
- **Reason**: The divergence is a maintenance risk. If the schema adds a new required field, the manual validator won't catch its absence at runtime. If the manual validator adds a new decision value to the allowed set, the schema doesn't know.
- **Critical note**: The current two-layer design (schema at commit, manual at runtime) works in practice because pre-commit catches structural errors before they reach runtime. The risk is limited to: (1) direct state file edits followed by `programstart advance` without committing, (2) schema evolution that isn't mirrored in manual checks. For a solo-operator planning repo, this is low risk. Worth a CONSIDER, not a hard AUTOMATE.

#### Finding SCH-B: Registry schema does not constrain `workflow_guidance` or `workflow_state` inner structure

- **Verdict: CONSIDER**
- **Source of truth**: `schemas/process-registry.schema.json` defines `workflow_guidance` and `workflow_state` as `"type": "object"` with no `properties`, no `required`, and no `additionalProperties` constraint. The actual structure (per-stage guidance with prompts/scripts/files arrays, entry_criteria, step_files, etc.) is entirely convention-enforced.
- **Current state**: The registry schema validates that `workflow_guidance` and `workflow_state` exist as objects. It does not validate that any particular stage has guidance, that prompts arrays contain strings, that entry_criteria is an array, or that step_files maps to valid paths. A registry edit that accidentally deletes all stage guidance or malforms an entry_criteria array passes schema validation.
- **Suggested mapping**: Extend `process-registry.schema.json` to define inner structure for `workflow_guidance` (at minimum: `additionalProperties` with a stage-guidance schema requiring `prompts` and `scripts` as string arrays) and for `workflow_state` (at minimum: require `state_file` and `schema` as strings). This tightens pre-commit validation without adding runtime complexity.
- **Reason**: `workflow_guidance` is the data backbone for `programstart guide` (JIT Step 1). If its structure breaks, `programstart guide` returns wrong or empty results, which violates the JIT protocol silently. Finding 7-B (prompts missing from guidance) is a direct example — the schema did not prevent it.
- **Critical note**: Schema tightening is a one-time effort that prevents a class of registry malformation errors. However, `process-registry.json` is edited infrequently and always reviewed — the risk of silent malformation is low in practice. CONSIDER, not AUTOMATE.

#### Finding SCH-C: State schema `signoff.decision` is unconstrained (any string accepted)

- **Verdict: SKIP**
- **Source of truth**: `programbuild-state.schema.json` and `userjourney-state.schema.json` both define `signoff.decision` as `"type": "string"`. `validate_workflow_state()` at `validate.py:944` checks `decision not in ("approved", "go", "accepted")` — the manual validator is the enforcement point.
- **Current state**: The schema accepts `decision: "lgtm"` or `decision: ""` but the runtime validator rejects them.
- **Suggested mapping**: Add `"enum": ["approved", "go", "accepted", ""]` to `signoff.decision` in both state schemas. The empty string allows planned/upcoming stages where no decision has been made yet.
- **Reason**: Aligning schema and validator eliminates the divergence. A pre-commit hook would catch invalid decisions earlier than `programstart validate`.
- **Critical note**: Low value. The runtime validator already catches this. The benefit is earlier detection (commit time vs. validate time). For a solo-operator repo, the operator is the same person editing and validating. SKIP — the manual validator is sufficient.

### Canonical Authority Implications

**PROGRAMBUILD_CANONICAL.md** defines an authority map (25+ concern→file mappings), conflict resolution order, and maintenance rules. These affect several findings:

1. **Findings requiring new deliverables (5-A, 6-A, 8-A, 10-A)**: CANONICAL Rule 5 mandates that any new deliverable file be added to: (a) `PROGRAMBUILD_FILE_INDEX.md`, (b) the CANONICAL authority map if the file becomes authority for a concern, (c) a `sync_rule` if cross-referenced. The new prompts proposed in these findings are tooling files (not output documents), so they belong in the FILE_INDEX.md "Tooling and Enforcement" table and in `bootstrap_assets`. They do NOT require CANONICAL authority map entries unless a prompt becomes the sole authority for defining a concern's rules (unlikely for shaping prompts, which derive from PROGRAMBUILD.md sections). **Updated in each finding above.**

2. **Findings involving cross-file validation (0-C, 1-A, 4-B, 6-B)**: These propose validators that cross-reference files. Per CANONICAL conflict resolution (validated code > canonical reference > authority map > supporting), the validators should: (a) read the **authority file** first (per the relevant sync_rule), (b) then check the **dependent file** for consistency. Example: Finding 1-A should read FEASIBILITY.md (authority per `programbuild_feasibility_cascade` sync_rule) before checking DECISION_LOG.md (dependent). The implementations should respect this ordering.

3. **CANONICAL conflict resolution and automation.md verdicts**: The CANONICAL conflict resolution order is: validated running code > PROGRAMBUILD_CANONICAL.md > authority map source > supporting references. This means: (a) where running code (e.g., `validate_workflow_state()`) already handles a concern, it takes precedence — we should not add schema enforcement that contradicts working code; (b) where CANONICAL defines a requirement that code doesn't enforce, the code should be updated to align with CANONICAL (not the other way around).

### Source-of-Truth Protocol Implications

The JIT protocol from `source-of-truth.instructions.md` has four steps that affect automation design:

1. **Step 1: "derive context now — run `programstart guide`"** — Finding 7-B is a direct violation of this step. If prompts aren't in registry guidance, a JIT-compliant operator cannot discover them. This applies to any future prompts added by Findings 5-A, 6-A, 8-A, 10-A — they MUST be registered in workflow_guidance or they are invisible to JIT. **Already noted in each finding's Suggested Mapping.**

2. **Step 3: "canonical before dependent"** — Cross-file validators (Findings 0-C, 1-A, 4-B, 6-B) should validate the authority file's content first, then check the dependent file for consistency. This ordering is not just a code quality preference — it's a protocol requirement. If the authority file is missing or malformed, the dependent check is meaningless.

3. **Step 4: "verify after — run validate and drift; both must pass"** — This ties into Finding SCH-A: `programstart validate` and `programstart drift` are the verification tools the protocol mandates. If `validate --check workflow-state` doesn't include schema validation, the SoT Step 4 verification has a blind spot for schema-level errors. The practical impact is minimal (pre-commit catches these at commit time, which is before Step 4 fires), but it's a protocol completeness concern.

4. **Temporal semantics**: `source-of-truth.instructions.md` says "If the product-level JIT protocol says to only read Files A, B, C, treat everything else as tentative." For new validators, this means they should read only what the registry points to for the relevant stage (via `workflow_guidance.*.step_files`), not scan the entire workspace. Finding 2-A (research-complete) and Finding 9-A (audit-complete) should scope their file reads to what the registry declares as step_files for those stages.

---

## Summary: Automation Coverage by Stage (revised)

```
PROGRAMBUILD
  Stage 0  inputs_and_mode_selection    ████████████████████  ~90%  (prompt + gate + tests)
  Stage 1  feasibility                  ████████████████████  ~90%  (prompt + gate + tests)
  Stage 2  research                     ██████████░░░░░░░░░░  ~50%  (prompt only, no gate by design)
  Stage 3  requirements_and_ux          ██████████████████░░  ~85%  (prompt + gate + tests, substring bug)
  Stage 4  architecture_and_risk_spikes ██████████████████░░  ~80%  (prompt + gate + tests, no spike check)
  Stage 5  scaffold_and_guardrails      ████░░░░░░░░░░░░░░░░  ~20%  (file checks only)
  Stage 6  test_strategy                ████░░░░░░░░░░░░░░░░  ~20%  (file checks only)
  Stage 7  implementation_loop          ██████░░░░░░░░░░░░░░  ~30%  (checklist only, prompts not surfaced)
  Stage 8  release_readiness            ████░░░░░░░░░░░░░░░░  ~20%  (file checks only)
  Stage 9  audit_and_drift_control      ████████░░░░░░░░░░░░  ~40%  (drift + audit prompt, no content gate)
  Stage 10 post_launch_review           ██░░░░░░░░░░░░░░░░░░  ~15%  (file checks only)

USERJOURNEY
  Phase 0  (decision freeze)            ████████░░░░░░░░░░░░  ~40%  (file/metadata + engineering-ready gate wired at preflight)
  Phase 1–8 (all other phases)          ████░░░░░░░░░░░░░░░░  ~20%  (file/metadata checks only)
```

---

## Implementation Sequencing Recommendation

If implementing Tier 1 findings, the recommended order is:

1. **7-B** (trivial config fix — unblocks guide for Stage 7)
2. **3-A** (trivial bug fix — one-line regex)
3. **UJ-C** (trivial config change — enables existing code)
4. **0-C, 1-A, 4-B** (DECISION_LOG checks — small, same pattern, batch together)
5. **4-A** (RISK_SPIKES validation — medium, new function)
6. **6-B** (test-strategy-complete — medium, new function, enables 7-A)
7. **7-A** (implementation entry criteria — medium, delegates to 4-A + 6-B)
8. **5-A, 6-A, 8-A, 10-A** (new prompts — medium each, no code dependency between them)
9. **8-B, 9-A** (release-ready + audit-complete validation — medium, new functions)
10. **5-B** (scaffold-complete — medium, weakest of the Tier 1 validations)
