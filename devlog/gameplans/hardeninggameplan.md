# Hardening Gameplan — Post-Enhancement Coverage, Observability, and Defence

Purpose: Prioritized hardening plan for all items deferred from Phase N of `enhancegameplan.md` plus new coverage gaps identified from the post-enhancement-gameplan baseline. Phases are ordered by severity, dependency, and value impact. Each phase is scoped for a single execution session.
Status: **NOT STARTED**
Authority: Non-canonical working plan derived from `devlog/gameplans/enhancegameplan.md` Phase N deferred items, post-Phase-N coverage run (1288 tests, 93.19%, 2026-04-14), and `config/process-registry.json`.
Last updated: 2026-04-14

---

## 1. Current State

Baseline recorded 2026-04-14 (post enhancegameplan Phase N — commit `df7f5e8`):

- **1288 tests**, **0 failures**, **1 warning**
- **93.19% aggregate coverage** on 30 modules, `fail_under = 90`
- `programstart validate --check all` PASSES
- `programstart drift` PASSES
- All 14 Phases A–N from `enhancegameplan.md` COMPLETE

### Coverage Snapshot (post-Phase-N)

| Module | Coverage | Uncovered Lines |
|---|---|---|
| validate.py | 94% | 83-84, 136, 162, 235-236, 273, 333, 410, 530-535, 556, 622, 625, 673, 716, 720, 793-798, 797, 815, 842, 860, 935, 949, 952, 954, 961, 968-969, 993, 996, 999, 1005, 1075, 1081-1097, 1112, 1130-1136, 1142, 1157, 1176, 1179, 1387, 1389, 1397, 1417, 1423, 1425, 1429 |
| recommend.py | 93% | 143, 180, 365-371, 506, 542-549, 555, 577, 581-583, 634, 741, 787, 799, 921, 1050-1052, 1116, 1211, 1233, 1248-1254, 1262, 1264, 1305-1310, 1410-1430 |
| research_delta.py | 92% | 101, 111, 114-115, 184, 188, 244, 258, 273, 309, 385-387 |
| common.py | 92% | 33-35, 129-132, 223, 376, 402, 404, 436, 442, 445, 448 |
| refresh_integrity.py | 91% | 47, 53-54, 61, 74, 96-106 |
| prompt_eval.py | 91% | 79, 86, 118, 125-134, 136, 139, 200, 202, 227-228, 232, 254, 274 |
| create.py | 90% | 72, 88, 90, 127, 143, 149, 191, 195, 207, 259, 264, 303, 320, 338-341, 382, 812, 825-826, 907-908, 955-960, 1006-1008, 1024-1026, 1036-1040, 1047, 1050 |
| workflow_state.py | 94% | 131-132, 180-182, 380, 387-391, 438-440, 516-518 |
| **serve.py** | **83%** | 195-207, 240-241, 268, 305, 347-349, 369-370, 408-436, 451-472, 545, 572-576, 580-585, 606, 608, 624, 632-637, 660, 702-722, 742, 839-843, 851-871, 875-881 |
| **retrieval.py** | **84%** | 177-179, 283-281, 469-492 (ChromaDB — permanently blocked), 500-527 (ChromaDB — permanently blocked), 556-563, 729-746, 750-759, 779, 818, 821, 909-919, 937 |

---

## 2. Prioritized Gap Registry

### P0 — Coverage Deficits (below 90% target, or within 1% of it)

| ID | Gap | Module | Missing Lines | Phase |
|---|---|---|---|---|
| **COV-06** | serve.py at 83% — HTTP handler, advance/save error paths, update_tracker_slice | serve.py | 77 | C |
| **COV-07** | retrieval.py at 84% — LiteLLM paths (mockable); ChromaDB (469-527, permanently blocked) | retrieval.py | 63 | C |
| **COV-03** | create.py at 90% — factory plan edge cases, output generation error paths | create.py | 25 | A |

### P1 — Low-Hanging Coverage Push (90–94%, all unblocked)

| ID | Gap | Module | Missing Lines | Phase |
|---|---|---|---|---|
| **COV-01** | common.py at 92% — timeout path, state path edge cases, FileLock error branch | common.py | 15 | A |
| **COV-02** | workflow_state.py at 94% — advance edge cases, rollback paths | workflow_state.py | 14 | A |
| **COV-08a** | research_delta.py at 92% — subprocess error paths | research_delta.py | 10 | A |
| **COV-08b** | refresh_integrity.py at 91% — manifest write edge cases | refresh_integrity.py | 8 | A |
| **COV-08c** | prompt_eval.py at 91% — scenario load/run error paths | prompt_eval.py | 15 | A |
| **COV-04** | validate.py at 94% — edge cases across all `--check` modes | validate.py | 47 | B |
| **COV-05** | recommend.py at 93% — scoring, rendering, conditional recommendation branches | recommend.py | 44 | B |

### P2 — Structural Hardening (code quality, observability)

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **KB-2** | BM25 retrieval has no relevance threshold — always returns all above-zero results | LOW | §15 | D |
| **B-1** | Bootstrap header extraction is fragile — line-count assumptions rather than marker/regex | LOW | §16 | D |
| **SD-2** | No explicit versioning contract between process-registry.json and scripts | LOW | §18 | D |
| **W-4** | `workflow_guidance` entries don't reference expected outputs — no enforcement | LOW | §12 | D |
| **S-3** | No sync rule enforcement for `pyproject.toml` ↔ `requirements.txt` versions | LOW | §8 | D |
| **H-2** | No structured logging anywhere — bare `print()` used throughout non-CLI paths | LOW | §1 | E |

### P3 — Feature Gaps

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **W-2** | No stage expiry/staleness tracking — stages can be inactive indefinitely with no flag | LOW | §12 | F |
| **W-3** | USERJOURNEY phases have no entry criteria — phases start with no validation of prerequisites | LOW | §12 | F |
| **G-3** | No git hook for branch protection — direct push to main unguarded | LOW | §11 | F |
| **KB-3** | No `programstart kb` subcommand — knowledge base not queryable from CLI | LOW | §15 | G |
| **F-3** | No `programstart diff` command — no way to compare state between snapshots | LOW | §5 | G |
| **F-4** | No `programstart state rollback` command — no way to restore previous workflow state | LOW | §5 | G |

### P4 — Test Quality & Process Hygiene

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **R-6** | `copilot-instructions.md` rules not runtime-enforceable — no tests validate key rules | INFO | §6 | H |
| **T-6** | No performance regression tests — no benchmark for recommend, retrieval, or context | LOW | §3 | H |
| **SD-3** | `devlog/` exempt from rules with no retention policy — unbounded accumulation | LOW | §18 | I |
| **SD-4** | `BACKUPS/` has one manually created snapshot — no automation | LOW | §18 | I |
| **UI-3** | Golden screenshot tests are Linux-only — Windows CI always skips them | LOW | §14 | H |

### P5 — Strategic / Large Scope

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **B-2** | `programstart_create.py` is 1040+ LoC single file — maintainability risk | LOW | §16 | J |
| **SD-1** | `process-registry.json` is 900+ lines — single point of failure, $include pattern needed | MEDIUM | §18 | J |
| **T-5** | No mutation testing — correctness of core business logic not verified by mutation | LOW | §3 | J |
| **S-5** | Prompt builder Mode B — arbitrary repos, not just bootstrapped | Strategic | §25 | J |
| **S-6** | Registry Pydantic models — `load_registry()` returns validated typed model | Strategic | §25 | J |
| **S-7** | `programstart sync --from-template` — prompt update channel | Strategic | §25 | J |

---

## 3. Phase Sequence

| Phase | Gap(s) | Type | Est. edits | Target |
|---|---|---|---|---|
| A | COV-01, COV-02, COV-03, COV-08a/b/c | Coverage push — small modules | 6-8 test files | 94%+ coverage |
| B | COV-04, COV-05 | Coverage push — validate & recommend | 2-3 test files | 95%+ coverage |
| C | COV-06, COV-07 | Coverage push — serve & retrieval | 2-3 test files | 87%/90%+ |
| D | KB-2, B-1, SD-2, W-4, S-3 | Structural hardening | 4-6 files | All checks pass |
| E | H-2 | Structured logging pass | 10-15 scripts | Observability |
| F | W-2, W-3, G-3 | Feature gaps & guards | 3-4 files | New capabilities |
| G | KB-3, F-3, F-4 | Feature gaps — medium | 4-6 files | New commands |
| H | R-6, T-6, UI-3 | Test quality | 3-4 test files | Quality gates |
| I | SD-3, SD-4 | Process hygiene | 2-3 files | Automation |
| J | B-2, SD-1, T-5, S-5, S-6, S-7 | Strategic (large) | Multiple | Future-facing |

---

## 4. Detailed Phase Instructions

### ✅ Phase A: Coverage Push — Small Unblocked Modules (COV-01, COV-02, COV-03, COV-08a/b/c)

**Status**: COMPLETE — commit `cfd46fa`
**Result**: common 92%→95%, workflow_state 94%→97%, research_delta 92%→95%, refresh_integrity 91%→99%, prompt_eval 91%→94%. Total 93.19%→93.75%.

#### A-1: Cover common.py missing lines (COV-01)

**Pre-flight**: Read `scripts/programstart_common.py` at lines 33-35 (standalone guard), 129-132 (timeout check in `run_command`), 223 (unused pattern branch), 376, 402, 404 (state path edge cases), 436, 442, 445, 448 (error branches — likely `write_json` retry failure paths).

**Edits**: In `tests/test_programstart_common.py` (or `tests/test_common.py`), add test methods covering:
1. The standalone `if __name__ == "__main__"` guard at lines 33-35 — skip if not testable.
2. The timeout path in `run_command` — mock `subprocess.run` to raise `subprocess.TimeoutExpired`, assert the error return.
3. State path edge cases at 376, 402, 404 — likely bad/missing path conditions; mock `Path.exists()` or pass bad paths.
4. `write_json` retry failure branches at 436-448 — mock `PermissionError` to persist beyond retry limit; assert exception propagates correctly.

**Verification**:
```powershell
uv run pytest tests/ -k "common" --cov=scripts/programstart_common --cov-report=term-missing --tb=short
```
Expected: common.py ≥ 95%.

---

#### A-2: Cover workflow_state.py missing lines (COV-02)

**Pre-flight**: Read `scripts/programstart_workflow_state.py` at lines 131-132 (advance validation failure), 180-182 (state load error path), 387-391 (rollback or integrity check), 438-440 (write failure), 516-518 (CLI edge path).

**Edits**: In `tests/test_programstart_workflow_state.py` (or equivalent), add tests covering:
1. Lines 131-132 — likely a guard condition when advancing fails early; test with bad state.
2. Lines 180-182 — state load error path; corrupt or missing state file.
3. Lines 387-391 — integrity/rollback branch; simulate bad checksum or missing backup.
4. Lines 438-440 — write failure; mock `write_json` to raise.
5. Lines 516-518 — CLI `__main__` guard or argument-parsing edge case.

**Verification**:
```powershell
uv run pytest tests/ -k "workflow_state" --cov=scripts/programstart_workflow_state --cov-report=term-missing --tb=short
```
Expected: workflow_state.py ≥ 96%.

---

#### A-3: Cover create.py missing lines (COV-03)

**Pre-flight**: Read `scripts/programstart_create.py` at lines 72, 88, 90 (early validation guard), 127, 143, 149 (factory plan generation errors), 191, 195, 207 (output writing edge cases), 259, 264, 303, 320 (shape-specific generation paths), 338-341, 382 (plan body edge cases), 812, 825-826 (late-stage generation), 907-908, 955-960, 1006-1008, 1024-1026, 1036-1040, 1047, 1050 (end-of-file generation or write paths).

**Edits**: In `tests/test_programstart_create.py` (or equivalent), add tests covering:
1. Lines 72-90 — early validation guard (missing required arg or bad shape); assert error exit.
2. Lines 127-149 — factory plan generation error paths; mock a file write to fail.
3. Lines 191-207 — output writing edge cases; unavailable output directory.
4. Lines 338-382 — shape-specific plan body edge cases; test with uncommon shape values.
5. Lines 812, 825-826, 907-908 — late-stage generation paths; trigger via specific shape/output combinations.
6. Lines 955-1050 — end-of-file paths; test complete generation flow for a less-exercised shape.

**Verification**:
```powershell
uv run pytest tests/ -k "create" --cov=scripts/programstart_create --cov-report=term-missing --tb=short
```
Expected: create.py ≥ 93%.

---

#### A-4: Cover research_delta, refresh_integrity, prompt_eval (COV-08a/b/c)

**Pre-flight**:
- Read `scripts/programstart_research_delta.py` at lines 101, 111, 114-115 (subprocess error), 184, 188 (file write edge case), 244, 258, 273 (delta computation edge), 309, 385-387 (output path).
- Read `scripts/programstart_refresh_integrity.py` at lines 47, 53-54, 61 (file I/O guards), 74 (manifest write), 96-106 (integrity check branch).
- Read `scripts/programstart_prompt_eval.py` at lines 79, 86 (early exit paths), 118, 125-134 (scenario load error), 136, 139 (eval runner edge), 200, 202 (result write), 227-228, 232, 254, 274 (output formatting).

**Edits**: Add targeted tests in each module's test file (or add to `tests/test_audit_fixes.py` if no dedicated file exists):
1. `research_delta` — mock `subprocess.run` to raise/return non-zero; test empty-delta edge case.
2. `refresh_integrity` — mock `Path.glob` to return empty list (no scripts found); test write failure.
3. `prompt_eval` — mock scenario file missing; mock eval runner returning empty results; test output formatting with zero scenarios.

**Verification**:
```powershell
uv run pytest tests/ -k "research_delta or refresh_integrity or prompt_eval" --cov-report=term-missing --tb=short 2>&1 | Select-String "research_delta|refresh_integrity|prompt_eval|PASSED|FAILED|ERROR"
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```
Expected: Each module ≥ 94%. Total test count increases.

---

**Phase A verification**:
```powershell
uv run pytest --cov --cov-report=term --tb=no -q 2>&1 | Select-String "common|workflow_state|create|research_delta|refresh_integrity|prompt_eval|TOTAL"
uv run programstart validate --check all
uv run programstart drift
```
Expected: All targeted modules ≥ 94%. Total ≥ 93.5%. validate PASS, drift PASS.

---

### ✅ Phase B: Coverage Push — Validate & Recommend (COV-04, COV-05) — COMPLETE

**Goal**: Push validate.py (94%→97%) and recommend.py (93%→96%) by covering the high-value missing branches in each.

#### B-1: Cover validate.py missing lines (COV-04)

**Pre-flight**: Read `scripts/programstart_validate.py` at all uncovered ranges: 83-84, 136, 162, 235-236, 273, 333, 410 (early guard conditions in different `--check` modes), 530-535, 556 (schema validation edge), 622, 625 (authority sync edge), 673, 716, 720 (planning references edge), 793-798, 815, 842, 860 (workflow-state check edge), 935, 949, 952, 954, 961, 968-969 (bootstrap-assets check), 993, 996, 999, 1005 (validate-all accumulation), 1075, 1081-1097, 1112, 1130-1136, 1142, 1157, 1176, 1179 (comprehensive validation passes/failures), 1387, 1389, 1397, 1417, 1423, 1425, 1429 (late CLI and output paths).

**Edits**: In `tests/test_programstart_validate.py` (or `tests/validate/`), group uncovered lines by `--check` mode and add parametrized test cases:
1. Each `--check` mode (schema, authority-sync, planning-references, workflow-state, bootstrap-assets) should have at least one test that triggers the failure path of its guard condition.
2. Test `--check all` when one sub-check fails — assert accumulation and reporting.
3. Test the late CLI paths (1387-1429) by invoking the `main()` CLI entry point with arguments that trigger edge conditions (unknown check name, `--strict` with warnings, empty project directory).

**Verification**:
```powershell
uv run pytest tests/ -k "validate" --cov=scripts/programstart_validate --cov-report=term-missing --tb=short 2>&1 | Select-String "validate|PASSED|FAILED"
```
Expected: validate.py ≥ 97%.

---

#### B-2: Cover recommend.py missing lines (COV-05)

**Pre-flight**: Read `scripts/programstart_recommend.py` at: 143, 180 (early guard for shape or input validation), 365-371 (scoring branch for edge case shape), 506 (recommendation assembly edge), 542-549, 555 (conditional recommendation block), 577, 581-583 (coverage warning logic), 634 (threshold guard), 741 (stage relevance filter), 787, 799 (output formatter), 921 (CLI output format), 1050-1052 (alternative shape path), 1116 (late-stage recommendation), 1211, 1233 (advanced scoring branch), 1248-1254, 1262, 1264 (recommendation finalization), 1305-1310 (cross-shape advisory), 1410-1430 (CLI and output paths).

**Edits**: In `tests/test_programstart_recommend.py` (or add to existing test file):
1. Lines 143, 180 — test early guard paths with missing or malformed inputs.
2. Lines 365-371 — test scoring for an edge-case shape (no-code/CLI hybrid) that triggers the alternative scoring path.
3. Lines 542-549, 555 — test recommendation path where coverage_warnings is empty vs. populated.
4. Lines 577-583 — test coverage_warnings logic with shape + stage combinations that trigger the branch.
5. Lines 1248-1254, 1262-1264 — test recommendation finalization for shapes that hit the deep advisory path.
6. Lines 1410-1430 — test CLI `main()` with `--json` flag and `--system` argument edge cases.

**Verification**:
```powershell
uv run pytest tests/ -k "recommend" --cov=scripts/programstart_recommend --cov-report=term-missing --tb=short 2>&1 | Select-String "recommend|PASSED|FAILED"
```
Expected: recommend.py ≥ 96%.

---

**Phase B verification**:
```powershell
uv run pytest --cov --cov-report=term --tb=no -q 2>&1 | Select-String "validate|recommend|TOTAL"
uv run programstart validate --check all
uv run programstart drift
```
Expected: validate.py ≥ 97%, recommend.py ≥ 96%, total ≥ 94%. validate PASS, drift PASS.

---

### ✅ Phase C: Coverage Push — Serve & Retrieval (COV-06, COV-07) — COMPLETE

**Goal**: Push serve.py (83%→90%) and retrieval.py (84%→88%). serve.py is the biggest single coverage gap. retrieval.py has a permanently blocked ChromaDB block (469-527) that cannot be covered without the optional dependency.

#### C-1: Cover serve.py missing lines (COV-06)

**Pre-flight**: Read `scripts/programstart_serve.py` at:
- Lines 195-207 — `get_state_json`: failure path when state file is missing or corrupt.
- Lines 240-241 — response-writing edge case.
- Lines 268, 305 — query parameter parsing guards.
- Lines 347-349 — request handler guard condition.
- Lines 369-370, 408-436 — advance workflow request handler (including the advance call, error marshaling).
- Lines 451-472 — save/patch handler paths.
- Lines 545 — standalone subprocess error path.
- Lines 572-576 — `advance_workflow_with_signoff` error path.
- Lines 580-585 — error response marshaling.
- Lines 606, 608, 624, 632-637, 660 — `save_workflow_signoff` path variants.
- Lines 702-722, 742 — `update_implementation_tracker_slice` full block.
- Lines 839-843 — bootstrap validation block.
- Lines 851-871, 875-881 — request handler exception paths.

**Edits**: In `tests/test_programstart_serve.py` (or `tests/serve/`), add tests using the existing test HTTP server or mock approach:
1. Test `get_state_json` endpoint with missing state file — expect 404 or error JSON.
2. Test `advance_workflow_with_signoff` endpoint: mock `advance()` to raise, assert error response JSON structure.
3. Test `save_workflow_signoff` endpoint with each missing-field variant (no signoff_by, no stage, no timestamp) — assert 400 response.
4. Test `update_implementation_tracker_slice` endpoint: mock file write to fail; test with valid slice data.
5. Test bootstrap validation block: call the endpoint with/without a bootstrapped project path.
6. Test request handler exception paths (851-881): send malformed JSON bodies to POST endpoints.

**Verification**:
```powershell
uv run pytest tests/ -k "serve" --cov=scripts/programstart_serve --cov-report=term-missing --tb=short 2>&1 | Select-String "serve|PASSED|FAILED"
```
Expected: serve.py ≥ 90%. Note: lines 469-492 and 500-527 in retrieval.py are ChromaDB-only and will remain uncovered — this is acceptable and should be documented in the test file as a comment.

---

#### C-2: Cover retrieval.py mockable paths (COV-07)

**Pre-flight**: Read `scripts/programstart_retrieval.py` at:
- Lines 177-179, 283-281, 297-295, 308-298 — guard branches before ChromaDB calls.
- Lines 556-563 — error path in retrieval pipeline.
- Lines 729-746, 750-759 — LiteLLM `_generate_litellm` and `_generate_structured` methods.
- Lines 779, 818, 821 — generation error paths.
- Lines 909-919, 937 — CLI `main()` subcommands (likely `ask` and `search` sub-subcommands).

**Edits**: In `tests/test_programstart_retrieval.py`:
1. Mock `litellm.completion` to exercise lines 729-746 (`_generate_litellm`). Assert the response is parsed correctly.
2. Mock `litellm.completion` to raise `litellm.APIError` and cover the error path at line 779.
3. Mock `litellm.completion` for `_generate_structured` (750-759) — return a mock JSON response.
4. Test CLI `main()` with `ask` and `search` subcommands (909-919, 937) using `subprocess` or `click`'s `CliRunner`.
5. Test the guard branches at 177-179 and 556-563 by passing `chromadb_available=False` or equivalent flag.

Note: lines 469-527 are permanently blocked (require `chromadb` installed). Add a comment in the test file explaining why they are excluded from the coverage target.

**Verification**:
```powershell
uv run pytest tests/ -k "retrieval" --cov=scripts/programstart_retrieval --cov-report=term-missing --tb=short 2>&1 | Select-String "retrieval|PASSED|FAILED"
```
Expected: retrieval.py ≥ 88% (ChromaDB block at 469-527 is permanently excluded).

---

**Phase C verification**:
```powershell
uv run pytest --cov --cov-report=term --tb=no -q 2>&1 | Select-String "serve|retrieval|TOTAL"
uv run programstart validate --check all
uv run programstart drift
```
Expected: serve.py ≥ 90%, retrieval.py ≥ 88%, total ≥ 95%. validate PASS, drift PASS.

---

### ✅ Phase D: Structural Hardening (KB-2, B-1, SD-2, W-4, S-3) — COMPLETE (D-4 deferred to Phase J)

**Goal**: Fix 5 low-severity structural defects that affect correctness or maintainability. None require schema changes.

#### D-1: Add BM25 relevance threshold (KB-2)

**Pre-flight**: Read `scripts/programstart_retrieval.py` at the `LexicalSearcher.search()` method (likely around line 200–350). Identify where results are aggregated and returned after BM25 scoring. Confirm the method signature and return type.

**Edits**:
1. Add a `min_score: float = 0.0` parameter to `LexicalSearcher.search()`.
2. Before returning results, filter out any (doc, score) pairs where `score <= min_score`.
3. Add a test in `tests/test_programstart_retrieval.py` that verifies: (a) all results returned when `min_score=0.0`, (b) zero-score results filtered out when `min_score=0.01`, (c) `min_score` default does not break existing callers.

**Verification**:
```powershell
uv run pytest tests/ -k "retrieval and lexical" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### D-2: Harden bootstrap header extraction (B-1)

**Pre-flight**: Read `scripts/programstart_bootstrap.py` — find the header extraction logic (likely loads a template file and parses leading metadata lines). Identify the line-count assumption or fixed-offset that makes it fragile.

**Edits**:
1. Replace line-count-based extraction with a marker-based approach: define a sentinel string (e.g., `---`) or regex pattern that reliably identifies where the header ends.
2. Add a test in `tests/test_programstart_bootstrap.py` that verifies extraction works when a new non-blank line is inserted before the header end marker.
3. Ensure the existing passing tests still pass.

**Verification**:
```powershell
uv run pytest tests/ -k "bootstrap" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### D-3: Add schema_version contract test (SD-2)

**Pre-flight**: Read `config/process-registry.json` — find the `version` or `schema_version` field at the top level. Read `scripts/programstart_common.py` or `scripts/programstart_validate.py` — find where `load_registry()` is called, check if the version is asserted.

**Edits**:
1. Add a test in `tests/test_schema_conformance.py` (or create it) that:
   a. Loads `config/process-registry.json`.
   b. Asserts a `version` (or `schema_version`) key exists.
   c. Asserts the value matches a defined minimum version (read it from the registry at test time, not hardcoded).
2. Add a check in `scripts/programstart_common.py` `load_registry()` that warns (not errors) if the registry lacks a `version` key.

**Verification**:
```powershell
uv run pytest tests/ -k "schema" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### D-4: Enforce workflow_guidance expected_outputs reference (W-4)

**Pre-flight**: Read `config/process-registry.json` — find the `workflow_guidance` entries for both `programbuild` and `userjourney` systems. Check if any entries already have an `expected_outputs` field. Read `schemas/process-registry.schema.json` to see if `expected_outputs` is defined in the schema.

**Edits**:
1. Add `expected_outputs` as an optional array field in `schemas/process-registry.schema.json` for `workflow_guidance` items.
2. Add at least 3 representative `expected_outputs` values to `workflow_guidance` entries in `config/process-registry.json` (for stages/steps that have well-defined primary outputs).
3. Add a test in `tests/test_schema_conformance.py` that asserts each `workflow_guidance` entry with a non-empty `step_files` list also has a non-empty `expected_outputs` list.
4. If the test cannot realistically pass for all stages yet, add an exclusion list with a TODO comment.

**Verification**:
```powershell
uv run pre-commit run check-json --all-files
uv run pytest tests/ -k "schema" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### D-5: Add sync rule enforcement test for pyproject.toml ↔ requirements.txt (S-3)

**Pre-flight**: Read `pyproject.toml` `[project.dependencies]` and `requirements.txt`. Check if the versions are consistent or if `requirements.txt` is derived from `pyproject.toml`. Read `config/process-registry.json` `sync_rules` to see if this pairing is already tracked.

**Edits**:
1. Add a test in `tests/test_schema_conformance.py` (or `tests/test_audit_fixes.py`) that:
   a. Parses `pyproject.toml` `[project.dependencies]` package names.
   b. Parses `requirements.txt` package names.
   c. Asserts every package in `requirements.txt` is also in `pyproject.toml` dependencies (one-way: requirements.txt is a subset).
2. If the existing `requirements.txt` was generated from `uv export`, add a comment explaining the derivation.
3. Add a `sync_rules` entry in `config/process-registry.json` documenting `pyproject.toml` as the authority over `requirements.txt`.

**Verification**:
```powershell
uv run pre-commit run check-json --all-files
uv run pytest tests/ -k "schema or sync" --tb=short
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

**Phase D verification**:
```powershell
uv run pre-commit run --all-files
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```
Expected: All checks pass. validate PASS, drift PASS.

---

### ✅ Phase E: Structured Logging Pass (H-2) — COMPLETE

**Goal**: Replace bare `print()` calls in non-CLI paths of all production scripts with `logging.getLogger(__name__)`. CLI entry points (`main()` functions and their direct output helpers) may retain `print()`. This improves observability and allows log level filtering.

#### E-1: Add structured logging to production scripts

**Pre-flight**: Run `grep -rl "print(" scripts/ --include="*.py"` to enumerate scripts with `print()`. For each script, identify which `print()` calls are CLI output (should stay `print()`) vs. internal diagnostic/error paths (should become `logger.warning()` or `logger.error()`).

**Edits**:
1. At the top of each production script body (not `__init__.py`), add `import logging` and `logger = logging.getLogger(__name__)` after existing imports.
2. Replace internal diagnostic `print()` calls (not in `main()` or click command functions) with appropriate log levels:
   - Informational progress: `logger.info()`
   - Warnings about missing optional inputs: `logger.warning()`
   - Errors before fallback: `logger.error()`
   - Debug-only tracing: `logger.debug()`
3. Do NOT replace `print()` calls in `main()`, `@click.command()` handlers, or any function whose purpose is CLI output. These remain `print()` for user-facing output.
4. Configure basicConfig in the CLI entry point modules (e.g., `programstart_cli.py`) rather than in library modules.

**Order**: Apply per-module, alphabetically. Commit as a single `feat(logging): add structured logging to production scripts` commit once all scripts are done.

**Verification**:
```powershell
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
uv run programstart validate --check all
```
Tests should not be broken by this change (no behavioral change, only replacing bare prints with log calls in non-CLI paths). If a test was asserting printed output from an internal path, update the test to use `caplog` instead.

---

### Phase F: Feature Gaps & Guards (W-2, W-3, G-3)

**Goal**: Implement 3 small features that improve workflow observability and protection.

#### F-1: Stage expiry/staleness tracking in status output (W-2)

**Pre-flight**: Read `scripts/programstart_status.py` to understand how the current status display works, what date fields are available in the state JSON, and where stage summaries are printed.

**Edits**:
1. In `scripts/programstart_status.py`, read the `updated_at` or `last_advanced` timestamp from the state JSON for the active stage.
2. Calculate `days_inactive = (today - updated_at).days`.
3. If `days_inactive > 14` (2 weeks), append `[STALE — N days]` to the stage status line in the output.
4. Make the staleness threshold configurable via environment variable `PROGRAMSTART_STALE_DAYS` (default: 14).
5. Add a test in `tests/test_programstart_status.py` verifying: (a) stale label appears when last update > threshold, (b) no label when within threshold, (c) custom threshold via env var.

**Verification**:
```powershell
uv run pytest tests/ -k "status" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### F-2: USERJOURNEY phase entry criteria validation (W-3)

**Pre-flight**: Read `config/process-registry.json` `userjourney` `step_order` entries. Check if any already have an `entry_criteria` field. Read `USERJOURNEY/DELIVERY_GAMEPLAN.md` for the expected upstream phases for each step.

**Edits**:
1. Add `entry_criteria` as an optional array of step-name strings in `schemas/process-registry.schema.json` for `step_order` items.
2. Add `entry_criteria` to the first 3 USERJOURNEY `step_order` entries in `config/process-registry.json` (using the actual prerequisite step names from `DELIVERY_GAMEPLAN.md`).
3. Add a check in `scripts/programstart_validate.py` (or `scripts/programstart_workflow_state.py`) that, when advancing a USERJOURNEY step, verifies all `entry_criteria` steps are marked complete. Emit a warning (not hard failure) if not.
4. Add a test verifying the warning is emitted when advancing with incomplete entry criteria.

**Verification**:
```powershell
uv run pre-commit run check-json --all-files
uv run pytest tests/ -k "userjourney or entry_criteria or workflow_state" --tb=short
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### F-3: Git hook for main branch protection (G-3)

**Pre-flight**: List `.git/hooks/` to see what hooks already exist. Confirm whether a `pre-push` hook is present. Check `CONTRIBUTING.md` for existing branch protection rules.

**Edits**:
1. Create `.git/hooks/pre-push` (executable) that blocks direct push to `main` branch unless the environment variable `PROGRAMSTART_ALLOW_MAIN_PUSH=1` is set.
2. The hook script should be cross-platform (PowerShell and bash-compatible, or detect shell).
3. Create `scripts/install_hooks.py` that copies the hook to `.git/hooks/` and makes it executable, with a `--uninstall` flag.
4. Add `uv run python scripts/install_hooks.py` to the CONTRIBUTING.md setup steps (update `docs/toolchain.md` or CONTRIBUTING.md).
5. Add a test in `tests/test_audit_fixes.py` (or a new test file) that verifies `scripts/install_hooks.py` creates the expected file.

**Verification**:
```powershell
uv run python scripts/install_hooks.py --check
uv run pytest tests/ -k "hook or pre_push" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

**Phase F verification**:
```powershell
uv run pre-commit run --all-files
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```
Expected: All checks pass. New features tested.

---

### Phase G: Feature Gaps — Medium (KB-3, F-3, F-4)

**Goal**: Implement 3 medium-complexity new commands: `programstart kb`, `programstart diff`, and `programstart state rollback`.

#### G-1: Add `programstart kb` subcommand (KB-3)

**Pre-flight**: Read `scripts/programstart_cli.py` to find the command registration pattern. Read `scripts/programstart_retrieval.py` to find `LexicalSearcher.search()` and `SemanticSearcher.search()` entry points. Read `scripts/programstart_command_registry.py` to confirm the whitelist.

**Edits**:
1. Add `kb` command group to `scripts/programstart_cli.py` with subcommands:
   - `programstart kb search <query>` — lexical search via `LexicalSearcher`.
   - `programstart kb ask <question>` — semantic/generative search (if LLM configured) or lexical fallback.
2. Register `kb`, `kb:search`, `kb:ask` in `scripts/programstart_command_registry.py` whitelist.
3. Add tests in `tests/test_programstart_cli.py` (or `tests/test_kb_cli.py`) covering both subcommands with mock retriever.
4. Update `PROGRAMBUILD/ARCHITECTURE.md` if the command changes any documented contract.

**Verification**:
```powershell
uv run programstart kb search "architecture"
uv run pytest tests/ -k "kb" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### G-2: Add `programstart diff` command (F-3)

**Pre-flight**: Read `scripts/programstart_workflow_state.py` to understand the state JSON structure, what fields change between stages, and whether there are existing snapshot/backup files in `BACKUPS/`. Read `scripts/programstart_cli.py` for command registration pattern.

**Edits**:
1. Add `programstart diff [--from <snapshot-path>] [--to <snapshot-path>]` command to `scripts/programstart_cli.py`.
2. If no `--from`, use the last committed state (from `BACKUPS/` or git). If no `--to`, use the current state.
3. Output a human-readable diff of stage completion status, timestamps, and signoff changes.
4. Register in `scripts/programstart_command_registry.py`.
5. Add tests covering: diff with identical states shows no changes; diff between states shows changed fields; `--from` / `--to` path resolution.

**Verification**:
```powershell
uv run programstart diff
uv run pytest tests/ -k "diff" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### G-3: Add `programstart state rollback` command (F-4)

**Pre-flight**: Read `scripts/programstart_workflow_state.py` to find state write paths and understand current backup behavior. Read `BACKUPS/` to see what snapshot files exist. Confirm the state file path from the registry.

**Edits**:
1. Add `programstart state rollback [--to <snapshot-path>]` command.
2. Before rolling back, create a backup of the current state.
3. If `--to` is not provided, list available snapshots from `BACKUPS/` and prompt the user to select (or accept `--to last` to rollback to the most recent backup).
4. Require explicit `--confirm` flag to apply the rollback (no accidental rollbacks).
5. Register in `scripts/programstart_command_registry.py`.
6. Add tests covering: rollback creates backup before restoring; `--confirm` flag required; rollback with no snapshots shows a clear error.

**Verification**:
```powershell
uv run programstart state rollback --help
uv run pytest tests/ -k "rollback" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

**Phase G verification**:
```powershell
uv run pre-commit run --all-files
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```
Expected: All 3 new commands registered, tested, and working. All checks pass.

---

### Phase H: Test Quality (R-6, T-6, UI-3)

**Goal**: Improve test quality with rule-enforcement tests, performance benchmarks, and platform-portable golden screenshot tests.

#### H-1: Rule enforcement tests for copilot-instructions.md (R-6)

**Pre-flight**: Read `.github/copilot-instructions.md` and `.github/instructions/source-of-truth.instructions.md`. Identify 5-7 key rules that can be mechanically checked (e.g., a rule that says authority docs must be updated before dependent docs — check that `sync_rules` entries exist for every authority/dependent pair in the registry).

**Edits**: Add `tests/test_instruction_enforcement.py` with tests that:
1. Assert every file listed as a `sync_rules` `authority` in `process-registry.json` actually exists in the workspace.
2. Assert every `sync_rules` `dependents` entry also exists.
3. Assert `workflow_guidance` entries for both systems reference at least one file in `step_files`.
4. Assert `.github/copilot-instructions.md` references `config/process-registry.json` (instruction file is not totally disconnected from the registry).
5. Assert `.github/instructions/source-of-truth.instructions.md` mentions `programstart drift` (the core protocol is present).

**Verification**:
```powershell
uv run pytest tests/test_instruction_enforcement.py -v --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### H-2: Performance regression benchmarks (T-6)

**Pre-flight**: Read `scripts/programstart_recommend.py` `build_recommendation()` entry point. Read `scripts/programstart_retrieval.py` `LexicalSearcher.search()` and `build_context_index()`. Identify the minimal inputs needed to exercise each path in under 5 seconds.

**Edits**: Add `tests/test_performance_benchmarks.py` with benchmark tests using `time.perf_counter()`:
1. `test_build_recommendation_under_threshold` — call `build_recommendation()` with a minimal valid input; assert duration < 2.0 seconds.
2. `test_lexical_search_under_threshold` — call `LexicalSearcher.search("architecture")` on a mock index; assert duration ≤ 0.5 seconds.
3. `test_build_context_index_under_threshold` — call `build_context_index()` on a small file set; assert duration < 3.0 seconds.
4. Mark all three tests with `@pytest.mark.slow` so they can be excluded from the fast test run.
5. Add `slow` marker to `pyproject.toml` `[tool.pytest.ini_options] markers`.

**Verification**:
```powershell
uv run pytest tests/test_performance_benchmarks.py -v --tb=short -m slow
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### H-3: Windows-compatible golden screenshot tests (UI-3)

**Pre-flight**: Read the existing golden screenshot test file (likely `tests/test_dashboard_golden.py` or similar). Identify the Linux-specific dependency (likely `playwright` or a subprocess call to a Linux-only tool). Check what `pytest.mark.skipif` condition is used.

**Edits**:
1. If the golden screenshots rely on `playwright`, verify `playwright` supports Windows (it does). Replace the `skipif(sys.platform != "linux")` guard with a `skipif(not shutil.which("playwright") and not shutil.which("npx"))` check or a `requires_playwright` fixture.
2. If the skip is due to font rendering differences across platforms, use image-comparison tolerance (e.g., `pixel_diff_threshold=0.05`) rather than platform-exclusion.
3. Regenerate golden images on Windows if needed (add a `--update-goldens` flag to the test file).
4. Add a CI matrix entry or note in `.github/workflows/` about golden test requirements.

**Verification**:
```powershell
uv run pytest tests/ -k "golden" -v --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

**Phase H verification**:
```powershell
uv run pre-commit run --all-files
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

### Phase I: Process & Platform Hygiene (SD-3, SD-4)

**Goal**: Add a retention policy for `devlog/` and automate `BACKUPS/` snapshots.

#### I-1: devlog retention policy test (SD-3)

**Pre-flight**: Read `CONTRIBUTING.md` and `.github/copilot-instructions.md` for any existing retention guidance. List `devlog/` subdirectories to understand the current structure.

**Edits**:
1. Add a `tests/test_platform_hygiene.py` test: `test_devlog_retention_policy` — asserts that `devlog/` contains no files older than 365 days (based on `git log --follow --format="%ai"` last touch). Log a warning (not hard failure) for files approaching 365 days.
2. Add a `CONTRIBUTING.md` section on devlog retention: "Entries in `devlog/` older than 12 months SHOULD be archived to `devlog/archive/YYYY/`. They MAY be deleted after archival."
3. Create `devlog/archive/` directory with a `.gitkeep` file.

**Verification**:
```powershell
uv run pytest tests/test_platform_hygiene.py -v --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

#### I-2: Automated BACKUPS snapshot (SD-4)

**Pre-flight**: Read the `BACKUPS/` directory structure and the existing snapshot file. Read `scripts/programstart_cli.py` to find the `clean` and `log` commands for precedent on state-touching operations.

**Edits**:
1. Add a `programstart backup create [--label <label>]` command that:
   a. Copies the current state files (`PROGRAMBUILD/STATE.json`, `USERJOURNEY/STATE.json`) to `BACKUPS/YYYY-MM-DD_<label>/`.
   b. Writes a `BACKUPS/YYYY-MM-DD_<label>/MANIFEST.txt` with the timestamp, git commit hash, and changed files.
2. Register in `scripts/programstart_command_registry.py`.
3. Add `programstart backup` to the pre-commit config (or nox session `ci`) as a post-advance step (optional, operator-triggered).
4. Add tests: backup creates expected files, backup with label uses the label in the directory name.

**Verification**:
```powershell
uv run programstart backup create --label test-phase-I
uv run pytest tests/ -k "backup" --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

**Phase I verification**:
```powershell
uv run pre-commit run --all-files
uv run programstart validate --check all
uv run programstart drift
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

### Phase J: Strategic (B-2, SD-1, T-5, S-5, S-6, S-7)

**Goal**: Large-scope improvements deferred from the enhancement gameplan. Execute only when Phase A–I are complete and the team has a dedicated session for each item. Each sub-item in Phase J is effectively its own session.

#### J-1: Split programstart_create.py (B-2)

**Pre-flight**: Read `scripts/programstart_create.py` end-to-end (1040+ lines). Identify logical sections: input parsing, factory plan generation, output formatting, file writing, CLI entry. Confirm test coverage after split won't regress.

**Edits**: Split into:
- `programstart_create_core.py` — factory plan logic and shape-specific generation.
- `programstart_create_output.py` — output formatting and file writing.
- `programstart_create.py` — CLI entry point and orchestration (thin wrapper).
Update imports in all files that import from `programstart_create`.

---

#### J-2: Split process-registry.json (SD-1)

**Pre-flight**: Read `config/process-registry.json` end-to-end. Identify separable logical sections: programbuild system, userjourney system, sync_rules, workflow_guidance, metadata_rules. Design a composable `$include` or merge pattern that `load_registry()` can handle.

**Edits**: Introduce a `config/registry/` subdirectory. Split into per-system files. Update `load_registry()` to merge sub-files. All tests must still pass.

---

#### J-3: Mutation testing (T-5)

**Install `mutmut`**: `uv add --dev mutmut`. Run on core modules: `uv run mutmut run --paths-to-mutate=scripts/programstart_recommend.py --no-progress`. Review survivors and add targeted tests.

---

#### J-4: Registry Pydantic models (S-6)

Replace the raw `dict` returned by `load_registry()` with a Pydantic model. Define `ProcessRegistry`, `ProgramBuildSystem`, `UserJourneySystem`, `SyncRule`, `WorkflowGuidance` models in `scripts/programstart_models.py`. Validate on load.

---

#### J-5: Prompt builder Mode B (S-5)

**Pre-flight**: Read `scripts/programstart_prompt_build.py` Mode A implementation. Understand the shape-context injection mechanism. Design Mode B: instead of requiring a bootstrapped project directory, accept arbitrary context fields via CLI flags.

---

#### J-6: programstart sync --from-template (S-7)

Design and implement a command that pulls latest `.github/prompts/*.prompt.md` from the upstream PROGRAMSTART repository and applies them to the current project's `.github/prompts/`, preserving local customizations.

---

**Phase J note**: Each J-* item MUST have its own session and planning pass before starting. Do not start any J item within a coverage or small-hardening session.

---

## 5. Verification Suite

Run after completing all phases to confirm full baseline integrity:

```powershell
uv run programstart validate --check all --strict
uv run programstart drift --strict
uv run pytest --cov --cov-report=term-missing --tb=no -q 2>&1 | Select-String "^TOTAL|FAIL|PASS"
uv run pre-commit run --all-files
```

All four MUST pass. Coverage MUST be ≥ 95% total (after Phases A–C) and MUST NOT drop below 90% at any intermediate commit.

---

## 6. Commit Convention

Follow Conventional Commits for each phase commit:

```
feat(coverage): Phase A — push common, workflow_state, create, research_delta to 94%+
feat(coverage): Phase B — push validate, recommend to 96%+
feat(coverage): Phase C — push serve to 90%+, retrieval to 88%+
fix(retrieval): add BM25 relevance threshold (KB-2)
fix(bootstrap): replace header line-count extraction with marker-based (B-1)
fix(registry): add schema_version contract enforcement test (SD-2)
fix(workflow_guidance): add expected_outputs to registry entries (W-4)
fix(sync): add pyproject.toml ↔ requirements.txt sync rule (S-3)
feat(logging): add structured logging to production scripts (H-2)
feat(workflow): add stage staleness tracking to status output (W-2)
feat(userjourney): add entry criteria validation for phase advancement (W-3)
feat(hooks): add pre-push hook for main branch protection (G-3)
feat(cli): add programstart kb search/ask subcommand (KB-3)
feat(cli): add programstart diff command (F-3)
feat(cli): add programstart state rollback command (F-4)
test(rules): add instruction enforcement tests (R-6)
test(perf): add performance regression benchmarks (T-6)
feat(hygiene): add devlog retention policy and BACKUPS automation (SD-3, SD-4)
```
