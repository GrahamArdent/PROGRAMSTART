# Stage 5 Gameplan — USERJOURNEY Prompts, Research Validator, Phase Completions

Purpose: Implementation plan for closing the remaining gaps identified in `promptaudit.md` Part 13 after stage4gameplan Phases A-E.
Status: **PENDING — not started**
Authority: Non-canonical working plan derived from `promptaudit.md` (Part 13, remaining open items), `promptingguidelines.md` (What Still Needs Doing), and `automation.md` (Tier 2 CONSIDER findings).
Last updated: 2026-04-13

---

## 1. The Remaining Gaps

Five actionable gaps remain after stage4gameplan. One architectural gap is deferred.

| Gap | Scope | Severity |
|---|---|---|
| Gap-5 | USERJOURNEY has no phase-specific shaping prompts — 22 of 26 files unprotected | HIGH |
| Gap-7 | `shape-research.prompt.md` has undocumented `## Notes` section not in PROMPT_STANDARD | LOW |
| Phase F | Cross-stage validation not invoked by any shaping prompt (❌ across all 10 prompts) | MEDIUM |
| Phase G | `sync_rules` not explicitly cited in Protocol Steps (❌ across all 10 prompts, beyond Output Ordering) | MEDIUM |
| PA-8 | Stage 2 has no content-gate validator (`validate_research_complete()` not yet implemented) | CONSIDER |

**Architectural gap — deferred, not addressed in this gameplan:**

| Gap | Scope | Note |
|---|---|---|
| JIT Step 1 | Protocol Declaration present but file list is hardcoded, not registry-derived via `programstart guide` | Requires runtime registry integration. Deferred until there is a concrete use-case for un-hardcoding the authority file list. |

---

## 2. Phase Sequence

Ordered smallest-first: quick wins before complex new files before broad cross-cutting edits.

| Phase | Gap | Type | Est. edits |
|---|---|---|---|
| Pre-work | — | Record test + validate + drift baseline | 0 edits |
| A | Gap-7 | Edit 1 existing prompt | 1 file edit |
| B | PA-8 | Edit 1 script + add tests + update 1 prompt gate | 1 script edit + ~5 test functions + 1 prompt edit |
| C | Gap-5 | Create 3 new UJ shape prompts + register in process-registry.json | 3 new files + 1 registry edit |
| D (deferred) | Phase F | Edit 10 existing prompts | 10 file edits |
| E (deferred) | Phase G | Edit 10+ existing prompts and supporting docs | 10+ file edits |

Phases D and E are lower priority than A–C. Phases A–C are the core work.

---

## 3. Phases

---

### Pre-work: Record Baseline

Before any edits, confirm the current test and validate baseline.

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 10
uv run programstart validate --check all
uv run programstart drift
```

Expected baseline (post-stage4gameplan): 3 pre-existing failures (`test_drift_check_passes_with_no_violations`, `test_drift_check_system_filter`, `test_main_status_fail_on_due_returns_one`), ~717 passed. Post-phase gate requires no *new* failures — not that the baseline is clean.

---

### Phase A: Fix `shape-research.prompt.md` `## Notes` Anomaly (Gap-7)

**Goal**: Close Gap-7. Remove the undocumented `## Notes` section from `shape-research.prompt.md`. This heading does not appear in PROMPT_STANDARD and creates a discrepancy with the standard.

**Why first**: Single-file, 5-minute edit. Removes a structural discrepancy before creating new prompts that must match the standard exactly.

**What to do**:

1. Read `shape-research.prompt.md` — specifically the `## Notes` section content and the sections immediately surrounding it (`## Verification Gate` and `## Next Steps`).
2. Evaluate the content:
   - If it contains operator guidance relevant to research → merge into the `## Protocol` section as a note or into `## Next Steps` as context.
   - If it is redundant with content elsewhere → delete it.
   - If it is a general reminder about the research process → delete it.
3. Remove the `## Notes` heading. Ensure `## Verification Gate` is immediately followed by `## Next Steps` (or a blank line then `## Next Steps`) with no `## Notes` in between.

**Approach**: One `replace_string_in_file` call. Anchor on `## Verification Gate` … `## Next Steps` block to catch the `## Notes` section between them without accidentally editing other content.

**Verification**:

```powershell
Get-Content .github/prompts/shape-research.prompt.md | Select-String "^## "
```

`## Notes` must not appear. `## Verification Gate` must be followed by `## Next Steps`. Run `uv run programstart validate --check all` and `uv run programstart drift` — both must pass.

**Commit**: `fix(prompts): remove undocumented Notes section from shape-research (Gap-7)`

---

### Phase B: Add `validate_research_complete()` for Stage 2 (PA-8)

**Goal**: Close PA-8 / automation.md Finding 2-A. Stage 2 (`research`) is the only early PROGRAMBUILD stage with a shaping prompt but no content-gate validator. All other stages 0–10 now have `--check <stage>` validators.

**Why CONSIDER promoted to AUTOMATE**: After stage4gameplan, the cross-stage consistency of validators is complete except for Stage 2. The absence is now more visible. The check is lightweight (structural presence, not content quality) and adds a real gate to `shape-research.prompt.md` Verification Gate.

**Validator logic** (in `scripts/programstart_validate.py`):

```python
def validate_research_complete(root: Path) -> list[str]:
    """Check RESEARCH_SUMMARY.md exists and has at least one ## section heading."""
    problems = []
    research_path = root / "PROGRAMBUILD" / "RESEARCH_SUMMARY.md"
    if not research_path.exists():
        problems.append("RESEARCH_SUMMARY.md: file does not exist")
        return problems
    content = research_path.read_text(encoding="utf-8")
    if not re.search(r"^## ", content, re.MULTILINE):
        problems.append(
            "RESEARCH_SUMMARY.md: no ## section headings found "
            "(expected structured research output with at least one section)"
        )
    return problems
```

**Required edits (3 files)**:

1. **`scripts/programstart_validate.py`**: Add `validate_research_complete()`. Wire it into the `--check research-complete` dispatch. Pattern: follow exactly how `validate_risk_spikes()` is structured and dispatched.

2. **`scripts/programstart_workflow_state.py`**: Add `"research-complete"` to `stage_checks` dict for the `research` stage. Pattern: follow how `"risk-spikes"` is wired into `stage_checks` for `architecture_and_risk_spikes`.

3. **`.github/prompts/shape-research.prompt.md`**: Update `## Verification Gate` to add `--check research-complete` alongside the existing drift command.

**Tests** (new file `tests/test_programstart_validate_research.py`):

Write 4 tests following the pattern in `tests/test_programstart_validate_feasibility.py`:
- `test_missing_research_summary_fails` — file does not exist → reports problem
- `test_empty_research_summary_fails` — file exists but has no `## ` headings → reports problem
- `test_valid_research_summary_passes` — file has at least one `## ` heading → no problems
- `test_research_complete_check_via_cli` — `validate --check research-complete` returns zero exit code with a valid file

**Pre-flight**: Read `scripts/programstart_validate.py` around the `validate_risk_spikes()` function and its dispatch entry before writing the new function. Read `scripts/programstart_workflow_state.py` around the `stage_checks` dict before editing it. Confirm `re` is already imported.

**Approach**: Read each file before editing. Make 3 `replace_string_in_file` calls. Create the test file.

**Verification**:

```powershell
uv run programstart validate --check research-complete  # against a project WITH RESEARCH_SUMMARY.md
uv run pytest tests/test_programstart_validate_research.py -v
uv run programstart validate --check all
uv run programstart drift
```

All tests must pass. Validate and drift must pass.

**Commit**: `feat(validate): add validate_research_complete for Stage 2 research gate (PA-8)`

---

### Phase C: Create USERJOURNEY Shaping Prompts (Gap-5)

**Goal**: Close Gap-5. Create the 3 minimum viable USERJOURNEY phase-specific shaping prompts. These provide structured operator guidance for the UJ planning phases that currently have zero prompt coverage beyond `userjourney-next-slice.prompt.md`.

**Why 3 prompts**: They map to the 4 USERJOURNEY `sync_rules` that have no prompt coverage. `userjourney_implementation_sequence` is partially covered by `userjourney-next-slice.prompt.md`. The other 4 sync_rules map to 3 prompt clusters (legal drafts consolidate 2 sync_rules).

**USERJOURNEY sync_rule → prompt mapping**:

| sync_rule | Authority files | Prompt |
|---|---|---|
| `userjourney_route_state_logic` | `DECISION_LOG.md`, `ROUTE_AND_STATE_FREEZE.md`, `STATES_AND_RULES.md` | `shape-uj-decision-freeze.prompt.md` |
| `userjourney_legal_consent_behavior` | `DECISION_LOG.md`, `LEGAL_AND_CONSENT.md` | `shape-uj-legal-drafts.prompt.md` |
| `userjourney_external_review_packet` | `OPEN_QUESTIONS.md`, `LEGAL_REVIEW_NOTES.md`, `LEGAL_AND_CONSENT.md` | `shape-uj-legal-drafts.prompt.md` (same prompt — both legal sync_rules handled together) |
| `userjourney_ux_surfaces_copy` | `SCREEN_INVENTORY.md`, `USER_FLOWS.md`, `UX_COPY_DRAFT.md` | `shape-uj-ux-surfaces.prompt.md` |

**Files protected by each prompt**:

| Prompt | Files it guides the operator through | workflow_guidance phase |
|---|---|---|
| `shape-uj-decision-freeze.prompt.md` | DECISION_LOG.md, ROUTE_AND_STATE_FREEZE.md, STATES_AND_RULES.md + dependents: USER_FLOWS.md, SCREEN_INVENTORY.md | phase_0 and phase_3 |
| `shape-uj-legal-drafts.prompt.md` | LEGAL_AND_CONSENT.md, OPEN_QUESTIONS.md, LEGAL_REVIEW_NOTES.md + dependents: TERMS_OF_SERVICE_DRAFT.md, PRIVACY_POLICY_DRAFT.md, EXTERNAL_REVIEW_PACKET.md, ACCEPTANCE_CRITERIA.md | phase_1 |
| `shape-uj-ux-surfaces.prompt.md` | SCREEN_INVENTORY.md, USER_FLOWS.md, UX_COPY_DRAFT.md + dependents: ACCEPTANCE_CRITERIA.md, ANALYTICS_AND_OUTCOMES.md | phase_2 |

**PROMPT_STANDARD conformance**: All 3 prompts MUST follow PROMPT_STANDARD. All 10 mandatory `##` sections in order. They are operator-facing prompts, not utility or internal-build — no exemption applies.

**Protocol Declaration authority**: Cite `USERJOURNEY/DELIVERY_GAMEPLAN.md` as the authority section (it is the canonical cross-document execution guide for USERJOURNEY, per its own metadata: "Authority: Canonical cross-document execution and sync guide for USERJOURNEY").

**Verification Gate per prompt**: No dedicated `--check uj-*` command exists yet. Use `uv run programstart validate --check authority-sync` (validates cross-system sync_rule compliance) + `uv run programstart drift`. This is consistent with how UJ drift is currently gated.

**Output Ordering section per prompt**: Each prompt MUST cite the relevant `sync_rules` in its `## Output Ordering` section, with authority-before-dependent write order.

---

#### Prompt 1: `shape-uj-decision-freeze.prompt.md`

**Purpose**: Guide the operator through freezing product decisions and locking the route and state model. This is the first major USERJOURNEY planning milestone — decisions recorded in DECISION_LOG.md drive everything downstream.

**YAML frontmatter**:
```yaml
---
description: "Freeze product decisions, lock route/state model, synchronize DECISION_LOG → ROUTE_AND_STATE_FREEZE → STATES_AND_RULES. Use at USERJOURNEY Phase 0/3."
name: "UJ Decision Freeze"
argument-hint: "Phase to freeze: decisions, route model, or both"
agent: "agent"
---
```

**Authority Loading** files to load:
1. `USERJOURNEY/DELIVERY_GAMEPLAN.md` — canonical UJ execution guide (the Protocol Declaration authority)
2. `USERJOURNEY/DECISION_LOG.md` — resolved product and route decisions
3. `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` — frozen route and state structure
4. `USERJOURNEY/STATES_AND_RULES.md` — lifecycle state semantics

**Output Ordering** (per `userjourney_route_state_logic` sync_rule):
1. `USERJOURNEY/DECISION_LOG.md` — first: record the decision to freeze
2. `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` — second: express the frozen state in route terms
3. `USERJOURNEY/STATES_AND_RULES.md` — third: align lifecycle semantics
4. `USERJOURNEY/USER_FLOWS.md`, `USERJOURNEY/SCREEN_INVENTORY.md` — last: update dependents

**Kill Criteria Re-check**: Not directly applicable (no PROGRAMBUILD FEASIBILITY.md). Instead: re-read `USERJOURNEY/OPEN_QUESTIONS.md` before starting. If any engineering blocker is listed that affects routing or state decisions, STOP and flag it.

**Protocol steps** (derive from DELIVERY_GAMEPLAN.md Source Of Truth Matrix "resolved defaults" and "route structure and state boundaries" rows):
1. Read DELIVERY_GAMEPLAN.md Source Of Truth Matrix for "resolved defaults and product decisions" and "route structure and state boundaries" concerns.
2. For each unresolved item in OPEN_QUESTIONS.md that has been resolved externally, record the decision in DECISION_LOG.md first.
3. Verify ROUTE_AND_STATE_FREEZE.md reflects DECISION_LOG.md. Update if inconsistent.
4. Verify STATES_AND_RULES.md lifecycle semantics are consistent with ROUTE_AND_STATE_FREEZE.md.
5. Update `first_value_achieved` definition if any state changes affect the activation event.

**Verification Gate**: `uv run programstart validate --check authority-sync` + `uv run programstart drift`

---

#### Prompt 2: `shape-uj-legal-drafts.prompt.md`

**Purpose**: Guide the operator through drafting and reviewing legal documents — Terms of Service, Privacy Policy, consent flows, and the external review packet. This prompt covers both the `userjourney_legal_consent_behavior` and `userjourney_external_review_packet` sync_rules.

**YAML frontmatter**:
```yaml
---
description: "Draft legal documents (ToS, Privacy Policy, consent flows) and external review packet. Enforces authority-before-dependent write order. Use at USERJOURNEY Phase 1."
name: "UJ Legal Drafts"
argument-hint: "Which legal area to address: all, terms-of-service, privacy-policy, consent-flows, or external-review-packet"
agent: "agent"
---
```

**Authority Loading** files to load:
1. `USERJOURNEY/DELIVERY_GAMEPLAN.md` — canonical UJ execution guide
2. `USERJOURNEY/LEGAL_AND_CONSENT.md` — legal consent authority
3. `USERJOURNEY/OPEN_QUESTIONS.md` — unresolved legal/operational items
4. `USERJOURNEY/LEGAL_REVIEW_NOTES.md` — external review notes
5. `USERJOURNEY/DECISION_LOG.md` — resolved legal decisions

**Output Ordering** (per `userjourney_external_review_packet` and `userjourney_legal_consent_behavior` sync_rules):
1. `USERJOURNEY/LEGAL_AND_CONSENT.md` — first: update or confirm consent authority
2. `USERJOURNEY/LEGAL_REVIEW_NOTES.md` — second: record any new review notes
3. `USERJOURNEY/TERMS_OF_SERVICE_DRAFT.md` — third: derive from consent authority
4. `USERJOURNEY/PRIVACY_POLICY_DRAFT.md` — fourth: derive from consent authority
5. `USERJOURNEY/EXTERNAL_REVIEW_PACKET.md` — last: compile a summary of all drafts for external reviewers
6. `USERJOURNEY/UX_COPY_DRAFT.md`, `USERJOURNEY/ACCEPTANCE_CRITERIA.md` — update only if consent behavior changed

**Critical constraint**: **Do not invent legal text that is not traceable to a decision in DECISION_LOG.md or a note in LEGAL_REVIEW_NOTES.md.** Any legal assertion must be authorized. See DELIVERY_GAMEPLAN.md: "Do not let implementation invent legal text that is not reflected in these docs."

**Kill Criteria Re-check**: Re-read `OPEN_QUESTIONS.md`. If any item is an engineering or legal blocker that is not yet resolved, STOP and flag it. Do not draft around an unresolved blocker.

**Protocol steps** (derive from DELIVERY_GAMEPLAN.md Step 1 "Close Remaining External Decisions"):
1. Read DELIVERY_GAMEPLAN.md Step 1 and the Source Of Truth Matrix "legal and consent requirements" row.
2. Identify which OPEN_QUESTIONS.md items are legal or operational. For each resolved item, record the decision in DECISION_LOG.md.
3. Update LEGAL_AND_CONSENT.md to reflect the resolved decisions.
4. Derive TERMS_OF_SERVICE_DRAFT.md content from LEGAL_AND_CONSENT.md (not from external examples).
5. Derive PRIVACY_POLICY_DRAFT.md content from LEGAL_AND_CONSENT.md.
6. Update LEGAL_REVIEW_NOTES.md with any open review items.
7. Compile EXTERNAL_REVIEW_PACKET.md as a summary of: governing law decision, liability approach, retention policy, support contact path, and any items still requiring external sign-off.

**Verification Gate**: `uv run programstart validate --check authority-sync` + `uv run programstart drift`

---

#### Prompt 3: `shape-uj-ux-surfaces.prompt.md`

**Purpose**: Guide the operator through designing and syncing UX screens, user flows, and copy. Covers the `userjourney_ux_surfaces_copy` sync_rule.

**YAML frontmatter**:
```yaml
---
description: "Design screens, user flows, and UX copy. Enforces SCREEN_INVENTORY → USER_FLOWS → UX_COPY → ACCEPTANCE_CRITERIA write order. Use at USERJOURNEY Phase 2."
name: "UJ UX Surfaces"
argument-hint: "Which UX concern: all, screen-inventory, user-flows, ux-copy, or acceptance-criteria"
agent: "agent"
---
```

**Authority Loading** files to load:
1. `USERJOURNEY/DELIVERY_GAMEPLAN.md` — canonical UJ execution guide
2. `USERJOURNEY/SCREEN_INVENTORY.md` — surface inventory (authority)
3. `USERJOURNEY/USER_FLOWS.md` — flow definition (authority)
4. `USERJOURNEY/UX_COPY_DRAFT.md` — copy drafts (authority)
5. `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` — route constraints (read-only, do not modify)
6. `USERJOURNEY/DECISION_LOG.md` — resolved design decisions

**Output Ordering** (per `userjourney_ux_surfaces_copy` sync_rule):
1. `USERJOURNEY/SCREEN_INVENTORY.md` — first: define or update surfaces
2. `USERJOURNEY/USER_FLOWS.md` — second: derive or update user flows from surfaces
3. `USERJOURNEY/UX_COPY_DRAFT.md` — third: write copy for surfaces defined in inventory
4. `USERJOURNEY/ACCEPTANCE_CRITERIA.md` — fourth: derive acceptance criteria from flows + copy
5. `USERJOURNEY/ANALYTICS_AND_OUTCOMES.md` — last: update outcome metrics if surfaces changed

**Route boundary**: Do not modify `ROUTE_AND_STATE_FREEZE.md` or `STATES_AND_RULES.md` during this phase. UX surface design operates within the frozen route model. If a surface design requires a route change, STOP and run `shape-uj-decision-freeze.prompt.md` first.

**Kill Criteria Re-check**: Re-read `USERJOURNEY/DECISION_LOG.md` entries for any UX or consent decisions that constrain surface design. If a surface conflicts with a frozen decision, STOP and flag it.

**Protocol steps** (derive from DELIVERY_GAMEPLAN.md Source Of Truth Matrix "UX surfaces and copy" row):
1. Read DELIVERY_GAMEPLAN.md Source Of Truth Matrix "UX surfaces and copy" concern.
2. List all user-facing screens implied by `ROUTE_AND_STATE_FREEZE.md` and `USER_FLOWS.md`. Update SCREEN_INVENTORY.md if surfaces are missing or renamed.
3. Verify USER_FLOWS.md entry/exit conditions are consistent with SCREEN_INVENTORY.md surface list.
4. Write or update UX copy for each surface in SCREEN_INVENTORY.md into UX_COPY_DRAFT.md.
5. Derive or update ACCEPTANCE_CRITERIA.md from the flows and copy — each criterion must trace to a specific surface and a specific user goal.
6. If activation event (`first_value_achieved`) is affected by surface changes, flag it and update ANALYTICS_AND_OUTCOMES.md.

**Verification Gate**: `uv run programstart validate --check authority-sync` + `uv run programstart drift`

---

#### Supporting edits for Phase C

**Edit 1: `config/process-registry.json` — add to `workflow_guidance.userjourney` phases and `bootstrap_assets`**

Add each new prompt to the appropriate `workflow_guidance.userjourney` phase `prompts` array:
- `shape-uj-decision-freeze.prompt.md` → `phase_0.prompts` AND `phase_3.prompts`
- `shape-uj-legal-drafts.prompt.md` → `phase_1.prompts`
- `shape-uj-ux-surfaces.prompt.md` → `phase_2.prompts`

Add all 3 new prompts to `bootstrap_assets` array (after `shape-audit.prompt.md`).

**After bootstrap_assets edit**: Run `uv run programstart refresh --date $(Get-Date -Format yyyy-MM-dd)` to regenerate the manifest.

**Edit 2: `PROMPT_STANDARD.md` — no change needed**

UJ shaping prompts are operator-facing and not exempt. No exempt list update required.

**Approach**: Create all 3 prompt files first (one `create_file` per prompt). Then make a single `multi_replace_string_in_file` call for the registry edits. Then run `programstart refresh`.

**Verification**:

```powershell
Get-ChildItem .github/prompts/shape-uj-*.prompt.md  # → 3 files
Get-Content .github/prompts/shape-uj-decision-freeze.prompt.md | Select-String "^## "  # → 10 headings
uv run programstart validate --check bootstrap-assets
uv run programstart validate --check all
uv run programstart drift
```

**Commit**: `feat(prompts): create 3 USERJOURNEY shaping prompts for decision-freeze, legal-drafts, ux-surfaces (Gap-5)`

---

### Phase D (Deferred): Add Cross-Stage Validation Invocation to All 10 Prompts

**Goal**: Close Phase F. All 10 shaping prompts should reference `programstart-cross-stage-validation.prompt.md` in their `## Kill Criteria Re-check` (or `## Upstream Verification`) section so operators know to invoke it.

**Why deferred**: Cross-stage validation is advisory, not blocking. Operators can already discover `programstart-cross-stage-validation` via `programstart guide`. The change is mechanical but low reward until there is a documented case of a contradiction that cross-stage validation would have caught.

**When to un-defer**: When a downstream stage finds a contradiction with an upstream authority doc that cross-stage validation would have caught. At that point, add a one-liner to each prompt's Kill Criteria Re-check section: "Run `programstart-cross-stage-validation.prompt.md` to verify no upstream contradictions."

**Scope when executed**: 10 `replace_string_in_file` calls, one per shaping prompt.

---

### Phase E (Deferred): Explicitly Cite `sync_rules` in Protocol Steps

**Goal**: Close Phase G. Protocol steps across all 10+ prompts should explicitly name the `sync_rule` that governs write ordering (e.g., "This write order follows `programbuild_architecture_contracts` in `config/process-registry.json`").

**Why deferred**: Output Ordering sections (added in stage4gameplan Phase A) already cite sync_rules for write ordering. The additional citation within Protocol Steps is a "make the implicit explicit" improvement with limited practical impact today.

**When to un-defer**: When an operator questions why a particular write order is required and the Output Ordering section is not sufficient to explain it.

---

## 4. Documentation Updates (Post Phases A–C)

After Phases A–C are executed, update:

1. **`promptaudit.md`**:
   - Part 2 matrix: Add `shape-uj-*` row or add UJ section to matrix with 3 new prompts
   - Part 13: Mark Gap-7 **CLOSED**, Gap-5 **CLOSED**, add PA-8 **CLOSED**
   - Recommended Fix Order: Mark items 12 (Gap-5) and 13 (PA-8) as ✅
   - PA-8 finding row: Update status to ✅ RESOLVED
   - Header: Update "Last updated" + description

2. **`promptingguidelines.md`**:
   - What Still Needs Doing: Mark Gap-5 and PA-8 closed; update Remaining Open list

3. **`stage5gameplan.md`** (this file): Update Status to `COMPLETE — Phases A–C executed [date]`

---

## 5. Gate

After every phase:

```powershell
uv run programstart validate --check all
uv run programstart drift
```

After Phase C:

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 5
```

Expected: No new test failures vs pre-work baseline. New tests from Phase B (`test_programstart_validate_research.py`) must all pass.
