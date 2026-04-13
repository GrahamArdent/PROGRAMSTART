# Stage 4 Gameplan — Prompt Polish, Stage 9 Coverage, Output Ordering

Purpose: Implementation plan for closing the 6 remaining gaps identified in `promptaudit.md` Part 13 after the Phase A-I protocol alignment pass.
Status: **COMPLETE — Phases A–E executed 2026-04-13.**
Authority: Non-canonical working plan derived from `promptaudit.md` (Part 13, Recommended Fix Order items 8–14), `promptingguidelines.md` (What Still Needs Doing), and `automation.md` (Tier 2 CONSIDER findings).
Last updated: 2026-04-13

---

## 1. The Problem

After Phase A-I, all 9 shaping prompts have Protocol Declaration, Pre-flight drift, Authority Loading, DECISION_LOG mandate, Verification Gate, and Next Steps. The compliance score rose from 5/60 to 62/106 ✅.

Six structural gaps remain:

| Gap | Scope | Severity |
|---|---|---|
| Gap-1 | Stage 9 has no shaping prompt — validator exists, no operator guide | HIGH |
| Gap-2 | Output Ordering (PROMPT_STANDARD §8) absent from all 9 prompts | HIGH |
| Gap-3 | Stages 2–10 Authority Loading loads `PROGRAMBUILD_CANONICAL.md §N` but Protocol Declaration cites `PROGRAMBUILD.md §N` — inconsistency | MEDIUM |
| Gap-4a | `shape-architecture` Verification Gate missing `--check risk-spikes` | MEDIUM |
| Gap-4b | `shape-release-readiness` missing PRODUCT_SHAPE Conditioning section | LOW |
| Gap-5 | USERJOURNEY has no phase-specific shaping prompts (22/26 files unprotected) | MEDIUM |
| Gap-6 | `audit-process-drift.prompt.md` predates PROMPT_STANDARD and is non-compliant | LOW |

Additionally, `automation.md` Finding 2-A (CONSIDER verdict): Stage 2 is the only early stage with a shaping prompt but no content-gate validator.

---

## 2. Phase Sequence

Phases are ordered so that foundational changes (Output Ordering, Authority Loading) complete before new files are created, so new files are written to the correct standard from the start.

| Phase | Gap | Type | Est. edits |
|---|---|---|---|
| Pre-work | — | Record test + validate + drift baseline | 0 edits |
| A | Gap-2 | Edit 9 existing prompts | 9 file edits |
| B | Gap-3 | Edit 7 existing prompts | 7 file edits |
| C | Gap-4a + Gap-4b | Targeted fixes: 2 prompts | 2 file edits |
| D | Gap-1 | Create new file + 3 supporting edits | 1 new prompt + 3 file edits |
| E | Gap-6 | Edit 3 existing files | 3 file edits |
| F | Gap-5 | Create new files (3) | 3 new prompts |
| G | automation.md 2-A | Edit script + tests | 1 script + tests |

Phases F and G are lower priority and can be deferred. Phases A–E are the core work.

---

## 3. Phases

---

### Pre-work: Record Baseline

Before any edits, confirm the current test and validate baseline so post-phase verification has a known starting point.

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 10  # record pass/fail count
uv run programstart validate --check all                    # must already pass
uv run programstart drift                                   # must already pass
```

Record any pre-existing test failures. The post-phase gate requires no *new* failures — not that the baseline is clean. If `validate` or `drift` are already failing, resolve them before proceeding.

---

### Phase A: Add Output Ordering Section to All 9 Shaping Prompts

**Goal**: Close Gap-2. Add the `## Output Ordering` mandatory section (PROMPT_STANDARD §8) to every shaping prompt.

**Why first**: It is the single largest remaining compliance gap — the whole Output Ordering row in `promptingguidelines.md` is ❌. It is also a mechanical add (same section template, different sync_rule citation per prompt), making it parallelisable across all 9 files in one `multi_replace_string_in_file` call.

**Addresses**: Gap-2, PA-1 (JIT Step 3 partial → full), PA-6 partial

**Section template** (from PROMPT_STANDARD §8):
```markdown
## Output Ordering

Write files in authority-before-dependent order per `config/process-registry.json` `sync_rules`:

1. [Authority file] — write first
2. [Dependent file(s)] — derive from authority content
```

**Placement**: Between `## Protocol` (§7) and `## DECISION_LOG` (§9). Each prompt's Protocol section ends before DECISION_LOG — insert `## Output Ordering` there.

**Per-prompt content**:

| Prompt | sync_rule(s) to cite | Write order |
|---|---|---|
| `shape-idea.prompt.md` | None named (Stage 0 kickoff) | `PROGRAMBUILD_IDEA_INTAKE.md` first → seed `PROGRAMBUILD_KICKOFF_PACKET.md` second |
| `shape-feasibility.prompt.md` | `programbuild_feasibility_cascade` | `FEASIBILITY.md` first → `DECISION_LOG.md` second |
| `shape-research.prompt.md` | `programbuild_feasibility_cascade` (governs the cross-stage FEASIBILITY.md → RESEARCH_SUMMARY.md relationship; at Stage 2, FEASIBILITY.md is read-only input from Stage 1 — do not re-write it) | `RESEARCH_SUMMARY.md` first (primary Stage 2 new output) → `DECISION_LOG.md`, `RISK_SPIKES.md` second |
| `shape-requirements.prompt.md` | `programbuild_requirements_scope` | `REQUIREMENTS.md` first → `USER_FLOWS.md` second |
| `shape-architecture.prompt.md` | `programbuild_architecture_contracts` + `architecture_decision_alignment` | `ARCHITECTURE.md` first → `RISK_SPIKES.md` second → `DECISION_LOG.md` third |
| `shape-scaffold.prompt.md` | None named (no sync_rule for scaffold code outputs) | `SCAFFOLD_SUMMARY.md` written last (after scaffold files committed). `ARCHITECTURE.md` is read-only input — do not modify during Stage 5. Verify exact output file name against `validate_scaffold_complete()` in `scripts/programstart_validate.py` before writing this section. |
| `shape-test-strategy.prompt.md` | `requirements_test_alignment` | `TEST_STRATEGY.md` primary output → `DECISION_LOG.md` if decisions made |
| `shape-release-readiness.prompt.md` | `programbuild_architecture_contracts` (RELEASE_READINESS is a dependent of ARCHITECTURE.md) | `RELEASE_READINESS.md` first → `DECISION_LOG.md` second |
| `shape-post-launch-review.prompt.md` | None named (terminal stage) | `POST_LAUNCH_REVIEW.md` first → `DECISION_LOG.md` second |

**Note on shape-idea sync_rule**: `PROGRAMBUILD_IDEA_INTAKE.md` and `PROGRAMBUILD_KICKOFF_PACKET.md` appear as `dependent_files` in the `programbuild_control_inventory` sync_rule, but that rule governs *system editing* (modifying PROGRAMSTART template files), not *project execution* (an operator filling a kickoff packet for their project). "None named" in the table above is correct for project-execution context.

**Approach**: One `multi_replace_string_in_file` call with 9 replacements. For each prompt, use the literal heading `\n## DECISION_LOG` as the insertion anchor — do not anchor on the Protocol step content, which varies per prompt and produces fragile matches. The `\n## DECISION_LOG` heading exists immediately after `## Protocol` in all 9 prompts (confirmed by section scan).

**Known anomaly**: `shape-research.prompt.md` has an undocumented `## Notes` section between `## Verification Gate` and `## Next Steps`. It is not in PROMPT_STANDARD and is unaffected by Phase A (insertion is between `## Protocol` and `## DECISION_LOG` — the anomaly is downstream of both). Flag for cleanup in a future pass. Record as a named finding in `promptaudit.md` Part 13 (e.g., Gap-7: shape-research undocumented `## Notes` section) during the Section 4 documentation update step so it is not lost after this implementation completes.

**Verification**: After edits, run `Get-ChildItem .github/prompts/shape-*.prompt.md | Select-String "## Output Ordering"` — should return 9 matches. Additionally, read-check one representative prompt (e.g., `shape-research.prompt.md`) to confirm `## Output Ordering` appears between `## Protocol` and `## DECISION_LOG` in the section list — not before or after other sections. Run `uv run programstart validate --check all` and `uv run programstart drift` — both must pass (no validators check for Output Ordering sections, so this is a content spot-check only).

---

### Phase B: Fix Authority Loading Inconsistency in Stages 2–10

**Goal**: Close Gap-3. Make Authority Loading consistent with Protocol Declaration: both should reference `PROGRAMBUILD.md §N`.

**Decision** (document in DECISION_LOG.md):
- `PROGRAMBUILD_CANONICAL.md §N` correctly tells the AI which files are required outputs for a stage and how stage boundaries are defined.
- `PROGRAMBUILD.md §N` tells the AI what the *procedural protocol* is — *how* to do the work.
- **Resolution**: Load **both**. Keep the existing `PROGRAMBUILD_CANONICAL.md §N` line, and add `PROGRAMBUILD.md §N` as an additional bullet in Authority Loading. The Protocol Declaration (which already says `PROGRAMBUILD.md §N`) then becomes accurate.

**Affected prompts** (7):

| Prompt | Current Authority Loading | Fix |
|---|---|---|
| `shape-research.prompt.md` | `PROGRAMBUILD_CANONICAL.md §9` | Add `PROGRAMBUILD/PROGRAMBUILD.md §9` bullet |
| `shape-requirements.prompt.md` | `PROGRAMBUILD_CANONICAL.md §10` | Add `PROGRAMBUILD/PROGRAMBUILD.md §10` bullet |
| `shape-architecture.prompt.md` | `PROGRAMBUILD_CANONICAL.md §11` | Add `PROGRAMBUILD/PROGRAMBUILD.md §11` bullet |
| `shape-scaffold.prompt.md` | `PROGRAMBUILD_CANONICAL.md §12` | Add `PROGRAMBUILD/PROGRAMBUILD.md §12` bullet |
| `shape-test-strategy.prompt.md` | `PROGRAMBUILD_CANONICAL.md §13` | Add `PROGRAMBUILD/PROGRAMBUILD.md §13` bullet |
| `shape-release-readiness.prompt.md` | `PROGRAMBUILD_CANONICAL.md §15` | Add `PROGRAMBUILD/PROGRAMBUILD.md §15` bullet |
| `shape-post-launch-review.prompt.md` | `PROGRAMBUILD_CANONICAL.md §17` | Add `PROGRAMBUILD/PROGRAMBUILD.md §17` bullet |

**Pre-flight**: Confirm `PROGRAMBUILD/PROGRAMBUILD.md` exists: `Test-Path PROGRAMBUILD/PROGRAMBUILD.md`. If absent, STOP — the Protocol Declarations added in Phase A-I may already be citing a non-existent file. Audit all 9 Protocol Declarations to determine what authority file they actually reference before proceeding.

**Approach**: One `multi_replace_string_in_file` call with 7 replacements. In each prompt, find the Authority Loading block and add the `PROGRAMBUILD.md §N` bullet immediately after the `PROGRAMBUILD_CANONICAL.md §N` bullet.

**Verification**: Read-check `shape-research.prompt.md` (first edited) and `shape-post-launch-review.prompt.md` (last edited) to confirm the `PROGRAMBUILD.md §N` bullet appears immediately after the `PROGRAMBUILD_CANONICAL.md §N` bullet in each Authority Loading block. Run `uv run programstart validate --check all` and `uv run programstart drift`.

---

### Phase C: Targeted Fixes on Two Prompts

**Goal**: Close Gap-4a (shape-architecture) and Gap-4b (shape-release-readiness).

**Part 1 — shape-architecture Verification Gate (Gap-4a)**:

The `stage_checks` dict in `programstart_workflow_state.py` runs BOTH `architecture-contracts` AND `risk-spikes` when preflight fires for Stage 4. The prompt's Verification Gate only runs `--check architecture-contracts`. An operator following the prompt will pass the architecture gate but miss the risk-spikes gate.

**Fix**: In `shape-architecture.prompt.md`, find the Verification Gate block and add a second `uv run programstart validate --check risk-spikes` line after the existing `--check architecture-contracts` line. **Pre-flight**: Before editing the prompt, run `uv run programstart validate --check risk-spikes` to confirm the CLI accepts this check. If it fails with an 'invalid choice' error, add `risk-spikes` to argparse choices in `programstart_validate.py` first (before editing the prompt).

**Part 2 — shape-release-readiness PRODUCT_SHAPE Conditioning (Gap-4b)**:

Stages 3, 4, 5, 6 all have a `## PRODUCT_SHAPE Conditioning` section. Stage 8 does not. The section documents how CLI vs. web app vs. API requirements differ so the AI knows to ask about smoke check URLs (web app), endpoint liveness (API), or deployment scripts (CLI) rather than applying a generic checklist.

**Fix**: In `shape-release-readiness.prompt.md`, add a `## PRODUCT_SHAPE Conditioning` section after `## Kill Criteria Re-check` and before `## Protocol`, following the pattern in `shape-test-strategy.prompt.md`.

**Section content spec** (implement these shape-specific bullets — do not paraphrase):
- **CLI tool**: Smoke check = run the binary with `--version` or `--help` and confirm exit 0. No database migration risk. Rollback = redeploy previous artifact/binary.
- **Web app**: Smoke check = GET primary route returns HTTP 200. Runbook must include a database migration rollback plan and blue/green or zero-downtime deploy procedure.
- **API service**: Smoke check = health endpoint returns HTTP 200. Runbook must include a contract compatibility check and canary or staged rollback procedure.
- **Other shapes**: Default to the closest analogue above. Flag any shape-specific rollback complexity in the runbook.

**Approach**: `multi_replace_string_in_file` with 2 replacements (one per file).

**Verification**: Read-check both files. Run `uv run programstart validate --check all` and `uv run programstart drift` — both must pass.

**Note on multi-phase edits**: `shape-release-readiness.prompt.md` is edited in Phases A, B, and C (Output Ordering added in A, PROGRAMBUILD.md §15 bullet added in B, PRODUCT_SHAPE Conditioning added in C). Each edit targets a different section so they should not conflict, but verify the section scan after each phase to confirm anchors still resolve correctly before proceeding to the next. Conflict risk is low: Phase A targets the line immediately before `## DECISION_LOG`, Phase B targets the `PROGRAMBUILD_CANONICAL.md §15` bullet in Authority Loading, and Phase C targets text in the Kill Criteria Re-check section — these are in separate, non-adjacent regions of the file.

---

### Phase D: Create shape-audit.prompt.md for Stage 9

**Goal**: Close Gap-1. Stage 9 (`audit_and_drift_control`) is the only stage with a validator but no shaping prompt. The validator (`--check audit-complete`) confirms `AUDIT_REPORT.md` exists and is structured, but no prompt guides the operator through producing it.

**Addresses**: Gap-1, PA-4 (partial), automation.md Finding 9-A

**File**: `.github/prompts/shape-audit.prompt.md`

**PROMPT_STANDARD compliance**: Full — all mandatory sections + Kill Criteria Re-check (§O2, Stage 2+). Before writing the file, re-read `PROMPT_STANDARD.md` to confirm the exact `##` heading list and count. The verification step below assumes 10 `##` headings (YAML frontmatter has no `##` heading; Kill Criteria Re-check §O2 is included as heading #5). Adjust the spec and verification count if live PROMPT_STANDARD diverges.

**Mandatory section content**:

| Section | Content |
|---|---|
| YAML frontmatter | `description: "Stage 9 audit and drift control — guide to producing AUDIT_REPORT.md and passing audit-complete gate. Use at Stage 9."` / `name: "Shape Audit"` / `argument-hint: "Name the project being audited"` / `agent: "agent"` — all four fields required per PROMPT_STANDARD §1 |
| Data Grounding Rule | Copy verbatim from PROMPT_STANDARD §2 |
| Protocol Declaration | JIT Steps 1-4. Authority: `PROGRAMBUILD/PROGRAMBUILD.md §16 — audit_and_drift_control` |
| Pre-flight | `uv run programstart drift` — STOP if violations |
| Authority Loading | `PROGRAMBUILD/PROGRAMBUILD.md §16`, `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md §16`, `PROGRAMBUILD/FEASIBILITY.md` (required by Kill Criteria Re-check), `PROGRAMBUILD/ARCHITECTURE.md`, `PROGRAMBUILD/DECISION_LOG.md`, `PROGRAMBUILD/RISK_SPIKES.md`, `PROGRAMBUILD/RELEASE_READINESS.md`, `PROGRAMBUILD/AUDIT_REPORT.md` (if it exists). Stage-specific deliverables (RESEARCH_SUMMARY.md, REQUIREMENTS.md, TEST_STRATEGY.md) are loaded during Protocol Steps as the audit walks each stage — not pre-loaded here. |
| Kill Criteria Re-check | Re-read FEASIBILITY.md kill criteria — if any triggered, flag before continuing |
| Protocol Steps | Load PROGRAMBUILD.md §16. Audit procedure: check stage-gate evidence for each completed stage, check DECISION_LOG completeness, run drift check, produce `AUDIT_REPORT.md` with findings. |
| Output Ordering | `AUDIT_REPORT.md` is the primary output — write it first. `DECISION_LOG.md` is updated after audit conclusions are written, not before. |
| DECISION_LOG mandate | You MUST update `PROGRAMBUILD/DECISION_LOG.md` after writing `AUDIT_REPORT.md`. Record the audit verdict (pass/fail), any re-opened spikes, and the `audit-complete` gate status. |
| Verification Gate | `uv run programstart validate --check audit-complete` then `uv run programstart drift` |
| Next Steps | If audit passed: run `programstart-stage-transition` to advance to Stage 10. If audit found gaps: STOP — do not advance. Resolve gaps, re-run `shape-audit`, and re-confirm the gate before transitioning. |

**PRODUCT_SHAPE Conditioning**: Stage 9 is explicitly exempt — an audit reviews all stage outputs regardless of product shape. Numerically, Stage 9 falls within the "Stages 3+" trigger window in PROMPT_STANDARD O1, so the exemption is *categorical* (audit content is shape-agnostic by definition), not numerical. **Additional deliverable**: Add an explicit exemption note to `PROMPT_STANDARD.md §O1` and `promptingguidelines.md §O1` ("Stage 9 `shape-audit` exempt — audit reviews all stage outputs and is shape-agnostic by definition") to prevent compliance checkers from treating the absence of a PRODUCT_SHAPE section as a gap.

**Additional deliverable**: Register `shape-audit.prompt.md` in `config/process-registry.json` under `workflow_guidance.programbuild.audit_and_drift_control.prompts`. This ensures `programstart guide --system programbuild` surfaces the prompt when Stage 9 is active. Every other stage already has its shape prompt registered; Stage 9 is the only gap.

**Approach**: `create_file` for the new prompt, then `replace_string_in_file` to add the Stage 9 exemption note to `PROMPT_STANDARD.md §O1` and `promptingguidelines.md §O1`, then `replace_string_in_file` to add the prompt entry to `config/process-registry.json`.

**Verification**:
- `Get-Content .github/prompts/shape-audit.prompt.md | Select-String "^## "` — must return exactly 10 `##` headings in PROMPT_STANDARD order: Data Grounding Rule → Protocol Declaration → Pre-flight → Authority Loading → Kill Criteria Re-check → Protocol → Output Ordering → DECISION_LOG → Verification Gate → Next Steps. (YAML frontmatter has no `##` heading; the count is 10 not 11.)
- Confirm `shape-audit.prompt.md` appears in `config/process-registry.json` `audit_and_drift_control.prompts`.
- Confirm "Stage 9" exemption note appears in `PROMPT_STANDARD.md §O1` and `promptingguidelines.md §O1`.
- Run `uv run programstart validate --check all`.

---

### Phase E: Upgrade audit-process-drift.prompt.md

**Goal**: Close Gap-6. This prompt predates PROMPT_STANDARD. It is registered as an operator-facing prompt but is missing Protocol Declaration, Pre-flight, DECISION_LOG mandate, and Verification Gate.

**Classification decision**: This prompt is a *utility* (can be run at any stage as a diagnostic), not a *stage-advancing* prompt. Two options were considered: (A) full upgrade to PROMPT_STANDARD structure, or (B) utility exemption with Pre-flight only. Option A was rejected because mandatory DECISION_LOG enforcement and a hard Verification Gate would be misleading for a diagnostic prompt that does not advance a stage. **Decision: Option B** — add utility exemption notice, abbreviated Protocol Declaration, and Pre-flight.

**Current state of `audit-process-drift.prompt.md`**:
- ✅ YAML frontmatter (present)
- ✅ Data Grounding Rule (present — verbatim match)
- ❌ Protocol Declaration (absent)
- ❌ Pre-flight drift check (absent)
- ❌ Authority Loading (absent — intentionally omitted for utility)
- ❌ DECISION_LOG mandate (absent — intentionally omitted for utility)
- ❌ Verification Gate (absent — intentionally omitted for utility)

**What is being added** (Option B minimum):
1. A utility exemption notice immediately after the title: "This is a utility prompt. It does not advance a stage and is exempt from stage-gate Authority Loading, DECISION_LOG mandate, and Verification Gate requirements."
2. An abbreviated Protocol Declaration citing JIT Steps 1-4 apply when relevant; no specific stage authority section.
3. Pre-flight: `uv run programstart drift` before running audit steps.

**Additional deliverables** (both must happen in the same commit as the prompt edit):
- Update the exempt prompts list in `PROMPT_STANDARD.md` to include `audit-process-drift.prompt.md`. Currently the list names only `implement-gameplan-phase*`, `implement-stage2-gameplan`, `implement-phase-f`, `implement-protocol-alignment`.
- Update the exempt prompts list in `promptingguidelines.md` "What This Document Is For" section to include `audit-process-drift.prompt.md`.

**Approach**: Three `replace_string_in_file` calls on `audit-process-drift.prompt.md` — one per new element — then two more on `PROMPT_STANDARD.md` and `promptingguidelines.md` for the exempt lists. Target structure of `audit-process-drift.prompt.md` after Phase E (in section order):

1. YAML frontmatter (existing)
2. Title line: "Audit process drift using the repository workflow rules." (existing)
3. Utility exemption notice (NEW — insert after title, before Data Grounding Rule)
4. Data Grounding Rule (existing)
5. Abbreviated Protocol Declaration (NEW — insert after Data Grounding Rule)
6. Pre-flight (NEW — insert after Protocol Declaration, before Tasks)
7. Tasks 1–4 (existing)

Anchor the exemption notice insertion on the title line. Anchor the Protocol Declaration insertion on the closing sentence of the Data Grounding Rule. Anchor the Pre-flight insertion on the "Tasks:" heading.

**Verification**: Read-check all three files. Run `Get-Content .github/prompts/audit-process-drift.prompt.md | Select-String "^## |^> \*\*UTILITY"` to confirm the exemption notice and Pre-flight heading appear. Confirm `audit-process-drift.prompt.md` appears in the exempt lists of both standard documents.

---

### Phase F: Create USERJOURNEY Shaping Prompts (Deferred)

**Goal**: Close Gap-5. Three minimum-viable USERJOURNEY phase prompts to cover the 22 currently unprotected authority/dependent files.

**Why deferred**: Estimated effort is 3× the effort of Phase D (3 new files, more complex authority chains, legal file sensitivity). PROGRAMBUILD coverage is the system's primary user-facing concern. USERJOURNEY shaping prompts add value when the USERJOURNEY workflow is actually being executed (not during planning-system maintenance).

**Addresses**: Gap-5, PA-9, PA-10, automation.md UJ-A, UJ-B

**Prompt set**:

| File | Phase | Authority files | Verification Gate |
|---|---|---|---|
| `shape-uj-decision-freeze.prompt.md` | UJ Phase 0 | `ROUTE_AND_STATE_FREEZE.md`, `STATES_AND_RULES.md`, `DECISION_LOG.md` (UJ) | No validator yet — run `drift` only |
| `shape-uj-legal-drafts.prompt.md` | UJ Phase 1 | `LEGAL_AND_CONSENT.md`, `OPEN_QUESTIONS.md`, `LEGAL_REVIEW_NOTES.md` → `TERMS_OF_SERVICE_DRAFT.md`, `PRIVACY_POLICY_DRAFT.md`, `EXTERNAL_REVIEW_PACKET.md` | No validator yet — run `drift` only |
| `shape-uj-ux-surfaces.prompt.md` | UJ Phase 2 | `DELIVERY_GAMEPLAN.md`, `USER_FLOWS.md` (UJ), `ACCEPTANCE_CRITERIA.md` → `SCREEN_INVENTORY.md`, `UX_COPY_DRAFT.md`, `ANALYTICS_AND_OUTCOMES.md` | No validator yet — run `drift` only |

**Note**: These prompts should also cite `userjourney_external_review_packet`, `userjourney_route_state_logic`, and `userjourney_implementation_seq` sync_rules in their Output Ordering sections. UJ prompts do not require a PRODUCT_SHAPE Conditioning section (§O1 applies to PROGRAMBUILD stages 3+ only — USERJOURNEY authority chains are product-shape-independent).

**Approach**: `create_file` × 3. Deferrable — start only after Phases A–E are complete. **Trigger for deferred execution**: Execute Phase F when a USERJOURNEY workflow run is actively planned or underway — not during PROGRAMBUILD-only maintenance passes.

**Verification**: For each new UJ prompt, run `Get-ChildItem .github/prompts/shape-uj-*.prompt.md | Select-String "^## "` to confirm all 11 mandatory PROMPT_STANDARD sections are present in order. Run `uv run programstart drift`. No `validate` gate exists for UJ phases yet — drift is the only structural check available.

---

### Phase G: Create validate_research_complete() (Deferred)

**Goal**: Close automation.md Finding 2-A. Stage 2 is the only early stage with a shaping prompt but no content gate. An empty `RESEARCH_SUMMARY.md` passes advance silently.

**Why deferred**: The original gameplan (stage2gameplan.md Q3) intentionally deferred this because research quality is hard to validate structurally. The CONSIDER verdict in `automation.md` reflects this. Deferring allows real operator usage to inform what a useful check looks like before implementing a structural constraint.

**Trigger for deferred execution**: Execute Phase G after encountering 2+ real research phases where quality issues went undetected by the existing validate gate — i.e., when operational evidence exists that a structural content check is needed.

**Deliverables**:
- `validate_research_complete()` in `scripts/programstart_validate.py` — checks: (1) `RESEARCH_SUMMARY.md` exists and has non-template sections (## Findings, ## Alternatives or similar), (2) `DECISION_LOG.md` has at least one entry referencing research or low-confidence decisions
- Add `"research": "research-complete"` to `stage_checks` dict in `programstart_workflow_state.py`
- Add `"research-complete": validate_research_complete` to `run_stage_gate_check()` dispatch
- Add `research-complete` to argparse choices in CLI
- Update `shape-research.prompt.md` Verification Gate from `--check all` to `--check research-complete` once validator exists

**Tests**: Add `tests/test_programstart_validate_research.py` mirroring pattern of `test_programstart_validate_feasibility.py`.

**Verification**: `uv run pytest tests/test_programstart_validate_research.py -v` — all tests pass. `uv run programstart validate --check research-complete` on a package with and without `RESEARCH_SUMMARY.md`.

---

## 4. Post-Phase Verification

After completing all phases, run the full gate:

```bash
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=short -q
```

All three must pass. Then update:
- `promptaudit.md` header (Last updated, remaining gaps)
- `promptaudit.md` Part 2 matrix:
  - All ❌ Output Ordering cells → ✅ (Phase A)
  - All ⚠️ Authority Loading cells → ✅ (Phase B)
  - Add S9 (`shape-audit`) as a 10th prompt column, inserted between S8 and S10 to maintain stage order — mark all Phase D mandatory sections ✅, PRODUCT_SHAPE Conditioning as N/A, score numerator increases by 11
- `promptingguidelines.md` Per-Stage Compliance table:
  - Same Output Ordering and Authority Loading cell updates
  - Add S9 (`shape-audit`) as a new column, inserted between S8 and S10 to maintain stage order (table currently covers S0, S1, S2, S3, S4, S5, S6, S8, S10 — 9 columns; S9 is absent)
- `PROMPT_STANDARD.md §O1` — add Stage 9 exemption note (Phase D deliverable)
- `promptingguidelines.md §O1` — add Stage 9 exemption note (Phase D deliverable)
- `PROMPT_STANDARD.md` and `promptingguidelines.md` exempt prompts lists — add `audit-process-drift.prompt.md` (Phase E deliverable)

Target compliance score after Phases A–E: **~80+/106 ✅ for existing 9 prompts** (current 62/106, gaining approximately +9 via Phase A, +7 via Phase B, +2 via Phase C = ~80; exact count depends on whether Gap-3 tracks as 1 or 2 cells per affected prompt in the live matrix) **+ 11/11 ✅ for new shape-audit** (new meaningful-cell total ≈91/117 after adding S9 column). Recount from the live matrix after Phase E completes rather than relying on this estimate.

---

## 5. Decision Log Entry Required

When executing Phase B (Gap-3 resolution), record the PROGRAMBUILD_CANONICAL.md vs PROGRAMBUILD.md authority loading decision in `PROGRAMBUILD/DECISION_LOG.md`:

> **Decision**: Both `PROGRAMBUILD_CANONICAL.md §N` and `PROGRAMBUILD.md §N` are required in shaping prompt Authority Loading sections. `PROGRAMBUILD_CANONICAL.md` provides stage boundaries and required output list. `PROGRAMBUILD.md` provides the procedural protocol for how to do the work. Loading only one creates a gap. Loading both ensures the AI derives all protocol from authority docs, not from prompt-hardcoded steps.

**Scope clarification**: This is a PROGRAMSTART *system design* decision about how the template tool itself works — not a product-level project decision. Record it under a dedicated heading such as `## PROGRAMSTART System Design` or tag it with a `[system]` label to prevent confusion with product decisions logged during a live PROGRAMBUILD project run.

---

## 6. Execution Prompt

Implementation of Phases A–E may be done manually or through an execution prompt.

If creating an execution prompt (e.g., `implement-stage4-gameplan.prompt.md`), it should:
1. Be marked as an internal build prompt (exempt from PROMPT_STANDARD)
2. Execute phases in strict sequence (A → B → C → D → E)
3. Run `uv run programstart validate --check all` and `uv run programstart drift` after each phase before proceeding to the next
4. Run the full post-phase gate from Section 4 (`validate --check all` + `drift` + `pytest --tb=short -q`) after completing Phase E, before updating documentation
5. Update `promptaudit.md` and `promptingguidelines.md` compliance tables last (correctness validation takes priority over tracking document updates)

Phases F and G are separate work — do not include in the execution prompt.
