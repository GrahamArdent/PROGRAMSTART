# Prompt & Source-of-Truth Audit

Purpose: Critical audit of how source-of-truth files, protocols, and authority rules are (or are not) referenced across the entire PROGRAMSTART codebase. Identifies where prompts, scripts, validators, and instruction files interact — and where they don't.
Last updated: 2026-04-13 (stage6gameplan Phases C–D complete: cross-stage validation ref added to all 13 shaping prompts; sync_rules ordering notes added to all 10 PB shaping protocols)
Method: Full codebase trace of every SoT file declared in `config/process-registry.json` across all prompts, scripts, validators, instruction files, and tests.

**Companion document**: `automation.md` audits the same system from the automation gap angle. Findings here are cross-referenced with Finding IDs (e.g., 5-A, 7-B) from that audit where they overlap.

**Implementation plans**: `stage3gameplan.md` — COMPLETE (Phases A-I, 2026-04-12). `stage4gameplan.md` — COMPLETE (Phases A-E, 2026-04-13). `stage5gameplan.md` — active plan for remaining gaps.

**Remaining gaps**: See Part 13 for a concise list of what still needs doing. See `stage5gameplan.md` for the active implementation plan.

---

## Reading Guide

This audit answers three questions:

1. **Are the prompts actually using the protocols we defined?** (No.)
2. **Are the SoT files referenced where they should be?** (Many are invisible.)
3. **How does everything interact — and where are the seams?** (The layers don't talk to each other.)

Severity ratings: **CRITICAL** (actively undermines system guarantees), **HIGH** (creates silent gaps), **MEDIUM** (structural weakness, not yet causing failures), **LOW** (cosmetic or edge-case only).

---

## Part 1: The Three Layers and How They Fail to Connect

PROGRAMSTART has three enforcement layers. Each was designed independently. They don't integrate.

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: Instruction Files (.instructions.md)                  │
│  Define protocols: JIT, canonical-before-dependent, drift-first │
│  Trigger: applyTo file-path patterns                            │
│  Problem: Prompts don't trigger applyTo; instructions are       │
│           invisible during prompt execution                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ (no connection)
┌──────────────────────────────▼──────────────────────────────────┐
│  LAYER 2: Shaping Prompts (.prompt.md)                          │
│  Define task steps: read X, write Y, validate Z                 │
│  Trigger: operator invokes prompt by name                       │
│  Status (post stage4gameplan): All 10 shaping prompts (incl.   │
│           shape-audit S9) have Protocol Declaration, Pre-flight,│
│           Authority Loading (PROGRAMBUILD.md §N + CANONICAL §N),│
│           Output Ordering, DECISION_LOG mandate, Verification   │
│           Gate, and Next-prompt routing. JIT Step 1 still       │
│           hardcodes file list (not registry-derived). See       │
│           Part 2 matrix for remaining ⚠️ cells.                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │ (more connected after stage4gameplan)
┌──────────────────────────────▼──────────────────────────────────┐
│  LAYER 3: Scripts & Validators (scripts/*.py)                   │
│  Define structural checks: file existence, content parsing      │
│  Trigger: CLI commands (validate, drift, advance)               │
│  Status (post Phase A-I): Validators now exist for all 9        │
│           stages (0-9). stage_checks dict wired for all stages. │
│           _check_decision_log_entries wired into 3 validators.  │
│           RISK_SPIKES validator added. All 9 Verification Gates │
│           reference the correct --check value.                  │
└─────────────────────────────────────────────────────────────────┘
```

**The fundamental design flaw**: The instruction files define the protocols. The prompts define the workflow. The scripts enforce gates. But:
- The prompts don't reference the instruction files.
- The instruction files don't mention the prompts.
- The scripts are called by only some prompts and only as a final step.

An operator using a shaping prompt never encounters the JIT protocol, canonical ordering, or drift checking — because those exist in a different layer that the prompt doesn't activate.

---

## Part 2: Protocol Compliance Matrix (All 9 Shaping Prompts)

Note: Stage 7 (implementation_loop) uses `implement-gameplan-phase*.prompt.md` files — no single shape prompt. Stage 9 (audit_and_drift_control) now has `shape-audit.prompt.md` (created in stage4gameplan Phase D — Gap-1 closed).

| Protocol Element | S0 idea | S1 feasibility | S2 research | S3 requirements | S4 architecture | S5 scaffold | S6 test-strategy | S8 release | S9 audit | S10 post-launch |
|---|---|---|---|---|---|---|---|---|---|---|
| **JIT Step 1**: Protocol Declaration referencing JIT Steps 1-4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **JIT Step 2**: Pre-flight drift baseline | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **JIT Step 3**: Output Ordering section (canonical-before-dependent) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **JIT Step 4**: Verification Gate (validate + drift after) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Kill Criteria re-check** | N/A | N/A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| **DECISION_LOG.md mandatory language** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **PROGRAMBUILD.md §N in Authority Loading** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Data Grounding Rule** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Verification Gate (correct --check value)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Next-prompt routing (## Next Steps)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Cross-stage validation invoked** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **`sync_rules` explicitly cited** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **PRODUCT_SHAPE Conditioning** | N/A | N/A | N/A | ✅ | ✅ | ✅ | ✅ | ✅ | N/A (exempt) | N/A |

**Legend**: ✅ fully implemented, ⚠️ present but incomplete, ❌ absent, N/A not applicable at this stage.

**Score (post stage6gameplan + PA-16 fixup): 117/117 meaningful cells ✅ (10 prompts × 13 protocol elements, minus N/A cells). 0 ⚠️. 0 ❌.**

**Key notes:**
- All 10 PB shaping prompts now run `programstart guide --system programbuild` in Pre-flight alongside the drift baseline, making JIT Step 1 concrete rather than merely declared.
- Verification Gate S4 (shape-architecture): runs `--check architecture-contracts`, `--check risk-spikes`, and `--check risk-spikes-resolved` — fully covers `stage_checks["architecture_and_risk_spikes"]`.
- All Authority Loading sections (S2–S10) load both `PROGRAMBUILD_CANONICAL.md §N` (stage definition) and `PROGRAMBUILD.md §N` (procedural protocol) — consistent with Protocol Declaration.

---

## Part 3: Source-of-Truth File Reference Heatmap

How often each SoT file is referenced by prompts, scripts, validators, and tests.

### PROGRAMBUILD Output Files (the documents operators produce)

| File | Stage Created | Prompts (read) | Prompts (write) | Validator | Tests | Severity |
|---|---|---|---|---|---|---|
| `FEASIBILITY.md` | 1 | 4 prompts | 1 prompt | ✅ deep | ✅ dedicated | — |
| `DECISION_LOG.md` | 0–10 | 6+ prompts | 5 prompts (conditional) | ⚠️ ADR orphan only | ❌ none | **HIGH** |
| `RESEARCH_SUMMARY.md` | 2 | 1 prompt | 1 prompt | ❌ none | ❌ none | **HIGH** |
| `REQUIREMENTS.md` | 3 | 5+ prompts | 1 prompt | ✅ deep | ✅ dedicated | — |
| `USER_FLOWS.md` | 3 | 3+ prompts | 1 prompt | ⚠️ cross-ref only | ❌ none (in requirements tests) | **MEDIUM** |
| `ARCHITECTURE.md` | 4 | 6+ prompts | 1 prompt | ✅ deep | ✅ dedicated | — |
| `RISK_SPIKES.md` | 1–4 | 4 prompts | 3 prompts | ✅ `validate_risk_spikes` (Phase F) | ✅ 6 tests | resolved |
| `TEST_STRATEGY.md` | 6 | 3+ prompts | ✅ `shape-test-strategy` (Phase H) | ✅ `validate_test_strategy_complete` (Phase G) | ✅ tests | resolved |
| `RELEASE_READINESS.md` | 8 | 1 prompt | ✅ `shape-release-readiness` (Phase H) | ✅ `validate_release_ready` (Phase G) | ✅ tests | resolved |
| `AUDIT_REPORT.md` | 9 | 1 prompt | ❌ no shape prompt for Stage 9 | ✅ `validate_audit_complete` (Phase G) | ✅ tests | **gap remains** |
| `POST_LAUNCH_REVIEW.md` | 10 | 1 prompt | ✅ `shape-post-launch-review` (Phase H) | ✅ checked by `audit-complete` | ✅ tests | resolved |

**Pattern (updated)**: All stages now have either a shaping prompt or a validator. The only remaining coverage cliff is Stage 9 (audit_and_drift_control) which has a validator (`audit-complete`) but no shaping prompt to guide the operator through producing `AUDIT_REPORT.md`.

### PROGRAMBUILD Control Files

| File | Prompts | Validators | Role Gap |
|---|---|---|---|
| `PROGRAMBUILD.md` | ❌ 0 shaping prompts reference it | ❌ no validator reads it | **CRITICAL** — the main playbook that defines all stage rules is never loaded by any shaping prompt. Every prompt re-derives protocol from its own steps instead of reading the authority. |
| `PROGRAMBUILD_GAMEPLAN.md` | 2 transition prompts | ❌ no validator | **MEDIUM** — only transition prompts use it; shaping prompts don't |
| `PROGRAMBUILD_CHECKLIST.md` | 1 prompt (phase1 only) | ❌ no content validator (checklist_progress.py is a tracker, not a validator) | **MEDIUM** — the comprehensive checklist that covers all stages is barely referenced |
| `PROGRAMBUILD_CHALLENGE_GATE.md` | 2 transition prompts | `_check_challenge_gate_log()` (advisory only) | **MEDIUM** — gate protocol exists but is advisory and disconnected from shaping |
| `PROGRAMBUILD_CANONICAL.md` | 2 internal gameplan prompts | `validate_authority_sync()` reads it | **LOW** — correctly scoped to system editing, not project execution |
| `PROGRAMBUILD_FILE_INDEX.md` | 1 internal gameplan prompt | `validate_authority_sync()` reads it | **LOW** — same |

### USERJOURNEY Files

| File | Registry Role | Prompts | Scripts/Validators | Severity |
|---|---|---|---|---|
| `DELIVERY_GAMEPLAN.md` | core (impl seq) | `uj-next-slice` reads it | status, validate, attach | — |
| `OPEN_QUESTIONS.md` | authority (external review) | `uj-next-slice` reads it | status, serve, validate (eng-ready) | — |
| `ROUTE_AND_STATE_FREEZE.md` | authority (route/state) | ❌ none | context.py only | **HIGH** |
| `STATES_AND_RULES.md` | authority (route/state) | ❌ none | context.py only | **HIGH** |
| `LEGAL_AND_CONSENT.md` | authority (legal, external review) | `propagate-canonical` (1 generic ref) | ❌ none | **HIGH** |
| `DECISION_LOG.md` (UJ) | authority (legal, route/state) | ❌ none | ❌ none | **CRITICAL** |
| `IMPLEMENTATION_TRACKER.md` | authority (impl seq) | `uj-next-slice` reads it | status, serve, dashboard | — |
| `SCREEN_INVENTORY.md` | authority (UX surfaces) | ❌ none | ❌ none | **HIGH** |
| `UX_COPY_DRAFT.md` | authority (UX surfaces) | ❌ none | ❌ none | **HIGH** |
| `USER_FLOWS.md` (UJ) | authority (UX surfaces) | ❌ none | ❌ none | **HIGH** |
| `TERMS_OF_SERVICE_DRAFT.md` | dependent (legal, external review) | ❌ none | ❌ none | **HIGH** |
| `PRIVACY_POLICY_DRAFT.md` | dependent (legal, external review) | ❌ none | ❌ none (1 test as example data) | **HIGH** |
| `EXTERNAL_REVIEW_PACKET.md` | dependent (external review) | ❌ none | ❌ none | **HIGH** |
| `EXECUTION_SLICES.md` | dependent (impl seq) | `uj-next-slice` | status, serve | — |
| `ACCEPTANCE_CRITERIA.md` | dependent (UX, legal) | ❌ none | dashboard, status | **MEDIUM** |
| `ANALYTICS_AND_OUTCOMES.md` | dependent (UX surfaces) | ❌ none | ❌ none (1 test) | **MEDIUM** |

**Of 26 USERJOURNEY files, exactly 1 prompt (`userjourney-next-slice`) touches 4 of them. The other 22 have zero prompt coverage.** Of those 22, 10 are declared as authority or dependent files in sync_rules.

---

## Part 4: The DECISION_LOG.md Problem

DECISION_LOG.md deserves special attention because it is the most cross-referenced file in the system and the most weakly enforced.

### What the authority docs say

| Source | Requirement |
|---|---|
| GAMEPLAN Stage 0 step 5 | "Record all three decisions in DECISION_LOG.md" — **mandatory** |
| GAMEPLAN Stage 1 step 3 | "Record the recommendation in DECISION_LOG.md" — **mandatory** |
| GAMEPLAN Stage 2 | "Low-confidence decisions recorded in DECISION_LOG" — **mandatory** |
| GAMEPLAN Stage 4 step 5 | "Record spike outcomes and decisions" — **mandatory** |
| GAMEPLAN Stage 7+ | "Any new architecture-level decision made during this task is recorded" — **mandatory** |
| `sync_rules[3]` (feasibility_cascade) | FEASIBILITY.md → DECISION_LOG.md (authority → dependent) |
| `sync_rules[15]` (arch_decision_alignment) | ARCHITECTURE.md → DECISION_LOG.md (authority → dependent, soft) |
| `source-of-truth.instructions.md` L75 | DECISION_LOG.md listed as authority file for "Decisions and reversals" |
| `copilot-instructions.md` L23 | "record it in DECISION_LOG.md and update ARCHITECTURE.md in the same commit" |

### What the prompts actually do (post Phase A-I)

| Prompt | DECISION_LOG treatment | Strength |
|---|---|---|
| shape-idea | "You MUST update DECISION_LOG.md with any decisions made during this stage." | ✅ Mandatory language, but validator doesn't yet enforce content (automation.md Finding 0-C) |
| shape-feasibility | "You MUST update DECISION_LOG.md with the go/no-go/limited-spike decision and rationale." | ✅ Mandatory language, validator now checks for decision entries (Phase E) |
| shape-research | "You MUST update DECISION_LOG.md with any research-driven decisions." | ✅ Mandatory language |
| shape-requirements | "You MUST update DECISION_LOG.md with any scope decisions." | ✅ Mandatory language |
| shape-architecture | "You MUST update DECISION_LOG.md with architecture decisions and rationale." | ✅ Mandatory language, validator now checks for entries (Phase E) |
| shape-scaffold | "You MUST update DECISION_LOG.md with any scaffold design decisions." | ✅ Mandatory language |
| shape-test-strategy | "You MUST update DECISION_LOG.md with any test strategy decisions." | ✅ Mandatory language |
| shape-release-readiness | "You MUST update DECISION_LOG.md with the go/no-go decision." | ✅ Mandatory language |
| shape-post-launch-review | "You MUST update DECISION_LOG.md with any post-launch reversals." | ✅ Mandatory language |
| stage-transition | Part F: "Check DECISION_LOG.md for unreconciled reversals" | READ only — confirms shaping populated it |

### What the validators check

| Validator | DECISION_LOG check |
|---|---|
| `validate_intake_complete()` | ❌ doesn't read it |
| `validate_feasibility_criteria()` | ❌ doesn't read it |
| `validate_requirements_complete()` | ❌ doesn't read it |
| `validate_architecture_contracts()` | ❌ doesn't read it |
| `validate_authority_sync()` | ⚠️ checks file-list alignment via sync_rules but not content |
| `validate_adr_coverage()` | ⚠️ checks orphaned ADRs reference DECISION_LOG rows — but checks ADR→DECISION_LOG direction only |

**The result**: 5 GAMEPLAN stages mandate DECISION_LOG entries. 0 validators check for them. 4 of 5 prompts treat DECISION_LOG as optional. The only enforcement is `stage-transition` reading it for reversals — after the operator has already moved past the stage where the entry should have been written.

---

## Part 5: PROGRAMBUILD.md — The Invisible Playbook

`PROGRAMBUILD.md` is the most important document in the system. It defines:
- All 11 stage protocols (Sections 3–17)
- PRODUCT_SHAPE conditioning rules
- Contract structure per shape
- Test strategy rules (purpose test, auth test, golden test)
- Scaffold protocol
- Release readiness gates
- Audit protocol
- Post-launch review protocol

**Zero shaping prompts reference it.**

Every shaping prompt re-derives its protocol from first principles in its own `## Protocol` section, rather than loading PROGRAMBUILD.md and applying the relevant section. This means:

1. **Protocol drift is invisible.** If PROGRAMBUILD.md Section 12 (scaffold) changes, no prompt reflects the change because no prompt reads the file.
2. **The prompts are restatements, not derivations.** shape-feasibility's protocol is a human-authored summary of PROGRAMBUILD.md Section 8, not a dynamic loading of it. If the section changes, the prompt is stale.
3. **This contradicts JIT Step 1.** The JIT protocol says "derive context from the registry, not memory." The prompts ARE memory — they're static copies of what PROGRAMBUILD.md said at the time the prompt was written.

### Why this matters for the missing prompts

Findings 5-A, 6-A, 8-A, and 10-A propose creating shape prompts for Stages 5, 6, 8, and 10. If these are created using the same pattern (hardcoded protocol steps derived from PROGRAMBUILD.md), they will have the same drift problem from day one.

**The better pattern**: each prompt should explicitly load PROGRAMBUILD.md and reference the section number it implements. This makes the prompt a JIT-compliant accessor of the authority doc rather than a static copy.

---

## Part 6: Sync Rules — Authority Ordering in Practice

There are 16 sync_rules. Here's which ones have prompt-level enforcement of their authority ordering:

| # | Rule Name | Authority → Dependent | Prompt Enforces Ordering? |
|---|---|---|---|
| 1 | `programbuild_control_inventory` | CANONICAL + FILE_INDEX → 11 dependents | ⚠️ instructions enforce it (path-triggered), prompts don't |
| 2 | `programbuild_architecture_contracts` | ARCHITECTURE → TEST_STRATEGY, RELEASE_READINESS, RISK_SPIKES | ❌ no prompt for TEST_STRATEGY/RELEASE_READINESS |
| 3 | `programbuild_requirements_scope` | REQUIREMENTS → USER_FLOWS, ARCHITECTURE, TEST_STRATEGY | ⚠️ shape-requirements writes REQUIREMENTS first, but doesn't cite the rule |
| 4 | `programbuild_feasibility_cascade` | FEASIBILITY → DECISION_LOG, RESEARCH_SUMMARY, REQUIREMENTS, RISK_SPIKES | ⚠️ shape-feasibility writes FEASIBILITY first, but doesn't cite the rule |
| 5 | `programbuild_variant_alignment` | PROGRAMBUILD.md → LITE, PRODUCT, ENTERPRISE | ❌ no prompt |
| 6 | `userjourney_external_review_packet` | OPEN_Q + LEGAL_REVIEW + LEGAL_AND_CONSENT → EXTERNAL_REVIEW, TOS, PRIVACY | ❌ no prompt |
| 7 | `userjourney_route_state_logic` | DECISION_LOG(UJ) + ROUTE_FREEZE + STATES_RULES → USER_FLOWS(UJ), SCREEN_INV, IMPL_PLAN, IMPL_TRACKER | ❌ no prompt |
| 8 | `userjourney_legal_consent_behavior` | DECISION_LOG(UJ) + LEGAL_AND_CONSENT → TOS, PRIVACY, LEGAL_REVIEW, UX_COPY, ACCEPTANCE | ❌ no prompt |
| 9 | `userjourney_ux_surfaces_copy` | SCREEN_INV + USER_FLOWS(UJ) + UX_COPY → ACCEPTANCE, ANALYTICS | ❌ no prompt |
| 10 | `userjourney_implementation_sequence` | IMPL_TRACKER → EXEC_SLICES, FILE_CHECKLIST, DELIVERY_GAMEPLAN | ⚠️ uj-next-slice reads all 4 but doesn't enforce ordering |
| 11 | `decisions_adr_template` | ADR_TEMPLATE → docs/decisions/*.md | ❌ soft rule, no prompt |
| 12 | `commit_enforcement_alignment` | conventional-commits.instructions.md → check_commit_msg.py, pre-commit, gitlint | ⚠️ instructions handle this |
| 13 | `knowledge_base_docs_alignment` | KB.json, docs/knowledge-base.md → README | ❌ no prompt |
| 14 | `automation_gate_jit_alignment` | noxfile, tasks.json, SoT instructions → copilot-instructions, QUICKSTART | ⚠️ instructions handle this |
| 15 | `architecture_decision_alignment` | ARCHITECTURE → DECISION_LOG | ❌ advisory, no prompt enforces |
| 16 | `requirements_test_alignment` | REQUIREMENTS → TEST_STRATEGY | ❌ no prompt for TEST_STRATEGY |

**Result: 0/16 sync_rules are explicitly enforced by prompts.** 4 have implicit (accidental) ordering because the prompt happens to write the authority file first. 3 are handled by instruction files (path-triggered, not prompt-triggered). 9 have zero enforcement of any kind in prompts.

---

## Part 7: The step_files vs. guidance Divergence

The registry has two overlapping file-list systems:

1. **`workflow_guidance.*.files`** — broad lists used by `programstart guide`
2. **`workflow_state.*.step_files`** — narrow lists used by `programstart advance` and drift checking

These diverge significantly:

| Stage | guidance.files count | step_files count | Missing from step_files |
|---|---|---|---|
| inputs_and_mode_selection | 7+ (PROGRAMBUILD.md, CHECKLIST, FILE_INDEX, CANONICAL, KICKOFF, IDEA_INTAKE, GAMEPLAN) | 2 (PROGRAMBUILD.md, CHECKLIST) | KICKOFF_PACKET, IDEA_INTAKE (read and written by shape-idea) |
| feasibility | 5+ (FEASIBILITY, DECISION_LOG, CHECKLIST, CHALLENGE_GATE, GAMEPLAN) | 2 (FEASIBILITY, DECISION_LOG) | CHECKLIST, CHALLENGE_GATE, GAMEPLAN |
| research | 4+ (RESEARCH_SUMMARY, DECISION_LOG, CHALLENGE_GATE, GAMEPLAN) | 2 (RESEARCH_SUMMARY, DECISION_LOG) | CHALLENGE_GATE, GAMEPLAN |
| requirements_and_ux | 4+ (REQUIREMENTS, USER_FLOWS, CHALLENGE_GATE, GAMEPLAN) | 2 (REQUIREMENTS, USER_FLOWS) | CHALLENGE_GATE, GAMEPLAN |
| architecture_and_risk_spikes | 4+ (ARCHITECTURE, RISK_SPIKES, CHALLENGE_GATE, GAMEPLAN) | 2 (ARCHITECTURE, RISK_SPIKES) | CHALLENGE_GATE, GAMEPLAN |
| implementation_loop | 5+ (CHECKLIST, DECISION_LOG, CHALLENGE_GATE, GAMEPLAN + prompts) | 2 (DECISION_LOG, CHECKLIST) | CHALLENGE_GATE, GAMEPLAN, all implementation prompts |

**Impact**: `programstart advance` and drift checking only track `step_files`. If an operator modifies CHALLENGE_GATE.md, GAMEPLAN.md, or KICKOFF_PACKET.md during a stage, the advance/drift machinery doesn't notice. The guidance layer knows these files are relevant, but the enforcement layer doesn't.

This isn't necessarily wrong — step_files may intentionally track only the stage's primary deliverables. But it means:
- CHALLENGE_GATE.md changes are invisible to enforcement (consistent with Finding 1-B — advisory only)
- KICKOFF_PACKET.md changes at any stage after 0 are invisible to enforcement
- GAMEPLAN.md (the source of cross-stage validation rules) is invisible to all enforcement

---

## Part 8: The Kill Criteria Evaporation Problem

Kill criteria are the system's most important safety mechanism. They're the explicit "stop if this happens" conditions. Here's their journey through the system:

```
Stage 0: shape-idea creates KILL_SIGNAL_* entries in IDEA_INTAKE.md
         └── ❌ No check that they were created (Stage 0 creates criteria, no re-check needed)
         
Stage 1: shape-feasibility transfers KILL_SIGNALs to FEASIBILITY.md kill criteria
         └── ✅ validate_feasibility_criteria() checks ≥3 criteria exist, format correct
         
Stage 2: shape-research — kill criteria re-check ADDED (Phase D)
         └── ✅ Dedicated "Kill Criteria Re-check" section: re-read FEASIBILITY.md before research work

Stage 3: shape-requirements — kill criteria re-check ADDED (Phase D)
         └── ✅ Dedicated "Kill Criteria Re-check" section: checks if research findings trigger a criterion
         
Stage 4: shape-architecture — kill criteria re-check ADDED (Phase D)
         └── ✅ Dedicated "Kill Criteria Re-check" section

Stage 5: shape-scaffold — kill criteria re-check ADDED (Phase H)
         └── ✅ Kill Criteria Re-check section present

Stage 6: shape-test-strategy — kill criteria re-check ADDED (Phase H)
         └── ✅ Kill Criteria Re-check section present

Stage 7: implementation — no shaping prompt surfaced by guide
         └── ❌ product-jit-check.prompt.md exists and is now registered in implementation_loop.prompts
            but still not prominently surfaced

Stage 8: shape-release-readiness — kill criteria re-check ADDED (Phase H)
         └── ✅ Kill Criteria Re-check section present

Stage 9: No shaping prompt (remaining gap)
         └── ❌ No kill criteria check for audit stage; audit-process-drift.prompt.md is generic

Stage 10: shape-post-launch-review — kill criteria are post-launch (no longer blocking)
         └── ✅ DECISION_LOG mandate covers decision confirmation/reversal
```

**Kill criteria are now re-checked at Stages 1–6 and 8 (7 of 9 active stages). The evaporation problem is largely resolved for operator-facing shaping prompts. Stage 7 (implementation) and Stage 9 (audit) remain unguarded.**

The GAMEPLAN says the Challenge Gate (Part A: "Re-read kill criteria") runs at every stage transition. But:
- The Challenge Gate is advisory only (Finding 1-B)
- No shaping prompt invokes it
- Stage-transition prompt invokes it, but no shaping prompt routes to stage-transition

So in practice, kill criteria are created at Stage 1 and never structurally re-evaluated unless the operator independently remembers to run the stage-transition prompt.

---

## Part 9: Interactions That Should Exist But Don't

### 9.1 Prompt → Instruction file connection

**Expected**: When a shaping prompt runs and edits files under `PROGRAMBUILD/`, the `source-of-truth.instructions.md` (with `applyTo: "{PROGRAMBUILD,USERJOURNEY,config,scripts}/**"`) should activate and inject JIT protocol requirements.

**Actual**: VS Code's `applyTo` triggers on the file being edited, not on the prompt being invoked. The instruction file technically activates when the agent writes to `PROGRAMBUILD/FEASIBILITY.md` during `shape-feasibility`. But the prompt's protocol steps override with specific instructions, and the agent follows the prompt's explicit steps rather than the background instruction file's general rules. The instruction file says "run drift first" but the prompt says "step 1: read these files" — the prompt wins.

**Fix needed**: Either the prompts must incorporate the JIT protocol explicitly, or the instruction file must be restructured as a prompt wrapper that activates BEFORE prompts run.

### 9.2 Shaping prompt → Stage-transition prompt connection

**Expected**: After completing a shaping prompt (e.g., shape-requirements), the operator runs stage-transition to validate the stage and advance.

**Actual**: No shaping prompt mentions stage-transition. No prompt routes to any other prompt. The operator must know the workflow from GAMEPLAN reading.

### 9.3 Script validation → Prompt guidance connection

**Expected**: When `programstart validate --check feasibility-criteria` fails, the error message should suggest running `shape-feasibility.prompt.md` to fix the issues.

**Actual**: Validation errors are generic strings ("FEASIBILITY.md has fewer than 3 kill criteria"). They don't reference which prompt can fix the problem or which PROGRAMBUILD.md section defines the requirement.

### 9.4 `programstart guide` → Prompt availability connection

**Expected**: `programstart guide --system programbuild` at Stage 7 returns the implementation prompts so the operator can discover them.

**Actual**: Finding 7-B — implementation prompts are in `bootstrap_assets` but not in `implementation_loop.prompts`, so `programstart guide` doesn't surface them. The JIT-compliant operator can't find them.

### 9.5 USERJOURNEY sync_rules → Prompt enforcement

**Expected**: The 5 USERJOURNEY sync_rules (external_review_packet, route_state_logic, legal_consent_behavior, ux_surfaces_copy, implementation_sequence) should have prompts that enforce their authority ordering.

**Actual**: `userjourney-next-slice.prompt.md` is the only UJ prompt. It reads 4 files, doesn't enforce authority ordering, and doesn't cover 22 of 26 USERJOURNEY files. 5 of 5 USERJOURNEY sync_rules have zero prompt enforcement.

---

## Part 10: PROGRAMBUILD.md as the Unread Authority

`PROGRAMBUILD.md` is the canonical reference for all stage protocols (Sections 3–17). It defines:

| Section | Content | Which prompt should read it | Actually reads it? |
|---|---|---|---|
| §3 | Product shape conditioning | shape-idea | ❌ |
| §4-6 | Kickoff, inputs, mode selection | shape-idea | ❌ |
| §7 | Idea intake protocol | shape-idea | ❌ (reads IDEA_INTAKE.md directly) |
| §8 | Feasibility protocol | shape-feasibility | ❌ |
| §9 | Research protocol | shape-research | ❌ |
| §10 | Requirements protocol | shape-requirements | ❌ |
| §11 | Architecture protocol | shape-architecture | ❌ |
| §12 | Scaffold protocol | (no prompt) | — |
| §13 | Test strategy protocol | (no prompt) | — |
| §14 | Implementation protocol | (product-jit-check, orphaned) | ❌ |
| §15 | Release readiness protocol | (no prompt) | — |
| §16 | Audit protocol | audit-process-drift | ❌ |
| §17 | Post-launch review | (no prompt) | — |

**Zero prompts read PROGRAMBUILD.md for their protocol.** Every prompt hardcodes a summary of the relevant section. This means:
- Prompts can drift from PROGRAMBUILD.md without detection
- The JIT protocol ("derive from authority, not memory") is violated by design — the prompts ARE memory
- When PROGRAMBUILD.md changes (e.g., adding a new shape-conditional rule), prompts must be manually updated — there's no derivation chain

---

## Part 11: The Orphaned Prompt Problem

Several prompts exist but are effectively unreachable through normal workflow:

| Prompt | Purpose | In registry guidance? | Discoverable via `programstart guide`? | Referenced by other prompts? |
|---|---|---|---|---|
| `product-jit-check.prompt.md` | Pre-coding alignment check | ❌ not in `implementation_loop.prompts` | ❌ | ❌ |
| `implement-gameplan-phase*.prompt.md` (8 files) | PROGRAMSTART's own build prompts | ❌ not in any stage's guidance prompts | ❌ | ❌ |
| `propagate-canonical-change.prompt.md` | Authority change propagation | ❌ not in any stage's guidance prompts | ❌ | ❌ (copilot-instructions.md mentions it) |
| `programstart-cross-stage-validation.prompt.md` | Cross-stage consistency | ❌ not in any stage's guidance prompts | ❌ | ❌ |
| `implement-stage2-gameplan.prompt.md` | Stage2 automation gameplan execution | ❌ | ❌ | ❌ |
| `implement-phase-f.prompt.md` | Phase F integration tests | ❌ | ❌ | ❌ |

**6 prompts (representing 14 files) are invisible to a JIT-compliant operator.** They exist in `.github/prompts/` but are not in any `workflow_guidance.*.prompts` array in the registry. Per JIT Step 1, an operator who runs `programstart guide` and reads "only the files it returns" will never discover them.

Note: `implement-gameplan-*`, `implement-stage2-gameplan`, and `implement-phase-f` are PROGRAMSTART's own internal build prompts — they're meant for PROGRAMSTART development, not for project operators. But `product-jit-check`, `propagate-canonical-change`, and `cross-stage-validation` are operator-facing tools that should be discoverable.

---

## Part 12: What a Protocol-Compliant Prompt System Looks Like

Based on everything defined in the authority docs, a properly wired prompt should have these sections:

### Mandatory sections (from existing protocols)

| Section | Source | Purpose |
|---|---|---|
| **Data Grounding Rule** | All existing prompts | Prompt injection defense |
| **Protocol declaration** | New — identifies which JIT steps apply | Declares "this prompt follows JIT Steps 1-4" |
| **Pre-flight: drift baseline** | `source-of-truth.instructions.md` Step 2 | `programstart drift` before any edits |
| **Authority file loading** | `source-of-truth.instructions.md` Step 3 | Read PROGRAMBUILD.md §N for the stage protocol; read authority files per sync_rules |
| **Upstream verification** | GAMEPLAN cross-stage validation | Re-read kill criteria (Stages 2+); verify previous stage outputs are still consistent |
| **Protocol steps** | PROGRAMBUILD.md §N (loaded, not hardcoded) | Stage-specific work, derived from the authority doc |
| **Output ordering** | `sync_rules` authority-before-dependent | Write authority files first, then dependents |
| **DECISION_LOG mandate** | GAMEPLAN per-stage steps | "You MUST update DECISION_LOG.md with [specific decisions]. The gate validator will reject advance if missing." |
| **Verification gate** | `source-of-truth.instructions.md` Step 4 | `programstart validate --check <stage-check>` AND `programstart drift` |
| **Workflow routing** | GAMEPLAN + transition prompt | "After completing this prompt, run `programstart-stage-transition` to validate and advance." |

### Optional sections (based on stage)

| Section | When | Purpose |
|---|---|---|
| **PRODUCT_SHAPE conditioning** | Stages 3+ | Branch behavior based on shape (different contracts for web-app vs. CLI tool) |
| **Kill criteria re-check** | Stages 2+ | Structured re-evaluation against FEASIBILITY.md kill criteria |
| **Entry criteria verification** | Stage 7 | Check the 4 implementation entry criteria before starting |

---

## Summary: Severity-Ranked Findings

### CRITICAL (actively undermines system guarantees)

| ID | Finding | Status | Remaining Work |
|---|---|---|---|
| PA-1 | **Zero shaping prompts reference the JIT protocol** — no drift check, no canonical ordering, no verify-after | ⚠️ PARTIALLY RESOLVED (Phase A, D, H, stage4gameplan A) — all 10 prompts now have Protocol Declaration, Pre-flight, Authority Loading, Output Ordering, Verification Gate | JIT Step 1 is declared but not registry-driven (hardcoded file loading, not derived from `programstart guide`) — architectural gap, deferred |
| PA-2 | **PROGRAMBUILD.md is never loaded by any shaping prompt** — prompts hardcode protocol summaries | ✅ RESOLVED (Phase D, H, stage4gameplan Phase B) — all 10 prompts now load both `PROGRAMBUILD.md §N` and `PROGRAMBUILD_CANONICAL.md §N` in Authority Loading | — |
| PA-3 | **Kill criteria evaporate after Stage 1** — no shaping prompt re-reads them | ✅ RESOLVED (Phase D, H, stage4gameplan Phase D) — all Stages 2–6, 8, and 9 now have dedicated Kill Criteria Re-check sections | — |
| PA-4 | **Four output files have zero prompt + zero validator + zero tests** — TEST_STRATEGY, RELEASE_READINESS, AUDIT_REPORT, POST_LAUNCH_REVIEW | ✅ RESOLVED (Phase G, H, stage4gameplan Phase D) — all 10 stages including S9 now have shaping prompts and validators | — |
| PA-5 | **DECISION_LOG.md is conditional in 4/5 prompts while the GAMEPLAN mandates it at every stage** | ✅ RESOLVED (Phase A, D, E, H) — all 9 prompts now have mandatory DECISION_LOG language; validator enforcement added for 3 stages via `_check_decision_log_entries` | Validator enforcement for Stages 0, 7, 10 still uses weaker checks. See automation.md Finding 0-C |

### HIGH (creates silent gaps in SoT coverage)

| ID | Finding | Status | Remaining Work |
|---|---|---|---|
| PA-6 | **Three operator-facing prompts are orphaned** — product-jit-check, propagate-canonical-change, cross-stage-validation | ✅ RESOLVED (Phase B, C) — `implementation_loop.prompts` and `cross_cutting_prompts` added to registry; all now discoverable via `programstart guide` | — |
| PA-7 | **RISK_SPIKES.md has no validator and no dedicated tests** | ✅ RESOLVED (Phase F) — `validate_risk_spikes()` added, 6 dedicated tests | — |
| PA-8 | **RESEARCH_SUMMARY.md has no validator and no dedicated tests** | ✅ RESOLVED — `validate_research_complete()` implemented, 4 tests added (stage5gameplan Phase B 2026-04-13) |
| PA-9 | **5 of 5 USERJOURNEY sync_rules have zero prompt enforcement** | PARTIALLY RESOLVED (Phase C+D stage6) — 3 UJ shaping prompts now include cross-stage validation ref and sync_rules ordering note but full UJ phase-by-phase enforcement still absent | See Gap-5 in Part 13 |
| PA-10 | **10 USERJOURNEY authority/dependent files have zero prompt + zero script coverage** | PARTIALLY RESOLVED (Phase C stage6) — 3 UJ prompts now include cross-stage validation one-liner; uj-next-slice still covers only 4 of 26 UJ files | See Gap-5 in Part 13 |
| PA-11 | **No prompt routes to any other prompt** | ✅ RESOLVED (Phase I) — all 9 shaping prompts now end with `## Next Steps` routing to `programstart-stage-transition`; stage-transition has a routing table to next shape prompt | — |
| PA-12 | **step_files vs. guidance divergence** — enforcement tracks 2 files per stage while guidance lists 5-7 | UNRESOLVED — intentional design decision, no change needed unless a specific file-tracking gap causes a problem | — |

### MEDIUM (structural weakness, not yet causing failures)

| ID | Finding | Status | Remaining Work |
|---|---|---|---|
| PA-13 | **Instruction files and prompts operate independently** — instructions use `applyTo` path triggers that don't inject into prompt execution | UNRESOLVED — architectural limitation of VS Code `applyTo` | Low priority; PROMPT_STANDARD.md is now the prompt-level equivalent of instructions |
| PA-14 | **Cross-stage validation exists as a prompt but is disconnected** | ✅ RESOLVED (Phase C stage6) — one-liner invoking `programstart validate --check all` added to all 13 shaping prompts (10 PB + 3 UJ) | — |
| PA-15 | **Validation error messages don't reference prompts or PROGRAMBUILD.md sections** | PARTIALLY RESOLVED (Phase I) — stage-transition routing table added; main validators still emit generic error strings | Could add prompt references to individual validator error messages |
| PA-16 | **Stage-transition prompt doesn't route to the next shaping prompt** | ✅ RESOLVED (Phase I) — routing table added to stage-transition | — |
| PA-17 | **USER_FLOWS.md (PB) has no dedicated tests** | UNRESOLVED | Low priority; covered by requirements validator cross-reference |

### LOW (cosmetic or edge-case)

| ID | Finding | Impact |
|---|---|---|
| PA-18 | **PROGRAMBUILD_CHANGELOG.md referenced in many implementation prompts but not a SoT concern** | Changelog is narrative, not authority — low risk |
| PA-19 | **Variant files (LITE/PRODUCT/ENTERPRISE) have zero prompt coverage** | Expected — they're reference docs, not operator-editable |
| PA-20 | **PROGRAMBUILD_SUBAGENTS.md has no prompt coverage** | Expected — it's a catalog for dashboard display |

---

## Recommended Fix Order (Post Phase A-I — Remaining Work)

Items 1–7 from the original order are complete. Remaining work:

1. ✅ **Define a prompt standard** — `PROMPT_STANDARD.md` created (Phase A); `promptingguidelines.md` companion guide created
2. ✅ **Upgrade existing 5 shaping prompts** — all upgraded to standard (Phase D)
3. ✅ **Register orphaned prompts** — `cross_cutting_prompts` and `implementation_loop.prompts` added (Phases B, C)
4. ✅ **Create missing shaping prompts for Stages 5, 6, 8, 10** — `shape-scaffold`, `shape-test-strategy`, `shape-release-readiness`, `shape-post-launch-review` created (Phase H)
5. ✅ **Wire stage-transition routing** — routing table added (Phase I)
6. ✅ **Add DECISION_LOG validators** — `_check_decision_log_entries` wired into 3 validators (Phase E)
7. ✅ **Add RISK_SPIKES validator** — `validate_risk_spikes()` added (Phase F)

**Completed in stage4gameplan Phases A–E (2026-04-13):**

8. ✅ **Create `shape-audit.prompt.md` for Stage 9** (Gap-1) — DONE
9. ✅ **Add Output Ordering section to all 9 shaping prompts** (Gap-2) — DONE
10. ✅ **Fix PROGRAMBUILD.md vs PROGRAMBUILD_CANONICAL.md inconsistency in Stages 2–10** (Gap-3) — DONE
11. ✅ **Fix shape-architecture Verification Gate** — DONE
14. ✅ **Add PRODUCT_SHAPE Conditioning to `shape-release-readiness`** (Gap-4) — DONE

**Active remaining priorities (see `stage5gameplan.md`):**

12. ✅ **Address USERJOURNEY prompt gap** — `shape-uj-decision-freeze.prompt.md`, `shape-uj-legal-drafts.prompt.md`, `shape-uj-ux-surfaces.prompt.md` created (Gap-5). Phase C of stage5gameplan — DONE 2026-04-13
13. ✅ **Add `validate_research_complete()`** (automation.md Finding 2-A) — Stage 2 research gate implemented, 4 tests added. Phase B of stage5gameplan — DONE 2026-04-13

---

## Part 13: Remaining Gaps — What Still Needs Doing

Concise list of open work after Phase A-I implementation. Each item has an ID that matches the Recommended Fix Order above and cross-references to the relevant finding.

### Gap-1: Stage 9 has no shaping prompt — **CLOSED 2026-04-13**

**Stage**: audit_and_drift_control  
**Resolution**: `shape-audit.prompt.md` created in stage4gameplan Phase D. Follows PROMPT_STANDARD with all 10 mandatory `##` headings. Registered in `process-registry.json` bootstrap_assets and audit_and_drift_control.prompts. Stage 9 exempted from PRODUCT_SHAPE Conditioning in PROMPT_STANDARD §O1.  
**Corresponds to**: PA-4 (partial), automation.md Finding 9-A.

---

### Gap-2: Output Ordering section missing from all prompts — **CLOSED 2026-04-13**

**Scope**: All 9 shaping prompts  
**Resolution**: `## Output Ordering` section added to all 9 prompts in stage4gameplan Phase A. Each cites the relevant `sync_rules` entry and lists authority-before-dependent write order.  
**Corresponds to**: PA-1 (JIT Step 3 partial), PA-6 partial.

---

### Gap-3: PROGRAMBUILD.md vs PROGRAMBUILD_CANONICAL.md inconsistency — **CLOSED 2026-04-13**

**Scope**: shape-research, shape-requirements, shape-architecture, shape-scaffold, shape-test-strategy, shape-release-readiness, shape-post-launch-review (Stages 2–10)  
**Resolution**: Both `PROGRAMBUILD_CANONICAL.md §N` AND `PROGRAMBUILD.md §N` now required in Authority Loading of all 7 affected prompts. Decision recorded in DECISION_LOG.md as DEC-006. CANONICAL provides stage boundaries and required output list; PROGRAMBUILD.md provides procedural protocol for how to do the work.  
**Corresponds to**: PA-2.

---

### Gap-4: shape-release-readiness missing PRODUCT_SHAPE Conditioning — **CLOSED 2026-04-13**

**Scope**: `shape-release-readiness.prompt.md`  
**Resolution**: `## PRODUCT_SHAPE Conditioning` section added in stage4gameplan Phase C. Added after `## Kill Criteria Re-check` and before `## Protocol`. Also added `--check risk-spikes` to shape-architecture Verification Gate in the same phase (Gap-4a).

---

### Gap-5: USERJOURNEY has no shape prompts (22 of 26 files unprotected) — **CLOSED 2026-04-13**

**Scope**: All USERJOURNEY authority and dependent files  
**Resolution**: Three USERJOURNEY shaping prompts created in stage5gameplan Phase C: `shape-uj-decision-freeze.prompt.md` (phases 0 and 3), `shape-uj-legal-drafts.prompt.md` (phase 1), `shape-uj-ux-surfaces.prompt.md` (phase 2). All follow PROMPT_STANDARD with 10 mandatory `##` sections. Registered in process-registry.json workflow_guidance.userjourney phases and bootstrap_assets.  
**Corresponds to**: PA-9, PA-10, automation.md UJ-A, UJ-B.

---

### Gap-6: audit-process-drift.prompt.md does not follow PROMPT_STANDARD — **CLOSED 2026-04-13**

**Scope**: `.github/prompts/audit-process-drift.prompt.md`  
**Resolution**: Reclassified as a utility prompt (stage-agnostic diagnostic, not stage-advancing). Added utility exemption notice, abbreviated Protocol Declaration, and Pre-flight section in stage4gameplan Phase E. Added to exempt list in PROMPT_STANDARD.md and promptingguidelines.md.

---

### Gap-7: shape-research has an undocumented `## Notes` section — **CLOSED 2026-04-13**

**Scope**: `shape-research.prompt.md`  
**Resolution**: `## Notes` section removed in stage5gameplan Phase A. Notes content merged into `## Verification Gate` as a blockquote paragraph. `--check research-complete` added to the Verification Gate bash block.
