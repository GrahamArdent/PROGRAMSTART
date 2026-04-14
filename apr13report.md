# PROGRAMSTART Full System Audit Report

Purpose: Complete system audit of the PROGRAMSTART repository covering wiring, standardization, coverage, authority model, CI/CD alignment, and centralization opportunities.
Status: **Complete** — audit conducted 2026-04-13.
Authority: Non-canonical working document derived from live tool output (`programstart validate --check all`, `programstart drift`, `pytest --cov`), code inspection, and registry cross-referencing.
Last updated: 2026-04-13

---

## 1. Overall Health Score

| Dimension | Grade | Notes |
|---|---|---|
| **Wiring & Entry Points** | **A** | 24 CLI subcommands, 16 console_scripts, zero orphaned scripts |
| **Prompt Standardization** | **A** | 36 prompts, 100% YAML frontmatter, 100% registry coverage |
| **Authority Model** | **A** | 14 sync_rules, all authority + dependent files exist, drift check passes |
| **Test Coverage** | **B** | 88% overall (tracked modules), but 16 modules not tracked at all |
| **CI/CD Alignment** | **A** | 6 workflows, 15 pre-commit hooks, nox sessions match 1:1 |
| **Schema Enforcement** | **B+** | 3 schemas enforced at commit-time; gap at runtime |
| **Documentation** | **A** | 11 docs in mkdocs, 7 ADRs indexed, 25 PB + 24 UJ files all registered |
| **Code Centralization** | **B+** | `programstart_common.py` does the heavy lifting; a few scattered patterns remain |

---

## 2. Live Tool Output (2026-04-13)

### `programstart validate --check all`

```
Validation passed for check: all
Warnings:
- DEC-005 (Cross-cutting prompts registered via `cross_cutting_prompts`) is ACTIVE but has no corresponding ADR in docs/decisions/
- DEC-006 (Both `PROGRAMBUILD_CANONICAL.md §N` and `PROGRAMBUILD.md §N`) is ACTIVE but has no corresponding ADR in docs/decisions/
```

### `programstart drift`

```
Drift check passed.
Notes:
- programbuild_control_inventory: authority files changed without dependent files: PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md
- programbuild_feasibility_cascade: authority files changed without dependent files: PROGRAMBUILD/FEASIBILITY.md
```

### `pytest` (886 collected)

```
3 failed, 883 passed, 1 warning in 201.29s
FAILED tests/test_programstart_drift_check.py::test_drift_check_passes_with_no_violations
FAILED tests/test_programstart_drift_check.py::test_drift_check_system_filter
FAILED tests/test_programstart_research_delta.py::test_main_status_fail_on_due_returns_one
```

---

## 3. Critical Findings (Action Required)

### CRIT-1: Three Pre-existing Test Failures

| Test | Root Cause |
|---|---|
| `test_drift_check_passes_with_no_violations` | Test calls `main()` with real registry on disk. Drift notes now emitted for `programbuild_control_inventory` and `programbuild_feasibility_cascade` (authority files changed without dependent files). Test expects precisely `"Drift check passed"` in stdout but the output also contains `"Notes:"` lines. Test does not mock git state or registry. |
| `test_drift_check_system_filter` | Same root cause — real registry produces drift notes when `--system programbuild` is passed with benign files `README.md noxfile.py`. |
| `test_main_status_fail_on_due_returns_one` | `research_delta --status` exit code path changed; test expects `rc == 1` for "overdue" items but implementation returns 0. |

**Impact:** These block CI `nox -s tests` if strict zero-failure is enforced.

### CRIT-2: Two Missing ADRs Flagged by Validate

```
DEC-005 — Cross-cutting prompts registered via cross_cutting_prompts — ACTIVE, no ADR
DEC-006 — Both PROGRAMBUILD_CANONICAL.md §N and PROGRAMBUILD.md §N — ACTIVE, no ADR
```

**Impact:** `programstart validate --check all` passes but emits warnings. These are decisions already in effect with no formal record.

### CRIT-3: Drift Notes (Non-blocking but Meaningful)

```
programbuild_control_inventory: authority files changed without dependent files: PROGRAMBUILD_FILE_INDEX.md
programbuild_feasibility_cascade: authority files changed without dependent files: FEASIBILITY.md
```

**Impact:** Dependent docs may be stale relative to their authority files.

---

## 4. Test Suite Inventory

### Summary

- **886 tests collected** across 48 test files
- **883 passed**, 3 failed (pre-existing)
- **152 prompt compliance tests** (test_prompt_compliance.py) — all pass
- **Coverage: 88% overall** on tracked modules (4,449 statements, 433 missed)

### Per-Module Coverage (Tracked)

| Module | Stmts | Coverage | Assessment |
|---|---|---|---|
| `programstart_log.py` | 53 | **100%** | Perfect |
| `programstart_checklist_progress.py` | 46 | **100%** | Perfect |
| `programstart_models.py` | 223 | **100%** | Perfect |
| `programstart_command_registry.py` | 11 | **100%** | Perfect |
| `programstart_step_guide.py` | 63 | **99%** | Excellent |
| `programstart_dashboard.py` | 145 | **99%** | Excellent |
| `programstart_drift_check.py` | 88 | **98%** | Excellent |
| `programstart_cli.py` | 92 | **97%** | Excellent |
| `programstart_status.py` | 119 | **97%** | Excellent |
| `programstart_attach.py` | 62 | **95%** | Strong |
| `programstart_common.py` | 274 | **95%** | Strong |
| `programstart_validate.py` | 792 | **94%** | Strong |
| `programstart_init.py` | 64 | **93%** | Strong |
| `programstart_refresh_integrity.py` | 80 | **91%** | Good |
| `programstart_bootstrap.py` | 182 | **91%** | Good |
| `programstart_create.py` | 379 | **90%** | Good |
| `programstart_context.py` | 221 | **89%** | Good |
| `programstart_clean.py` | 48 | **89%** | Good |
| `programstart_workflow_state.py` | 317 | **81%** | Needs attention |
| `programstart_retrieval.py` | 430 | **77%** | Below floor if standalone |
| `programstart_recommend.py` | 694 | **76%** | Below floor if standalone |
| `programstart_impact.py` | 66 | **70%** | Below floor |
| **TOTAL** | **4,449** | **88%** | Above 80% floor |

### Modules NOT Tracked by Coverage

These 16 modules are excluded from `[tool.coverage.run].source` in `pyproject.toml`. They have varying levels of indirect testing but their coverage is invisible.

| Module | Est. LOC | Has Test File? | Test Count | Risk |
|---|---|---|---|---|
| `programstart_serve.py` | ~2,450 | Yes (`test_programstart_serve.py` + `test_serve_endpoints.py`) | 52 | **HIGH** — largest file, HTTP server |
| `programstart_starter_scaffold.py` | ~800 | Yes (`test_programstart_starter_scaffold.py`) | 28 | **HIGH** — generates all project scaffolding |
| `programstart_markdown_parsers.py` | ~200 | Yes (`test_programstart_markdown_parsers.py`) | 20 | **MEDIUM** — used by validators |
| `programstart_prompt_eval.py` | ~150 | Yes (`test_programstart_prompt_eval.py`) | 7 | LOW |
| `programstart_health_probe.py` | ~100 | Yes (`test_programstart_health_probe.py`) | 11 | LOW |
| `programstart_research_delta.py` | ~100 | Yes (`test_programstart_research_delta.py`) | 9 | LOW |
| `programstart_smoke_helpers.py` | ~50 | No (test utility) | 0 | LOW — test infra |
| `programstart_cli_smoke.py` | ~80 | No (smoke script) | 0 | LOW — test infra |
| `programstart_dashboard_smoke.py` | ~100 | No (smoke script) | 0 | LOW — test infra |
| `programstart_dashboard_smoke_readonly.py` | ~70 | No (smoke script) | 0 | LOW — test infra |
| `programstart_dashboard_browser_smoke.py` | ~120 | No (smoke script) | 0 | LOW — test infra |
| `programstart_dashboard_golden.py` | ~80 | No (smoke script) | 0 | LOW — test infra |
| `programstart_dist_smoke.py` | ~60 | No (smoke script) | 0 | LOW — test infra |
| `programstart_factory_smoke.py` | ~120 | No (smoke script) | 0 | LOW — test infra |
| `programstart_repo_clean_check.py` | ~50 | No | 0 | LOW — utility |
| `check_commit_msg.py` | ~70 | No | 0 | LOW — pre-commit hook |

**Total invisible LOC:** ~4,600 lines — roughly equal to the 4,449 tracked lines.
**Reality:** Coverage tracking covers only ~50% of the Python codebase by lines. The 88% figure is accurate for what it tracks, but the denominator is half the repo.

---

## 5. Prompt & Documentation Standardization

### What IS Standardized (Complete)

- **All 10 PB shaping prompts:** 117/117 protocol matrix compliance (verified by `test_prompt_compliance.py`, 152 tests)
- **All 3 UJ shaping prompts:** Cross-stage ref, DECISION_LOG, kill criteria, gate values — all pass
- **All 4 instruction files:** Proper YAML frontmatter with `description`, `name`, `applyTo`
- **All 3 agent files:** Proper frontmatter with `tools`, `user-invocable`
- **All 7 ADRs:** MADR 4.0 format, indexed in `decisions/README.md`
- **14 sync_rules:** All have authority files, dependent files, and prompt references
- **Commit enforcement:** `.pre-commit-config.yaml` + `check_commit_msg.py` + `.gitlint` + `conventional-commits.instructions.md` all aligned
- **Schema enforcement at commit-time:** 3 JSON schemas validated by pre-commit hooks and nox lint session

### What Is NOT Standardized

| Gap | Detail |
|---|---|
| **S7 (implementation_loop) has no shaping prompt** | Stages 0–6, 8–10 all have `shape-*.prompt.md`. Stage 7 is intentionally a loop but has zero prompt file. If this is by design, it should be documented. |
| **Utility prompts don't follow PROMPT_STANDARD** | Guide prompts (`programstart-stage-guide`, `programstart-what-next`, `start-programstart-project`) lack Protocol Declaration and Verification Gate. They're marked as exempt but there's no formal exemption registry. |
| **Internal build prompts are a separate format** | 14 `implement-*.prompt.md` files follow "Binding Rules" format, not PROMPT_STANDARD. The exemption is noted in PROMPT_STANDARD but not machine-enforced. |
| **Prompt exemption only in prose** | PROMPT_STANDARD says "internal build prompts exempt" but there is no machine-readable `prompt_categories` classification in `process-registry.json` to enforce this. |

---

## 6. Authority Model & Registry Health

### Sync Rules (14 total) — All Healthy

All 14 sync_rules have:
- Authority files that exist on disk
- Dependent files that exist on disk
- At least one prompt reference citing the rule name

### Bootstrap Assets — Complete

~270 entries in `process-registry.json` `bootstrap_assets`. Spot-checked: all exist on disk. All test files, prompt files, workflow files, scripts, schemas, and docs are registered.

### State Files

| System | Active | Status |
|---|---|---|
| PROGRAMBUILD | `inputs_and_mode_selection` (Stage 0) | `in_progress`, variant not yet selected |
| USERJOURNEY | `phase_1` (legal_drafts) | `in_progress`, phase_0 completed |

---

## 7. CI/CD Alignment

| CI Workflow | Nox Session | Pre-commit Hook | Aligned? |
|---|---|---|---|
| `process-guardrails.yml` (PR gate) | `gate_safe` | ruff, pyright, schemas, validate, drift | Yes |
| `full-ci-gate.yml` (daily) | `ci` (full) | All hooks | Yes |
| `docs-pages.yml` | `docs` | N/A | Yes |
| `release-package.yml` | `package` | N/A | Yes |
| `codeql.yml` (SAST) | N/A (external) | N/A | Yes |
| `weekly-research-delta.yml` | N/A (custom) | N/A | Yes |

**Verdict:** Perfect alignment. No workflow does work that lacks a local nox equivalent. No nox session is missing from CI.

---

## 8. Centralization Opportunities

### Already Well-Centralized

- `programstart_common.py` — workspace detection, registry loading, JSON I/O, metadata parsing (used by 20+ scripts)
- `programstart_models.py` — Pydantic data models (shared cleanly)
- `programstart_command_registry.py` — CLI command catalog + dashboard allowlist

### Opportunities

| Opportunity | Current State | Recommendation | Effort |
|---|---|---|---|
| **Schema runtime validation** | Pre-commit validates schemas, but `validate_workflow_state()` does 50+ lines of manual checks | Use the JSON schemas at runtime too: `jsonschema.validate(state_data, schema)` in one function. Currently schema changes require updating TWO places (schema file + manual validator). | Medium — high value |
| **Coverage tracking expansion** | `[tool.coverage.run].source` lists 22 of 38 modules (excluding smoke scripts: 22 of 28 production modules) | Add `programstart_serve`, `programstart_starter_scaffold`, `programstart_markdown_parsers`, `programstart_prompt_eval`, `programstart_health_probe`, `programstart_research_delta` to coverage tracking. | Low — add 6 lines |
| **Prompt exemption registry** | PROMPT_STANDARD says "internal build prompts exempt" in prose | Add a `prompt_categories` section to `process-registry.json` that classifies each prompt as `shaping`, `utility`, or `build` and declares which standard applies. Machine-enforce compliance. | Medium |
| **Missing ADR creation** | `DEC-005` and `DEC-006` active without ADR files | Create `docs/decisions/0008-*.md` and `0009-*.md`. | Low |

---

## 9. Orphaned Code & Dead Wiring

### Confirmed Orphans: **None Found**

Every script is either:
- Wired as a `console_scripts` entry in `pyproject.toml`, OR
- Dispatched via `programstart_cli.py` subcommands, OR
- Imported by another wired module, OR
- A smoke/test infrastructure script used by noxfile sessions

### Potential Dead Code (Untestable Without Coverage)

| Location | Concern |
|---|---|
| `programstart_serve.py` (~2,450 LOC) | Large HTTP server with many route handlers and API endpoints. Without unit test coverage tracking, dead routes are invisible. Dashboard smoke tests only exercise the happy path. |
| `programstart_recommend.py` (76% coverage, 147 missed statements) | Largest recommendation engine. Uncovered branches likely handle rare product shapes or edge-case stack combinations. |
| `programstart_retrieval.py` (77% coverage, 94 missed statements) | RAG retrieval paths. Uncovered code is likely LLM-dependent paths that can't run without API keys. |
| `programstart_impact.py` (70% coverage, 14 missed statements) | Lowest coverage of any tracked module. Small but proportionally weak. |

---

## 10. Summary: Priority Action Items

| Priority | Item | Type | Impact |
|---|---|---|---|
| **P0** | Fix 3 pre-existing test failures | Bug | CI reliability — unblocks strict zero-failure enforcement |
| **P1** | Add 6 production modules to coverage tracking | Config | Coverage visibility on ~3,900 LOC; makes 80% floor meaningful |
| **P1** | Create ADRs for DEC-005 and DEC-006 | Docs | Eliminate `validate --check all` warnings |
| **P1** | Resolve drift notes (FILE_INDEX.md, FEASIBILITY.md propagation) | Docs | Clean drift baseline |
| **P1** | Raise `programstart_impact.py` coverage (70% → 90%+) | Tests | Lowest tracked module |
| **P1** | Raise `programstart_recommend.py` coverage (76% → 85%+) | Tests | 147 missed statements — highest absolute miss count |
| **P1** | Raise `programstart_retrieval.py` coverage (77% → 85%+) | Tests | 94 missed statements |
| **P1** | Raise `programstart_workflow_state.py` coverage (81% → 90%+) | Tests | 57 missed statements |
| **P2** | Runtime schema validation in `validate_workflow_state()` | Code | Single source of truth for state validation |
| **P2** | Document Stage 7 prompt exemption | Docs | Completeness |
| **P2** | Write tests for `check_commit_msg.py` | Tests | Only production script with no test file |
| **P3** | Add `vulture` dead code analysis to CI | Tooling | Catch unused code across ~8,800 LOC |
| **P3** | Additional unit tests for `programstart_serve.py` coverage gaps | Tests | Largest file in repo, only smoke-tested |

---

## 11. File Inventory Quick Reference

### Scripts (38 files)

| Category | Count | Tracked by Coverage? |
|---|---|---|
| CLI entry points (console_scripts) | 16 | Yes (all 16) |
| CLI-dispatched (no console_script) | 6 | Partially (4 of 6) |
| Library/helper modules | 6 | Partially (4 of 6) |
| Smoke/test infrastructure | 8 | No (by design) |
| Utility (pre-commit hook, PS1, __init__) | 2 | No |

### Tests (48 files, 886 tests)

| Category | Files | Tests |
|---|---|---|
| Validation tests | 16 | ~320 |
| CLI & core | 10 | ~160 |
| Prompt compliance | 1 | 152 |
| USERJOURNEY | 4 | ~40 |
| Serve/dashboard | 2 | 52 |
| Specialized (RAG, hypothesis, models, etc.) | 15 | ~162 |

### Prompts (36 files)

| Category | Count | Standard |
|---|---|---|
| PB shaping prompts | 10 | PROMPT_STANDARD (117/117) |
| UJ shaping prompts | 3 | PROMPT_STANDARD subset |
| Utility prompts | 9 | Exempt (documented) |
| Internal build prompts | 14 | Binding Rules format (exempt) |

### Documentation (87 files total)

| Category | Count | 100% Referenced? |
|---|---|---|
| PROGRAMBUILD docs | 25 | Yes — registry + FILE_INDEX |
| USERJOURNEY docs | 24 | Yes — registry + sync_rules |
| MkDocs site docs | 11 | Yes — all in mkdocs.yml nav |
| ADR decision records | 7 | Yes — indexed in decisions/README.md |
| Schemas | 3 | Yes — pre-commit enforced |
| Config files | 3 | Yes — registry self-references |
| Root docs (README, etc.) | 14 | Yes |

---

**Bottom line:** This is an exceptionally well-organized repository. The authority model, prompt standardization, CI/CD alignment, and registry system are all operating tightly. The main gaps are: (1) coverage tracking only covers ~50% of the codebase by LOC — the 88% figure is real but the denominator is half the repo, (2) three stale test failures need addressing, (3) two active decisions need formal ADR records, and (4) four tracked modules sit below the 80% individual floor (impact 70%, recommend 76%, retrieval 77%, workflow_state 81%). No orphaned code, no dead wiring, no broken references.

---

## 12. Safety Net Gap Analysis — Why Didn't Automation Catch These?

The six issues found in this audit were all detectable. The system has the _data_ to catch them — validators know about warnings, drift_check knows about notes, coverage knows which modules are tracked — but the _enforcement policy_ lets them through. This section traces each issue to the specific automation gap that allowed it.

### Issue-by-Issue Root Cause

#### 1. Three Pre-existing Test Failures → No Baseline Enforcement

**What automation exists:** CI runs `uv run pytest --cov-report=term-missing --cov-report=xml` in `process-guardrails.yml` (line 124). The nox `tests` session runs `coverage run -m pytest`. Pre-commit does not run tests.

**Why it didn't catch the failures:** CI detects new failures introduced _by a commit_ but does not enforce that the baseline starts clean. If 3 tests were already failing before the most recent change, they pass through CI because the commit itself didn't break them — they were already broken. There is no "zero pre-existing failures" gate.

**Evidence:** `process-guardrails.yml` line 124 runs pytest but the workflow step succeeds as long as the _step itself_ exits 0. Pre-existing failures exit non-zero, so technically this _should_ block — but in practice, if the workflow was already passing with these failures (e.g., tests were added broken in the same commit that introduced the CI config), the failure becomes the "known state."

**Missing automation:** A baseline health check that asserts the test suite is at zero failures _before_ evaluating a new change. Alternatively, a nightly/weekly scheduled run that fails loudly if any test fails, separate from PR-gated CI.

---

#### 2. Six Production Modules Not in Coverage Tracking → Manual Config, No Validation

**What automation exists:** `pyproject.toml` `[tool.coverage.run].source` is a hand-maintained list of 22 module names. `validate_test_coverage()` (validate.py line 1090) checks that `scripts/programstart_*.py` files have matching test files — but it does **not** check whether those scripts are in the coverage `source` list.

**Why it didn't catch the gap:** Adding a new script to `scripts/` is two manual steps:

1. Create the script ✓ (developer does this naturally)
2. Add `"scripts.<module_name>"` to `pyproject.toml` ✗ (no automation reminds or enforces)

The validator only checks for test file _existence_, not coverage config _registration_. Six production modules were added over time with test files (step 1 done) but never registered for coverage tracking (step 2 missed). Coverage reports simply omitted them — the `scripts.programstart_serve` module didn't appear in `pytest --cov` output at all, so its 2,450 lines were invisible.

**Missing automation:** A `validate_coverage_source_completeness()` check that compares `scripts/programstart_*.py` glob against `[tool.coverage.run].source` entries and flags any script that exists on disk but is not in the source list.

---

#### 3. Four Modules Below 90% Coverage → Aggregate-Only Threshold

**What automation exists:** `pyproject.toml` sets `fail_under = 80` — a single threshold applied to the **aggregate** TOTAL across all tracked modules. No per-module threshold exists.

**Why it didn't catch the gap:** A module at 70% coverage passes CI as long as the weighted aggregate stays above 80%. With 22 modules averaging 88%, one module at 70% barely dents the aggregate. The `coverage report` command exits 0 if the TOTAL line is ≥80%, regardless of individual module scores.

**Evidence from pyproject.toml (lines 155–158):**
```toml
[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 80
```

No `[tool.coverage:run]` per-module overrides. No post-coverage script that parses per-module output.

**Missing automation:** Per-module coverage enforcement. Options:

- Coverage.py doesn't natively support per-module `fail_under`, but a post-test script could parse `coverage json` output and flag any module below a module-level threshold (e.g., 85%).
- Alternatively, a validate check that reads `.coverage` data and reports modules below a configurable per-module floor.

---

#### 4. Missing ADRs for DEC-005 and DEC-006 → Warnings Exit 0

**What automation exists:** `validate_adr_coverage()` (validate.py line 1058) checks every DECISION_LOG.md entry for a matching ADR file in `docs/decisions/`. Missing ADRs are added to the `warnings` list. The main function (validate.py line 1306–1311):

```python
print(f"Validation passed for check: {args.check}")
if warnings:
    print("Warnings:")
    for warning in warnings:
        print(f"- {warning}")
return 0  # ← exits 0 even with warnings
```

**Why it didn't catch the gap:** Warnings are informational. They print to stdout but **do not affect the exit code**. CI runs `uv run programstart validate --check all` (process-guardrails.yml line 156) and checks the exit code — which is 0 when only warnings exist. The warnings appear in CI logs but nobody reads CI logs unless a step fails.

**There is no `--strict` flag.** If there were, CI could run `validate --check all --strict` to treat warnings as errors.

**Missing automation:** A `--strict` mode for `validate` that returns exit code 1 when warnings are present. Then selective use in CI: `validate --check all --strict` for merge-blocking validation.

---

#### 5. Drift Notes (FILE_INDEX.md, FEASIBILITY.md) → Notes Exit 0

**What automation exists:** `evaluate_drift()` (drift_check.py) returns two lists: `violations` (exit 1) and `notes` (informational). The `main()` function (drift_check.py lines 118–134):

```python
if violations:
    print("Drift check failed:")
    ...
    return 1

print("Drift check passed.")
if notes:
    print("Notes:")
    ...
return 0  # ← notes don't block
```

**Why it didn't catch the gap:** Same pattern as validate warnings. Notes are printed but exit 0. CI runs `uv run programstart drift` (process-guardrails.yml line 168) and sees exit 0. Authority files were modified without updating their dependents, producing drift notes — but notes are designed to be non-blocking.

**There is no `--strict` flag.** Drift notes are genuinely informational in some cases (e.g., a cosmetic authority file change that doesn't materially affect dependents), so making them always-blocking is wrong. But there's no way to opt into strict mode when you _want_ a clean baseline.

**Missing automation:** A `--strict` flag for `drift` that treats notes as violations. CI could use `drift --strict` on the main branch to enforce a clean baseline, with `drift` (non-strict) on feature branches where drift notes may be in-progress.

---

#### 6. `check_commit_msg.py` Has No Test File → Incomplete Pattern Matching

**What automation exists:** `validate_test_coverage()` (validate.py line 1090) globs `scripts/programstart_*.py` and checks for matching `tests/test_programstart_*.py` files. Smoke scripts (`*_smoke.py`) are excluded.

```python
for script in sorted(scripts_dir.glob("programstart_*.py")):
    if script.name.endswith("_smoke.py"):
        continue
    test_file = tests_dir / f"test_{script.name}"
```

**Why it didn't catch the gap:** The glob pattern is `programstart_*.py`. The file `check_commit_msg.py` does not match this pattern — it doesn't start with `programstart_`. The validator literally cannot see it.

This is the only production script that breaks the naming convention. It's a pre-commit hook with a different name because it runs as a standalone commit-msg hook (not part of the `programstart` CLI).

**Missing automation:** Broaden the glob to cover _all_ non-infrastructure scripts in `scripts/`, or maintain an explicit exclusion list of scripts that don't need tests (smoke helpers, `__init__`) and validate everything else.

---

### Systemic Patterns

The six individual gaps reduce to **four systemic weaknesses** in the automation safety net:

| # | Systemic Gap | Issues Caused | Root Cause |
|---|---|---|---|
| **S-1** | Warnings and notes are non-blocking | #4 (ADRs), #5 (drift) | `validate` and `drift` both have a two-tier severity model (problems → exit 1, warnings/notes → exit 0) with no `--strict` flag to opt into stricter enforcement. CI runs the non-strict versions. |
| **S-2** | Coverage config is manually maintained with no validation | #2 (6 modules untracked), #3 (no per-module floor) | `pyproject.toml [tool.coverage.run].source` is a hand-edited list. No automation cross-checks it against the actual scripts directory. No per-module enforcement exists. |
| **S-3** | Test-file discovery uses a single naming pattern | #6 (check_commit_msg) | `validate_test_coverage()` only globs `programstart_*.py`, missing scripts with different naming conventions. |
| **S-4** | No baseline enforcement | #1 (3 pre-existing failures) | CI detects regressions introduced by a commit but doesn't assert the entire suite was green beforehand. Pre-existing failures persist indefinitely. |

### What Would Fix This

These are the minimum automation additions that would have prevented all six issues:

| Fix | Prevents | Effort | Description |
|---|---|---|---|
| **Add `--strict` flag to `validate` and `drift`** | S-1 (#4, #5) | Low | One argument + one `if` in each script. CI uses `--strict` on main. |
| **Add `validate_coverage_source_completeness()` check** | S-2 (#2) | Low | Glob `scripts/programstart_*.py` + `scripts/check_*.py`, compare against `pyproject.toml source` list, flag missing entries. ~20 lines. |
| **Add per-module coverage check** | S-2 (#3) | Medium | Post-test script that parses `coverage json` and flags modules below a per-module floor (e.g., 85%). ~40 lines. |
| **Broaden test-file discovery pattern** | S-3 (#6) | Low | Change glob from `programstart_*.py` to `*.py`, add explicit exclusion list for `__init__.py` and smoke scripts. ~5 lines changed. |
| **Add scheduled baseline health check** | S-4 (#1) | Low | A weekly CI workflow that runs `pytest -x --tb=short` and fails on _any_ failure, regardless of which commit introduced it. ~15 lines of YAML. |

### Why This Matters

The PROGRAMSTART system is designed around authority models, sync rules, and validation gates — all of which work correctly for their intended scope. But the validation _meta-layer_ (who validates the validators?) has blind spots:

- **The validator doesn't validate its own config.** Coverage tracking config, test discovery patterns, and ADR completeness are side-channels that slip through the main validation gate.
- **Informational output is treated as non-actionable.** Warnings and notes are printed to stdout in formats that look actionable ("DEC-005 has no ADR"), but the exit code says "all clear." The UI communicates urgency that the automation doesn't enforce.
- **CI mirrors local behavior.** When `validate --check all` exits 0 locally, it exits 0 in CI. There's no opportunity for CI to be stricter than the local developer experience — because no `--strict` flag exists.

The good news: every one of these gaps is small (5–40 lines of code each) and fits naturally into the existing validate/drift architecture. The `--strict` flag alone would have caught issues #4 and #5 the moment they were introduced.
