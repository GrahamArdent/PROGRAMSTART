# Stage 7 Gameplan — Test Coverage Push

Purpose: Close all coverage gaps identified in the 2026-04-13 full system audit (`apr13report.md`). Fix pre-existing test failures, expand coverage tracking to all production modules, raise per-module coverage on every module below 90%, and create missing test files. After these phases, the PROGRAMSTART test suite should have zero failures and ≥90% coverage on every tracked production module.
Status: **PLANNED**
Authority: Non-canonical working plan derived from `apr13report.md` (Section 3 Critical Findings, Section 4 Test Suite Inventory, Section 10 Priority Action Items), `pyproject.toml` `[tool.coverage]` config, and live `pytest --cov` output from 2026-04-13.
Last updated: 2026-04-13

---

## 1. Current State

Baseline recorded 2026-04-13:

> **Note**: These numbers are stale — 52 test files now exist (up from 48) and total test count has likely increased. Re-run pytest during Pre-work to capture current state.

- **886 tests collected** across 48 test files
- **883 passed**, **3 failed** (pre-existing)
- **Coverage: 88%** on 22 tracked modules (4,449 stmts, 433 missed)
- **Coverage floor: 80%** (`fail_under = 80` in `pyproject.toml`)
- **16 modules NOT tracked** by coverage (~4,600 LOC invisible)
- `programstart validate --check all` PASSES with 2 warnings (DEC-005, DEC-006 missing ADRs)
- `programstart drift` PASSES with 2 notes (FILE_INDEX.md, FEASIBILITY.md authority-without-dependent)

### 4 Modules Below 90% Individual Coverage

| Module | Stmts | Missed | Coverage | Gap to 90% |
|---|---|---|---|---|
| `programstart_impact.py` | 66 | 14 | **70%** | 13 stmts |
| `programstart_recommend.py` | 694 | 147 | **76%** | 78 stmts |
| `programstart_retrieval.py` | 430 | 94 | **77%** | 51 stmts |
| `programstart_workflow_state.py` | 317 | 57 | **81%** | 25 stmts |

### 6 Production Modules Not Tracked (with existing tests)

| Module | Est. LOC | Existing Tests | Test Count |
|---|---|---|---|
| `programstart_serve.py` | ~2,450 | `test_programstart_serve.py` + `test_serve_endpoints.py` | 52 |
| `programstart_starter_scaffold.py` | ~800 | `test_programstart_starter_scaffold.py` | 28 |
| `programstart_markdown_parsers.py` | ~200 | `test_programstart_markdown_parsers.py` | 20 |
| `programstart_prompt_eval.py` | ~150 | `test_programstart_prompt_eval.py` | 7 |
| `programstart_health_probe.py` | ~100 | `test_programstart_health_probe.py` | 11 |
| `programstart_research_delta.py` | ~100 | `test_programstart_research_delta.py` | 9 |

### 1 Production Script With No Tests

| Script | Purpose |
|---|---|
| `check_commit_msg.py` | Pre-commit hook — validates commit messages against Conventional Commits format |

### 3 Pre-existing Test Failures

| Test | File | Root Cause |
|---|---|---|
| `test_drift_check_passes_with_no_violations` | `test_programstart_drift_check.py:36` | Calls `main()` with real registry. Drift notes now emitted for `programbuild_control_inventory` and `programbuild_feasibility_cascade` (authority files changed without dependent files). Test asserts only `"Drift check passed"` in stdout but extra `"Notes:"` lines now appear. |
| `test_drift_check_system_filter` | `test_programstart_drift_check.py:66` | Same root cause — real registry produces notes when `--system programbuild` is passed with benign files `README.md noxfile.py`. |
| `test_main_status_fail_on_due_returns_one` | `test_programstart_research_delta.py:99` | Test expects `rc == 1` when overdue items exist with `--fail-on-due`, but implementation returns 0. Either the exit code logic changed and the test was not updated, or the `--fail-on-due` flag is not wired to the exit path correctly. |

---

## 2. Remaining Gaps

Confirmed by code inspection and `apr13report.md` Section 10 priorities.

| ID | Gap | Priority | Source |
|---|---|---|---|
| **T-1** | 3 pre-existing test failures block strict CI | P0 | apr13report.md CRIT-1 |
| **T-2** | 6 production modules excluded from coverage tracking | P1 | apr13report.md Section 4 / pyproject.toml |
| **T-3** | `programstart_impact.py` at 70% (14 missed stmts) | P1 | apr13report.md Section 4 |
| **T-4** | `programstart_recommend.py` at 76% (147 missed stmts) | P1 | apr13report.md Section 4 |
| **T-5** | `programstart_retrieval.py` at 77% (94 missed stmts) | P1 | apr13report.md Section 4 |
| **T-6** | `programstart_workflow_state.py` at 81% (57 missed stmts) | P1 | apr13report.md Section 4 |
| **T-7** | `check_commit_msg.py` has no test file | P2 | apr13report.md Section 4 |
| **T-8** | DEC-005 and DEC-006 active without ADR files | P1 | apr13report.md CRIT-2, validate warnings |
| **T-9** | Drift notes for FILE_INDEX.md and FEASIBILITY.md | P1 | apr13report.md CRIT-3, drift output |
| **T-10** | Push remaining 14 modules ≥90% → ≥95% where feasible | P2 | Coverage push goal |
| **T-11** | Raise `programstart_serve.py` coverage once tracked | P2 | apr13report.md Section 9 — largest file |
| **T-12** | No `--strict` flag on `validate` or `drift` — warnings/notes exit 0 | P1 | apr13report.md Section 12 (S-1) |
| **T-13** | No `validate_coverage_source_completeness()` — scripts can exist without coverage tracking | P1 | apr13report.md Section 12 (S-2) |
| **T-14** | `validate_test_coverage()` glob misses `check_*.py` scripts | P1 | apr13report.md Section 12 (S-3) |
| **T-15** | `--fail-on-due` only works with `--status` in research_delta | P1 | apr13report.md Section 12 (S-5) |
| **T-16** | pytest addopts missing `--strict-markers` | P2 | apr13report.md Section 12 (S-6) |
| **T-17** | `post_launch_review` stage has no gate checks in `stage_checks` dict | P1 | apr13report.md Section 12 (S-7) |
| **T-18** | `nox -s ci` doesn't include `format_code` or `requirements` sessions | P2 | apr13report.md Section 12 (S-8) |
| **T-19** | No schema conformance tests in pytest — 3 JSON schemas validated only by pre-commit hooks, invisible to test suite | P1 | Gameplan audit 2026-04-13 |
| **T-20** | No runtime schema validation on state write — `workflow_state.py` writes JSON without validating against schema | P1 | Gameplan audit 2026-04-13 |
| **T-21** | `fail_under = 80` stale after coverage push — should be raised to lock in gains | P2 | Gameplan audit 2026-04-13 |

---

## 3. Phase Sequence

| Phase | Gap(s) | Type | Est. edits | Target |
|---|---|---|---|---|
| Pre-work | — | Record baseline | 0 edits | Snapshot test + coverage numbers |
| A | T-1 | Fix 3 test failures | 2–3 test file edits, 0–1 implementation edit | 0 failures |
| B | T-2 | Expand coverage tracking | 1 config edit (pyproject.toml) | 28 modules tracked |
| C | T-3 | Raise `impact.py` 70% → 90%+ | 1 test file edit | ≥90% on impact |
| D | T-6 | Raise `workflow_state.py` 81% → 90%+ | 1 test file edit | ≥90% on workflow_state |
| E | T-5 | Raise `retrieval.py` 77% → 85%+ | 1 test file edit | ≥85% on retrieval |
| F | T-4 | Raise `recommend.py` 76% → 85%+ | 1 test file edit | ≥85% on recommend |
| G | T-7 | Create `test_check_commit_msg.py` | 1 new test file | check_commit_msg.py covered |
| H | T-8 | Create ADRs for DEC-005 and DEC-006 | 2 new ADR files + index update | validate warnings eliminated |
| I | T-9 | Resolve drift notes | 2–4 doc edits (propagate dependents) | drift passes with 0 notes |
| J | T-10, T-11 | Push newly-tracked + remaining modules toward 95% | Multiple test file edits | ≥90% on all newly tracked; ≥95% where feasible |
| K | T-12–T-18 | Safety net hardening | 5–7 script edits, 1 config edit | Automation catches future drift |
| L | T-19, T-20 | Schema conformance hardening | 1 new test file, 1 script edit | State mutations validated against schema |
| Docs | T-21 | Sync docs + lock coverage floor | Update apr13report, raise fail_under, run validate + drift | Clean baseline |

Phases A–B first (unblock CI, expand visibility). C–F next (raise tracked modules above floor). G–I (missing tests, docs debt). J (polish). K (safety net hardening — prevent recurrence). L (schema conformance — close the pre-commit-only validation gap). Docs after all code phases.

---

## 4. Phases

---

### Pre-work: Record Baseline

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 10
uv run pytest --cov --cov-report=term-missing 2>&1 | Select-Object -Last 30
uv run programstart validate --check all
uv run programstart drift
```

Capture exact test count, failure list, per-module coverage %, validate output, and drift output. This is the "before" snapshot. All phases measure improvement against this baseline.

Expected: 886 tests, 3 failures, 88% coverage on 22 modules, validate passes with 2 warnings, drift passes with 2 notes.

---

### Phase A: Fix 3 Pre-existing Test Failures (T-1)

**Goal**: All 886 tests pass. Zero failures.

---

#### A-1: Fix `test_drift_check_passes_with_no_violations` and `test_drift_check_system_filter`

**Root cause**: Both tests call `main()` against the real on-disk registry and file set. Since authority files (FILE_INDEX.md, FEASIBILITY.md) have been changed without corresponding dependent file updates, `main()` now emits `"Notes:"` lines in stdout. The tests assert either exact string `"Drift check passed"` or just `result == 0` but the notes cause stdout mismatch.

**Fix strategy**: Two options — choose the one that matches existing test patterns:

- **Option 1 (preferred)**: Make the tests resilient to notes. Assert `result == 0` (return code = success) and `"Drift check passed" in captured` rather than exact stdout matching. Notes are informational, not failures. The `result == 0` assertion already passes; only the stdout check needs relaxing.
- **Option 2**: Mock the changed-files input to pass files that do not trigger notes. This is fragile — as the registry evolves, the "safe" file set changes.

**Pre-flight**: Read `test_programstart_drift_check.py` lines 36–80 to confirm which assertion is failing (stdout match or return code). Read the `main()` function in `programstart_drift_check.py` to understand when notes are emitted vs. when violations are emitted.

**Edit**: `tests/test_programstart_drift_check.py` — update both test functions.

**Verification**:

```powershell
uv run pytest tests/test_programstart_drift_check.py -v
```

Expected: all drift_check tests pass including the two previously failing.

---

#### A-2: Fix `test_main_status_fail_on_due_returns_one`

**Root cause**: The test at `test_programstart_research_delta.py:99` calls `main(["--status", "--date", "2026-04-10", "--fail-on-due", "--json"])` and expects `result == 1`. Either:

1. The `--fail-on-due` flag's exit-code logic was changed (implementation returns 0 even when due items exist), OR
2. The test date `2026-04-10` no longer produces overdue entries with the current `knowledge-base.json` data.

**Fix strategy**: Investigate both possibilities:

- Read `programstart_research_delta.py` to find the `--fail-on-due` exit path. If the implementation silently returns 0 when it should return 1, fix the implementation (1 line — `sys.exit(1)` or `return 1`).
- If the test date is stale (no tracks are overdue at 2026-04-10 given current `last_review_date` values), update either the test date or the fixture data to guarantee an overdue item.

**Pre-flight**: Read `scripts/programstart_research_delta.py` — find the `--fail-on-due` handling and the exit code path. Read `config/knowledge-base.json` `research_ledger.tracks` to check freshness dates.

**Edit**: Either `scripts/programstart_research_delta.py` (if implementation bug) or `tests/test_programstart_research_delta.py` (if test date is stale), or both.

**Verification**:

```powershell
uv run pytest tests/test_programstart_research_delta.py -v
```

Expected: all research_delta tests pass.

---

#### Phase A Summary Verification

```powershell
uv run pytest --tb=short -q 2>&1 | Select-Object -Last 5
```

Expected: `886 passed` (or slightly more if new tests added), `0 failed`.

**Commit**: `fix(tests): resolve 3 pre-existing test failures in drift_check and research_delta`

---

### Phase B: Expand Coverage Tracking (T-2)

**Goal**: Add 6 production modules to `[tool.coverage.run].source` in `pyproject.toml` so their coverage is measured and enforced by the 80% floor.

**Modules to add**:

```toml
  "scripts.programstart_serve",
  "scripts.programstart_starter_scaffold",
  "scripts.programstart_markdown_parsers",
  "scripts.programstart_prompt_eval",
  "scripts.programstart_health_probe",
  "scripts.programstart_research_delta",
```

**Risk**: If any newly-tracked module is below 80%, the `fail_under = 80` threshold still applies to the aggregate TOTAL, not per-module. The aggregate total will shift but is extremely unlikely to drop below 80% given 22 existing modules averaging 88%. Verify by running coverage after adding.

**Edit**: `pyproject.toml` — insert 6 lines into `[tool.coverage.run].source` list.

**Pre-flight**: Run coverage with the new modules to see their initial numbers before committing.

```powershell
uv run pytest --cov=scripts.programstart_serve --cov=scripts.programstart_starter_scaffold --cov=scripts.programstart_markdown_parsers --cov=scripts.programstart_prompt_eval --cov=scripts.programstart_health_probe --cov=scripts.programstart_research_delta --cov-report=term-missing 2>&1 | Select-Object -Last 15
```

**Verification**:

```powershell
uv run pytest --cov --cov-report=term-missing 2>&1 | Select-Object -Last 35
```

Expected: 28 modules tracked, TOTAL still above 80%. Record the initial coverage % for each newly-tracked module — these become Phase J baselines.

**Commit**: `chore: add 6 production modules to coverage tracking`

---

### Phase C: Raise `programstart_impact.py` from 70% to 90%+ (T-3)

**Goal**: Cover at least 59/66 statements (currently 52/66).

**Pre-flight**: Run coverage with `--cov-report=term-missing` to get exact missed line numbers. Read those lines in `scripts/programstart_impact.py` to identify untested branches.

```powershell
uv run pytest --cov=scripts.programstart_impact --cov-report=term-missing tests/test_programstart_impact.py -v 2>&1 | Select-Object -Last 20
```

**Approach**: The 14 missed statements in a 66-line module are likely 2–3 untested branches. Identify them from the missing-lines report, then add targeted tests for each branch. Expected: 3–5 new test functions.

**Edit**: `tests/test_programstart_impact.py` — add new test functions for uncovered branches.

**Verification**:

```powershell
uv run pytest --cov=scripts.programstart_impact --cov-report=term-missing tests/test_programstart_impact.py -v
```

Expected: ≥90% on `programstart_impact.py`.

**Commit**: `test(impact): raise coverage from 70% to 90%+`

---

### Phase D: Raise `programstart_workflow_state.py` from 81% to 90%+ (T-6)

**Goal**: Cover at least 285/317 statements (currently 260/317).

**Pre-flight**: Same pattern — get missed line numbers, read the code, identify untested branches.

```powershell
uv run pytest --cov=scripts.programstart_workflow_state --cov-report=term-missing tests/test_programstart_workflow_state.py -v 2>&1 | Select-Object -Last 30
```

**Approach**: 57 missed statements across 317 lines. Likely a mix of:

- Edge-case advance paths (unusual system/step combinations)
- Error handling branches (invalid state files, malformed JSON)
- Less-used CLI sub-subcommands (e.g., `state reset`, `state set`)

Add targeted tests for each missed branch. Expected: 8–12 new test functions.

**Edit**: `tests/test_programstart_workflow_state.py` — add new test functions.

**Verification**:

```powershell
uv run pytest --cov=scripts.programstart_workflow_state --cov-report=term-missing tests/test_programstart_workflow_state.py -v
```

Expected: ≥90% on `programstart_workflow_state.py`.

**Commit**: `test(workflow_state): raise coverage from 81% to 90%+`

---

### Phase E: Raise `programstart_retrieval.py` from 77% to 85%+ (T-5)

**Goal**: Cover at least 365/430 statements (currently 336/430).

**Pre-flight**:

```powershell
uv run pytest --cov=scripts.programstart_retrieval --cov-report=term-missing tests/test_programstart_retrieval.py tests/test_hypothesis_retrieval.py -v 2>&1 | Select-Object -Last 40
```

Note: `programstart_retrieval.py` is the RAG retrieval engine. Some uncovered paths may be LLM-dependent (require API keys for embedding calls). For those paths:

- **Mockable paths**: Test with mocked embedding responses. These are the highest-value additions.
- **API-gated paths**: If a path cannot be tested without a real API key, document it as a known exclusion and add a `# pragma: no cover` comment with justification.

**Approach**: 94 missed statements. Likely 60–70% are mockable (error handling, fallback logic, cache miss paths). Target 30+ new covered statements to reach 85%.

**Edit**: `tests/test_programstart_retrieval.py` — add new test functions with mocked API responses where necessary.

**Verification**:

```powershell
uv run pytest --cov=scripts.programstart_retrieval --cov-report=term-missing tests/test_programstart_retrieval.py tests/test_hypothesis_retrieval.py -v
```

Expected: ≥85% on `programstart_retrieval.py`. Note: 90% may not be achievable if significant LLM-only paths exist. Document any pragmatic exclusions.

**Commit**: `test(retrieval): raise coverage from 77% to 85%+`

---

### Phase F: Raise `programstart_recommend.py` from 76% to 85%+ (T-4)

**Goal**: Cover at least 590/694 statements (currently 547/694).

**Pre-flight**:

```powershell
uv run pytest --cov=scripts.programstart_recommend --cov-report=term-missing tests/test_programstart_recommend.py -v 2>&1 | Select-Object -Last 40
```

**Approach**: 147 missed statements — the highest absolute gap. This module handles recommendation logic for different product shapes and stack combinations. Uncovered branches likely include:

- Rare product-shape handlers (e.g., `browser-extension`, `desktop-app`, `data-pipeline`)
- Edge-case stack combinations
- Error paths for malformed input

Target 60+ newly covered statements (the most impactful branches first). Expected: 10–15 new test functions with varied product-shape and stack fixtures.

**Edit**: `tests/test_programstart_recommend.py` — add new test functions.

**Verification**:

```powershell
uv run pytest --cov=scripts.programstart_recommend --cov-report=term-missing tests/test_programstart_recommend.py -v
```

Expected: ≥85% on `programstart_recommend.py`.

**Commit**: `test(recommend): raise coverage from 76% to 85%+`

---

### Phase G: Create `test_check_commit_msg.py` (T-7)

**Goal**: Create a test file for `check_commit_msg.py` — the only production script with zero test coverage.

**Pre-flight**: Read `scripts/check_commit_msg.py` to understand its interface — it likely reads a commit message file path from argv and validates against Conventional Commits format.

**Test cases** (expected based on `conventional-commits.instructions.md`):

- Valid commit message with type + description → exit 0
- Valid commit message with scope → exit 0
- Valid commit message with body and footer → exit 0
- Invalid type → exit non-zero
- Subject exceeding 100 chars → exit non-zero
- Missing colon separator → exit non-zero
- Merge commit → exempt, exit 0
- WIP commit → exempt, exit 0
- `BREAKING CHANGE:` footer recognized → exit 0

**Approach**: Create `tests/test_check_commit_msg.py` with 8–10 parametrized tests. Each test writes a commit message to a temp file, calls the script's main function, and checks the exit code.

**Edit**: New file `tests/test_check_commit_msg.py`.

**Verification**:

```powershell
uv run pytest tests/test_check_commit_msg.py -v
```

Expected: all tests pass.

**Commit**: `test: add test_check_commit_msg.py for commit message validation script`

---

### Phase H: Create ADRs for DEC-005 and DEC-006 (T-8)

**Goal**: Eliminate the 2 warnings from `programstart validate --check all` by creating formal ADR records.

**Pre-flight**: Read `PROGRAMBUILD/DECISION_LOG.md` entries for DEC-005 and DEC-006 to understand the decisions. Read `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` for the MADR 4.0 template. Read `docs/decisions/README.md` for the index format and current highest ADR number.

**DEC-005**: Cross-cutting prompts registered via `cross_cutting_prompts` — decision to add a registry key rather than embed cross-cutting validation calls in every prompt individually.

**DEC-006**: Both `PROGRAMBUILD_CANONICAL.md §N` and `PROGRAMBUILD.md §N` — decision about how canonical section numbering aligns between the two documents.

**Edits**:

1. New file: `docs/decisions/0008-cross-cutting-prompts-registry.md` (DEC-005 ADR)
2. New file: `docs/decisions/0009-canonical-section-alignment.md` (DEC-006 ADR)
3. Update `docs/decisions/README.md` — add entries to the index table

**Verification**:

```powershell
uv run programstart validate --check all
```

Expected: `Validation passed for check: all` with zero warnings.

**Commit**: `docs: add ADR-0008 and ADR-0009 for DEC-005 and DEC-006`

---

### Phase I: Resolve Drift Notes (T-9)

**Goal**: Clean drift baseline — `programstart drift` passes with zero notes.

**Pre-flight**: Run `programstart drift` to confirm the 2 notes are still:

1. `programbuild_control_inventory`: authority files changed without dependent files: `PROGRAMBUILD_FILE_INDEX.md`
2. `programbuild_feasibility_cascade`: authority files changed without dependent files: `FEASIBILITY.md`

**Root cause**: Authority files (FILE_INDEX.md, FEASIBILITY.md) were modified in commits that did not also touch their dependent files. The drift checker sees the authority's `last_modified` date is newer than the dependents'.

**Fix strategy**: Use the `propagate-canonical-change` prompt pattern:

1. Read FILE_INDEX.md and identify what changed.
2. Propagate the change to its dependents per `programbuild_control_inventory` sync_rule.
3. Read FEASIBILITY.md and identify what changed.
4. Propagate the change to its dependents per `programbuild_feasibility_cascade` sync_rule.

If the authority file changes are cosmetic (e.g., formatting, date bumps) and dependents are already correct, a no-op touch of the dependents is acceptable — but document the rationale in the commit message.

**Edits**: 2–4 files in `PROGRAMBUILD/` depending on what actually changed.

**Verification**:

```powershell
uv run programstart drift
```

Expected: `Drift check passed.` with zero notes.

**Commit**: `docs: propagate FILE_INDEX.md and FEASIBILITY.md changes to dependents`

---

### Phase J: Push Newly-Tracked and Remaining Modules Toward 95% (T-10, T-11)

**Goal**: Raise all tracked modules to ≥90%; push toward 95% where feasible.

**Scope**: After Phase B adds 6 modules to tracking, run coverage to get their initial baselines. Then:

#### J-1: Newly-tracked modules below 80%

Any of the 6 newly-tracked modules that fall below 80% need immediate test additions to stay above `fail_under`. Based on existing test counts:

- `programstart_serve.py` (52 tests, largest codebase) — likely 60–70% initial. Needs the most work.
- `programstart_starter_scaffold.py` (28 tests) — likely 70–80%. May need a few additions.
- Others (7–20 tests each, small modules) — likely 80%+.

#### J-2: Already-tracked modules between 90–95%

Push `programstart_create.py` (90%), `programstart_context.py` (89%), `programstart_clean.py` (89%), `programstart_bootstrap.py` (91%), `programstart_refresh_integrity.py` (91%) toward 95% where the uncovered branches are testable.

#### J-3: `programstart_serve.py` deep coverage

The largest file (~2,450 LOC) with only smoke-level testing. Add targeted unit tests for:

- API route handlers (JSON responses, error codes)
- WebSocket event handlers
- Template rendering edge cases
- CORS and security middleware paths

**Approach**: Run per-module missing-lines reports. Prioritize by uncovered-statement count: serve first, then scaffold, then the smaller modules. Write focused tests for each uncovered branch.

**Verification** (after all J sub-phases):

```powershell
uv run pytest --cov --cov-report=term-missing 2>&1 | Select-Object -Last 40
```

Expected: All tracked modules ≥80% (enforced by `fail_under`), most ≥90%, several at 95%+.

**Commits**: One commit per sub-phase (`test(serve): raise coverage to N%`, etc.) or batch if small.

---

### Phase K: Safety Net Hardening (T-12–T-18)

**Goal**: Close the systemic automation gaps identified in `apr13report.md` Section 12. These are the root causes that allowed issues T-1 through T-11 to accumulate undetected. After Phase K, the same categories of issue cannot recur.

---

#### K-1: Add `--strict` flag to `validate` and `drift` (T-12)

> **Prerequisite**: Phases H and I MUST complete before K-1. Adding `--strict` to CI while warnings/notes still exist will break the pipeline. The implementation can be done at any time, but the CI workflow change (`process-guardrails.yml`) and pre-commit hook changes MUST NOT be merged until H+I have resolved all warnings and notes.
>
> **Contingency**: If H or I resolves only partial warnings/notes, defer the CI and pre-commit `--strict` edits (items 3 and 4 below) to a follow-up commit after the remaining items are cleared. The script-level `--strict` flag (items 1 and 2) can still be merged immediately.

**What**: Both `programstart_validate.py` and `programstart_drift_check.py` have a two-tier severity model (problems → exit 1, warnings/notes → exit 0) with no way to opt into stricter enforcement. CI runs the non-strict versions, so missing ADRs and drift notes pass silently.

**Edits**:

1. **`scripts/programstart_validate.py`** — add `--strict` argument to argparse. In the main function after `print(f"Validation passed for check: {args.check}")`, change to:

```python
if args.strict and warnings:
    print("Validation failed (strict mode) — warnings treated as errors:")
    for warning in warnings:
        print(f"- {warning}")
    return 1
```

2. **`scripts/programstart_drift_check.py`** — add `--strict` argument to argparse. In the main function after `print("Drift check passed.")`, change to:

```python
if args.strict and notes:
    print("Drift check failed (strict mode) — notes treated as violations:")
    for note in notes:
        print(f"- {note}")
    return 1
```

3. **`.github/workflows/process-guardrails.yml`** — update CI to use `--strict` on the main branch:
   - Line 156: `uv run programstart validate --check all --strict`
   - Line 168: `uv run programstart drift --strict`

4. **`.pre-commit-config.yaml`** — update hooks to also use `--strict`:
   - Line 78: change `entry: uv run programstart validate --check all` → `entry: uv run programstart validate --check all --strict`
   - Line 85: change `entry: uv run programstart drift` → `entry: uv run programstart drift --strict`

**Tests**: Add tests for ```--strict` behavior in `test_programstart_validate.py` and `test_programstart_drift_check.py` — 2–3 tests each verifying exit code 1 when strict + warnings/notes present, and exit code 0 when strict + no warnings/notes.

**Verification**:

```powershell
uv run programstart validate --check all --strict
uv run programstart drift --strict
```

Expected: Both exit 1 until Phases H and I resolve the existing warnings/notes. After H+I, both exit 0.

**Commit**: `feat(validate): add --strict flag to validate and drift for CI enforcement`

---

#### K-2: Add `validate_coverage_source_completeness()` (T-13)

**What**: No automation checks whether scripts in `scripts/` are also registered in `pyproject.toml [tool.coverage.run].source`. New modules escape coverage tracking silently.

**Edit**: `scripts/programstart_validate.py` — add a new function:

```python
def validate_coverage_source_completeness(_registry: dict) -> list[str]:
    """Warn about production scripts not registered in [tool.coverage.run].source."""
    problems: list[str] = []
    scripts_dir = workspace_path("scripts")
    if not scripts_dir.exists():
        return problems
    pyproject = workspace_path("pyproject.toml")
    if not pyproject.exists():
        return problems
    # Parse source list from pyproject.toml
    import tomllib
    config = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    source_list = config.get("tool", {}).get("coverage", {}).get("run", {}).get("source", [])
    source_modules = {s.replace("scripts.", "") for s in source_list}
    # Check all production scripts
    EXCLUDED_SUFFIXES = ("_smoke.py", "_smoke_readonly.py")
    EXCLUDED_NAMES = {"__init__.py", "programstart_smoke_helpers.py", "programstart_dashboard_golden.py"}
    for script in sorted(scripts_dir.glob("*.py")):
        if script.name in EXCLUDED_NAMES or any(script.name.endswith(s) for s in EXCLUDED_SUFFIXES):
            continue
        module_name = script.stem
        if module_name not in source_modules:
            problems.append(
                f"scripts/{script.name} is not in [tool.coverage.run].source in pyproject.toml"
            )
    return problems
```

Wire into the `--check all` path and add `"coverage-source"` to the dispatch.

Specifically, in the `if args.check == "all"` block (lines 1227–1244), add:

```python
        warnings.extend(validate_coverage_source_completeness(registry))
```

Also add `"coverage-source"` to the `elif` dispatch chain for standalone use.

**Tests**: 3 tests — missing module flagged, all modules present passes, excluded smoke scripts not flagged.

**Commit**: `feat(validate): add coverage source completeness check`

---

#### K-3: Broaden `validate_test_coverage()` Pattern (T-14)

**What**: The current glob `scripts/programstart_*.py` misses `check_commit_msg.py` and any future non-`programstart_` prefixed scripts.

**Edit**: `scripts/programstart_validate.py` line 1100 — change the glob and exclusion logic:

```python
# Before:
for script in sorted(scripts_dir.glob("programstart_*.py")):
    if script.name.endswith("_smoke.py"):
        continue

# After:
EXCLUDED_SUFFIXES = ("_smoke.py", "_smoke_readonly.py")
EXCLUDED_NAMES = {"__init__.py", "programstart_smoke_helpers.py", "programstart_dashboard_golden.py"}
for script in sorted(scripts_dir.glob("*.py")):
    if script.name in EXCLUDED_NAMES or any(script.name.endswith(s) for s in EXCLUDED_SUFFIXES):
        continue
```

> **Note**: `programstart_dashboard_golden.py` is browser automation / smoke tooling (not production code) and does not match the `_smoke.py` suffix convention. It is explicitly excluded to prevent false positives.

**Tests**: 1 test verifying `check_commit_msg.py` appears in warnings when its test file is absent.

**Commit**: `fix(validate): broaden test discovery to all production scripts`

---

#### K-4: Fix `--fail-on-due` Outside `--status` Path (T-15)

**What**: `programstart_research_delta.py` line 382 always returns 0 in the template-generation path, even when `--fail-on-due` is set and tracks are overdue.

**Edit**: `scripts/programstart_research_delta.py` — after the template-generation block (line ~381), add:

```python
if args.fail_on_due:
    report = build_status(args.date)
    if has_due_tracks(report):
        return 1
return 0
```

**Tests**: 1 test calling `main(["--fail-on-due", "--date", "<overdue-date>"])` without `--status` and verifying `rc == 1`.

**Commit**: `fix(research_delta): honor --fail-on-due in template generation path`

---

#### K-5: Add `--strict-markers` to Pytest Config (T-16)

**What**: Pytest marker typos (e.g., `@pytest.mark.slwo` instead of `@pytest.mark.slow`) are silently treated as valid marks.

**Edit**: `pyproject.toml` line 124:

```toml
# Before:
addopts = "-ra"

# After:
addopts = "-ra --strict-markers"
```

Also add a `markers` list if any custom marks are used in the test suite, to prevent `--strict-markers` from failing on legitimate custom marks.

**Pre-flight**: Search for all `@pytest.mark.` usage in `tests/` to identify custom markers that need registration.

**Verification**:

```powershell
uv run pytest --co -q 2>&1 | Select-Object -Last 5
```

Expected: All tests collected with no marker warnings.

**Commit**: `chore: add --strict-markers to pytest config`

---

#### K-6: Add `post_launch_review` Gate Check (T-17)

**What**: `programstart_workflow_state.py` line 136 `stage_checks` dict covers 10 of 11 PROGRAMBUILD stages. `post_launch_review` is missing — the final stage can advance without any validation.

**Edit**:

1. **`scripts/programstart_validate.py`** — add `validate_post_launch_review()` function. At minimum, check that `PROGRAMBUILD/POST_LAUNCH_REVIEW.md` exists and has content (not a stub). Follow the existing validator pattern.

2. **`scripts/programstart_validate.py`** — add `"post-launch-review"` to the dispatch dict and argparse choices.

3. **`scripts/programstart_workflow_state.py`** — add to `stage_checks`:

```python
"post_launch_review": "post-launch-review",
```

4. **`scripts/programstart_validate.py`** — wire `validate_post_launch_review()` into the `--check all` block (lines 1227–1244). Add after the existing `validate_engineering_ready()` call:

```python
        problems.extend(validate_post_launch_review(registry))
```

Also add `"post-launch-review"` to the `elif` dispatch chain.

**Tests**: 2 tests — missing file fails, file with content passes.

**Commit**: `feat(validate): add post_launch_review gate check for Stage 10 advance`

---

#### K-7: Add `format_check` and `requirements` to `nox -s ci` (T-18)

**What**: The `ci` meta-session omits formatting and requirements freshness checks. `format_code` exists but auto-fixes in place (unsuitable for CI). `requirements` exists but isn't notified.

**Pre-flight confirmed**: `format_code` session (noxfile.py line 280) runs `ruff check --fix .` and `ruff format .` — both auto-fix in place. Adding this directly to `nox -s ci` would mutate source during CI runs, which is incorrect.

**Edit**: `noxfile.py` — two changes:

1. **Create a new `format_check` session** (check-only, no auto-fix):

```python
@nox.session(reuse_venv=True)
def format_check(session: nox.Session) -> None:
    """Check formatting without modifying files."""
    install_dev(session)
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
```

2. **Update the `ci` session notify list** — add `format_check` (NOT `format_code`) and `requirements`:

```python
# Before:
for name in ("lint", "typecheck", "tests", "validate", "smoke", "docs", "package", "security"):

# After:
for name in ("lint", "typecheck", "tests", "validate", "smoke", "docs", "package", "security", "format_check", "requirements"):
```

Note: The existing `format_code` session (auto-fix) is kept for local developer use. Only `format_check` (read-only) goes into CI.

**Verification**:

```powershell
uv run nox -s ci --list
```

Expected: All sessions including `format_check` and `requirements` listed.

**Commit**: `chore: add format_check and requirements sessions to nox ci gate`

---

#### Phase K Summary Verification

```powershell
uv run pytest tests/test_programstart_validate.py tests/test_programstart_drift_check.py tests/test_programstart_research_delta.py -v
uv run programstart validate --check all
uv run programstart drift
```

Expected: All new tests pass. Validate and drift still pass (strict mode will only be enforced in CI after Phases H+I clean the baseline).

---

### Phase L: Schema Conformance Hardening (T-19, T-20)

**Goal**: Close the gap where JSON schema validation runs only in pre-commit hooks and is invisible to pytest and the runtime. After Phase L, schema conformance is tested in the test suite AND enforced on every state write.

---

#### L-1: Create Schema Conformance Tests (T-19)

**What**: Three JSON schemas exist in `schemas/` and are validated by pre-commit hooks (`check-jsonschema`), but zero pytest tests verify conformance. If a schema changes or a state file drifts, only manual `pre-commit run` catches it — not `pytest`, not CI's test step.

**Edit**: New file `tests/test_schema_conformance.py`:

```python
"""Validate JSON data files against their schemas."""
import json
from pathlib import Path
import pytest

try:
    import jsonschema
except ImportError:
    pytest.skip("jsonschema not installed", allow_module_level=True)

ROOT = Path(__file__).resolve().parent.parent

@pytest.mark.parametrize("data_file, schema_file", [
    ("PROGRAMBUILD/PROGRAMBUILD_STATE.json", "schemas/programbuild-state.schema.json"),
    ("USERJOURNEY/USERJOURNEY_STATE.json", "schemas/userjourney-state.schema.json"),
    ("config/process-registry.json", "schemas/process-registry.schema.json"),
])
def test_data_conforms_to_schema(data_file: str, schema_file: str) -> None:
    data = json.loads((ROOT / data_file).read_text(encoding="utf-8"))
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.validate(instance=data, schema=schema)

@pytest.mark.parametrize("schema_file", [
    "schemas/programbuild-state.schema.json",
    "schemas/userjourney-state.schema.json",
    "schemas/process-registry.schema.json",
])
def test_schema_is_valid_json_schema(schema_file: str) -> None:
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
```

**Pre-flight (BLOCKER)**: `jsonschema` is NOT currently a direct dependency — only `check-jsonschema>=0.37.1` (a CLI tool) is listed. Add `"jsonschema>=4.0.0"` to `[project.optional-dependencies].dev` in `pyproject.toml` before executing L-1 or L-2. Without this, both phases fail with `ModuleNotFoundError`.

> **Version compatibility**: `check-jsonschema` depends on `jsonschema` transitively. Before adding the direct dep, run `uv pip show check-jsonschema` to confirm its pinned `jsonschema` version range. Use a compatible constraint (e.g., if check-jsonschema pins `jsonschema>=4.5,<5`, use `"jsonschema>=4.5"` rather than `>=4.0.0`). Verify with `uv lock --dry-run` that no resolution conflict occurs.

```powershell
uv run python -c "import jsonschema; print(jsonschema.__version__)"
```

**Tests**: 6 tests total — 3 data-vs-schema conformance, 3 schema self-validation.

**Verification**:

```powershell
uv run pytest tests/test_schema_conformance.py -v
```

Expected: All 6 tests pass.

**Commit**: `test: add schema conformance tests for state and registry JSON files`

---

#### L-2: Add Runtime Schema Validation to State Writes (T-20)

**What**: `programstart_workflow_state.py` writes state JSON (line 207: `snap_path.write_text(json.dumps(payload, ...))`) without validating against the schema. A bug in state mutation logic could persist invalid JSON that passes tests but fails pre-commit.

**Edit**: `scripts/programstart_workflow_state.py` — add schema validation before writing:

```python
def _validate_state_against_schema(state: dict, system: str) -> None:
    """Validate state dict against the appropriate JSON schema before writing."""
    schema_map = {
        "programbuild": "schemas/programbuild-state.schema.json",
        "userjourney": "schemas/userjourney-state.schema.json",
    }
    schema_path = workspace_path(schema_map.get(system, ""))
    if not schema_path.exists():
        return  # Schema not found — skip validation (bootstrap scenario)
    import jsonschema
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=state, schema=schema)
```

Call `_validate_state_against_schema(payload, system)` before the `snap_path.write_text(...)` line.

**Tests**: 2 tests in `test_programstart_workflow_state.py`:
- Valid state writes successfully
- Invalid state (e.g., missing `active_stage`) raises `jsonschema.ValidationError`

**Verification**:

```powershell
uv run pytest tests/test_programstart_workflow_state.py -v -k schema
```

Expected: Both tests pass.

**Commit**: `feat(workflow_state): validate state against schema before writing`

---

#### Phase L Summary Verification

```powershell
uv run pytest tests/test_schema_conformance.py tests/test_programstart_workflow_state.py -v
uv run programstart validate --check all
uv run programstart drift
```

Expected: All schema tests pass. Validate and drift still pass.

---

### Post-Phase Docs

After all code phases (A–L) are complete:

1. **Run full validation suite**:

```powershell
uv run pytest --cov --cov-report=term-missing 2>&1 | tail -40
uv run programstart validate --check all --strict
uv run programstart drift --strict
```

2. **Raise `fail_under` coverage floor (T-21)**: After recording final aggregate coverage, raise `fail_under` in `pyproject.toml` to match the achieved level (rounded down to nearest 5). Example: if aggregate is 91%, set `fail_under = 90`. This prevents regression back to the old 80% floor.

```toml
# pyproject.toml — update to actual achieved floor
fail_under = 90  # previously 80; raised after Stage 7 coverage push
```

3. **Update `apr13report.md`**: Add a "Post Stage 7" addendum section with final numbers: test count, 0 failures, per-module coverage table, validate/drift status, and confirmation that `--strict` mode passes.

4. **Update this file (`stage7gameplan.md`)**: Change Status from `PLANNED` to `COMPLETE` with execution date. Record actual coverage numbers achieved per phase.

5. **Commit**: `docs: update apr13report.md and stage7gameplan.md post stage 7 execution`

---

## 5. Success Criteria

| Criterion | Threshold |
|---|---|
| Test failures | **0** |
| Modules tracked by coverage | **≥28** (currently 22) |
| Aggregate coverage (TOTAL) | **≥88%** (maintain or improve) |
| Per-module minimum | **≥80%** (enforced by fail_under) |
| Per-module target for below-floor modules | **≥85–90%** (impact, recommend, retrieval, workflow_state) |
| Validate warnings | **0** |
| Drift notes | **0** |
| All production scripts tested | **Yes** (check_commit_msg.py newly tested) |
| `validate --strict` passes | **Yes** (no warnings) |
| `drift --strict` passes | **Yes** (no notes) |
| All PROGRAMBUILD stages have gate checks | **Yes** (post_launch_review added) |
| Coverage source completeness | **Yes** (new validate check enforces) |
| Test discovery covers all script patterns | **Yes** (broadened from `programstart_*.py`) |
| Schema conformance tested in pytest | **Yes** (3 data files × 3 schemas validated) |
| State writes validated against schema | **Yes** (runtime guard in workflow_state.py) |
| Coverage floor raised to lock in gains | **Yes** (`fail_under` raised from 80 to achieved level) |
| Newly-tracked modules pushed toward 95% | **≥90%** on all newly tracked; **≥95%** where feasible (Phase J) |
| `--fail-on-due` works outside `--status` path | **Yes** (K-4 fix verified by test) |
| `--strict-markers` active in pytest | **Yes** (pyproject.toml addopts updated, no rogue markers) |
| `nox -s ci` includes format check + requirements | **Yes** (`format_check` and `requirements` in notify list) |

---

## 6. Out of Scope

The following items from `apr13report.md` are intentionally NOT included in this gameplan:

| Item | Reason |
|---|---|
| Full runtime schema validation on every JSON read | Reads are trusted if writes are validated — Phase L covers write-path validation only |
| Stage 7 prompt exemption doc | Documentation concern, not test coverage |
| `vulture` dead code analysis | Tooling addition — separate CI gameplan |
| Prompt exemption registry in process-registry.json | Registry design change — separate scope |
| Smoke/test-infrastructure scripts coverage | By design not tracked — these are test tooling, not production code |
| Coverage ratchet / regression tracking (S-10) | Requires external infra (Codecov or similar) — separate scope |
| Pre-commit `--fix` removal (S-9) | Intentional design — auto-fix on commit is standard practice; removing it is a workflow change, not a safety gap |
| Scheduled baseline CI health check (S-4) | Addressed indirectly by Phase A (fix failures) + Phase K-1 (`--strict` catches drift); a dedicated nightly job is a CI infra addition outside this gameplan |
