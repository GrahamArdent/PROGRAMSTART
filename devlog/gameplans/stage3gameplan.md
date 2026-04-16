# Stage 3 Gameplan — Protocol Alignment & Coverage Completion

Purpose: Implementation plan for aligning all prompts with JIT protocol, fixing known bugs, adding missing validators, creating missing shaping prompts, and closing the coverage gaps identified in `automation.md` (40 findings) and `promptaudit.md` (20 findings PA-1 through PA-20).
Status: **COMPLETE — All 9 phases (A-I) implemented. Post-impl gate passed 2026-04-12.**
Authority: Non-canonical working plan derived from `automation.md` and `promptaudit.md` audits of 2026-04-12.
Prompt: exempt — bootstrap
Last updated: 2026-04-12

---

## 1. The Problem

PROGRAMSTART has three enforcement layers that were designed independently and do not integrate:

1. **Instruction files** define the JIT protocol (derive context, baseline first, canonical before dependent, verify after)
2. **Prompts** guide stage-specific work but hardcode protocol summaries instead of loading them from authority docs
3. **Scripts/validators** enforce file-existence and structural checks but don't reference prompts or PROGRAMBUILD.md sections

**Result**: Zero shaping prompts reference the JIT protocol. PROGRAMBUILD.md is never loaded by any prompt. Kill criteria evaporate after Stage 1. DECISION_LOG is conditional in 4/5 prompts while mandatory per the gameplan. Stages 5, 6, 8, 10 have no prompt guidance and no content-level enforcement.

**Evidence**: `promptaudit.md` Part 2 protocol compliance matrix: 5/60 cells pass, 48/60 are ❌, 7/60 are partial. `automation.md` coverage chart: Stages 5-10 range from 15-40% automation density.

---

## 2. Reconciled Fix Order

`automation.md` recommends small wins first (trivial config → bug fixes → validators → prompts).
`promptaudit.md` recommends foundational work first (prompt standard → upgrade prompts → register orphans → create missing prompts → validators).

**Reconciled sequence**: Define the prompt standard first (it's a document, not code and unblocks all prompt work), then do the trivial code fixes (quick wins that unblock nothing but reduce noise), then upgrade existing prompts, then build new validators, then create missing prompts.

---

## 3. Phases

### Phase A: Define the Prompt Standard

**Goal**: Codify `promptaudit.md` Part 12 as a reusable reference document that all prompts must follow.

**Addresses**: PA-1, PA-2 (foundational — defines the contract all prompts must meet)

**Deliverables**:
- `.github/prompts/PROMPT_STANDARD.md` — reference document (not a `.prompt.md` file) defining the 10 mandatory sections + 3 optional sections
- Registered in `copilot-instructions.md` as a convention reference

**Mandatory sections** (from Part 12):

| # | Section | Source |
|---|---|---|
| 1 | YAML frontmatter | VS Code convention |
| 2 | Data Grounding Rule | All existing prompts |
| 3 | Protocol declaration | New — identifies which JIT steps apply |
| 4 | Pre-flight: drift baseline | `source-of-truth.instructions.md` Step 2 |
| 5 | Authority file loading | `source-of-truth.instructions.md` Step 3 |
| 6 | Upstream verification | Cross-stage validation |
| 7 | Protocol steps | PROGRAMBUILD.md §N (loaded, not hardcoded) |
| 8 | Output ordering | `sync_rules` authority-before-dependent |
| 9 | DECISION_LOG mandate | Per-stage gate requirement |
| 10 | Verification gate | `source-of-truth.instructions.md` Step 4 |
| 11 | Workflow routing | → stage-transition prompt |

**Optional sections** (based on stage):

| # | Section | When |
|---|---|---|
| O1 | PRODUCT_SHAPE conditioning | Stages 3+ |
| O2 | Kill criteria re-check | Stages 2+ |
| O3 | Entry criteria verification | Stage 7 |

**Verification**: Document review only — no code, no tests.

---

### Phase B: Trivial Fixes

**Goal**: Fix three known bugs/misconfigurations that require ≤3 lines each.

**Addresses**: automation.md 7-B, 3-A, UJ-C

| Fix | File | Change | Lines |
|---|---|---|---|
| **7-B** | `config/process-registry.json` | Add `implement-gameplan-phase*` to `implementation_loop.prompts` | ~1 array entry |
| **3-A** | `scripts/programstart_validate.py` line 261 | Fix substring cross-ref matching — use `re.search(r'\bREQ-\d+', ...)` instead of plain `in` | 1 line |
| **UJ-C** | `config/process-registry.json` | Set `userjourney.enforce_engineering_ready` to `true` (currently `false`, code already exists at validate.py line 601/605/1002) | 1 value |

**Verification**: `uv run pytest --cov-report=term-missing` — all existing tests must pass. Add one test for the 3-A regex fix.

---

### Phase C: Register Orphaned Prompts

**Goal**: Make three operator-facing prompts discoverable via `programstart guide`.

**Addresses**: PA-6

| Prompt | Target registry location |
|---|---|
| `product-jit-check.prompt.md` | `workflow_guidance.implementation_loop.prompts` |
| `propagate-canonical-change.prompt.md` | Cross-cutting — add to all stages' prompts arrays, or to a new `cross_cutting_prompts` key |
| `programstart-cross-stage-validation.prompt.md` | Cross-cutting — same treatment as propagate |

**Design decision needed**: Should cross-cutting prompts go in every stage's `prompts` array (noisy) or in a new `cross_cutting_prompts` array at the workflow level? Record decision in `DECISION_LOG.md`.

**Verification**: `uv run programstart guide --system programbuild` must list all three prompts. `uv run programstart validate` must pass.

---

### Phase D: Upgrade Existing Shaping Prompts

**Goal**: Bring all 5 `shape-*.prompt.md` files into compliance with the prompt standard from Phase A.

**Addresses**: PA-1, PA-2, PA-3, PA-5, PA-11, PA-16

**Changes per prompt** (applied to shape-idea, shape-feasibility, shape-research, shape-requirements, shape-architecture):

1. **Add Protocol declaration** — "This prompt follows JIT Steps 1-4"
2. **Add Pre-flight drift baseline** — `programstart drift` before any edits
3. **Add Authority file loading** — read PROGRAMBUILD.md §N for the relevant stage
4. **Add kill criteria re-check** (shape-research, shape-requirements, shape-architecture) — structured re-evaluation against FEASIBILITY.md kill criteria
5. **Change DECISION_LOG from conditional to mandatory** — "You MUST update DECISION_LOG.md. The gate validator will reject advance if missing."
6. **Add Verification gate** — `programstart validate --check <stage-check>` AND `programstart drift` (shape-idea and shape-research already have this; verify others)
7. **Add Workflow routing** — "After completing this prompt, run `programstart-stage-transition` to validate and advance."

**Constraint**: Do NOT rewrite the protocol steps themselves. The existing step content is correct. Only wrap them with the standard sections.

**Verification**: Read each updated prompt and confirm all 10+applicable optional sections are present. `uv run programstart validate` must pass. `uv run programstart drift` must pass.

---

### Phase E: DECISION_LOG Validators

**Goal**: Add DECISION_LOG entry checks to gate validators for Stages 0, 1, 4.

**Addresses**: automation.md 0-C, 1-A, 4-B; promptaudit PA-5

**Implementation**:
- Add a shared helper `_check_decision_log_entries(stage_name: str) -> list[str]` in `programstart_validate.py` that:
  - Reads `PROGRAMBUILD/DECISION_LOG.md`
  - Checks that at least one entry references the given stage name or stage number
  - Returns a list of problems (empty = pass)
- Wire into `validate_intake_complete()` (line 69), `validate_feasibility_criteria()` (line 138), `validate_architecture_contracts()` (line 269)
- `sync_rules` reference: `sync_rules[15]` (`architecture_decision_alignment`) — `DECISION_LOG.md` is a dependent of `ARCHITECTURE.md`

**Tests**: One test per stage confirming that a DECISION_LOG without the stage's entry triggers a validation warning. One test confirming a populated DECISION_LOG passes.

**Verification**: `uv run pytest --cov-report=term-missing` — new tests pass, no regressions.

---

### Phase F: RISK_SPIKES Validator

**Goal**: Add structural validation for RISK_SPIKES.md.

**Addresses**: automation.md 4-A; promptaudit PA-7

**Implementation**:
- New function `validate_risk_spikes(project_root: Path) -> list[str]` in `programstart_validate.py`
- Checks:
  - File exists and is non-empty
  - Contains at least one spike entry with: scope, acceptance criteria, time-box, status
  - Referenced by at least one entry in `ARCHITECTURE.md` or `FEASIBILITY.md`
- Wire into Stage 4 gate check (after `validate_architecture_contracts`)
- `sync_rules` reference: `sync_rules[5]` (`risk_spike_feasibility_link`) — `RISK_SPIKES.md` is a dependent of `FEASIBILITY.md`

**Tests**: Happy-path (valid spike doc passes), missing-file, empty-file, no-spike-entries, spike-without-acceptance-criteria.

**Verification**: `uv run pytest --cov-report=term-missing` — new tests pass, no regressions.

---

### Phase G: New Stage Validators

**Goal**: Add content-level validators for Stages 5, 6, 7, 8, 9.

**Addresses**: automation.md 6-B, 7-A, 5-B, 8-B, 9-A; promptaudit PA-4

**New functions** (all in `programstart_validate.py`):

| Function | Stage | Checks |
|---|---|---|
| `validate_test_strategy_complete()` | 6 | TEST_STRATEGY.md exists, has at least one test category, references requirements |
| `validate_implementation_entry_criteria()` | 7 | Delegates to test-strategy + architecture-contracts + risk-spikes; engineering-ready gate |
| `validate_scaffold_complete()` | 5 | Scaffold files exist per PRODUCT_SHAPE, pyproject.toml or equivalent present |
| `validate_release_ready()` | 8 | RELEASE_READINESS.md exists, has go/no-go decision, references test results |
| `validate_audit_complete()` | 9 | AUDIT_REPORT.md exists, has findings list, drift check recorded |

**Wire**: Each validator into its stage's gate check in the workflow state machinery or validate dispatch.

**Tests**: At least 2 per validator (happy-path + primary failure mode).

**Verification**: `uv run pytest --cov-report=term-missing` — all tests pass, coverage does not decrease.

---

### Phase H: New Shaping Prompts

**Goal**: Create shaping prompts for Stages 5, 6, 8, 10 using the prompt standard from Phase A.

**Addresses**: automation.md 5-A, 6-A, 8-A, 10-A; promptaudit PA-4

**Deliverables**:

| Prompt | Stage | Authority section |
|---|---|---|
| `shape-scaffold.prompt.md` | 5: scaffold_and_guardrails | PROGRAMBUILD.md §12 |
| `shape-test-strategy.prompt.md` | 6: test_strategy | PROGRAMBUILD.md §13 |
| `shape-release-readiness.prompt.md` | 8: release_readiness | PROGRAMBUILD.md §15 |
| `shape-post-launch-review.prompt.md` | 10: post_launch_review | PROGRAMBUILD.md §17 |

**Each prompt must include all 10 mandatory sections** from the prompt standard, plus applicable optional sections:
- PRODUCT_SHAPE conditioning (all four — Stage 5+)
- Kill criteria re-check (all four — Stage 2+)
- Entry criteria verification (none — that's Stage 7 only)

**Register each prompt** in the appropriate `workflow_guidance.*.prompts` array in `config/process-registry.json`.

**PROGRAMBUILD_CANONICAL.md Rule 5**: New prompts must be registered in the canonical file index. Update `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`.

**Verification**: `uv run programstart guide --system programbuild` must list each new prompt at its stage. `uv run programstart validate` must pass. `uv run programstart drift` must pass.

---

### Phase I: Routing, UX, and Error Messages

**Goal**: Wire prompts together so operators know what to do next after each step.

**Addresses**: PA-11, PA-14, PA-15, PA-16

**Deliverables**:
1. **Stage-transition → next-shaping-prompt routing**: Update `programstart-stage-transition.prompt.md` to include a "Next prompt" recommendation based on the stage being transitioned to
2. **Validation error → prompt/section references**: Update validation error messages in `programstart_validate.py` to include "See: shape-<stage>.prompt.md" or "See: PROGRAMBUILD.md §N" when a check fails
3. **Cross-stage-validation wiring**: Add a step to each shaping prompt's upstream verification that invokes cross-stage-validation concepts (not necessarily the full prompt, but the key checks)

**Verification**: Manual review of updated error messages. `uv run pytest --cov-report=term-missing` — all tests pass.

---

## 4. Dependency Graph

```
Phase A (prompt standard)
  ↓
Phase D (upgrade existing prompts)  ←── depends on A
Phase H (new shaping prompts)       ←── depends on A
  ↓
Phase I (routing & UX)              ←── depends on D + H

Phase B (trivial fixes)             ←── independent
Phase C (register orphans)          ←── independent

Phase E (DECISION_LOG validators)   ←── independent
Phase F (RISK_SPIKES validator)     ←── independent
Phase G (new stage validators)      ←── depends on E + F (7-A delegates)
```

**Recommended execution order**: A → B → C → E → F → D → G → H → I

Rationale: A is foundational (all prompt work depends on it). B and C are quick wins. E and F are prerequisites for G (the Stage 7 entry-criteria validator delegates to both). D upgrades existing prompts before H creates new ones. I wires everything together last.

---

## 5. Scope Boundaries

### In scope
- All AUTOMATE-tier findings from `automation.md` (15 findings)
- All CRITICAL and HIGH findings from `promptaudit.md` (PA-1 through PA-12)
- Cross-cutting schema findings SCH-A, SCH-B, SCH-C from `automation.md`

### Out of scope (deferred)
- CONSIDER-tier findings from `automation.md` (11 findings) — evaluate after Tier 1 is complete
- SKIP-tier findings from `automation.md` (12 findings) — intentionally deferred
- MEDIUM and LOW findings from `promptaudit.md` (PA-13 through PA-20) — structural improvements, not blocking
- USERJOURNEY phase-specific prompts (PA-9, PA-10) — large scope, should be its own gameplan
- `step_files` expansion evaluation (promptaudit fix order #9) — needs design discussion first

### Decision required before Phase C
- Cross-cutting prompt registration strategy (per-stage arrays vs. new workflow-level key)

### Decision required before Phase G
- Whether `validate_scaffold_complete()` should be PRODUCT_SHAPE-aware (different checks for CLI vs. web app) or generic

---

## 6. Verification Protocol

Every phase must pass this gate before the next phase begins:

1. `uv run programstart validate --check all` — pass
2. `uv run programstart drift` — pass (or clean baseline if drift is expected from the phase)
3. `uv run pytest --cov-report=term-missing` — all tests pass, coverage ≥ current baseline
4. `uv run pyright` — no new type errors
5. Commit with conventional commit message: `<type>[scope]: <description>`

---

## 7. Cross-Reference Index

| Gameplan Phase | automation.md Findings | promptaudit.md Findings |
|---|---|---|
| A | — | PA-1, PA-2 |
| B | 7-B, 3-A, UJ-C | — |
| C | — | PA-6 |
| D | — | PA-1, PA-2, PA-3, PA-5, PA-11, PA-16 |
| E | 0-C, 1-A, 4-B | PA-5 |
| F | 4-A | PA-7 |
| G | 6-B, 7-A, 5-B, 8-B, 9-A | PA-4 |
| H | 5-A, 6-A, 8-A, 10-A | PA-4 |
| I | — | PA-11, PA-14, PA-15, PA-16 |
