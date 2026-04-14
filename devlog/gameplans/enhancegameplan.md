# Enhancement Gameplan — Prioritized Implementation Plan

Purpose: Prioritized implementation plan for all findings from `devlog/reports/enhanceopportunity.md` Parts 1–3 (89 findings: 80 Part 1 + 9 Part 3; 3 resolved on review, 2 new findings added; 25 strategic recommendations). Phases are ordered by severity, dependency, and value impact. Each phase is scoped for a single execution session.
Status: **NOT STARTED**
Authority: Non-canonical working plan derived from `devlog/reports/enhanceopportunity.md` (Parts 1–3), current test baseline (1068 tests, 0 failures, 93% coverage), and `config/process-registry.json`.
Last updated: 2026-04-14

---

## 1. Current State

Baseline recorded 2026-04-14:

- **1068 tests**, **0 failures**, **1 warning**
- **93% aggregate coverage** on 30 modules, `fail_under = 90`
- `programstart validate --check all --strict` PASSES
- `programstart drift --strict` PASSES
- All Stage 7 gameplan phases COMPLETE
- Audit findings F-1 through F-5 from `apr14report.md` RESOLVED

### Source Document Summary

| Source | Findings | Strategic Items |
|---|---|---|
| Part 1: Defect Audit (§1–§18) | 80 total (3 HIGH, 24 MEDIUM, 52 LOW, 1 INFO) — 3 RESOLVED, 77 active | — |
| Part 2: Strategic Analysis (§19–§25) | 10 components scored, 10 considerations | 12 recommendations (3 tiers) |
| Part 3: UI/UX Gap Analysis (§26–§30) | 9 gaps (3 HIGH, 4 MEDIUM, 2 LOW), 8 considerations | 13 recommendations (3 tiers) |

> **Review note (2026-04-14):** Part 1 counts corrected: 80 total findings
> (3H + 24M + 52L + 1I), of which 3 are resolved (A-3, DEP-1, G-4) leaving
> 77 active (3H + 22M + 51L + 1I). H-5 (HIGH) and SD-5 (MEDIUM) added during
> review. Part 3 GAP-7 severity corrected from LOW to MEDIUM per body text.

---

## 2. Prioritized Gap Registry

### P0 — Foundation (blocks downstream work or prevents recurrence)

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **D-1** | `system_is_optional_and_absent()` duplicated in 4 scripts | HIGH | §2 | A |
| **D-2** | `system_is_attached()` duplicated in 4 scripts | HIGH | §2 | A |
| **GAP-1** | Idea Intake has no UI/UX question | HIGH | §28 | B |
| **GAP-2** | Kickoff Packet has no UI needs field | HIGH | §28 | B |
| **GAP-3** | `CAPABILITY_ALIASES` missing UI-specific terms | HIGH | §28 | B |
| **H-1** | Bare `except Exception` clauses suppress real errors (15 instances) | MEDIUM | §1 | C |
| **H-5** | Race condition in workflow state writes — no file locking | HIGH | §1 (review) | A |
| **SC-1** | `process-registry.schema.json` has `additionalProperties: true` on 8 critical objects | MEDIUM | §10 | D |

### P1 — Core Improvements (high value, reduce risk)

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **R-1** | No sync test between commit type list (instruction file) and `check_commit_msg.py` | MEDIUM | §6 | E |
| **R-2** | Prompt standard compliance not enforced in pre-commit | MEDIUM | §6 | K |
| **KB-1** | Context index `INDEX_VERSION` hardcoded to stale date | MEDIUM | §15 | E |
| **A-1** | No CI job for Python 3.13+ on Windows | MEDIUM | §4 | F |
| **A-2** | No automatic CHANGELOG update enforcement | MEDIUM | §4 | F |
| **A-3** | ~~No `dependabot.yml` github-actions ecosystem~~ | ~~MEDIUM~~ | §4 | ~~F~~ | ✅ RESOLVED — already exists |
| **DEP-1** | ~~`dependabot.yml` missing `github-actions` ecosystem~~ | ~~MEDIUM~~ | §13 | ~~F~~ | ✅ RESOLVED — DUPLICATE of A-3 |
| **T-1** | `programstart_serve.py` at 83% — lowest coverage | MEDIUM | §3 | G |
| **T-2** | `programstart_retrieval.py` at 85% — RAG pipeline undertested | MEDIUM | §3 | G |
| **T-3** | `programstart_research_delta.py` at 80% | MEDIUM | §3 | G |
| **G-1** | `programstart advance` has no post-advance verification | MEDIUM | §11 | H |
| **W-1** | Stage gates don't check content quality (TBD/TODO stubs pass) | MEDIUM | §12 | H |
| **UI-1** | Dashboard serves inline HTML from Python string literals | MEDIUM | §14 | L |
| **P-1** | No prompt versioning or deprecation mechanism | MEDIUM | §9 | K |
| **D-3** | Repeated `try/except ImportError` boilerplate in 30+ scripts | MEDIUM | §2 | M |
| **DX-1** | 39 `.py` files in `scripts/` with no namespace organization | MEDIUM | §17 | M |
| **SD-1** | `process-registry.json` is 900+ lines — single point of failure | MEDIUM | §18 | N |
| **S-1** | Drift check can't detect same-commit multi-file content drift | MEDIUM | §8 | N |
| **DOC-1** | `CHANGELOG.md` never updated past `[0.1.0]` | MEDIUM | §7 | J |

### P2 — Recommendation Engine Structural (UI/UX model improvements)

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **GAP-4** | `shape_profile()` treats shapes as mutually exclusive — no composite shape | MEDIUM | §28 | I |
| **GAP-5** | No `suggested_companion_surfaces` field on recommendation | MEDIUM | §28 | I |
| **GAP-6** | Coverage warnings don't fire for absent domains | MEDIUM | §28 | I |
| **GAP-7** | Prompt-eval scenarios don't test cross-shape UI | MEDIUM | §28 | I |
| **GAP-8** | Starter scaffold has no companion-UI option | LOW | §28 | I |
| **GAP-9** | Factory plan doesn't mention UI/UX considerations | LOW | §28 | I |
| **UI-5** | No companion surface field on ProjectRecommendation | MEDIUM | §30 | I |
| **UI-6** | No cross-shape UI advisory in coverage_warnings | MEDIUM | §30 | I |
| **UI-7** | No UI-tier classification in shape_profile | MEDIUM | §30 | I |
| **UI-8** | No hybrid-surface prompt-eval scenarios | MEDIUM | §30 | I |
| **UI-9** | No cross-shape decision rules in KB | MEDIUM | §30 | I |

### P3 — Polish & Defense in Depth

| ID | Gap | Severity | Source | Phase |
|---|---|---|---|---|
| **H-2** | No structured logging anywhere | LOW | §1 | N |
| **H-3** | `write_json` atomic write doesn't retry on Windows lock | LOW | §1 | N |
| **H-4** | `programstart_serve.py` no request timeout on subprocess calls | LOW | §1 | C |
| **R-3** | No enforcement that new scripts get added to coverage source | LOW | §6 | E |
| **R-4** | No enforcement that new ADRs update the index | LOW | §6 | E |
| **R-5** | `process-registry.json` version manually bumped | LOW | §6 | E |
| **T-4** | `programstart_create.py` at 90% — 25 uncovered lines | LOW | §3 | G |
| **T-5** | No mutation testing | LOW | §3 | N |
| **T-6** | No performance regression tests | LOW | §3 | N |
| **T-7** | `test_audit_fixes.py` is a grab-bag | LOW | §3 | N |
| **A-4** | `nox -s ci` runs format_check redundantly | LOW | §4 | F |
| **A-5** | No scheduled dependency audit workflow | LOW | §4 | F |
| **A-6** | Coverage not uploaded as a PR check | LOW | §4 | F |
| **F-1** | `programstart create` lacks `--list-shapes` | MEDIUM | §5 | K |
| **F-2** | No `programstart doctor` command | MEDIUM | §5 | K |
| **F-3** | No `programstart diff` command | LOW | §5 | N |
| **F-4** | No `programstart state rollback` | LOW | §5 | N |
| **F-5** | `programstart clean` doesn't clean nox temps | LOW | §5 | N |
| **F-6** | No `--json` output for `programstart status` | LOW | §5 | K |
| **DOC-2** | CONTRIBUTING.md says 80% but `fail_under = 90` | LOW | §7 | J |
| **DOC-3** | MkDocs nav doesn't include `docs/decisions/` | LOW | §7 | J |
| **DOC-4** | `docs/dashboard-api.md` may be stale | LOW | §7 | J |
| **DOC-5** | `SECURITY.md` vulnerability disclosure has no email | LOW | §7 | J |
| **DOC-6** | `QUICKSTART.md` leads with Windows-only `pb.ps1` | LOW | §7 | J |
| **S-2** | Drift check doesn't run on staged files by default | LOW | §8 | N |
| **S-3** | No sync rule for `pyproject.toml` ↔ `requirements.txt` | LOW | §8 | N |
| **S-4** | `knowledge_base_docs_alignment` sync rule too broad for README | LOW | §8 | N |
| **P-2** | `prompt-eval` only tests 6 scenarios | LOW | §9 | I |
| **P-3** | USERJOURNEY prompts missing kill-criteria sections | LOW | §9 | N |
| **P-4** | No implementation-sprint shaping prompt | LOW | §9 | N |
| **P-5** | `argument-hint` inconsistently populated | LOW | §9 | N |
| **SC-2** | State schema doesn't validate stage/phase names | LOW | §10 | D |
| **SC-3** | No schema for `knowledge-base.json` | LOW | §10 | D |
| **SC-4** | No schema for `prompt-eval-scenarios.json` | LOW | §10 | D |
| **G-2** | No guard against advancing PB while UJ is blocked | LOW | §11 | H |
| **G-3** | No git hook for branch protection | LOW | §11 | N |
| **G-4** | ~~`READONLY_MODE` not tested~~ | ~~LOW~~ | §11 | ~~G~~ | ✅ RESOLVED — `TestReadonlyModeGuard` exists |
| **W-2** | No stage expiry/staleness tracking | LOW | §12 | N |
| **W-3** | USERJOURNEY phases have no entry criteria | LOW | §12 | N |
| **W-4** | `workflow_guidance` doesn't reference expected outputs | LOW | §12 | N |
| **DEP-2** | `pip-audit` exit code 1 doesn't fail CI | LOW | §13 | F |
| **DEP-3** | No `uv.lock` integrity check in CI | LOW | §13 | F |
| **UI-2** | No CSP header on dashboard responses | LOW | §14 | L |
| **UI-3** | Golden screenshots Linux-only | LOW | §14 | N |
| **KB-2** | BM25 retrieval has no relevance threshold | LOW | §15 | N |
| **KB-3** | No `programstart kb` subcommand | LOW | §15 | N |
| **B-1** | Bootstrap header extraction is fragile | LOW | §16 | N |
| **B-2** | `programstart_create.py` is 1040+ LoC single file | LOW | §16 | N |
| **DX-2** | `pb.ps1` undocumented | LOW | §17 | J |
| **DX-3** | VS Code tasks not categorized in picker | LOW | §17 | J |
| **DX-4** | No `.editorconfig` rule for JSON indent | LOW | §17 | J |
| **SD-2** | No explicit versioning contract registry ↔ scripts | LOW | §18 | N |
| **SD-3** | `devlog/` exempted from rules, no retention policy | LOW | §18 | N |
| **SD-4** | `BACKUPS/` has one snapshot, no automation | LOW | §18 | N |
| **SD-5** | No file-placement automation — root hygiene is convention-only | MEDIUM | §18 (review) | K |
| **R-6** | `copilot-instructions.md` rules not runtime-enforceable | INFO | §6 | N |

### Strategic Items (from Parts 2 + 3)

> **Disambiguation note:** IDs S-1 through S-12 below are strategic
> recommendations from §25. They are distinct from defect findings S-1 through
> S-4 in the P3 table above (§8, Sync & Drift). Phase references in detailed
> sections always specify context (e.g., "Strategic S-2" vs. defect "S-2").

| ID | Recommendation | Source | Phase |
|---|---|---|---|
| **S-1** | Prompt builder Mode A (regenerate for bootstrapped repos) | §25 | L |
| **S-2** | Add `version:` field to prompt frontmatter | §25 | K |
| **S-3** | Extract dashboard HTML/CSS/JS to static files | §25 | L |
| **S-4** | Add `--json` output to core CLI commands | §25 | K |
| **S-5** | Prompt builder Mode B (arbitrary repos) | §25 | N |
| **S-6** | Registry Pydantic models | §25 | N |
| **S-7** | Prompt update channel (`programstart sync --from-template`) | §25 | N |
| **S-8** | "Prompt-only" bootstrap mode | §25 | N |
| **S-9** | VS Code webview extension | §25 | N |
| **S-10** | Multi-repo orchestration | §25 | N |
| **S-11** | LLM-in-the-loop prompt testing | §25 | N |
| **S-12** | Feedback loop from generated repos | §25 | N |
| **UI-10** | `admin_dashboard_plan()` starter scaffold | §30 | I |
| **UI-11** | Mono vs multi-repo guidance in factory plan | §30 | I |
| **UI-12** | UI Surface Assessment in shape-requirements prompt | §30 | I |
| **UI-13** | Companion-UI boundary in shape-architecture prompt | §30 | I |

> **Tracking notes:**
> - §30 Tier 1 recommendations (UI-1–4) are not tracked as separate rows; they
>   map 1:1 to GAP-1–3 + Phase B step B-2 (§30 UI-4). See Phase B note.
> - §30 Tier 2 (UI-5–9) appear in both the P2 gap registry and as strategic
>   recommendations. The 89-finding total counts original audit findings only
>   (80 Part 1 + 9 Part 3 GAPs). UI-5–9 are mapped into the gap registry as
>   implementation targets derived from §30, adding 5 extra rows (94 registry
>   entries total). They are also counted once in the 25-strategic-recommendation
>   total (as §30 Tier 2).
> - Phases C, E, F, G, H, and M describe changes in prose with pre-flight
>   and edit instructions but do not include inline code examples. Code will be
>   written during implementation using the pre-flight reads as context.

---

## 3. Phase Sequence

| Phase | Gap(s) | Type | Est. edits | Target |
|---|---|---|---|---|
| Pre-work | — | Record baseline | 0 edits | Snapshot test + coverage + validate + drift |
| A | D-1, D-2, H-5 | DRY consolidation + state write safety | 6–10 file edits + test consolidation | 2 functions in `programstart_common.py`, 8 script imports updated, file locking on state writes |
| B | GAP-1–3, §30 Tier 1 UI-1–4 | UI blind spot quick fixes | 4 file edits | Recommendation engine can surface UI needs |
| C | H-1, H-4 | Exception handling + subprocess timeouts | 4–6 file edits | Specific exceptions, timeouts on subprocess calls |
| D | SC-1, SC-2, SC-3, SC-4 | Schema hardening | 3–4 schema edits + 1 new schema | `additionalProperties: false` on 8 critical objects, KB schema generated |
| E | R-1, R-3, R-4, R-5, KB-1 | Rule enforcement + stale version fixes | 4–6 file edits (tests + hooks) | Commit types synced, coverage source enforced, ADR index enforced |
| F | A-1, A-2, A-4–6, DEP-2–3 | CI & dependency improvements | 3–4 workflow edits + 1 config edit | Windows 3.13 in CI, lockfile check (A-3/DEP-1 already resolved) |
| G | T-1–4 | Test coverage push — critical modules | 4–5 test file edits | serve.py ≥88%, retrieval ≥88%, research_delta ≥85% (G-4 already resolved) |
| H | G-1, G-2, W-1 | Post-advance verification + content quality gates | 3–4 script edits | Post-advance sanity check, content placeholder detection, cross-system warning |
| I | GAP-4–9, P-2, UI-5–13 | Recommendation engine structural — companion surfaces | 5–8 file edits | Composite shapes, `suggested_companion_surfaces` field, cross-shape advisory, hybrid eval scenarios |
| J | DOC-1–6, DX-2–4 | Documentation + DX polish | 8–10 file edits | CHANGELOG updated, CONTRIBUTING accurate, MkDocs nav complete, tasks grouped |
| K | F-1, F-2, F-6, P-1, R-2, SD-5, Strategic S-2, Strategic S-4 | CLI features + prompt versioning + file hygiene | 5–8 file edits | `--list-shapes`, `doctor`, `--json`, prompt `version:` field, pre-commit prompt lint, file-hygiene check |
| L | UI-1, UI-2, Strategic S-1, Strategic S-3 | Dashboard extraction + prompt builder Mode A | Major refactor | Static dashboard files, CSP headers, prompt builder `~300 LoC` |
| M | D-3, DX-1 | Import boilerplate + script organization | Structural refactor | Reduced boilerplate, consider subpackage split |
| N | All remaining LOW/INFO + Tier 3 strategic | Polish + future track | Multiple sessions | Defense-in-depth, rollback, structured logging, mutation testing, etc. |
| Docs | — | Post-implementation verification + docs sync | Config + doc edits | Clean validate + drift, CHANGELOG entry |

---

## 4. Phases

---

### Pre-work: Record Baseline

```powershell
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
uv run pytest --cov --cov-report=term-missing --tb=no -q 2>&1 | Select-String "^scripts|TOTAL"
uv run programstart validate --check all --strict
uv run programstart drift --strict
```

Capture: test count (expect 1068 passed), per-module coverage %, validate output, drift output. All phases measure improvement against this baseline.

---

### Phase A: DRY Consolidation + State Write Safety (D-1, D-2, H-5)

**Goal**: Eliminate the two HIGH-severity duplicate functions. One definition each in `programstart_common.py`, all 8 consuming scripts import from common. Add file locking to prevent race conditions in state writes.

#### A-1: Consolidate `system_is_optional_and_absent()` (D-1)

**Root cause**: Identical function defined independently in 4 scripts. Each has its own monkeypatched tests.

**Pre-flight**: Read each implementation to confirm they are byte-identical:
- `scripts/programstart_validate.py` line 45
- `scripts/programstart_drift_check.py` line 31
- `scripts/programstart_log.py` line 40
- `scripts/programstart_workflow_state.py` line 58

**Edits**:
1. Add `system_is_optional_and_absent(registry, system_name, repo_root)` to `scripts/programstart_common.py` — use the implementation from `programstart_validate.py` as canonical.
2. In each of the 4 scripts: delete the local function definition, add `from programstart_workflow.programstart_common import system_is_optional_and_absent` to the import block.
3. Update tests: consolidate 4 sets of monkeypatched tests into `tests/test_programstart_common.py`. Remove duplicate test functions from `test_programstart_validate.py`, `test_programstart_drift_check.py`, `test_programstart_log.py`, `test_programstart_workflow_state.py`.

**Verification**:
```powershell
uv run pytest tests/test_programstart_common.py tests/test_programstart_validate.py tests/test_programstart_drift_check.py tests/test_programstart_log.py tests/test_programstart_workflow_state.py -v --tb=short
```

Expected: all tests pass, no import errors.

#### A-2: Consolidate `system_is_attached()` (D-2)

**Root cause**: Near-identical function in 4 scripts but with **different parameter orders** (`registry, system_name` vs `system_name, registry`). This is especially fragile.

**Pre-flight**: Read each implementation to identify the argument order:
- `scripts/programstart_markdown_parsers.py` line 221 — check if reversed
- `scripts/programstart_dashboard.py` line 40
- `scripts/programstart_step_guide.py` line 32
- `scripts/programstart_status.py` line 31

**Edits**:
1. Add `system_is_attached(registry, system_name)` to `scripts/programstart_common.py` — standardize on `(registry, system_name)` parameter order.
2. In each of the 4 scripts: delete the local function definition, import from common.
3. **Critical**: If `programstart_markdown_parsers.py` has reversed parameter order, update **all callers** in that module to match the standard `(registry, system_name)` order.
4. Consolidate tests as with A-1.

**Verification**:
```powershell
uv run pytest tests/test_programstart_markdown_parsers.py tests/test_programstart_dashboard.py tests/test_programstart_step_guide.py tests/test_programstart_status.py -v --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

Expected: all 1068 tests still pass, zero regressions from parameter reordering.

#### A-3: Add file locking to workflow state writes (H-5)

**Root cause**: `write_json()` in `programstart_common.py` (lines 95-101) uses atomic temp-file-and-replace but has no file locking. Two concurrent callers (CLI + dashboard) could both read the same state, modify in memory, and the second write silently overwrites the first.

**Pre-flight**: Read `scripts/programstart_common.py` `write_json()` and `scripts/programstart_workflow_state.py` `save_workflow_state()`.

**Edits**:
1. Add a cross-platform file lock around the read-modify-write cycle in `save_workflow_state()`. Use Python's `filelock` library (already cross-platform) or implement with `fcntl`/`msvcrt`.
2. Add the same lock guard to `advance_workflow_with_signoff()` in `programstart_serve.py`.
3. Add a test that simulates concurrent writes (e.g. two threads calling `save_workflow_state()` simultaneously) and verifies no state is lost.

**Example** (using `filelock`):
```python
from filelock import FileLock

def save_workflow_state(registry, system_name, state_data, repo_root=None):
    state_path = _state_file_path(registry, system_name, repo_root)
    lock = FileLock(str(state_path) + ".lock", timeout=10)
    with lock:
        existing = load_workflow_state(registry, system_name, repo_root)
        # ... merge state_data into existing ...
        write_json(state_path, merged)
```

**Verification**:
```powershell
uv run pytest tests/test_programstart_workflow_state.py -v --tb=short -k "lock or concurrent"
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

### Phase B: UI Blind Spot Quick Fixes (GAP-1–3, §30 Tier 1 UI-1–4)

**Goal**: The recommendation engine can surface UI/frontend needs for non-web shapes. Users can express dashboard/admin-UI requirements through `--need`. Idea Intake and Kickoff Packet ask about UI needs.

> **Note:** "UI-1–4" here refers to §30 Tier 1 quick-win recommendations, not
> the Part 1 §14 defect finding UI-1 (Dashboard inline HTML), which is in Phase L.

#### B-1: Add UI-specific capability aliases (GAP-3, UI-3)

**Pre-flight**: Read `scripts/programstart_recommend.py` `CAPABILITY_ALIASES` dict (around line 55).

**Edit**: `scripts/programstart_recommend.py` — add new alias entries:
```python
"dashboard": {"dashboard", "admin dashboard", "admin panel", "management ui"},
"web interface": {"web interface", "web ui", "web portal", "portal"},
"monitoring ui": {"monitoring ui", "monitoring dashboard", "status page", "console"},
```
Map all three to the `"javascript"` canonical alias group (since they all imply frontend needs).

#### B-2: Add `_need_to_domain` entry for dashboard terms (§30 UI-4)

**Pre-flight**: Read `scripts/programstart_recommend.py` `_need_to_domain` dict (around line 307).

**Edit**: Add entries so `"dashboard"`, `"web interface"`, and `"monitoring ui"` all map to `"Web and frontend product delivery"`.

#### B-3: Add UI question to Idea Intake (GAP-1, UI-2)

**Pre-flight**: Read `PROGRAMBUILD/PROGRAMBUILD_IDEA_INTAKE.md` to find the 7 interview questions.

**Edit**: Add Question 8: "Will end users or operators interact with this system through a visual interface (web dashboard, admin panel, configuration UI)? If yes, describe the audience and their primary tasks."

#### B-4: Add `ADDITIONAL_SURFACES` field to Kickoff Packet (GAP-2, UI-1)

**Pre-flight**: Read `PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md` inputs block.

**Edit**: Add after `PRODUCT_SHAPE`:
```
ADDITIONAL_SURFACES:    [admin dashboard | monitoring UI | public web UI | documentation site | none]
```

Update the decision matrix to reference this field when non-empty.

#### B-5: Add tests for new aliases

**Edit**: `tests/test_programstart_recommend.py` — add parametrized tests verifying:
- `--need dashboard` triggers "Web and frontend product delivery" domain
- `--need "admin ui"` resolves through CAPABILITY_ALIASES to frontend domain
- API service shape with `--need dashboard` includes frontend stacks in recommendation

**Verification**:
```powershell
uv run pytest tests/test_programstart_recommend.py -v --tb=short -k "dashboard or alias or frontend"
uv run programstart recommend --product-shape "api service" --need rag --need dashboard
```

Expected: recommendation output now includes frontend stacks alongside backend stacks when `--need dashboard` is specified.

---

### Phase C: Exception Handling + Subprocess Timeouts (H-1, H-4)

**Goal**: Replace the most concerning bare `except Exception` clauses with specific exception types. Add timeouts to subprocess calls in the dashboard server.

#### C-1: Fix `programstart_serve.py` exception handling (H-1, H-4)

**Pre-flight**: Read `scripts/programstart_serve.py` at lines ~235, ~342 (request handlers) and all `subprocess.run()` calls.

**Edits**:
1. Replace `except Exception` in request handlers with `except (json.JSONDecodeError, KeyError, ValueError)` where the handler processes JSON input, and `except subprocess.SubprocessError` where it runs commands. Keep a final `except Exception as exc:` only where genuinely needed, but add `logging.exception("Unexpected error in %s", endpoint)`.
2. Add `timeout=60` to all `subprocess.run()` calls in `run_command()` and `run_bootstrap()`.
3. Catch `subprocess.TimeoutExpired` separately and return a meaningful error response.

#### C-2: Fix `programstart_retrieval.py` exception handling (H-1)

**Pre-flight**: Read `scripts/programstart_retrieval.py` at lines ~669, ~687, ~931.

**Edits**: Replace bare `except Exception` with specific exceptions (`FileNotFoundError`, `json.JSONDecodeError`, `ImportError` for optional chromadb). Log with traceback.

#### C-3: Fix `programstart_dashboard_browser_smoke.py` exception handling (H-1)

**Pre-flight**: Read at lines ~147, ~220, ~268, ~293.

**Edits**: Smoke tests should NOT silently swallow exceptions — they should fail loudly. Replace `except Exception` with `except (ConnectionError, TimeoutError)` for network-related catches only; let other exceptions propagate.

**Verification**:
```powershell
uv run pytest tests/test_programstart_serve.py tests/test_programstart_retrieval.py -v --tb=short
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

Expected: all tests pass. Exception paths now log diagnostically.

---

### Phase D: Schema Hardening (SC-1, SC-2, SC-3, SC-4)

**Goal**: Tighten JSON schemas to catch typos. Generate missing schemas.

#### D-1: Set `additionalProperties: false` on critical registry schema objects (SC-1)

**Pre-flight**: Read `schemas/process-registry.schema.json` to identify which objects should be locked.

**Edits**: Set `additionalProperties: false` on:
- `sync_rules` items
- `system` definitions (programbuild, userjourney)
- `metadata_rules` objects
- `stage_order` (PROGRAMBUILD) / `step_order` (USERJOURNEY) items

Leave `additionalProperties: true` on `workflow_guidance` and top-level (for extensibility during development).

**Verification**:
```powershell
uv run pytest tests/test_schema_conformance.py -v --tb=short
uv run pre-commit run check-json --all-files
```

Ensure the live `process-registry.json` still passes the tightened schema. If it has extra fields, either add them to the schema or remove them from the config.

#### D-2: Add stage/phase name validation to state schemas (SC-2)

**Edit**: In `schemas/programbuild-state.schema.json` and `schemas/userjourney-state.schema.json`, add `enum` constraints for valid stage/phase names. Derive the enum values from `process-registry.json` `stage_order` (PROGRAMBUILD) / `step_order` (USERJOURNEY).

Alternatively, add a _programmatic_ test in `tests/test_schema_conformance.py` that loads the state schema, loads the registry, and asserts the state file keys are a subset of registry stage/phase names.

#### D-3: Generate `knowledge-base.schema.json` from Pydantic (SC-3)

**Pre-flight**: Read `scripts/programstart_models.py` to find the KB Pydantic model.

**Edit**: Add a script or nox session: `uv run python -c "from programstart_workflow.programstart_models import KnowledgeBase; import json; print(json.dumps(KnowledgeBase.model_json_schema(), indent=2))" > schemas/knowledge-base.schema.json`. Add to pre-commit hooks.

#### D-4: Add `prompt-eval-scenarios.schema.json` (SC-4)

**Edit**: Create a minimal JSON Schema for the scenario file structure. Add to pre-commit hooks.

**Verification**:
```powershell
uv run pre-commit run --all-files
uv run pytest tests/test_schema_conformance.py -v
```

---

### Phase E: Rule Enforcement + Stale Version Fixes (R-1, R-3, R-4, R-5, KB-1)

**Goal**: Add sync-enforcing tests for commit types, coverage source completeness, ADR index, and fix stale version strings.

#### E-1: Sync commit types between instruction file and `check_commit_msg.py` (R-1)

**Edit**: Add a test in `tests/test_check_commit_msg.py` (or `test_audit_fixes.py`) that:
1. Reads `.github/instructions/conventional-commits.instructions.md`
2. Extracts the valid types from the markdown table (`feat|fix|docs|chore|ci|refactor|test`)
3. Reads `scripts/check_commit_msg.py` and extracts `VALID_TYPES` (or equivalent regex)
4. Asserts they match

#### E-2: Enforce new scripts get added to coverage source (R-3)

**Edit**: Add a test that:
1. Scans `scripts/` for `programstart_*.py` files
2. Reads `pyproject.toml` `[tool.coverage.run]` source list
3. Asserts each production script is listed (with an explicit exclusion list for smoke/non-production scripts)

#### E-3: Enforce ADR index completeness (R-4)

**Edit**: Add a test that:
1. Lists `docs/decisions/0*.md` files
2. Reads `docs/decisions/README.md`
3. Asserts each ADR file has a row in the index table

#### E-4: Fix stale `INDEX_VERSION` (KB-1)

**Pre-flight**: Read `scripts/programstart_context.py` line 42 to find the hardcoded version.

**Edit**: Either:
- Update the version string to `"2026-04-14"`, or
- Replace the hardcoded string with a hash derived from the index structure (e.g., `hashlib.md5(json.dumps(INDEX_SCHEMA, sort_keys=True).encode()).hexdigest()[:10]`)

#### E-5: Add registry version freshness test (R-5)

**Edit**: Add a test that compares `process-registry.json` `version` date against `git log -1 --format=%ai -- config/process-registry.json` output, warning when the version date is older than the last modification date.

**Verification**:
```powershell
uv run pytest tests/test_check_commit_msg.py tests/test_audit_fixes.py -v --tb=short -k "commit_type or coverage_source or adr_index or registry_version"
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

### Phase F: CI & Dependency Improvements (A-1, A-2, A-4–6, DEP-2–3; A-3/DEP-1 resolved)

**Goal**: Expand CI matrix, add missing Dependabot ecosystems, add lockfile integrity check.

#### F-1: Add Python 3.13 to Windows CI matrix (A-1)

**Pre-flight**: Read `.github/workflows/process-guardrails.yml` matrix section.

**Edit**: Add `'3.13'` to the `python-version` array alongside `'3.12'`.

#### F-2: ~~Add `github-actions` ecosystem to Dependabot~~ — RESOLVED (A-3, DEP-1)

> **Review note (2026-04-14):** `.github/dependabot.yml` already contains the
> `github-actions` ecosystem entry (lines 43-60). A-3 and DEP-1 are duplicates
> of the same finding, and both are already resolved. No action needed.
> Skip this step.

#### F-3: Add `uv lock --check` to CI (DEP-3)

**Edit**: Add a step in the guardrails workflow after `uv sync`: `run: uv lock --check`

#### F-4: Make `pip-audit` a blocking check (DEP-2)

**Pre-flight**: Read the `pip-audit` step in `process-guardrails.yml`.

**Edit**: Remove the exit-code-1 suppression. If specific advisories must be tolerated, use `--ignore-vuln <CVE>` instead.

#### F-5: Remove redundant `format_check` from nox ci (A-4)

**Pre-flight**: Read `noxfile.py` `ci` session to confirm `format_check` is redundant with `lint` (which runs pre-commit including ruff-format).

**Edit**: Remove `format_check` from the `ci` session list if confirmed redundant.

#### F-6: Add CHANGELOG enforcement (A-2)

**Edit**: Add a CI step (or pre-commit hook) that checks: if files in `scripts/` or `config/` changed in the PR, `CHANGELOG.md` must also be changed. Exempt `chore:` and `ci:` commits (parse the PR title or commit messages).

#### F-7: Add scheduled `pip-audit` (A-5)

**Edit**: Add a scheduled weekly run of `pip-audit` either as a new workflow or appended to the `full-ci-gate.yml` daily run.

#### F-8: Add coverage upload to CI (A-6)

**Edit**: Add a step that posts coverage as a PR comment or uses `codecov` action with the coverage XML artifact.

**Verification**:
```powershell
uv run nox -s ci 2>&1 | Select-Object -Last 20
```

---

### Phase G: Test Coverage Push — Critical Modules (T-1–4; G-4 resolved)

**Goal**: Raise coverage on the three lowest-covered production modules. Add READONLY_MODE tests.

#### G-1: `programstart_serve.py` 83% → 88%+ (T-1)

**Pre-flight**: Read uncovered lines from `uv run pytest --cov --cov-report=term-missing -q 2>&1 | Select-String "programstart_serve"`.

**Edits**: Add tests to `tests/test_programstart_serve.py` for:
- Signoff POST flow (valid + malformed JSON)
- Bootstrap error paths
- Timeout handling (after Phase C adds timeouts)

> **Note (2026-04-14):** G-4 (`READONLY_MODE` test) is already resolved —
> `TestReadonlyModeGuard` exists in `tests/test_serve_endpoints.py` (lines ~406-435).
> No additional READONLY_MODE tests needed here.

#### G-2: `programstart_retrieval.py` 85% → 88%+ (T-2)

**Pre-flight**: Read uncovered lines.

**Edits**: Add conditional tests (skip if chromadb not installed) for vector search. Add mock-based tests for RAG response formatting.

#### G-3: `programstart_research_delta.py` 80% → 88%+ (T-3)

**Pre-flight**: Read uncovered lines.

**Edits**: Add tests for `complete_review()`, status report generation, and `--fail-on-due` flag behavior.

#### G-4: `programstart_create.py` 90% → 93%+ (T-4)

**Pre-flight**: Read uncovered lines.

**Edits**: Add mock-based tests for GitHub API error paths and service provisioning edge cases.

**Verification**:
```powershell
uv run pytest --cov --cov-report=term-missing --tb=no -q 2>&1 | Select-String "programstart_serve|programstart_retrieval|programstart_research_delta|programstart_create"
```

Expected: all four modules above their targets.

---

### Phase H: Post-Advance Verification + Content Quality Gates (G-1, G-2, W-1)

**Goal**: State-changing operations validate their own results. Stage gates detect placeholder content.

#### H-1: Add post-advance sanity check (G-1)

**Pre-flight**: Read `scripts/programstart_workflow_state.py` advance logic.

**Edit**: After the state file is written by `advance()`:
1. Reload the state file
2. Verify the active step matches the expected next step
3. Run `validate --check workflow-state` programmatically
4. If any check fails, emit a warning (don't auto-rollback — too dangerous)

#### H-2: Add content placeholder detection to stage gates (W-1)

**Pre-flight**: Read `scripts/programstart_validate.py` stage gate check functions.

**Edit**: Add a shared helper `_check_content_quality(filepath)` that checks for:
- Placeholder strings: `"TBD"`, `"TODO"`, `"[FILL IN]"`, `"PLACEHOLDER"`, `"Lorem ipsum"`
- Minimum word count per required section (configurable, e.g., 20 words)
- Return warnings (not errors) so it's non-blocking but visible

Wire into stage gates after file-exists checks.

#### H-3: Add cross-system health warning (G-2)

**Pre-flight**: Read `scripts/programstart_status.py` and `scripts/programstart_step_guide.py` to find where `next` output is generated.

**Edit**: In the `next` command output, if both systems are active, compare stage index vs phase index. If one is ≥2 steps ahead of the other, emit a warning: "PROGRAMBUILD is at Stage N but USERJOURNEY is at Phase M — consider advancing USERJOURNEY before proceeding."

**Verification**:
```powershell
uv run pytest tests/test_programstart_validate.py tests/test_programstart_workflow_state.py -v --tb=short -k "placeholder or post_advance or cross_system"
```

---

### Phase I: Recommendation Engine Structural — Companion Surfaces (GAP-4–9, P-2, UI-5–13)

**Goal**: The recommendation engine understands that non-web shapes can have companion UI surfaces. Eval scenarios cover hybrid shapes. Starter scaffold includes companion-UI option.

#### I-1: Add `suggested_companion_surfaces` and composite shape support (GAP-4, GAP-5, UI-5)

**Pre-flight**: Read `scripts/programstart_recommend.py` `ProjectRecommendation` dataclass and `shape_profile()` function.

**Edit**: Add field to `ProjectRecommendation` and extend `shape_profile()` to accept an optional `companion_surfaces` parameter (addressing GAP-4's mutually-exclusive shapes):
```python
suggested_companion_surfaces: list[str] = field(default_factory=list)
```

#### I-2: Add cross-shape UI advisory logic (GAP-6, UI-6)

**Edit**: After `build_stack_candidates()` and before returning the recommendation, add logic:
```python
# If shape is not web/mobile and any need commonly implies UI:
ui_adjacent_needs = {"monitoring", "dashboard", "admin", "config", "analytics", "reporting"}
if product_shape not in ("web app", "mobile app") and user_needs & ui_adjacent_needs:
    recommendation.suggested_companion_surfaces.append("admin dashboard")
    recommendation.coverage_warnings.append(
        "Your API/CLI needs suggest a companion management UI. "
        "Consider adding --need dashboard or running a separate web app build."
    )
```

Also add a warning when "Web and frontend" domain was **never matched** but the product is likely to need operator access:
```python
if "Web and frontend product delivery" not in matched_domains and product_shape in ("api service", "data pipeline"):
    recommendation.coverage_warnings.append(
        "No frontend domain matched. Many production API services need "
        "an admin dashboard. Add --need dashboard if applicable."
    )
```

#### I-3: Add UI-tier classification (UI-7)

**Edit**: Add to `shape_profile()` return or as a new helper:
```python
def ui_tier(product_shape: str, needs: set[str]) -> str:
    """Classify UI tier: none | docs-only | minimal-admin | full-product-ui"""
    if product_shape in ("web app", "mobile app"):
        return "full-product-ui"
    if needs & {"dashboard", "admin ui", "monitoring ui", "web interface"}:
        return "minimal-admin"
    if product_shape == "library":
        return "docs-only"
    return "none"
```

#### I-4: Add hybrid prompt-eval scenarios (GAP-7, P-2, UI-8)

**Edit**: `config/prompt-eval-scenarios.json` — add 3 scenarios:
1. `api_service_with_admin_dashboard` — shape: "api service", needs: ["rag", "agents", "dashboard"]
2. `cli_tool_with_web_ui` — shape: "cli tool", needs: ["web interface"]
3. `data_pipeline_with_monitoring` — shape: "data pipeline", needs: ["monitoring ui"]

Each must assert that frontend stacks appear in recommendations and `suggested_companion_surfaces` is populated.

#### I-5: Add cross-shape decision rules to KB (UI-9)

**Edit**: `config/knowledge-base.json` `decision_rules` — add:
- "If shape is api_service AND need includes monitoring, recommend: status dashboard with Vite + React"
- "If shape is cli_tool AND target user is non-technical, recommend: web wrapper with Next.js"
- "If shape is data_pipeline AND need includes analytics, recommend: analytics dashboard"

#### I-6: Add `admin_dashboard_plan()` to starter scaffold (GAP-8, UI-10)

**Edit**: `scripts/programstart_starter_scaffold.py` — add a plan function that generates a minimal Vite + React SPA scaffold with:
- Basic auth-protected routes
- Dashboard layout component
- API client module pointing at the backend
- Playwright test setup

Wire this to trigger when `suggested_companion_surfaces` includes dashboard.

#### I-7: Add UI/UX guidance to factory plan (GAP-9, UI-11)

**Edit**: `scripts/programstart_create.py` `render_factory_plan()` — when companion surfaces are recommended, add a section:
```
## Companion UI Recommendation
This {shape} recommendation includes a suggested management UI.
- Recommended: {companion_surface}
- Stack: Vite + React (see starter scaffold)
- Architecture: Separate frontend repo recommended for API services.
  Monorepo recommended for CLI tools with web configuration UI.
```

#### I-8: Update requirement + architecture prompts (UI-12, UI-13)

**Edit**: `.github/prompts/shape-requirements.prompt.md` — add a "UI Surface Assessment" subsection under the requirements checklist that asks: "Does this product need any visual interface beyond what the primary shape provides? Reference the Kickoff Packet's `ADDITIONAL_SURFACES` field."

**Edit**: `.github/prompts/shape-architecture.prompt.md` — add a note in the system topology section: "If `ADDITIONAL_SURFACES` is non-empty, include the companion UI as a separate bounded context in the topology diagram."

**Verification**:
```powershell
uv run pytest tests/test_programstart_recommend.py -v --tb=short
uv run programstart recommend --product-shape "api service" --need rag --need dashboard
uv run programstart prompt-eval --scenario api_service_with_admin_dashboard
uv run pytest tests/test_prompt_compliance.py -q --tb=no
```

Expected: recommendation includes frontend stacks + companion surface advisory. Prompt compliance passes. New scenarios evaluate successfully.

---

### Phase J: Documentation + DX Polish (DOC-1–6, DX-2–4)

**Goal**: Docs are accurate, MkDocs nav is complete, VS Code tasks are organized.

#### J-1: Update CHANGELOG.md (DOC-1)

**Edit**: Cut `[0.2.0]` release with all changes since `[0.1.0]`. Group by category (Features, Fixes, Automation, Docs). Move current `[Unreleased]` content to `[0.2.0]` and start a fresh `[Unreleased]`.

#### J-2: Fix CONTRIBUTING.md coverage target (DOC-2)

**Edit**: Change "Aim for 80%+ coverage on new code" to "Maintain 90%+ test coverage (enforced by CI with `fail_under = 90`)."

#### J-3: Add decisions to MkDocs nav (DOC-3)

**Edit**: `mkdocs.yml` — add a "Decisions" section:
```yaml
  - Decisions:
      - Index: decisions/README.md
```
(The mkdocs-material theme can auto-discover files in the directory if configured.)

#### J-4: Add API endpoint sync test (DOC-4)

**Edit**: Add a test that extracts route patterns from `programstart_serve.py` handler registrations and asserts they match sections in `docs/dashboard-api.md`.

#### J-5: Fix SECURITY.md disclosure (DOC-5)

**Edit**: Either add GitHub Security Advisories link or add a contact email.

#### J-6: Fix QUICKSTART.md cross-platform (DOC-6)

**Edit**: Lead with `uv run programstart next` as the primary command. Move `pb.ps1` to a "Windows shortcut" subsection.

#### J-7: Document `pb.ps1` (DX-2)

**Edit**: Add a brief section in QUICKSTART.md: "`scripts/pb.ps1` is a PowerShell convenience wrapper. It's equivalent to `uv run programstart <command>`. Use the `uv run` form for cross-platform compatibility."

#### J-8: Add `.editorconfig` JSON rules (DX-4)

**Pre-flight**: Check if `.editorconfig` exists and read it.

**Edit**: Add or update `[*.json]` section with `indent_size = 2`.

#### J-9: Group VS Code tasks (DX-3)

**Edit**: `.vscode/tasks.json` — add `presentation.group` to tasks:
- "validate" group: Validate All, Validate Workflow State, Validate Authority Sync, etc.
- "test" group: Pytest, Pyright, Pre-commit All, Browser Smoke, Build Docs, Full CI Gate
- "workflow" group: Advance, Guide, State, Sign-off Log
- "build" group: What To Do Next, Refresh Dashboard, Launch Web Dashboard, Clean

**Verification**:
```powershell
uv run mkdocs build --strict 2>&1 | Select-Object -Last 5
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
```

---

### Phase K: CLI Features + Prompt Versioning + File Hygiene (F-1, F-2, F-6, P-1, R-2, SD-5, Strategic S-2, Strategic S-4)

**Goal**: Add `--list-shapes`, `doctor` command, `--json` output, prompt version field, pre-commit prompt lint, file-placement validation.

#### K-1: Add `--list-shapes` to recommend (F-1)

**Edit**: `scripts/programstart_recommend.py` — add a `--list-shapes` flag that prints all known shapes from `shape_profile()` with their archetype description.

Register in CLI argument parser and add a test.

#### K-2: Add `programstart doctor` (F-2)

**Edit**: Create `scripts/programstart_doctor.py` (~80-100 lines):
- Check Python version (≥3.12)
- Check `uv` is installed
- Check `pre-commit` is installed
- Check `playwright browsers` are installed (via `playwright --version`)
- Validate `process-registry.json` against schema
- Validate state files against schemas
- Check git repo is initialized
- Print summary with ✅/❌ per check

Register in `pyproject.toml` as `doctor` subcommand. Add to coverage source. Add tests.

#### K-3: Add `--json` output to core commands (F-6, Strategic S-4)

**Edit**: Add `--json` flag to `programstart status`, `programstart guide`, and `programstart drift`. When set, output structured JSON instead of formatted text.

#### K-4: Add `version:` field to prompt frontmatter (P-1, Strategic S-2)

**Edit**:
1. Update `.github/prompts/PROMPT_STANDARD.md` to include `version:` as optional field in the YAML frontmatter spec.
2. Add `version: "1.0"` to all 23 product prompts.
3. Add optional `deprecated:` boolean field.
4. Update `tests/test_prompt_compliance.py` to accept (not require) `version:` and `deprecated:` fields.

#### K-5: Add pre-commit prompt lint hook (R-2)

**Edit**: Add a lightweight pre-commit hook that:
1. Triggers when `.prompt.md` files change
2. Checks YAML frontmatter has required fields (`description`, `mode`)
3. Checks that mandatory `##` sections exist
4. Exits non-zero if any check fails

This catches non-compliant prompts before they reach the test suite.

#### K-6: Add `validate --check file-hygiene` (SD-5)

**Root cause**: No automation prevents files from being committed to the wrong directory. `enhanceopportunity.md` was created at the repo root instead of `devlog/reports/` and no validation caught it.

**Edit**: Add a `file-hygiene` check to `scripts/programstart_validate.py`:
1. Define an allowlist of expected root-level `.md` files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `QUICKSTART.md`, `CODEOWNERS`, `n8n.md`.
2. Scan repo root for `.md` files not on the allowlist → emit warning.
3. Register as a new check in the dispatch dict alongside existing checks.
4. Wire into `--check all` so it runs automatically.
5. Add tests.

```python
ALLOWED_ROOT_MD = {
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "SECURITY.md", "QUICKSTART.md", "CODEOWNERS",
}

def validate_file_hygiene(registry: dict) -> list[str]:
    """Check that no unexpected .md files are at the repo root."""
    problems = []
    root = workspace_path(".")
    for md in root.glob("*.md"):
        if md.name not in ALLOWED_ROOT_MD:
            problems.append(
                f"Unexpected .md file at repo root: {md.name} — "
                f"should it be in devlog/ or outputs/?"
            )
    return problems
```

**Verification**:
```powershell
uv run programstart validate --check file-hygiene
uv run programstart validate --check all --strict
```

**Verification**:
```powershell
uv run programstart recommend --list-shapes
uv run programstart doctor
uv run programstart status --json
uv run pre-commit run --all-files
uv run pytest tests/test_prompt_compliance.py -q --tb=no
```

---

### Phase L: Dashboard Extraction + Prompt Builder Mode A (UI-1, UI-2, Strategic S-1, Strategic S-3)

**Goal**: Extract inline HTML/CSS/JS from `programstart_serve.py` to static files. Add CSP headers. Build prompt builder Mode A.

**Note**: This is the largest phase and may span multiple sessions. Split into sub-phases if needed.

#### L-1: Extract dashboard static files (UI-1, Strategic S-3)

**Pre-flight**: Read `scripts/programstart_serve.py` to identify all inline HTML/CSS/JS blocks.

**Edits**:
1. Create `dashboard/` directory with: `index.html`, `style.css`, `app.js`
2. Move the ~1800 lines of HTML/CSS/JS from Python string literals to these files.
3. Update `programstart_serve.py` to serve static files from `dashboard/`:
   - `GET /` serves `dashboard/index.html`
   - `GET /static/<path>` serves CSS/JS
4. This reduces `programstart_serve.py` from ~2700 to ~900 lines.

#### L-2: Add Content-Security-Policy headers (UI-2)

**Edit**: In the HTTP response handler, add headers:
```python
self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'")
```
(`'unsafe-inline'` for styles only; scripts should be external files after extraction.)

#### L-3: Build prompt builder Mode A (Strategic S-1)

**Edit**: Create `scripts/programstart_prompt_build.py` (~300-400 LoC):

```
programstart prompt-build --stage feasibility --output .github/prompts/shape-feasibility.prompt.md

Steps:
  1. Load process-registry.json
  2. Find stage in stage_order → get name, main_output, id
  3. Find workflow_guidance[stage] → get step_files, scripts
  4. Find sync_rules matching stage files → get authority/dependent ordering
  5. Determine optional sections (O1 if stage >= 3, O2 if stage >= 2, O3 if stage == 7)
  6. Render template with all parameters
  7. Write .prompt.md file
  8. Run prompt compliance test against output
```

Mark generated prompts with `# AUTO-GENERATED by programstart prompt-build — do not hand-edit` header. Add `--eject` flag to convert a managed prompt to manually-maintained.

Register in CLI, add to coverage source, add tests.

**Verification**:
```powershell
uv run programstart prompt-build --stage feasibility --output /tmp/test-prompt.md
uv run pytest tests/test_prompt_compliance.py -q --tb=no
uv run pytest tests/test_programstart_serve.py -v --tb=short
```

---

### Phase M: Import Boilerplate Reduction + Script Organization (D-3, DX-1)

**Goal**: Reduce the ~600 lines of identical `try/except ImportError` boilerplate. Evaluate script namespace organization.

#### M-1: Centralize import fallback (D-3)

**Pre-flight**: Confirm the boilerplate pattern across scripts. Read 3-4 scripts to verify it's identical.

**Edit**: If the standalone-execution fallback (`python scripts/X.py`) is still needed:
- Create a helper in `programstart_common.py` that handles the import path setup
- Each script calls the helper instead of duplicating the try/except block

If standalone execution can be fully deprecated:
- Remove the try/except blocks entirely
- Add a deprecation warning for direct `python scripts/X.py` invocation
- Document `uv run programstart <command>` as the only supported entry point

#### M-2: Evaluate script namespace split (DX-1)

At 39 scripts and growing, evaluate whether subpackages would help. Proposed structure:
```
scripts/
  programstart_common.py     (stays — shared utilities)
  cli/                        (core CLI: status, guide, validate, advance, etc.)
  dashboard/                  (serve, browser smoke)
  factory/                    (create, bootstrap, scaffold, recommend)
  analysis/                   (drift, impact, retrieval, research_delta, context)
```

**Decision gate**: Only proceed if the count is ≥40 AND the import fallback boilerplate is resolved (D-3). Otherwise defer — the flat structure works for now.

**Verification**:
```powershell
uv run pytest --tb=no -q --no-header 2>&1 | Select-Object -Last 3
uv run programstart validate --check all --strict
```

---

### Phase N: Remaining Items — Polish + Future Track

This phase collects all remaining LOW, INFO, and Tier 3 strategic items. They can be addressed individually as time permits. No strict ordering.

#### Logging & Observability
- **H-2**: Introduce structured logging in `programstart_common.py` respecting `--verbose`/`--quiet`
- **H-3**: Add retry around `os.replace()` in `write_json` for Windows antivirus locks

#### Workflow Model
- **W-2**: Optional freshness tracking for stage completions (staleness after N days)
- **W-3**: Define entry criteria for critical USERJOURNEY phases
- **W-4**: Add `expected_outputs` field to workflow_guidance blocks

#### CLI Polish
- **F-3**: `--diff` flag for `programstart drift`
- **F-4**: `programstart state rollback` or `programstart state set --stage <name>`
- **F-5**: Unify `programstart clean` targets with `nox -s clean`

#### Sync Model
- **S-1**: Detect same-commit multi-file content drift (currently only cross-commit)
- **S-2**: Document staged-files behavior + add `--staged-only` flag to drift
- **S-3**: Add sync rule for `pyproject.toml` ↔ `requirements.txt`
- **S-4**: Narrow `knowledge_base_docs_alignment` sync rule to non-metadata changes

#### Rule Enforcement
- **R-6**: `copilot-instructions.md` rules are not runtime-enforceable (INFO — document as accepted risk, not actionable)

#### Prompt System
- **P-3**: Add kill-criteria/challenge-gate sections to USERJOURNEY prompts
- **P-4**: Consider `shape-implementation.prompt.md` for implementation sprints
- **P-5**: Decide on `argument-hint` — enforce or explicitly mark optional

#### Testing
- **T-5**: Add `nox -s mutation` session with `mutmut`
- **T-6**: Add `pytest-benchmark` tests for core hot paths
- **T-7**: Migrate individual `test_audit_fixes.py` tests to natural module test files

#### Dashboard
- **UI-3**: Per-OS golden screenshot baselines (or document why Linux-only is acceptable)

#### Knowledge Base
- **KB-2**: Add minimum score threshold to BM25 retrieval
- **KB-3**: Consider `programstart kb add-stack` subcommand

#### Bootstrap
- **B-1**: Improve header extraction — use metadata block pattern instead of `---` alone
- **B-2**: Consider splitting `programstart_create.py` into focused modules

#### Structural
- **SD-1**: Evaluate splitting `process-registry.json` into multiple files
- **SD-2**: Registry Pydantic models (S-6) for typed access
- **SD-3**: Document `devlog/` retention policy
- **SD-4**: Automate or document backup schedule

#### Guardrails
- **G-3**: Document branch protection rules in CONTRIBUTING.md

#### Strategic Tier 3 (evaluate when Tier 1-2 done)
- **S-5**: Prompt builder Mode B (arbitrary repos)
- **S-6**: Registry Pydantic models for typed access (see also SD-2)
- **S-7**: Prompt update channel (`programstart sync --from-template`)
- **S-8**: "Prompt-only" bootstrap mode
- **S-9**: VS Code webview extension (replace HTTP dashboard)
- **S-10**: Multi-repo orchestration
- **S-11**: LLM-in-the-loop prompt testing
- **S-12**: Feedback loop from generated repos

---

### Docs: Post-Implementation Verification

After all executed phases:

```powershell
uv run pytest --cov --cov-report=term-missing --tb=no -q 2>&1 | Select-Object -Last 40
uv run programstart validate --check all --strict
uv run programstart drift --strict
uv run pre-commit run --all-files
uv run mkdocs build --strict
```

Update `CHANGELOG.md` with all changes made. Commit with:

```
docs: update CHANGELOG for enhancement gameplan execution

Closes enhancegameplan Phases A–N as executed.
```

---

## 5. Execution Notes

### Dependency Graph

```
Pre-work → A (DRY consolidation + state write safety — touches common.py which other phases import)
         → B (UI blind spot — touches recommend.py, independent of A)
         → C (exceptions — independent of A and B)

A ← D (schema hardening — may need to validate updated common imports)
B ← I (recommendation structural — builds on B's alias + domain changes)

C, D, E ← F (CI — should be done after code changes stabilize)
         ← G (coverage push — benefits from C's exception handling fixes)

F, G ← H (workflow gates — validates the system after changes)

I ← J (docs — should reflect any new features from I)
J ← K (CLI features — tests may need doc updates)
K ← L (dashboard + prompt builder — largest phase, do last)
L ← M (structural — only after L stabilizes the codebase)

All ← N (polish — truly independent, do any time)
All ← Docs (final pass)
```

### Session Sizing

| Phase | Estimated Session Size | Notes |
|---|---|---|
| A | 1 focused session | Mechanical but touches many files — test carefully |
| B | 1 focused session | Small edits, clear verification |
| C | 1 focused session | Requires reading exception context per file |
| D | 1 focused session | Schema changes need validation against live data |
| E | 1 focused session | All new tests, straightforward |
| F | 1 focused session | Config/workflow edits, CI verification may need push |
| G | 1–2 sessions | Test writing for 4 modules |
| H | 1 focused session | Small logic additions with clear test points |
| I | 2 sessions | Largest feature phase — recommend + scaffold + eval + KB |
| J | 1 focused session | Doc edits, mostly mechanical |
| K | 2 sessions | 3-4 new features + prompt version field |
| L | 2–3 sessions | Major refactor (dashboard) + new tool (prompt builder) |
| M | 1 focused session | Depends on D-3 decision |
| N | Ongoing | Pick items as time allows |

**Total estimated: 15–20 focused sessions** for Phases A through M.
Phase N is open-ended polish.
