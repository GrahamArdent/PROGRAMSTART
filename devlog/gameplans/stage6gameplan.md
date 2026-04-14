# Stage 6 Gameplan — Final Automation Closure

Purpose: Close all remaining automatable gaps from `automation.md` and the deferred phases of `stage5gameplan.md`. After these phases, the PROGRAMSTART automation system is at maximum achievable coverage given its current architecture.
Status: **COMPLETE — Phases A–E executed 2026-04-13**
Authority: Non-canonical working plan derived from `automation.md` (open AUTOMATE/CONSIDER findings), `promptaudit.md` (Part 2 ❌ matrix cells, remaining UNRESOLVED findings), and stage5gameplan.md (deferred Phases D and E).
Last updated: 2026-04-13

---

## 1. Current State and What "Full Automation" Means

After stage5gameplan Phases A–C, the system has:

- ✅ All 11 PROGRAMBUILD stage gates implemented (`validate --check <stage>` for every stage)
- ✅ All 10 shaping prompts PROMPT_STANDARD-compliant (all 10 mandatory `##` sections)
- ✅ All shaping prompts discoverable via `programstart guide`
- ✅ DECISION_LOG enforcement wired into validators at Stages 0, 1, 3, 4
- ✅ 3 USERJOURNEY shaping prompts created (Gap-5 closed)
- ✅ `validate_research_complete()` implemented (PA-8 closed)

**"Full automation"** means: every stage gate catches what it should, every prompt invokes all required checks, and every auto-wired mechanism fires when it should. It does not mean replacing human protocol steps with scripts — it means the script layer has no gaps relative to what the authority docs require.

Three architectural limits are accepted as permanent and excluded from this gameplan:

| Limit | Why accepted |
|---|---|
| JIT Step 1 is hardcoded file loading, not registry-derived | Requires runtime registry integration with no concrete use-case to drive the change |
| Instruction files don't inject into prompt execution (`applyTo` limitation) | VS Code architectural constraint; `PROMPT_STANDARD.md` is the prompt-level equivalent |
| `step_files` vs. `guidance.files` divergence (PA-12) | Intentional — `step_files` tracks primary deliverables only |

---

## 2. Remaining Gaps

Confirmed by code inspection on 2026-04-13.

### Confirmed OPEN (from `scripts/programstart_validate.py` and `scripts/programstart_workflow_state.py`)

| ID | Gap | Severity | Source |
|---|---|---|---|
| **4-A** | No `validate_risk_spike_resolution()` — RISK_SPIKES.md rows with Status = "open" or "in-progress" silently pass the existing `risk-spikes` gate | HIGH | automation.md Finding 4-A |
| **UJ-C** | `validate_engineering_ready()` exists but never runs — `enforce_engineering_ready_in_all` is false, no UJ phase content gate in `preflight_problems()` | AUTOMATE | automation.md Finding UJ-C |

### Deferred from stage5gameplan (confirmed ❌ in Part 2 matrix)

| ID | Gap | Severity | Source |
|---|---|---|---|
| **PA-14** | Cross-stage validation not invoked by any of the 10 shaping prompts — currently PARTIALLY RESOLVED (prompt registered in `cross_cutting_prompts`; not yet referenced inside individual prompts) | MEDIUM | `promptaudit.md` PA-14, `promptingguidelines.md` Phase F |
| **Phase G** | `sync_rules` not explicitly named in Protocol Steps (beyond Output Ordering) | MEDIUM | `promptingguidelines.md` item 9 / Phase G, Part 2 matrix ❌ row "`sync_rules` explicitly cited" |

### CONSIDER items — promoted to DO for completeness

| ID | Gap | Impact | Source |
|---|---|---|---|
| **0-A** | No PRODUCT_SHAPE whitelist — any string silently passes `intake-complete` | Low today, breaks PRODUCT_SHAPE-conditional logic downstream | automation.md Finding 0-A |
| **3-C** | No USER_FLOWS.md section structure check — stub with requirement IDs passes | Low today; Section header check catches unfilled stubs | automation.md Finding 3-C |
| **6-C** | `test-coverage` name misleads — counts `tests/test_*.py` files, not TEST_STRATEGY.md coverage | Low; naming causes confusion | automation.md Finding 6-C |

### Confirmed RESOLVED (not in any phase below)

The following automation.md AUTOMATE verdicts were confirmed resolved by code inspection:

| Finding | What was done |
|---|---|
| 0-C | `_check_decision_log_entries("inputs_and_mode_selection")` in `validate_intake_complete()` |
| 1-A | `_check_decision_log_entries("feasibility_and_kill_criteria")` in `validate_feasibility_criteria()` |
| 3-A | Substring bug fixed: `re.search(rf"\b{re.escape(req_id)}\b", flow_text)` |
| 4-B | `_check_decision_log_entries("architecture_and_contracts")` in `validate_architecture_contracts()` |
| 7-A | `validate_implementation_entry_criteria()` wired at Stage 7 |
| 7-B | Implementation prompts wired into `implementation_loop.prompts` in registry |
| UJ-A | 3 USERJOURNEY shaping prompts created: `shape-uj-decision-freeze.prompt.md`, `shape-uj-legal-drafts.prompt.md`, `shape-uj-ux-surfaces.prompt.md` (stage5gameplan Phase C) |

The following were also resolved before this gameplan:
PA-1 through PA-8, PA-16. PA-9 (5 of 5 UJ sync_rules with zero enforcement) and PA-10 (10 UJ authority/dependent files with zero coverage) are substantially improved by stage5gameplan Gap-5 (3 UJ prompts now cover the 4 UJ sync_rules most material to solo-operator flow), but `promptaudit.md` still shows them UNRESOLVED — corrected in post-phase docs.

---

## 3. Phase Sequence

| Phase | Gap(s) | Type | Est. edits |
|---|---|---|---|
| Pre-work | — | Record baseline | 0 edits |
| A | 4-A | New validator function + tests + dispatch + stage_checks + implementation-entry wire + prompt gate | 4 script edits (3 in validate.py, 1 in workflow_state.py) + 5 tests + 1 prompt edit |
| B | UJ-C | UJ phase_0 content gate + dispatch extension + tests | 2 script edits + 3 tests |
| C | PA-14 | Add cross-stage validation call to 10 PB prompts + 3 UJ prompts | 13 prompt edits |
| D | Phase G | Add explicit `sync_rules` name to Protocol Steps of 10 prompts | 10 prompt edits |
| E | 0-A, 3-C, 6-C | Validator polish — 3 targeted additions/renames | 2 script edits (validate.py) |
| Docs | — | Update automation.md, promptaudit.md, promptingguidelines.md | 3 doc edits |

Phases A and B first (validators, highest value). C and D next (prompt layer, mechanical but broad). E last (polish).

---

## 4. Phases

---

### Pre-work: Record Baseline

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 10
uv run programstart validate --check all
uv run programstart drift
```

Expected: 3 pre-existing failures, ~721+ passed (includes 4 new research tests). Validate ✅, drift ✅.

---

### Phase A: `validate_risk_spike_resolution()` — Stage 4 Spike Resolution Gate (Finding 4-A)

**Goal**: Close Finding 4-A. The current `risk-spikes` gate validates RISK_SPIKES.md structure (table headers, non-empty method + pass-criteria per row). It does not check whether spikes have been resolved. An operator can advance from Stage 4 to Stage 5 with every spike in Status = "open". PROGRAMBUILD.md §11 and entry_criteria[0] both require all spikes resolved or deferred-with-decision before implementation.

**Why now**: It is the last confirmed-open AUTOMATE verdict in `automation.md`. It is also the most impactful remaining gap — unresolved spikes are the primary cause of assumption rot at implementation.

**Validator logic**:

Note on column names: RISK_SPIKES.md template has **both** a `Result` column (pass/fail from running the spike) and a `Decision` column (architectural decision: resolved/deferred/accepted). `parse_markdown_table()` returns a dict with both as keys, so `row.get("Result", fallback)` returns `row["Result"]` even when empty — the fallback is never reached. Use `or`-chaining instead. Also, an empty `Result` means the spike has not been run, which is an unresolved state and must be flagged.

```python
def validate_risk_spike_resolution(_registry: dict) -> list[str]:
    """Check all RISK_SPIKES.md rows have a resolved/deferred/accepted status."""
    problems: list[str] = []
    spikes_path = workspace_path("PROGRAMBUILD/RISK_SPIKES.md")
    if not spikes_path.exists():
        return problems  # file-existence is checked by validate_risk_spikes; no duplication
    rows = parse_markdown_table(spikes_path.read_text(encoding="utf-8"), "Spike Register")
    real_rows = [r for r in rows if r.get("Spike", "").strip() and r.get("Spike", "").strip() not in ("", "spike")]
    if not real_rows:
        return problems  # empty table handled by validate_risk_spikes
    RESOLVED_VALUES = {"resolved", "deferred", "accepted", "pass", "done", "closed"}
    for row in real_rows:
        # Use or-chaining: Result column exists but may be empty; fall through to Decision/Status
        result = (row.get("Result") or row.get("Decision") or row.get("Status", "")).strip().lower()
        if not result or (result not in RESOLVED_VALUES and not any(v in result for v in RESOLVED_VALUES)):
            spike_id = row.get("Spike", "unknown").strip()
            problems.append(
                f"RISK_SPIKES.md: spike '{spike_id}' has unresolved status '{result or 'empty'}' "
                "(expected one of: resolved, deferred, accepted, or equivalent)"
            )
    return problems
```

**Required edits (4 files)**:

1. **`scripts/programstart_validate.py`** — 3 changes in one file:
   - Add `validate_risk_spike_resolution()` after `validate_risk_spikes()`.
   - Add `"risk-spikes-resolved": validate_risk_spike_resolution` to dispatch dict (after `"risk-spikes"` line).
   - In `validate_implementation_entry_criteria()`, add `problems.extend(validate_risk_spike_resolution(registry))` after the existing `validate_risk_spikes(registry)` call. Automation.md Finding 7-A explicitly requires this: the implementation-entry delegate must include spike resolution, not just spike structure.

2. **`scripts/programstart_workflow_state.py`**:
   - Add `"risk-spikes-resolved"` to the architecture stage list: change from `["architecture-contracts", "risk-spikes"]` to `["architecture-contracts", "risk-spikes", "risk-spikes-resolved"]`.

3. **`.github/prompts/shape-architecture.prompt.md`** — `## Verification Gate` section:
   - Add `uv run programstart validate --check risk-spikes-resolved` to the gate bash block.

**Tests** (new file `tests/test_programstart_validate_risk_spike_resolution.py`):

4 tests using the fixture pattern from `test_programstart_validate_risk_spikes.py`:
- `test_missing_file_passes` — file absent → no problems (existence check is already in risk-spikes gate)
- `test_no_real_rows_passes` — header-only table (template placeholder row) → no problems
- `test_all_resolved_passes` — every row has Result = "Pass" → no problems
- `test_empty_result_fails` — row with both Result and Decision columns empty → reports problem (spike has not been run)
- `test_open_spike_fails` — row with Result = "Pending" → reports problem with spike ID

Note: That is 5 tests, not 4. Add `test_empty_result_fails` specifically to cover the `or`-chaining fix.

**Pre-flight**: Read `validate_risk_spikes()` function and its dispatch entry before writing the new function. Read `test_programstart_validate_risk_spikes.py` fixture pattern. Check `parse_markdown_table()` column-name handling — the Result/Decision/Status column may vary by project, so check the broadest set of column names.

**Verification**:

```powershell
uv run pytest tests/test_programstart_validate_risk_spike_resolution.py -v
uv run programstart validate --check all
uv run programstart drift
```

**Commit**: `feat(validate): add validate_risk_spike_resolution for Stage 4 spike resolution gate (Finding 4-A)`

---

### Phase B: Wire USERJOURNEY Phase 0 Content Gate (Finding UJ-C)

**Goal**: Close Finding UJ-C. `validate_engineering_ready()` exists at `validate.py:767` and is fully tested. It checks `OPEN_QUESTIONS.md` for unresolved items under "Remaining Operational And Legal Decisions". It is never called because `enforce_engineering_ready_in_all` is false and the `preflight_problems()` stage-gate block is PROGRAMBUILD-only. Wire it into USERJOURNEY `phase_0` advance specifically — not `--check all`.

**Why phase_0 only**: Phase 0 is "resolve all open questions and freeze decisions." That is exactly what `validate_engineering_ready()` checks. Running it at all UJ phases would produce spurious failures at phases where open questions are expected.

**Required edits (2 files)**:

1. **`scripts/programstart_workflow_state.py`** — add a USERJOURNEY content-gate block immediately after the programbuild block:

```python
    # --- Stage-gate content checks (userjourney only) ---
    if system == "userjourney" and active_step:
        uj_phase_checks: dict[str, str] = {
            "phase_0": "engineering-ready",
        }
        check_name = uj_phase_checks.get(active_step)
        if check_name:
            problems.extend(programstart_validate.run_stage_gate_check(registry, check_name))
```

2. **`scripts/programstart_validate.py`** — add `"engineering-ready"` to the dispatch dict:

```python
"engineering-ready": validate_engineering_ready,
```

(after `"audit-complete": validate_audit_complete`)

**Tests** (new file `tests/test_programstart_uj_phase0_gate.py` or extend existing UJ validate tests):

3 tests:
- `test_uj_phase0_advance_blocked_on_unresolved_questions` — preflight returns problem when OPEN_QUESTIONS has unresolved items at UJ phase_0
- `test_uj_phase0_advance_passes_on_resolved_questions` — no problems when questions all resolved
- `test_uj_non_phase0_advance_not_checked` — preflight at phase_1 does not run engineering-ready gate

**Pre-flight**: Read `validate_engineering_ready()` at `validate.py:767` — understand what it checks exactly. Read `programstart_workflow_state.py` lines 133–160 to understand where to insert the new block. Check how existing UJ advance tests work.

**Verification**:

```powershell
uv run pytest tests/test_programstart_uj_phase0_gate.py -v
uv run programstart validate --check all
uv run programstart drift
```

**Commit**: `feat(validate): wire engineering-ready gate into USERJOURNEY phase_0 advance (Finding UJ-C)`

---

### Phase C: Cross-Stage Validation Reference in All Shaping Prompts (PA-14)

**Goal**: Close PA-14. All 10 PROGRAMBUILD shaping prompts and 3 USERJOURNEY shaping prompts should reference `programstart-cross-stage-validation.prompt.md` in their Kill Criteria Re-check (or equivalent) section. This is the last ❌ cell in the Part 2 protocol compliance matrix that has a practical fix. After Phase C, the matrix is at ~107/117 — the only remaining ❌ cells are the architectural `sync_rules explicitly cited` (Phase D) and JIT Step 1 (deferred).

**What to add**: A one-liner in the `## Kill Criteria Re-check` section of each prompt:

```markdown
For cross-stage consistency, also run `programstart-cross-stage-validation.prompt.md` to verify upstream stages have not drifted relative to this stage's inputs.
```

For USERJOURNEY prompts (which don't have `## Kill Criteria Re-check` by that name, but have equivalent "re-read" instructions in their Kill Criteria Re-check section): add the same line.

**Why a one-liner**: The cross-stage validation prompt is advisory. Making it required would over-engineer — it's a "also run" suggestion, not a "you MUST run" gate. The addition closes the ❌ cell in the matrix without adding spurious gates.

**Scope**: 10 PROGRAMBUILD shaping prompts + 3 USERJOURNEY shaping prompts = 13 file edits.

**PB prompts** (Kill Criteria Re-check section):
`shape-idea.prompt.md`, `shape-feasibility.prompt.md`, `shape-research.prompt.md`, `shape-requirements.prompt.md`, `shape-architecture.prompt.md`, `shape-scaffold.prompt.md`, `shape-test-strategy.prompt.md`, `shape-release-readiness.prompt.md`, `shape-audit.prompt.md`, `shape-post-launch-review.prompt.md`

Note: `shape-idea` and `shape-post-launch-review` may not have a Kill Criteria section (Stage 0 creates criteria; Stage 10 is post-launch). For those, add a single-sentence cross-stage validation call in `## Next Steps` instead.

**UJ prompts** (Kill Criteria Re-check equivalent section):
`shape-uj-decision-freeze.prompt.md`, `shape-uj-legal-drafts.prompt.md`, `shape-uj-ux-surfaces.prompt.md`

**Approach**: Read each file before editing. Use `multi_replace_string_in_file` in batches of 4–5 prompts to avoid long serial chains. Anchor on the last sentence of the Kill Criteria Re-check section (or the first line of the next `##` heading) to avoid ambiguity.

**Verification**:

```powershell
Get-ChildItem .github/prompts/shape-*.prompt.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch "cross-stage-validation") {
        Write-Host "MISSING: $($_.Name)"
    }
}
uv run programstart validate --check all
uv run programstart drift
```

No `MISSING:` output should appear.

**Commit**: `feat(prompts): add cross-stage validation reference to all 13 shaping prompts (PA-14)`

---

### Phase D: Explicit `sync_rules` Citation in Protocol Steps (Phase G / Part 2 matrix row)

**Goal**: Close the Part 2 protocol compliance matrix ❌ row "`sync_rules` explicitly cited" across all 10 shaping prompts (`promptingguidelines.md` item 9, deferred as Phase G). **Note**: This is not PA-15. Actual PA-15 in `promptaudit.md` is "Validation error messages don't reference prompts or PROGRAMBUILD.md sections" (PARTIALLY RESOLVED, Phase I) — leave as-is; validator error message quality is a separate lower-priority concern. Currently, `## Output Ordering` already cites the rule name (e.g., "per `config/process-registry.json` `sync_rules` (`programbuild_feasibility_cascade`)"). But the `## Protocol` Steps don't name the rule — they describe the steps without saying which sync_rule the ordering follows.

**What to add**: In each prompt's `## Protocol` section, at the step where authority files are written (typically near the end of the protocol), add a reference. Example for shape-feasibility:

> **Ordering note**: This write order follows `sync_rule: programbuild_feasibility_cascade` in `config/process-registry.json`. FEASIBILITY.md is the authority file; DECISION_LOG.md, RESEARCH_SUMMARY.md, and REQUIREMENTS.md are dependents. Do not update a dependent before its authority file is complete.

**Why**: Makes the implicit explicit. When a future editor sees why step 3 comes before step 4, they can trace it to the registry rather than guessing. Reduces maintenance drift risk when PROGRAMBUILD.md rules are updated.

**Scope**: 10 PROGRAMBUILD shaping prompts. 1–2 sentence addition per prompt.

**Sync_rule by prompt** (verified against `config/process-registry.json`):

| Prompt | Stage | sync_rule |
|---|---|---|
| shape-idea | S0 | `programbuild_control_inventory` (kickoff packet → file index) |
| shape-feasibility | S1 | `programbuild_feasibility_cascade` (FEASIBILITY.md is authority; DECISION_LOG.md, RESEARCH_SUMMARY.md, REQUIREMENTS.md, RISK_SPIKES.md are dependents) |
| shape-research | S2 | `programbuild_feasibility_cascade` (FEASIBILITY.md is authority; RESEARCH_SUMMARY.md is a dependent — write FEASIBILITY.md before RESEARCH_SUMMARY.md, even at Stage 2 where RESEARCH_SUMMARY.md is the primary output) |
| shape-requirements | S3 | `programbuild_requirements_scope` (REQUIREMENTS.md is authority; USER_FLOWS.md, ARCHITECTURE.md, TEST_STRATEGY.md are dependents) |
| shape-architecture | S4 | `programbuild_architecture_contracts` (ARCHITECTURE.md is authority; TEST_STRATEGY.md, RELEASE_READINESS.md, RISK_SPIKES.md are dependents) |
| shape-scaffold | S5 | `programbuild_architecture_contracts` (scaffold reads ARCHITECTURE.md as authority; RISK_SPIKES.md is also a dependent of the same rule) |
| shape-test-strategy | S6 | `requirements_test_alignment` + `programbuild_architecture_contracts` (TEST_STRATEGY.md depends on both REQUIREMENTS.md and ARCHITECTURE.md) |
| shape-release-readiness | S8 | `programbuild_architecture_contracts` (RELEASE_READINESS.md is an explicit dependent of ARCHITECTURE.md in the registry) |
| shape-audit | S9 | `programbuild_control_inventory` (AUDIT_REPORT.md reviews all outputs against PROGRAMBUILD_CANONICAL.md + PROGRAMBUILD_FILE_INDEX.md) |
| shape-post-launch-review | S10 | No write-ordering sync_rule applies — POST_LAUNCH_REVIEW.md is a terminal output with no dependents. Cite `programbuild_feasibility_cascade` as the source of success metrics read during review, but make clear no write ordering is enforced. |

**Approach**: Read each prompt's `## Protocol` section before editing. Add the ordering note at the step immediately before writing begins (typically after "Load context" steps). Use `multi_replace_string_in_file` in batches.

**Verification**:

```powershell
Get-ChildItem .github/prompts/shape-[a-z]*.prompt.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch "sync_rule") {
        Write-Host "MISSING: $($_.Name)"
    }
}
uv run programstart validate --check all
uv run programstart drift
```

**Commit**: `feat(prompts): add explicit sync_rules citation to Protocol Steps of all 10 shaping prompts (PA-15)`

---

### Phase E: Validator Polish — CONSIDER Items (Findings 0-A, 3-C, 6-C)

**Goal**: Close the remaining CONSIDER items that have a clear, low-risk fix. These are mechanical improvements to existing validators rather than new validators.

---

#### E-1: PRODUCT_SHAPE Whitelist (Finding 0-A)

**What**: Add a `VALID_PRODUCT_SHAPES` constant to `validate_intake_complete()` in `validate.py`. After the non-empty `PRODUCT_SHAPE` check, verify the value is in the whitelist. If not, append a warning-level problem.

**Valid shapes** (from PROGRAMBUILD.md Section 3):
`web-app`, `mobile-app`, `API-service`, `CLI-tool`, `data-pipeline`, `browser-extension`, `desktop-app`, `library/SDK`, `platform/marketplace`, `AI-agent/assistant`

**Approach**: Case-insensitive strip + compare. Problem string: "PROGRAMBUILD_KICKOFF_PACKET.md: PRODUCT_SHAPE '{value}' is not a recognized shape. Valid shapes: ..." Add 1 test to `test_programstart_validate_intake.py`.

---

#### E-2: USER_FLOWS.md Section Structure Check (Finding 3-C)

**What**: In `validate_requirements_complete()`, after confirming USER_FLOWS.md exists and IDs cross-reference, add a check that at least one `## ` or `### ` section header exists in USER_FLOWS.md. This catches a stub that passes requirement ID matching but has no actual flow definitions.

**Approach**: `re.search(r"^#{2,3} .+", flow_text, re.MULTILINE)`. Problem string: "USER_FLOWS.md: no ## or ### section headings found (expected at least one flow definition section)". Add 1 test to `test_programstart_validate_requirements.py`.

---

#### E-3: Rename `test-coverage` → `template-test-coverage` (Finding 6-C)

**What**: The `validate --check test-coverage` check counts `tests/test_*.py` files in the workspace. The name implies it validates test coverage, but it only counts the PROGRAMSTART template's own test files. Rename to `template-test-coverage` in the dispatch dict, argparse choices, and any callers.

**Approach**: Search for `"test-coverage"` across `validate.py` and any test file or docs that reference it. Do a multi-replace across all files in one batch. Add no new tests — just verify existing tests still pass under the new name. Update `argparse` choices list.

**Pre-flight**: `grep -r "test-coverage"` to find all references before renaming.

---

**Combined Phase E verification**:

```powershell
uv run pytest tests/test_programstart_validate_intake.py tests/test_programstart_validate_requirements.py -v
uv run programstart validate --check all
uv run programstart drift
```

**Commit**: `fix(validate): add PRODUCT_SHAPE whitelist, USER_FLOWS section check, rename test-coverage (Findings 0-A, 3-C, 6-C)`

---

### Post-Phase Docs

After Phases A–E, update:

1. **`automation.md`**:
   - Last updated header → 2026-04-13 (stage6gameplan complete)
   - Finding 4-A: status → RESOLVED (`validate_risk_spike_resolution()` added)
   - Finding UJ-A: status → RESOLVED (3 UJ shaping prompts created, stage5gameplan Phase C)
   - Finding UJ-C: status → RESOLVED (wired into UJ phase_0 advance)
   - Finding 0-A: status → RESOLVED (PRODUCT_SHAPE whitelist added)
   - Finding 3-C: status → RESOLVED (USER_FLOWS section check added)
   - Finding 6-C: status → RESOLVED (`test-coverage` renamed)
   - **USERJOURNEY Phase 0 section** in automation.md: add row for `Phase 0 → engineering-ready` gate (now ✅). **Do NOT** edit "Stage 2 capability table" (that is PROGRAMBUILD Stage 2 / research, already ✅).
   - Stage 4 capability table: add `risk-spikes-resolved` row

2. **`promptaudit.md`**:
   - Last updated header
   - Part 2 matrix: `Cross-stage validation invoked` row → ✅ all 10 prompts (Phase C)
   - Part 2 matrix: `` `sync_rules` explicitly cited `` row → ✅ all 10 prompts (Phase D)
   - Part 2 matrix score → ~117/117 (minus architectural N/A cells)
   - PA-9: PARTIALLY RESOLVED — stage5gameplan Phase C created 3 UJ prompts covering 4/5 UJ sync_rules (external_review_packet, route_state_logic, legal_consent_behavior, ux_surfaces_copy). `implementation_sequence` partially covered by `uj-next-slice`.
   - PA-10: SUBSTANTIALLY IMPROVED — 3 UJ prompts now cover 3 additional authority files (DECISION_LOG.md, LEGAL_AND_CONSENT.md, UX_SURFACES.md); 10 → ~7 UJ authority/dependent files still have zero coverage.
   - PA-14 → RESOLVED (was PARTIALLY RESOLVED; Phase C closes it)
   - PA-15 remains PARTIALLY RESOLVED — **do not mark RESOLVED**; actual PA-15 (validator error messages) is separate from Phase D
   - Part 2 matrix score note: ❌ row for "`sync_rules` explicitly cited" → ✅ (Phase D), ❌ row for "Cross-stage validation invoked" → ✅ (Phase C)

3. **`promptingguidelines.md`**:
   - What Still Needs Doing: strike through item 3 (Phase F → CLOSED by Phase C) and item 4 / item 9 (Phase G → CLOSED by Phase D)
   - Note architectural limits in a new "Permanently Deferred" sub-section (JIT Step 1, `applyTo` limitation, `step_files` divergence)

**Commit**: `docs: update automation.md, promptaudit.md, promptingguidelines.md post stage6gameplan`

---

## 5. What Remains After This Gameplan

After Phases A–E, the following are permanently accepted as architectural limits or explicitly out-of-scope:

| Item | Reason |
|---|---|
| JIT Step 1: prompts load hardcoded file lists, not registry-derived | No concrete use case for un-hardcoding; `programstart guide` still serves the JIT intent |
| PA-12: `step_files` vs. `guidance.files` divergence | Intentional — step_files tracks primary deliverables; guidance lists context files |
| PA-13: instruction files don't inject into prompt execution | VS Code `applyTo` architectural constraint |
| Finding 1-B: Challenge Gate advisory-only | Solo operator preference; blocking for enterprise variant is a future decision |
| PA-17: USER_FLOWS.md dedicated test file | Covered by requirements validator cross-reference tests |
| Finding 7-C: test-pass validation before advance | PROGRAMSTART cannot run the generated project's tests |
| Finding UJ-B (phases 1-3): content validators for legal drafts, UX surfaces | USERJOURNEY is project-specific; prose-heavy docs resist structural validation |

At that point, the protocol compliance matrix from Part 2 of `promptaudit.md` reaches ✅ for every automatable cell.
