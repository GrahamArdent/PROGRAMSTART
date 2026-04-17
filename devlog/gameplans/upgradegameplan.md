# Upgrade Gameplan — Necessary Improvements for PROGRAMSTART

Purpose: Prioritized upgrade plan covering all necessary improvements identified from a full codebase audit on 2026-04-16. Addresses CI integrity, coverage debt, operator workflow gaps, architecture debt, release readiness, and remaining strategic items from the hardening gameplan.
Status: **IN PROGRESS**
Authority: Non-canonical working plan derived from full baseline audit (1488 tests, 92% coverage, pyright clean, validate PASS, drift PASS) on 2026-04-16.
Review scan count: **4** (Scan 1: baseline verification; Scan 2: post-update review; Scan 3: mutation scanner loop review; Scan 4: deadlock fix + accuracy corrections)
Last updated: 2026-04-17

---

## 1. Current State

Baseline recorded 2026-04-16 (post hardening Phases A–I, K complete; J partially complete):

- **1488 tests**, **0 failures**, **1 warning** (UserWarning in `detect_workspace_root` — cosmetic)
- **91.69% aggregate coverage** (8246 statements) on 42 source modules, `fail_under = 90`
- **Pyright**: 0 errors, 0 warnings, 0 informations
- `programstart validate --check all` PASSES
- `programstart drift` PASSES
- **Pre-commit**: **3 failures** — (1) ruff check: 27 errors across 4 files (11× E501 in `test_programstart_recommend.py`, 16× in `programstart_attach.py`, `programstart_mutation_edit_hook.py`, `programstart_mutation_loop.py`); (2) detect-secrets: 1 false positive (Base64 high-entropy string); (3) yamllint: `.pre-commit-config.yaml` line 49 exceeds 140 chars
- **MkDocs build**: succeeds but **39 broken cross-references across 11 ADR files** (links to files outside `docs/`)
- **Working tree**: **48 modified + 14 untracked files** (427 insertions, 89 deletions) — uncommitted changes from hardening J-phase work plus the Scan 4 deadlock fix. **This dirty tree must be committed or stashed before any upgrade work begins.**
- **Python**: 3.14.0
- **Package version**: 0.1.0
- **PROGRAMBUILD**: `inputs_and_mode_selection` — STALE (15 days as of 2026-04-16)
- **USERJOURNEY**: `phase_1` — STALE (20 days as of 2026-04-16)
- **Hardening gameplan**: Phases A–I COMPLETE, K-1 through K-10 COMPLETE, J-1 and J-2 COMPLETE, J-3 IN PROGRESS (13th run: 2209 killed / 1072 survived / 3281 total — 67.3% kill rate via scanner loop), J-4 through J-6 NOT STARTED

### Coverage Snapshot — Modules Below 90%

| Module | Coverage | Gap from 90% | Reason |
|---|---|---|---|
| `programstart_mutation_loop.py` | 53% | -37% | CLI-exposed developer tool (241 lines) — deadlock fix applied Scan 4; must reach ≥80% |
| `programstart_mutation_edit_hook.py` | 69% | -21% | CLI-exposed developer tool — must reach ≥80% |
| `programstart_backup.py` | 70% | -20% | **Production CLI command — unacceptable** |
| `install_hooks.py` | 84% | -6% | Git hook installer utility |
| `programstart_retrieval.py` | 85% | -5% | ChromaDB lines 469–527 permanently blocked |
| `programstart_serve.py` | 87% | -3% | HTTP handler/advance/save paths |
| `programstart_create.py` | 89% | -1% | CLI facade after core split |

### Coverage Snapshot — Modules at Boundary (90–91%)

| Module | Coverage | Note |
|---|---|---|
| `programstart_common.py` | 90% | 27 uncovered statements — fragile boundary |
| `programstart_closeout.py` | 90% | 5 uncovered statements |
| `programstart_create_core.py` | 90% | 16 uncovered statements after split |

---

## 2. Prioritized Gap Registry

### P0 — CI Gate Integrity (blocks everything)

| ID | Gap | Severity | Phase |
|---|---|---|---|
| **CI-01** | Pre-commit yamllint failure: `.pre-commit-config.yaml` line 49 exceeds 140 chars | BLOCKING | A |
| **CI-02** | MkDocs broken cross-references across 11 ADR files (39 broken links to files outside `docs/`) | HIGH | A |
| **CI-03** | Pre-commit ruff check failure: 27 errors across 4 files (E501 line-length + import violations) | BLOCKING | A |
| **CI-04** | Pre-commit detect-secrets failure: 1 false positive (Base64 high-entropy string) | BLOCKING | A |

### P1 — Coverage Floor Violations (below the 90% `fail_under` or near it)

| ID | Gap | Module | Current | Target | Phase |
|---|---|---|---|---|---|
| **COV-B1** | `programstart_backup.py` at 70% — production CLI command | backup.py | 70% → 97% | ≥90% | B ✅ |
| **COV-B2** | `install_hooks.py` at 84% — utility | install_hooks.py | 84% → 98% | ≥90% | B ✅ |
| **COV-B3** | `programstart_serve.py` at 87% — HTTP paths | serve.py | 87% → 94% | ≥90% | B ✅ |
| **COV-B4** | `programstart_create.py` at 89% — CLI facade | create.py | 89% → 95% | ≥90% | B ✅ |
| **COV-B5** | `programstart_retrieval.py` at 85% — ChromaDB blocked | retrieval.py | 85% → 90% | ≥88% | B ✅ |
| **COV-B6** | Mutation tooling (53%, 69%) — **now wired into CLI dispatch** (`mutation-edit-hook`, `mutation-loop` in `CLI_COMMANDS`) — must meet ≥80%. Deadlock fix (Scan 4) added `max_wait_seconds` timeout + 4 tests. | mutation_*.py | 53/69% → 95/97% | ≥80% | B ✅ |

### P2 — Boundary Consolidation (90–91%, fragile)

| ID | Gap | Module | Current | Target | Phase |
|---|---|---|---|---|---|
| **COV-C1** | `programstart_common.py` — 27 uncovered stmts | common.py | 90% → 96% | ≥93% | C ✅ |
| **COV-C2** | `programstart_closeout.py` — 5 uncovered stmts | closeout.py | 90% → 96% | ≥95% | C ✅ |
| **COV-C3** | `programstart_create_core.py` — 16 uncovered stmts | create_core.py | 90% → 96% | ≥93% | C ✅ |

### P3 — Operator Workflow Gaps

| ID | Gap | Severity | Phase |
|---|---|---|---|
| **OP-01** | No `jit-check` CLI command — JIT source-of-truth protocol is manual-only | HIGH | D |
| **OP-02** | No downstream sync mechanism — file changes can't propagate to adopted repos (Orchestra Agent) | MEDIUM | E |
| **OP-03** | Stale workflow state — both systems flagged stale with no explicit acknowledgment or deferral | LOW | F |

### P4 — Architecture Debt

| ID | Gap | Severity | Phase |
|---|---|---|---|
| **ARCH-01** | `validate.py` at 1710 lines (726 branches) — same monolith risk as pre-split `create.py` | MEDIUM | G |
| **ARCH-02** | Remaining J-4: Registry Pydantic models — `load_registry()` returns unvalidated dict | MEDIUM | G |

### P5 — Release Readiness

| ID | Gap | Severity | Phase |
|---|---|---|---|
| **REL-01** | Package still at 0.1.0 despite 15 ADRs, 1488 tests, 33 CLI commands, and a mature feature set | LOW | H |
| **REL-02** | CHANGELOG has no version sections — all changes under `[Unreleased]` | LOW | H |
| **REL-03** | No release workflow that bumps version + cuts changelog section | LOW | H |

### P6 — Remaining Strategic (from hardeninggameplan J-3 through J-6)

| ID | Gap | Severity | Phase |
|---|---|---|---|
| **STR-01** | J-3: Mutation testing survivor triage — kill/survive ratio at 2209/1072 (13th run via scanner loop) | LOW | I |
| **STR-02** | J-5: Prompt builder Mode B — arbitrary repos beyond bootstrapped | LOW | J |
| **STR-03** | J-6: `programstart sync --from-template` — prompt update channel | LOW | J |

---

## 3. Phase Sequence

| Phase | Gap(s) | Type | Est. scope | Target outcome |
|---|---|---|---|---|
| **0** | (none — prerequisite) | Dirty-tree resolution | 48 modified + 14 untracked | All hardening work committed; clean `git status` |
| **A** | CI-01, CI-02, CI-03, CI-04 | Gate repair | 5–8 files | Pre-commit (all 17 hooks) and MkDocs clean |
| **B** | COV-B1 through COV-B6 | Coverage floor enforcement | 4–6 test files | All production modules ≥90% (retrieval ≥88%, mutation ≥80%) |
| **C** | COV-C1 through COV-C3 | Boundary consolidation | 3 test files | Aggregate coverage ≥93% |
| **D** | OP-01 | `jit-check` CLI command | 4 files | Durable JIT protocol entry point |
| **E** | OP-02 | Downstream sync mechanism | 3–5 files | `programstart sync` command |
| **F** | OP-03 | Workflow state triage | State files + docs | Both systems un-staled or explicitly deferred |
| **G** | ARCH-01, ARCH-02 | Architecture debt | 5–8 files | validate.py split + Pydantic models |
| **H** | REL-01, REL-02, REL-03 | Release readiness | 3–5 files | Version bump to 0.9.0 + release workflow |
| **I** | STR-01 | Mutation triage closure | Test files | J-3 closed with documented survivor policy |
| **J** | STR-02, STR-03 | Strategic features | Multiple | Prompt Mode B + template sync |

---

## 4. Detailed Phase Instructions

### Phase 0: Dirty-Tree Resolution (prerequisite) ✅ d52f565

**Goal**: Commit or stash the 48 modified + 14 untracked files left over from hardening J-phase work and the Scan 4 deadlock fix. No upgrade work can begin on a dirty tree — this violates the JIT protocol’s "clean baseline" requirement.

**Pre-flight**:
```powershell
git status --short | Measure-Object  # Expect 62 lines
git diff --stat HEAD | Select-Object -Last 3  # Expect 48 files changed, 427 insertions, 89 deletions
```

**Steps**:
1. **Triage staged vs. unrelated changes**: Review the 48 modified files. Group them into logical commits (hardening J-phase work, ADR additions, test additions, tooling changes, deadlock fix).
2. **Commit in logical groups** using conventional commit format:
   - `feat(cli): wire mutation-edit-hook and mutation-loop into CLI dispatch`
   - `test(recommend): add comprehensive recommendation test suite`
   - `docs(adr): add ADRs 0014 and 0015`
   - `fix(mutation-loop): add max-wait timeout to prevent deadlock on orphan WSL processes`
   - `chore: update config fragments, .gitignore, tasks.json`
3. **Handle untracked files**: The 14 untracked files include `upgradegameplan.md`, `instructionsrepo.md`, mutation scripts/tests, orchestra reports, and ADR 0015. Decide per file: commit, `.gitignore`, or remove.
4. **Verify clean tree**:
```powershell
git status --short  # Expect 0 lines (or only intentionally untracked)
```

**Verification**:
```powershell
git status --short | Measure-Object  # 0 lines
uv run pre-commit run --all-files  # May still fail (that's Phase A's job)
uv run programstart validate --check all
uv run programstart drift
```

**Exit**: `git status --short` returns 0 lines. validate and drift both pass.

---

### Phase A: Gate Repair (CI-01, CI-02, CI-03, CI-04) ✅

**Goal**: Restore clean pre-commit and MkDocs baselines. This is the blocking prerequisite for every other phase. **Three** pre-commit hooks are currently failing, not one.

#### A-1: Fix yamllint long line in `.pre-commit-config.yaml` (CI-01)

**Pre-flight**: Read `.pre-commit-config.yaml` at line 49 to identify the offending entry.

**Edits**:
1. Break the long line at line 49 into a multi-line YAML format (use `|` block scalar or fold the URL/argument list).
2. Verify the hook still works after reformatting.

**Verification**:
```powershell
uv run pre-commit run yamllint --all-files
uv run pre-commit run --all-files
```

#### A-2: Fix MkDocs broken cross-references across 11 ADR files (CI-02)

**Pre-flight**: Run `uv run mkdocs build --strict 2>&1 | Select-String "not found"` to list all 39 broken links and the 11 affected files. The links point to files outside the `docs/` tree (e.g., `../../PROGRAMBUILD/...`, `../../config/...`, `../../scripts/...`, `../../devlog/...`).

**Edits**:
Two acceptable strategies (pick one):
1. **Convert to plain-text refs**: Replace clickable links to non-docs files with inline code references (`` `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` ``). This is the simpler approach since ADRs referencing source code can't resolve in MkDocs anyway.
2. **Add `docs_dir` symlinks or `nav` references**: More complex, only useful if those files should truly be browsable in the docs site.

Recommend option 1 — these are cross-references for human context, not navigable docs.

**Verification**:
```powershell
uv run mkdocs build --strict 2>&1 | Select-String "not found"
```
Expected: 0 matches.

#### A-3: Fix ruff check failures (CI-03)

**Pre-flight**: Run `uv run ruff check` to list all 27 errors. They are concentrated in 4 files:
- `tests/test_programstart_recommend.py` — 11× E501 (line too long)
- `scripts/programstart_attach.py` — E501 and import violations
- `scripts/programstart_mutation_edit_hook.py` — E501 and import violations
- `scripts/programstart_mutation_loop.py` — E501 and import violations

**Edits**:
1. Auto-fix what ruff can fix: `uv run ruff check --fix`.
2. For remaining E501 violations: break long lines manually or add `# noqa: E501` where breaking would reduce readability (e.g., long assert messages in tests).

**Verification**:
```powershell
uv run ruff check
uv run pre-commit run ruff-check --all-files
```
Expected: 0 errors found.

#### A-4: Fix detect-secrets false positive (CI-04)

**Pre-flight**: Run `uv run pre-commit run detect-secrets --all-files` to identify the flagged file and line. This is a Base64 high-entropy string being incorrectly flagged as a secret.

**Edits**: Two options:
1. **Update `.secrets.baseline`**: Re-run `detect-secrets scan > .secrets.baseline` and audit the results. Mark the false positive as allowed.
2. **Inline allowlist**: Add `# pragma: allowlist secret` to the flagged line if it's clearly not a secret.

Recommend option 1 — keeping the baseline current is better long-term hygiene than sprinkling suppressions.

**Verification**:
```powershell
uv run pre-commit run detect-secrets --all-files
```
Expected: Passed.

---

**Phase A verification**:
```powershell
uv run pre-commit run --all-files   # All 17 hooks must pass
uv run mkdocs build --strict         # 0 warnings
```
Expected: Both PASS with zero warnings. All 4 CI-0x items resolved.

---

### Phase B: Coverage Floor Enforcement (COV-B1 through COV-B6) ✅ bae73a6

**Goal**: Bring all production modules to ≥90% coverage. This is the single biggest quality gap — `backup.py` at 70% is a shipped CLI command with 30% of its logic untested.

#### B-1: Cover `programstart_backup.py` (COV-B1) — Critical

**Pre-flight**: Read `scripts/programstart_backup.py` at the uncovered lines: 37–42 (early validation), 49, 52, 54 (file-copy guards), 60–69 (manifest write path), 73–88 (CLI integration path), 150 (error path).

This module implements `programstart backup create --label <label>`. Uncovered paths likely include:
- Backup directory already exists
- Missing state files to back up
- Git commit hash resolution failure
- Manifest write error
- Label sanitization edge cases

**Edits**: In `tests/test_programstart_backup.py` (locate or create), add tests covering:
1. Successful backup with valid state files — assert directory and MANIFEST.txt created.
2. Backup when state file is missing — assert clear error, no partial directory left behind.
3. Backup with label containing special characters — assert sanitization or rejection.
4. Backup to an already-existing directory — assert error message and no overwrite.
5. Git hash resolution failure (no `.git/`) — assert backup still proceeds with "(unknown)" or similar.

**Verification**:
```powershell
uv run pytest tests/ -k "backup" --cov=scripts/programstart_backup --cov-report=term-missing --tb=short
```
Expected: backup.py ≥ 90%.

#### B-2: Cover `install_hooks.py` (COV-B2)

**Pre-flight**: Read `scripts/install_hooks.py` at uncovered lines: 27–28, 39–40, 54, 56–57, 81.

**Edits**: In `tests/test_install_hooks.py` (or `tests/test_audit_fixes.py`), add tests for:
1. Install when `.git/hooks/` doesn't exist — assert it's created.
2. `--uninstall` flag — assert hook file removed.
3. `--check` flag — assert exit code based on hook presence.
4. Install when hook already exists — assert overwrite or skip behavior.

**Verification**:
```powershell
uv run pytest tests/ -k "hook" --cov=scripts/install_hooks --cov-report=term-missing --tb=short
```
Expected: install_hooks.py ≥ 90%.

#### B-3: Cover `programstart_serve.py` (COV-B3)

**Pre-flight**: Read `scripts/programstart_serve.py` at the concentrated miss zones: 248–249, 276, 313, 377–378, 459–475, 553–632, 653–685, 751–791, 891–933.

These are HTTP handler error paths, advance/save request processing, and exception marshaling. The serve module has existing test infrastructure (test HTTP client or mock approach) from Phase C of the hardening gameplan.

**Edits**: Extend `tests/test_programstart_serve.py` with:
1. POST to advance endpoint with missing fields — assert 400 JSON error.
2. POST to save endpoint with corrupt JSON body — assert structured error response.
3. `update_implementation_tracker_slice` with valid and invalid payloads.
4. Request handler top-level exception path — send a request that triggers an unhandled exception in a mock handler.

**Verification**:
```powershell
uv run pytest tests/ -k "serve" --cov=scripts/programstart_serve --cov-report=term-missing --tb=short
```
Expected: serve.py ≥ 90%.

#### B-4: Cover `programstart_create.py` (COV-B4)

**Pre-flight**: Read `scripts/programstart_create.py` at lines 134–135, 190, 226–228, 244–246, 272, 279, 282. This is the slim CLI facade after the J-1 split — mostly dispatch and argument handling.

**Edits**: Add tests covering:
1. CLI invocation with invalid arguments — assert clean error exit.
2. CLI invocation that exercises the dispatch paths not hit by existing integration tests.
3. Help text rendering.

**Verification**:
```powershell
uv run pytest tests/ -k "create" --cov=scripts/programstart_create --cov-report=term-missing --tb=short
```
Expected: create.py ≥ 90%.

#### B-5: Cover `programstart_retrieval.py` mockable paths (COV-B5)

**Pre-flight**: Lines 469–527 are ChromaDB-only (permanently blocked). Remaining uncovered: 556 (pipeline error), 729–759 (LiteLLM generate), 779 (API error), 818, 821 (generation error), 909–937 (CLI subcommands).

**Edits**: Extend `tests/test_programstart_retrieval.py` with:
1. Mock `litellm.completion` for `_generate_litellm` and `_generate_structured` — verify parsing.
2. Mock API error raise at line 779 — verify error handling.
3. Test CLI `ask` and `search` subcommands via CliRunner or subprocess.

**Verification**:
```powershell
uv run pytest tests/ -k "retrieval" --cov=scripts/programstart_retrieval --cov-report=term-missing --tb=short
```
Expected: retrieval.py ≥ 88%. (ChromaDB block is documented and permanent.)

#### B-6: Cover mutation tooling (COV-B6) — CLI-exposed, not exemptable

**Pre-flight**: Read `scripts/programstart_mutation_loop.py` (229 lines) and `scripts/programstart_mutation_edit_hook.py` (720 lines). Both are now **wired into CLI dispatch** — `mutation-edit-hook` and `mutation-loop` are registered in `CLI_COMMANDS` in `programstart_command_registry.py` and dispatched via `programstart_cli.py`. This means they are operator-facing CLI commands, NOT internal-only automation.

**Current coverage**: `mutation_loop.py` at 53% (61/149 stmts missed, 241 lines), `mutation_edit_hook.py` at 69% (54/165 stmts missed, 720 lines). Combined: 314 statements, 115 missed, 63%.

**Scan 4 deadlock fix already applied**: `wait_for_no_active_mutation()` was an infinite `while True` loop with no timeout — orphan WSL mutmut worker processes after a cycle would deadlock the loop permanently. Fixed by adding `max_wait_seconds` (default 600s) with `time.monotonic()` deadline. 4 new tests added covering: immediate return, processes clearing, timeout firing, multi-process count in error message. This raised loop coverage from 48% → 53%.

**Coverage challenge**: The edit hook is 720 lines, but ~500 lines are scenario generator functions that build exact knowledge-base dicts for `recommend.py`. These are essentially test-data factories — not typical production logic. Covering them requires calling each `scenario_*()` function and verifying the rendered test string is valid Python.

**Decision**: Since they are CLI-exposed, they cannot be exempted from coverage requirements. Target ≥80% (not 90%) since they are developer-facing tools, not production ops.

**Edits**:
1. **Loop (53% → ≥80%)**: The remaining uncovered lines are `run_mutation_command()` (lines 104–118), `active_mutation_processes()` (lines 55–69), `run_shell_command()` (lines 88–100), and the main loop body (lines 217–277: subprocess + sleep + gate calls). The `wait_for_no_active_mutation()` timeout path is now covered (Scan 4 fix). Mock subprocess calls and exercise the main loop with `--cycles 1 --skip-gates --allow-repeat-without-edits` against a mocked `nox -s mutation` that returns a valid materialized summary.
2. **Edit hook (69% → ≥80%)**: The uncovered lines are the scenario generator function bodies (lines 42–652). Add tests that call each `scenario_*()` function and `compile()` the result to verify it's valid Python. Also test `run_external_command()` with a mocked subprocess, and `append_scenario()` + `record_application()` with a tmp_path.
3. Test CLI dispatch: `programstart mutation-edit-hook --help`, `programstart mutation-loop --help`.
4. Cover error paths: missing nox session, failed mutation run, missing diff output, `--cycles 0` rejection.

**Note**: If a future decision removes these from CLI dispatch (making them nox-only internal tools), an ADR should record that decision and they can be exempted at that point.

---

**Phase B verification**:
```powershell
uv run pytest --cov --cov-report=term --tb=no -q 2>&1 | Select-String "backup|install_hooks|serve|create|retrieval|mutation|TOTAL"
uv run programstart validate --check all
uv run programstart drift
```
Expected: All production modules ≥90% (retrieval ≥88%). Mutation tooling ≥80%. Total ≥93%.

---

### Phase C: Boundary Consolidation (COV-C1 through COV-C3) ✅ 2803eca

**Goal**: Push modules sitting at exactly 90% to ≥93% so they don't regress below the floor with a single missed branch.

#### C-1: Consolidate `programstart_common.py` (COV-C1)

**Pre-flight**: Read uncovered lines: 131, 138, 143, 170, 174–175, 184, 188–189, 358, 361–363, 369, 373–374, 387, 395, 403, 415, 536, 562, 564, 596, 602, 605, 608.

These are state-path edge cases, `run_command` timeout/error paths, `write_json` retry branches, and workspace detection fallbacks. Target the highest-value paths.

**Edits**: Add 5–8 tests targeting the listed lines. Priority: retry failure paths and state edge cases, since these affect correctness.

#### C-2: Consolidate `programstart_closeout.py` (COV-C2)

**Pre-flight**: Read uncovered lines: 50, 55, 113, 117, 151. Likely closeout validation error paths.

**Edits**: Add 2–3 tests for closeout failure modes (missing evidence, invalid state at closeout time).

#### C-3: Consolidate `programstart_create_core.py` (COV-C3)

**Pre-flight**: Read uncovered lines: 144, 150, 213–215, 283, 287, 299, 351, 356, 395, 412, 474, 528, 541–542. These are factory plan generation edge cases for less-exercised shapes.

**Edits**: Add 4–6 tests for uncommon shape/variant combinations that trigger the untested branches.

---

**Phase C verification**:
```powershell
uv run pytest --cov --cov-report=term --tb=no -q 2>&1 | Select-String "common|closeout|create_core|TOTAL"
```
Expected: common ≥93%, closeout ≥95%, create_core ≥93%. Total ≥93%.

---

### Phase D: `jit-check` CLI Command (OP-01) — COMPLETE

**Completed**: 2026-04-17. Commit `2f1c87d`. ADR-0017 (DEC-014). 6 tests added, 1723 total passing.

**Pre-flight**: Re-read `devlog/reports/instructionsrepo.md` for the **reference design (not approved for implementation — requires ADR before coding)**. Re-read `.github/instructions/source-of-truth.instructions.md` for the exact protocol steps.

**ADR checkpoint**: Before implementing, record the `jit-check` design as an ADR in `docs/decisions/`. The design in `instructionsrepo.md` is a reference sketch, not a binding decision. The ADR should cover: scope (what the command does and doesn't do), exit code semantics, interaction with existing `guide`/`drift` commands, and whether `jit-check` replaces or wraps those commands.

**What `programstart jit-check` does**:
1. Runs `programstart guide --system <system>` to derive the minimal file set (Step 1 of JIT protocol).
2. Runs `programstart drift` to verify baseline (Step 2 of JIT protocol).
3. Prints the authority → dependent file map from `config/process-registry.json` sync rules (supports Step 3).
4. Exits with status 0 if clean, status 1 if drift detected, status 2 if guide fails.

**Why it matters**: The JIT protocol is the core operational discipline of PROGRAMSTART. Running it is currently 3 separate commands that operators must remember in the right order. `jit-check` makes the protocol a single command.

**Edits**:
1. Add `"jit-check"` to `CLI_COMMANDS` in `scripts/programstart_command_registry.py`.
2. Implement `run_jit_check(system: str, strict: bool = False)` in `scripts/programstart_cli.py`:
   - Call `run_guide()` with `--system`.
   - Call `run_drift()`.
   - Print sync rule summary from registry.
   - Return aggregated exit code.
3. Update `.vscode/tasks.json` so `PROGRAMSTART: JIT Check` calls `uv run programstart jit-check --system programbuild`.
4. Add tests in `tests/test_programstart_cli.py`:
   - Test clean baseline → exit 0.
   - Test drift detected → exit 1.
   - Test with `--system programbuild` and `--system userjourney`.
5. Update `QUICKSTART.md` to mention `programstart jit-check` as the canonical protocol entry point.

**Verification**:
```powershell
uv run programstart jit-check --system programbuild
uv run pytest tests/ -k "jit_check" --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase E: Downstream Sync Mechanism (OP-02)

**Goal**: Implement a `programstart sync` command that propagates changed PROGRAMSTART files to an adopted downstream repo.

**Pre-flight**: Re-read `devlog/reports/instructionsrepo.md` § "Sync only the changed files" for the context. Re-read `scripts/programstart_attach.py` to understand the existing attach surface.

**Design**:
- `programstart sync --dest <path> [--dry-run] [--confirm] [--files <glob>]`
- Copies only the `scripts/`, `config/`, `.vscode/tasks.json`, and `tests/` files that were part of the original attachment.
- Uses a manifest file (`PROGRAMBUILD/.programstart-manifest.json`) written at attach time listing every file copied.
- `--dry-run` shows what would change without copying.
- **`--confirm` is required for actual writes** (no `--confirm` = `--dry-run` behavior). This prevents accidental overwrites of downstream customizations.
- Skips any file in the host repo's `.programstart-preserve` list (like the existing `README.md`/`.gitignore` preserve behavior from attach).

**ADR checkpoint**: Before implementing, record the sync mechanism design as an ADR. Key decisions: manifest format, conflict resolution strategy, `--confirm` vs. `--force` semantics, and whether sync is bidirectional or template-to-consumer only.

**Why it matters**: Without this, every change to PROGRAMSTART tooling requires manually identifying and copying files to every adopted repo. This is the operator pain point that emerged during the Orchestra Agent adoption.

**Edits**:
1. Modify `scripts/programstart_attach.py` to write `.programstart-manifest.json` during attach (list of all copied files, timestamps, source commit hash).
2. Create `scripts/programstart_sync.py` that reads the manifest, diffs source vs. dest, and copies changed files.
3. Register `"sync"` in `scripts/programstart_command_registry.py`.
4. Wire into `scripts/programstart_cli.py`.
5. Add tests: sync with no changes (no-op), sync with one changed file, sync with dry-run, sync with preserve list.

**Verification**:
```powershell
uv run programstart sync --dest "C:\PYTHON APPS\Orchestra Agent" --dry-run
uv run pytest tests/ -k "sync" --tb=short
uv run programstart validate --check all
```

---

### Phase F: Workflow State Triage (OP-03)

**Goal**: Resolve the stale workflow state flags. Both PROGRAMBUILD and USERJOURNEY have been stale for 15–20 days. Either advance them or explicitly defer them with a documented reason.

**Pre-flight**: Run `programstart next` to see what is blocking advancement.

**Decision tree**:
1. **If PROGRAMSTART-the-product is actively being worked**: Advance `inputs_and_mode_selection` to `feasibility` by completing the intake outputs. This is the normal path.
2. **If PROGRAMSTART is in maintenance/hardening mode**: Add a `deferred_reason` field to the state JSON and a `--defer` flag to `programstart advance` that marks a stage as intentionally paused without advancing it. This resets the staleness timer.
3. **If the USERJOURNEY attachment is no longer relevant**: Detach USERJOURNEY cleanly (remove USERJOURNEY_STATE.json reference from the workflow state).

**Most likely path**: PROGRAMSTART is a template/orchestration tool, not a user-facing product. The PROGRAMBUILD stages were bootstrapped for the template itself. If PROGRAMSTART is past the "inputs" phase in reality (it clearly is — it has 33 commands, 15 ADRs, 1488 tests), the state should be advanced to match reality, or the staleness detection should be taught about "template mode" where stage gates apply to generated repos, not to PROGRAMSTART itself.

**Recommended decision**: **Option B** — add `--defer` support. Rationale: PROGRAMSTART is a meta-tool; advancing its own PROGRAMBUILD stages to match a product lifecycle doesn't fit the template model. A `--defer` flag with documented reason is the most honest representation of the state.

**Edits** (depends on decision):
- Option A: Advance both systems to match actual reality, signing off completed stages.
- Option B: Add `--defer` support and defer both systems with documented reasons.
- Option C: Create a "template" variant that disables staleness for the PROGRAMSTART repo itself.

**Verification**:
```powershell
uv run programstart next
uv run programstart state show
uv run programstart validate --check all
```
Expected: No STALE flags in `next` output.

---

### Phase G: Architecture Debt (ARCH-01, ARCH-02)

**Goal**: Address the two remaining architecture risks.

#### G-1: Split `programstart_validate.py` (ARCH-01)

**Pre-flight**: Read `scripts/programstart_validate.py` (1710 lines, 726 branches). Identify logical sections: per-check-mode functions, schema validation, authority-sync checks, planning references, workflow-state checks, bootstrap-assets checks, ADR coverage, placeholder scanning, prompt-registry checks, CLI dispatch.

Follow the same approach as J-1 (create.py split):
- `programstart_validate_core.py` — individual check implementations.
- `programstart_validate.py` — CLI facade, dispatch, and result accumulation.

**Why**: 1710 lines with 726 branches makes this the hardest module to reason about and test. The split doesn't change behavior but makes each check mode independently testable and reviewable.

**ADR checkpoint**: Record the split decision as an ADR, documenting: which functions move to core, any API changes to the validation result type, and how it affects coverage tracking.

**Edits**:
1. Extract per-check functions to `programstart_validate_core.py`.
2. Keep CLI dispatch in `programstart_validate.py`.
3. Update imports. Add `programstart_validate_core` to coverage config.
4. All existing tests must pass without changes.

#### G-2: Complete J-4: Registry Pydantic Models (ARCH-02)

**Pre-flight**: Read `scripts/programstart_models.py` to see what models already exist. Read `scripts/programstart_common.py` `load_registry()` to see the current dict-based return.

**Note**: `programstart_models.py` already exists at 100% coverage. Assess whether the Pydantic models are already complete and just not wired to `load_registry()`, or if the model definitions need extension.

**Edits**:
1. If models exist but aren't used: update `load_registry()` to validate through the Pydantic models on load. Add a `--validate-schema` flag to `validate` that exercises the Pydantic path.
2. If models need extension: add `ProgramBuildSystem`, `UserJourneySystem`, `SyncRule`, `WorkflowGuidance` models. Don't break the existing dict API — expose a `load_validated_registry()` alongside the existing function.

**Verification**:
```powershell
uv run pytest tests/ -k "model or registry" --tb=short
uv run programstart validate --check all
uv run --extra dev pyright
```

---

### Phase H: Release Readiness (REL-01, REL-02, REL-03)

**Goal**: Prepare PROGRAMSTART for a semver release that reflects its actual maturity.

#### H-1: Version bump to 0.9.0 (REL-01)

**Pre-flight**: Assess whether 1.0.0 is justified:
- 33 CLI commands ✓
- 15 ADRs ✓
- 1488 tests ✓
- Full CI pipeline ✓
- Used to manage a real downstream project (Orchestra Agent) ✓
- Stable public API (CLI surface, registry format, state format) — **not yet committed**

**Recommendation**: Use **0.9.0**, not 1.0.0. Rationale:
- API stability has not been explicitly committed (no stability policy doc exists).
- Phases D, E, and G introduce new commands and potentially breaking refactors.
- The `sync` mechanism (Phase E) may reshape the public surface.
- 1.0.0 should be reserved for after the upgrade gameplan is complete and the API surface is explicitly frozen.

**Edits**:
1. Bump `version` in `pyproject.toml` to `0.9.0`.
2. Move content from `[Unreleased]` to `[0.9.0] - 2026-XX-XX` in `CHANGELOG.md`.
3. Git tag `v0.9.0`.

#### H-2: Add release workflow (REL-03)

**Pre-flight**: Read `.github/workflows/release-package.yml` — this may already exist.

**Edits** (if not present):
1. Create or update `.github/workflows/release-package.yml` to:
   - Trigger on tag push matching `v*`.
   - Build wheel.
   - Upload to GitHub Releases.
   - Run `nox -s ci` as a pre-release gate.

**Verification**:
```powershell
uv build
uv run nox -s package
```

---

### Phase I: Mutation Triage Closure (STR-01)

**Goal**: Close J-3 from the hardening gameplan with a documented survivor policy instead of continuing indefinite triage.

**Pre-flight**: Re-read J-3 checkpoint in `hardeninggameplan.md`. Current state: 13 runs (12 manual + 1 automated via scanner loop), 2209 killed, 1072 survived out of 3281 total (67.3% kill rate).

#### Scanner Loop Results (run today, 2026-04-16)

The `programstart mutation-loop` + `programstart mutation-edit-hook` pipeline ran its first automated cycle:
- **Before (12th manual run)**: killed=2189, survived=1092 (66.7%)
- **After (13th run, 1st automated)**: killed=2209, survived=1072 (67.3%)
- **Delta**: +20 killed, −20 survived in a single unattended cycle (~19 min at 3.98 mut/s)
- **Edit hook applied 2 scenarios**: `test_build_stack_candidates_mobile_resilience_exact_output` and `test_main_text_output_detailed_exact`
- **Remaining internal scenarios**: 7 of 9 still available
- **Cycles remaining on loop config**: 24 of 25

**Top survivor hotspots after 13th run**:

| Hotspot function | Survivors |
|---|---|
| `build_stack_candidates()` | 166 |
| `build_recommendation()` | 100 |
| `main()` | 95 |
| `infer_domain_names()` | 91 |
| `select_triggered_entries()` | 85 |
| `re_evaluate_project()` | 67 |
| `build_actionability_summary()` | 59 |

#### Scanner Loop Reusability Assessment

The `mutation-loop` + `mutation-edit-hook` pipeline is a **well-designed automation pattern** but has **narrow reusability as-is**:

**What works well (reusable pattern)**:
1. The loop driver (`mutation_loop.py`) is target-agnostic — it runs `nox -s mutation`, parses materialized summaries, records JSONL history, and updates status. This machinery needs zero changes to target a different module.
2. The JSONL history + status file pattern is clean and composable.
3. The `--before-cycle-command` hook point is a good extensibility seam.
4. The WSL-aware polling for active mutation processes is solid infrastructure.

**What is NOT reusable (hardcoded to recommend.py)**:
1. `mutation_edit_hook.py` has 9 scenario generators that are **entirely hardcoded to `programstart_recommend.py`** — each one builds exact knowledge-base dicts and calls specific recommend.py functions. None of these can target a different module.
2. The `SURVIVOR_KEY_RE` regex in both files is hardcoded to `scripts\.programstart_recommend\.x_`.
3. `[tool.mutmut].paths_to_mutate` in `pyproject.toml` is fixed to `["scripts/programstart_recommend.py"]`.
4. The `current_hotspots()` function reads from `mutants/scripts/programstart_recommend.py.meta` — a fixed path.
5. The 15-cycle autonomy prompt (`mutation_15_cycle_autonomy_prompt.md`) explicitly says "do not broaden mutation scope beyond `scripts/programstart_recommend.py`".

**To reuse for other modules**, you would need:
1. Make `paths_to_mutate` configurable (CLI flag or multiple mutmut profiles).
2. Make `SURVIVOR_KEY_RE` derive the module key from config rather than a constant.
3. Write a NEW edit hook with module-specific scenario generators for each target (this is the expensive part — each scenario requires deep domain knowledge of the target module's API).
4. The loop driver itself can be reused as-is with `--before-cycle-command` pointing to a different hook.

**Assessment**: The **loop driver is reusable today**. The **edit hook is not** — it's a one-off artifact for `recommend.py`, and writing equivalent scenario generators for other modules (e.g., `validate.py`, `serve.py`) would be a significant effort per module. The edit hook architecture is sound, but the scenario content is inherently module-specific.

**Recommendation for gameplan**: Do NOT plan to use the scanner loop for other modules during this upgrade cycle. The 7 remaining internal scenarios will exhaust within ~7 more automated cycles. After that, the hook becomes a no-op (with `--allow-noop`) and re-runs add diminishing value. The scanner loop's primary contribution is proving the automation pattern and closing J-3 with a measurable final baseline.

#### Closure Decision

**Decision**: A 67.3% kill rate on the recommendation engine is reasonable for a planning tool. The surviving mutants are concentrated in scoring and presentation logic where behavioral changes are caught by integration tests and operator review rather than unit assertions.

**Edits**:
1. Run the remaining 7 internal scenarios through the scanner loop (≤7 more cycles) to reach a natural plateau.
2. Document the final survivor policy: "Surviving mutants in `programstart_recommend.py` are accepted when they affect scoring precision or presentation formatting that is validated by integration and operator review rather than unit assertion. The kill target is ≥65%."
3. Record the final numbers in `hardeninggameplan.md` J-3 section with the scanner loop run history.
4. Mark J-3 as COMPLETE with the documented policy.
5. The scanner loop output files (`mutation_loop_runs.jsonl`, `mutation_loop_status.json`, `mutation_edit_hook_history.jsonl`) become the audit trail.

**Prerequisite**: The Scan 4 deadlock fix (`max_wait_seconds` timeout in `wait_for_no_active_mutation`) MUST be committed before running the scanner loop again. Without it, orphan WSL mutmut worker processes will deadlock the loop after cycle 1 — this is exactly what stopped the first run at 1/25 cycles.

**Verification**:
```powershell
uv run programstart mutation-loop --cycles 7 --max-wait-seconds 600 --before-cycle-command "uv run programstart mutation-edit-hook --allow-noop"
# After completion, verify final numbers:
Get-Content outputs/research/mutation_loop_status.json
```
Expected: 7 cycles complete (~2.2 hours total at ~19 min/cycle). If a cycle hits the 600s timeout on orphan processes, it will error cleanly instead of deadlocking.

---

### Phase J: Strategic Features (STR-02, STR-03)

**Goal**: Implement the remaining strategic items from the hardening gameplan. These are lower priority and each is its own session.

#### J-1: Prompt builder Mode B (STR-02)

Accept arbitrary repo context (not just bootstrapped projects) in `programstart prompt-build`. This enables using PROGRAMSTART's prompt generation for any repo.

#### J-2: `programstart sync --from-template` (STR-03)

Pull latest prompts and tooling from the PROGRAMSTART template into the current project. This is the inverse of `programstart sync --dest` from Phase E — it updates the consumer repo from the template.

**Each J-* item requires its own session and planning pass before starting.**

---

## 5. Dependency Graph

```
0 (dirty-tree) ─────────────────────┐
                                     │
A (gate repair) ─────────────────────┤
                                     ▼
B (coverage floor) ──→ C (boundary) ──→ H (release)
                                     │
D (jit-check) ─────────────────────→─┤
                                     │
E (downstream sync) ────────────────→─┤
                                     │
F (workflow triage) ────────────────→─┤
                                     │
G (arch debt) ──────────────────────→─┘
                                     │
I (mutation close) ──── independent ──┘
J (strategic) ────── independent ─────
```

Phase A is the only hard dependency (after Phase 0) — everything else blocks on a clean gate. Phases B–G can be done in any order after A. Phase H should come last since it cuts a release. Phases I and J are independent of everything.

**Note**: Phase J-2 (`sync --from-template`) is the inverse of Phase E (`sync --dest`). If both are implemented, they should share manifest format and conflict resolution logic. Design E's manifest with J-2 in mind.

---

## 6. Verification Suite

Run after completing all phases:

```powershell
uv run pre-commit run --all-files
uv run mkdocs build --strict
uv run --extra dev pyright
uv run pytest --cov --cov-report=term-missing --tb=no -q 2>&1 | Select-String "^TOTAL|FAIL|PASS"
uv run programstart validate --check all --strict
uv run programstart drift --strict
uv run nox -s gate_safe
```

All MUST pass. Coverage MUST be ≥93% total. No module below 90% except retrieval.py (≥88%) and mutation tooling (≥80%).

---

## 7. Exit Criteria

Each phase has a binary pass/fail gate. A phase is not complete until all its exit criteria are met.

| Phase | Exit Criteria |
|---|---|
| **0** | `git status --short` returns 0 lines; validate PASS; drift PASS |
| **A** | `uv run pre-commit run --all-files` — all 17 hooks PASS; `uv run mkdocs build --strict` — 0 warnings |
| **B** | All production modules ≥90% (retrieval ≥88%, mutation ≥80%); `fail_under = 90` PASSES |
| **C** | common ≥93%, closeout ≥95%, create_core ≥93%; aggregate ≥93% |
| **D** | `programstart jit-check --system programbuild` exits 0; ADR recorded; tests pass |
| **E** | `programstart sync --dest <path> --dry-run` produces correct diff; `--confirm` required for writes; ADR recorded; tests pass |
| **F** | `programstart next` shows no STALE flags; decision documented |
| **G** | validate.py ≤400 lines (facade); validate_core.py exists; Pydantic models wired; all tests pass; ADR recorded |
| **H** | `pyproject.toml` version = 0.9.0; CHANGELOG has `[0.9.0]` section; `uv build` succeeds; `nox -s package` PASSES |
| **I** | J-3 marked COMPLETE in hardeninggameplan.md; survivor policy documented |
| **J** | Each J-* sub-item has its own ADR and test suite |

---

## 8. Rollback Plan

If a phase introduces a regression:

1. **Before each phase**: Create a git tag `pre-phase-X` (e.g., `pre-phase-A`).
2. **If regression detected**: `git revert` the phase commits back to the `pre-phase-X` tag.
3. **Do not cherry-pick forward** — revert the entire phase, diagnose, and re-apply cleanly.
4. **Phase 0 is irreversible** (it commits existing work) — but it's also risk-free since it only commits what's already in the working tree.

---

## 9. Session Boundary Guidance

Each phase should be completed in a single session where possible. Between sessions:

1. **Commit all work** — no dirty tree between sessions.
2. **Run the phase exit criteria** before ending the session.
3. **If a phase spans sessions**: Update this gameplan with progress notes at the end of each session (e.g., "B-1 through B-3 complete, B-4 in progress").
4. **Re-verify baseline** at the start of each new session: `uv run pre-commit run --all-files && uv run programstart validate --check all && uv run programstart drift`.
5. **Maximum recommended session scope**: 1–2 phases per session (A+B is fine, A+B+C+D is too much).

---

## 10. Commit Convention

```
chore: Phase 0 — commit hardening J-phase work and resolve dirty tree
fix(ci): Phase A — repair yamllint, ruff, detect-secrets, and MkDocs broken links
feat(coverage): Phase B — enforce 90% floor on backup, serve, create, hooks, retrieval, mutation
feat(coverage): Phase C — consolidate common, closeout, create_core to 93%+
feat(cli): Phase D — add jit-check command for source-of-truth protocol
feat(cli): Phase E — add downstream sync mechanism with manifest tracking
chore(state): Phase F — triage and resolve stale workflow state
refactor(validate): Phase G-1 — split validate.py into core and facade
feat(models): Phase G-2 — wire Pydantic registry models to load_registry()
chore(release): Phase H — version bump to 0.9.0 and release workflow
docs(mutation): Phase I — close J-3 with documented survivor policy
feat(prompt-build): Phase J-1 — Mode B arbitrary repo context
feat(sync): Phase J-2 — programstart sync --from-template
```

---

## 11. Implementation Prompt

**Status**: SATISFIED — `execute-upgrade-gameplan.prompt.md` created and registered in `operator_prompt_files` per ADR-0016 (DEC-013).

**Prompt specification**: The execution prompt MUST follow `OPERATOR_PROMPT_STANDARD.md` and include all 10 mandatory sections:

1. YAML frontmatter (description, name, argument-hint, agent, version)
2. Data Grounding Rule (verbatim from standard)
3. Protocol Declaration (JIT Steps 1–4, authority hierarchy)
4. Pre-flight (baseline checks; failures are stop conditions)
5. Authority Loading (this gameplan, process-registry, ARCHITECTURE.md)
6. Scope Guard (permits only upgrade work; forbids unrelated feature delivery)
7. Execution Protocol (phase-by-phase loop: read → pre-flight reads → implement → test → validate/drift/typecheck → commit → update gameplan status)
8. Resumption Protocol (run gates, git log, find first incomplete phase, re-read)
9. Verification Gate (validate, drift, pyright, pytest, pre-commit)
10. Completion Rule (update gameplan status, record ADR triage outcome)

**Governance close-out loop**: MUST be included per ADR-0013 — the upgrade gameplan changes durable structure. Minimum: `validate --check adr-coverage`, `validate --check authority-sync`, `drift`, then ADR triage.

**Why this matters**: The gameplan is a planning document, not an execution document. An execution prompt converts each phase into a self-contained agent task that can be picked up in any session without re-reading the entire gameplan. It enforces JIT protocol, scope guards, and verification gates — the same machinery that keeps hardening, enhancement, and remediation gameplans trustworthy.
