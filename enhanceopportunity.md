# PROGRAMSTART Enhancement Opportunities

Critical audit of the entire PROGRAMSTART system — covering hardening, workflow, automation, features,
rule enforcement, documentation, sync, prompting, guardrails, and structural health.

Date: 2026-04-14
Scope: Full repository — scripts, tests, config, CI, prompts, schemas, docs, workflows

---

## Table of Contents

1. [Code Hardening](#1-code-hardening)
2. [Duplicate Code & DRY Violations](#2-duplicate-code--dry-violations)
3. [Test & Coverage Gaps](#3-test--coverage-gaps)
4. [Automation & CI Opportunities](#4-automation--ci-opportunities)
5. [CLI & Feature Enhancements](#5-cli--feature-enhancements)
6. [Rule Enforcement Gaps](#6-rule-enforcement-gaps)
7. [Documentation Gaps](#7-documentation-gaps)
8. [Sync & Drift Model Improvements](#8-sync--drift-model-improvements)
9. [Prompt System Improvements](#9-prompt-system-improvements)
10. [Schema & Validation Hardening](#10-schema--validation-hardening)
11. [Guardrails & Safety Nets](#11-guardrails--safety-nets)
12. [Workflow Model Weaknesses](#12-workflow-model-weaknesses)
13. [Dependency & Supply Chain](#13-dependency--supply-chain)
14. [Dashboard & Web UI](#14-dashboard--web-ui)
15. [Knowledge Base & Retrieval](#15-knowledge-base--retrieval)
16. [Bootstrap & Factory](#16-bootstrap--factory)
17. [Developer Experience](#17-developer-experience)
18. [Structural Debt](#18-structural-debt)

---

## 1. Code Hardening

### H-1. Bare `except Exception` clauses suppress real errors (MEDIUM)

15 instances of `except Exception` across production scripts. Most swallow the error silently
or log a generic message. Particularly concerning in:
- `programstart_serve.py` (lines 235, 342): server request handlers silently eat errors
- `programstart_retrieval.py` (lines 669, 687, 931): RAG pipeline errors silently degraded
- `programstart_dashboard_browser_smoke.py` (lines 147, 220, 268, 293): smoke tests hiding failures

**Recommendation:** Replace bare `except Exception` with specific exception types. Where a catch-all is
genuinely needed, at minimum log the exception with traceback so failures are diagnosable.

### H-2. No structured logging anywhere (LOW)

Only `programstart_retrieval.py` uses `logging` (2 calls). Every other script uses raw `print()`
for output. This makes it impossible to filter by severity, route output to files, or integrate
with observability tools.

**Recommendation:** Introduce a thin `logging` setup in `programstart_common.py` that respects
`--verbose` / `--quiet` flags. Non-breaking — `print()` can remain for user-facing CLI output
while logging handles diagnostic output.

### H-3. `write_json` uses `tempfile.NamedTemporaryFile` for atomic writes but doesn't handle Windows rename failures (LOW)

`programstart_common.py` writes JSON via temp file + rename. On Windows, `os.replace()` can fail
if antivirus has the target file locked. The noxfile has a `remove_tree` retry loop for this
exact Windows issue, but `write_json` does not.

**Recommendation:** Add a small retry around `os.replace()` in `write_json`, matching the pattern
already used in `remove_tree`.

### H-4. `programstart_serve.py` has no request rate limiting or timeout (LOW)

The dashboard server binds to localhost only (good), but has no protection against a runaway
local process flooding it with requests. No `timeout` on subprocess calls either — a hung
command could block the server indefinitely.

**Recommendation:** Add `timeout=60` to `subprocess.run()` calls in `run_command()` and
`run_bootstrap()`. Consider a basic per-IP rate limiter for POST endpoints (even on localhost,
a misbehaving browser tab or automation script could DoS the server).

---

## 2. Duplicate Code & DRY Violations

### D-1. `system_is_optional_and_absent()` duplicated in 4 scripts (HIGH)

Identical function defined independently in:
- `programstart_validate.py` (line 45)
- `programstart_drift_check.py` (line 31)
- `programstart_log.py` (line 40)
- `programstart_workflow_state.py` (line 58)

Each has its own set of tests monkeypatching the local copy. This is the most obvious DRY
violation in the codebase. One implementation in `programstart_common.py` would eliminate
4 definitions + reduce test surface.

**Recommendation:** Move to `programstart_common.py`, update all imports, collapse duplicate tests.

### D-2. `system_is_attached()` duplicated in 4 scripts (HIGH)

Identical (or near-identical) function defined independently in:
- `programstart_markdown_parsers.py` (line 221) — note reversed parameter order
- `programstart_dashboard.py` (line 40)
- `programstart_step_guide.py` (line 32)
- `programstart_status.py` (line 31)

Different function signatures (`registry, system_name` vs `system_name, registry`) make this
especially fragile — callers must remember which module has which argument order.

**Recommendation:** Consolidate into `programstart_common.py` with a single, consistent signature.

### D-3. Repeated `try/except ImportError` boilerplate in every script (MEDIUM)

Every script has a ~15-line `try/except ImportError` block to handle both package and standalone
import paths. This is ~600 lines of identical boilerplate across 30+ scripts.

**Recommendation:** This exists to support `python scripts/programstart_X.py` direct execution,
which is explicitly deprecated (every script warns about it). Consider whether this fallback
path is still worth maintaining. If kept, a helper in `programstart_common.py` could reduce the
per-file boilerplate.

---

## 3. Test & Coverage Gaps

### T-1. `programstart_serve.py` at 83% coverage — lowest of any production module (MEDIUM)

64 uncovered lines. The web server has the most complex attack surface in the codebase and the
least test coverage. Key uncovered areas include POST request handling, error paths in bootstrap
execution, and signoff mutation logic.

**Recommendation:** Priority coverage target. Add tests for: signoff POST flow, malformed JSON
handling, bootstrap error paths, `READONLY_MODE` enforcement on mutation endpoints.

### T-2. `programstart_retrieval.py` at 85% — RAG pipeline undertested (MEDIUM)

61 uncovered lines. The vectorDB integration paths (`chromadb` optional dependency) and the
RAG response generation are largely untested because they require the `[rag]` optional
dependency group.

**Recommendation:** Add conditional tests (skip if chromadb not installed) for the vector
search path. Mock-based tests for the RAG response formatting.

### T-3. `programstart_research_delta.py` at 80% — lowest coverage of any module (MEDIUM)

28 uncovered lines. The review completion flow and issue sync logic are not tested.

**Recommendation:** Add tests for `complete_review()` and the status report generation paths.

### T-4. `programstart_create.py` at 90% — 25 uncovered lines in the factory (LOW)

The one-shot project factory is complex (1040+ LoC) and several error paths are not covered:
GitHub repo creation, service provisioning error handling, and the `--open-in-vscode` flag.

**Recommendation:** Add mock-based tests for GitHub API error paths and service provisioning.

### T-5. No mutation testing (LOW)

The test suite has excellent line coverage (93%) but no mutation testing to verify the quality
of assertions. A tool like `mutmut` or `cosmic-ray` would identify tests that pass even when
code logic is inverted.

**Recommendation:** Add a `nox -s mutation` session as an optional quality gate.

### T-6. No performance regression tests (LOW)

No benchmarks for context indexing, retrieval search, or dashboard startup time. Regressions
in these areas would be invisible until a user notices.

**Recommendation:** Add a few `pytest-benchmark` tests for core hot paths.

### T-7. Test file `test_audit_fixes.py` is a grab-bag (LOW)

This file accumulates one-off regression tests for audit findings. As it grows, it becomes
harder to find where a specific behavior is tested.

**Recommendation:** When stable, move individual tests to their natural module test files.

---

## 4. Automation & CI Opportunities

### A-1. No CI job for Python 3.14 on Windows (MEDIUM)

`process-guardrails.yml` runs on `[ubuntu-latest, windows-latest]` but only `python-version: ['3.12']`.
`full-ci-gate.yml` has a `compatibility-smoke` job for `['3.13', '3.14']` but only on `ubuntu-latest`.
Windows + 3.13/3.14 is untested in CI.

**Recommendation:** Add Python 3.13 to the guardrails matrix for both OS targets. 3.14 can
remain Linux-only until it stabilizes.

### A-2. No automatic CHANGELOG update enforcement (MEDIUM)

CHANGELOG.md is manually maintained. There is no CI check that a PR touching production code
also updates the changelog.

**Recommendation:** Add a `danger`-style check or a simple script that fails CI if `scripts/`
or `config/` changed but `CHANGELOG.md` did not. Exempt `chore:` and `ci:` commits.

### A-3. No dependabot configuration for GitHub Actions (MEDIUM)

`dependabot.yml` covers `pip` dependencies but not `github-actions`. The workflow files pin
actions by SHA (good), but Dependabot won't open PRs when new SHA versions are available.

**Recommendation:** Add a `github-actions` ecosystem entry to `dependabot.yml`.

### A-4. `nox -s ci` includes `format_check` but the guardrails CI does not (LOW)

The nox `ci` session lists `format_check` as a gate, but `process-guardrails.yml` relies on
`pre-commit run --all-files` which includes ruff-format. These are functionally equivalent
but the nox session runs it twice — once via pre-commit and once standalone.

**Recommendation:** Remove `format_check` from the nox `ci` session since `lint` already runs
pre-commit which includes ruff-format.

### A-5. No scheduled dependency audit workflow (LOW)

`pip-audit` runs in CI on PRs but there's no weekly scheduled scan for newly disclosed CVEs
in existing dependencies (unlike the weekly research delta which does run scheduled).

**Recommendation:** Add a scheduled `pip-audit` job or add it to the existing `full-ci-gate.yml`
daily run.

### A-6. Coverage is not uploaded as a check (LOW)

Coverage XML is uploaded as an artifact but not posted as a PR check or comment. Contributors
can't see at a glance whether their PR improved or regressed coverage.

**Recommendation:** Add `codecov` or `coverage-comment` action to the guardrails workflow.

---

## 5. CLI & Feature Enhancements

### F-1. `programstart create` lacks a `--list-shapes` flag (MEDIUM)

Users must read docs or source code to discover available product shapes. The recommendation
engine knows all shapes but there's no CLI flag to list them.

**Recommendation:** Add `programstart recommend --list-shapes` and/or `programstart create --list-shapes`.

### F-2. No `programstart doctor` command for environment diagnostics (MEDIUM)

When something fails, users have to manually check Python version, uv installation, Playwright
browsers, pre-commit hooks, etc. A diagnostic command would reduce support burden.

**Recommendation:** Add `programstart doctor` that checks: Python version, uv, playwright
browser installed, pre-commit installed, registry schema valid, state files valid, git repo
initialized.

### F-3. No `programstart diff` command to preview changes (LOW)

The drift check says _what_ drifted but not _how_. Users have to manually diff files to
understand what changed.

**Recommendation:** Add `--diff` flag to `programstart drift` that shows the actual content
differences when authority/dependent mismatches are detected.

### F-4. No `programstart undo` or state rollback (LOW)

If `programstart advance` is run prematurely, there's no CLI way to revert the state file
to the previous stage. Users must manually edit the JSON.

**Recommendation:** Add `programstart state rollback` that reverts to the previous stage,
or at minimum `programstart state set --stage <name>`.

### F-5. `programstart clean` doesn't clean terminal history artifacts (LOW)

The clean command removes build artifacts but not `.tmp_nox_*` directories created by nox
sessions. The nox `clean` session handles these, but the CLI doesn't.

**Recommendation:** Unify the clean targets. `programstart clean` should handle what
`nox -s clean` handles.

### F-6. No `--json` output mode for `programstart status` (LOW)

`programstart status` prints human-readable text, but there's no machine-readable output mode.
Other commands (`prompt-eval`, `research`) support `--json` already.

**Recommendation:** Add `--json` flag to `programstart status`, `programstart guide`, and
`programstart drift` for pipeline/automation consumers.

---

## 6. Rule Enforcement Gaps

### R-1. `conventional-commits.instructions.md` defines valid types, but `check_commit_msg.py` is the only enforcer (MEDIUM)

The instruction file lists types `feat|fix|docs|chore|ci|refactor|test`. If a new type is
added to the instructions but not to the script's regex, commits would pass the instructions
but fail the hook (or vice versa). There's no test that the two stay in sync.

**Recommendation:** Add a test that extracts the valid types from the instruction file's
markdown table and asserts they match `check_commit_msg.py`'s `VALID_TYPES` set.

### R-2. Prompt standard compliance is checked in tests but not in pre-commit (MEDIUM)

`test_prompt_compliance.py` runs 117+ parametrized tests for prompt standard conformance,
but this only runs during `pytest`. Pre-commit doesn't run pytest, so a non-compliant prompt
could be committed if the developer doesn't run the full test suite.

**Recommendation:** Add a lightweight pre-commit hook that checks prompt YAML frontmatter
for required fields when `.prompt.md` files change.

### R-3. No enforcement that new scripts get added to coverage source (LOW)

A developer can add a new `scripts/programstart_*.py` file and forget to add it to
`[tool.coverage.run] source`. There's no test or CI check for this.

**Recommendation:** Add a test that scans `scripts/` for production `.py` files and asserts
each one is listed in `pyproject.toml` coverage sources (with a known exclusion list for
smoke scripts).

### R-4. No enforcement that new ADRs update the `docs/decisions/README.md` index (LOW)

ADR files can be created without updating the index table. The README says "Update this index
whenever a new ADR is added" but nothing enforces it.

**Recommendation:** Add a test that lists `docs/decisions/0*.md` files and asserts each has
a row in the README index table.

### R-5. `process-registry.json` version is manually bumped (LOW)

The registry version is `"2026-04-11"` — it's supposed to be updated when the registry changes,
but nothing enforces this. A change to `sync_rules` without bumping the version would go
unnoticed.

**Recommendation:** Add a pre-commit hook or test that checks the registry version date
whenever the file changes.

### R-6. `copilot-instructions.md` rules are not enforceable at runtime (INFO)

The copilot instructions contain rules like "read X before Y" and "do not invent behavior"
which are behaviorally important but only exist as prose. The agent can ignore them.

**Recommendation:** Where possible, encode rules as programmatic checks (pre-commit, validate)
rather than relying solely on prose instructions. The existing validate/drift system is
excellent — extend it to cover more of the instruction file's rules.

---

## 7. Documentation Gaps

### DOC-1. `CHANGELOG.md` still shows only `[Unreleased]` and `[0.1.0]` (MEDIUM)

The project has progressed through 7+ stages with dozens of features, but the changelog has
never been updated past the initial release. The `[Unreleased]` section is a flat list that
doesn't reflect the actual progression.

**Recommendation:** Cut a release (even `0.2.0`) that captures the current state. Structure
the Unreleased section with more granular grouping.

### DOC-2. `CONTRIBUTING.md` says "Aim for 80%+ coverage on new code" but `fail_under = 90` (LOW)

The contributing guide's coverage target is lower than the actual enforced minimum. This gives
contributors a false impression of the bar.

**Recommendation:** Update to "Maintain 90%+ test coverage (enforced by CI)."

### DOC-3. MkDocs `nav` doesn't include `docs/decisions/` (LOW)

9 ADR decision records exist in `docs/decisions/` but they're not in `mkdocs.yml`'s `nav`.
They won't appear in the built documentation site.

**Recommendation:** Add a "Decisions" section to `mkdocs.yml` nav that lists the ADR index.

### DOC-4. No documentation for the dashboard API endpoints (LOW)

`docs/dashboard-api.md` exists but may be stale relative to the actual routes in
`programstart_serve.py`. There's no test that the documented endpoints match the implemented ones.

**Recommendation:** Add a test that extracts route patterns from `programstart_serve.py` and
asserts they match `docs/dashboard-api.md`.

### DOC-5. `SECURITY.md` says "email the maintainers" but gives no email address (LOW)

The vulnerability disclosure policy tells reporters to email, but doesn't say where to send it.

**Recommendation:** Add a contact email or use GitHub's security advisory feature instead.

### DOC-6. `QUICKSTART.md` references `pb.ps1` which is PowerShell-only (LOW)

The quick start guide uses `.\scripts\pb.ps1 next` as the first command, which doesn't work
on Linux/macOS. The portable alternative `uv run programstart next` is mentioned later but not
as the primary entry point.

**Recommendation:** Lead with `uv run programstart next` (cross-platform), mention `pb.ps1`
as a Windows convenience shortcut.

---

## 8. Sync & Drift Model Improvements

### S-1. Drift check is git-based but doesn't detect same-commit multi-file drift (MEDIUM)

If a developer changes README.md and knowledge-base.json in the same commit, drift check
sees both as changed and passes — even if the README change contradicts the KB change.
The check only verifies _pairing_, not _content alignment_.

**Recommendation:** This is a known design tradeoff. For high-value sync rules, consider
adding content-level checks (e.g., verify that README.md's KB description mentions the same
version string as `knowledge-base.json`).

### S-2. Drift check doesn't run on staged files by default (LOW)

`git_changed_files()` queries `git diff --name-only` and `git diff --cached --name-only`,
but the pre-commit `programstart-drift` hook uses `pass_filenames: true` which passes the
list of staged files. The interaction between these two modes isn't documented.

**Recommendation:** Document how drift check behaves in pre-commit context vs CLI context.
Add a `--staged-only` flag for explicit control.

### S-3. No sync rule covering `pyproject.toml` ↔ `requirements.txt` (LOW)

The pre-commit hook `sync-requirements-txt` regenerates `requirements.txt` when `pyproject.toml`
or `uv.lock` changes, but there's no drift-level sync rule for this pair. If someone manually
edits `requirements.txt`, nothing catches it.

**Recommendation:** Add a sync rule or a test that asserts `requirements.txt` matches the
output of the uv export command.

### S-4. `knowledge_base_docs_alignment` sync rule is too broad for README.md (LOW)

The README.md → knowledge-base sync rule triggers on _any_ README change, even date-only
updates. This forced a workaround today (bumping `knowledge-base.json` version to satisfy
the rule when only updating the README date).

**Recommendation:** Either narrow the sync rule to trigger only when specific README sections
change, or make the drift check smarter about metadata-only changes.

---

## 9. Prompt System Improvements

### P-1. No prompt versioning or deprecation mechanism (MEDIUM)

24 product prompts and 15 internal prompts exist. There's no version field in prompt
frontmatter and no mechanism to mark a prompt as deprecated. Old prompts accumulate silently.

**Recommendation:** Add an optional `version:` field to prompt frontmatter. Add a
`deprecated:` field. Add a test that flags deprecated prompts still referenced in the registry.

### P-2. `prompt-eval` only tests 6 scenarios (LOW)

`config/prompt-eval-scenarios.json` defines 6 evaluation scenarios. The recommendation engine
supports many more shapes and need combinations than this covers. Edge cases (e.g., regulated
API service, mobile app without auth, data pipeline with ML) are untested.

**Recommendation:** Expand to 12-15 scenarios covering regulated, multi-need, and uncommon
shape combinations.

### P-3. USERJOURNEY prompts don't have kill-criteria or challenge-gate sections (LOW)

PROGRAMBUILD shaping prompts enforce kill criteria and challenge gates. USERJOURNEY prompts
(`shape-uj-*`) skip this. A USERJOURNEY phase could advance without any adversarial review.

**Recommendation:** Add challenge-gate or assumption-challenge sections to USERJOURNEY shaping
prompts, adapted for onboarding/consent/activation concerns.

### P-4. No prompt for Stage 7 implementation beyond the internal build prompts (LOW)

The implementation loop (Stage 7) has no product-facing shaping prompt. `product-jit-check.prompt.md`
exists for JIT protocol checking, but there's no prompt that helps a user _plan_ an
implementation sprint, break work into commits, or structure a gameplan.

**Recommendation:** Consider a `shape-implementation.prompt.md` that helps structure
implementation sprints using the gameplan + architecture contracts.

### P-5. `argument-hint` field inconsistently populated across prompts (LOW)

Some prompts have `argument-hint:`, others don't. The PROMPT_STANDARD.md lists it as part
of the YAML frontmatter spec, but compliance tests don't enforce it.

**Recommendation:** Either enforce `argument-hint:` in all prompts or explicitly mark it
optional in the standard.

---

## 10. Schema & Validation Hardening

### SC-1. `process-registry.schema.json` has `additionalProperties: true` everywhere (MEDIUM)

The registry schema allows any extra fields on every object. This means typos in field names
go undetected — e.g., `require_autority_when_dependents_change` would silently be ignored
instead of failing validation.

**Recommendation:** Set `additionalProperties: false` on critical objects (sync_rules items,
system definitions, metadata_rules). Use a known "extensions" object for intentional
extensibility.

### SC-2. State schema doesn't validate stage/phase names against the registry (LOW)

`programbuild-state.schema.json` and `userjourney-state.schema.json` use `additionalProperties`
for stage/phase entries. A state file could contain a misspelled stage name
(`inputs_and_mode_selecion`) and pass schema validation.

**Recommendation:** Add an `enum` of valid stage/phase names, or add a programmatic
validator that checks state keys against `stage_order` / `phase_order` in the registry.

### SC-3. No schema for `knowledge-base.json` (LOW)

`config/knowledge-base.json` is validated by Pydantic models at runtime but has no JSON Schema
file for pre-commit or CI static validation. It's the largest JSON file in the repo (~2000 lines)
and a structural error would only be caught by running Python.

**Recommendation:** Generate a JSON Schema from the Pydantic models (Pydantic v2 supports
`model.model_json_schema()`) and add a pre-commit hook for it.

### SC-4. No schema for `prompt-eval-scenarios.json` (LOW)

The prompt evaluation scenario file has no schema. A typo in a scenario field name would
cause a silent test failure rather than a clear validation error.

**Recommendation:** Add a JSON Schema and a pre-commit hook.

---

## 11. Guardrails & Safety Nets

### G-1. `programstart advance` has preflight checks but no post-advance verification (MEDIUM)

Stage advancement runs preflight validation, but nothing runs _after_ the state file is
written. If the advance succeeds but leaves the repo in a weird state (e.g., active stage
doesn't match the expected progression), nothing catches it until the next manual check.

**Recommendation:** Add a post-advance sanity check: reload state, verify active step
matches expected, run `programstart validate --check workflow-state`.

### G-2. No guard against advancing PROGRAMBUILD while USERJOURNEY is blocked (LOW)

PROGRAMBUILD and USERJOURNEY track independently. It's possible to advance PROGRAMBUILD to
release readiness while USERJOURNEY has blocked phases. Nothing warns about this.

**Recommendation:** Add a cross-system health check in `programstart next` that warns if
one system is significantly ahead of the other.

### G-3. No git hook for branch protection (LOW)

The pre-commit hooks run on commit, but there's no branch protection enforced locally. A
developer could commit directly to `main` and push without going through the full CI gate.

**Recommendation:** Document the recommended GitHub branch protection rules in
`CONTRIBUTING.md` or `SECURITY.md`. Consider a local push hook that warns about direct
main pushes.

### G-4. `READONLY_MODE` in the dashboard isn't tested (LOW)

`programstart_serve.py` checks `PROGRAMSTART_READONLY` env var but there are no tests
verifying that mutation endpoints actually return 403/405 in read-only mode.

**Recommendation:** Add tests that set `PROGRAMSTART_READONLY=1` and verify POST endpoints
are blocked.

---

## 12. Workflow Model Weaknesses

### W-1. Stage gates are structurally validated but not content-quality validated (MEDIUM)

Stage gate checks verify that files exist and have the right metadata/sections, but don't
assess content quality. A FEASIBILITY.md with "TBD" in every field passes the gate.

**Recommendation:** Add heuristic content checks: minimum word count per section, absence of
placeholder text ("TBD", "TODO", "[FILL IN]"), non-empty decision register entries.

### W-2. No concept of stage "expiry" or staleness for completed stages (LOW)

Once a stage is completed, its output docs are never re-validated. ARCHITECTURE.md written
3 months ago might be stale relative to current implementation, but nothing flags this.

**Recommendation:** Add optional freshness tracking to stage completions. If the state file
records a completion date, a staleness check could warn after N days.

### W-3. USERJOURNEY phases have no entry criteria (unlike PROGRAMBUILD) (LOW)

PROGRAMBUILD's `implementation_loop` has explicit `entry_criteria`. No USERJOURNEY phase has
any. Phases can be advanced without verifying downstream readiness.

**Recommendation:** Define entry criteria for at least the critical USERJOURNEY phases
(implementation, delivery, activation).

### W-4. `workflow_guidance` only maps stages to files/prompts — not to expected outputs (LOW)

The registry's `workflow_guidance` section lists files and prompts per stage, but doesn't
explicitly state what each stage must _produce_. The `stage_order` has `main_output` but
workflow guidance doesn't reference it.

**Recommendation:** Add an `expected_outputs` field to each stage's guidance block, cross-
referencing `stage_order[].main_output`.

---

## 13. Dependency & Supply Chain

### DEP-1. `dependabot.yml` missing `github-actions` ecosystem (MEDIUM)

Workflow files pin actions by SHA (excellent practice), but Dependabot won't
automatically open PRs for new action versions.

**Recommendation:** Add:
```yaml
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### DEP-2. `pip-audit` succeeds with exit code 1 in CI (LOW)

`process-guardrails.yml` runs `pip-audit --desc` in a PowerShell block that catches exit
code 1 and continues. This means known vulnerabilities don't fail the build.

**Recommendation:** Make pip-audit a blocking check. If advisory-only vulns need to be
tolerated, use `--ignore-vuln` for specific CVEs rather than blanket-allowing exit 1.

### DEP-3. No `uv.lock` integrity check in CI (LOW)

CI runs `uv sync --extra dev` which uses the lockfile, but doesn't verify the lockfile is
up-to-date with `pyproject.toml`. A stale lockfile could install different versions than
specified.

**Recommendation:** Add `uv lock --check` as a CI step.

---

## 14. Dashboard & Web UI

### UI-1. Dashboard serves inline HTML from Python string literals (MEDIUM)

`programstart_serve.py` has HTML/CSS/JS embedded in Python docstrings and string literals
(the file is 2600+ lines). This makes frontend changes extremely difficult and prevents
any frontend tooling (linting, formatting, minification).

**Recommendation:** Extract HTML/CSS/JS to static files under a `dashboard/` directory.
Serve them via the existing HTTP server. This is a significant refactor but would dramatically
improve maintainability.

### UI-2. No Content-Security-Policy header on dashboard responses (LOW)

The dashboard serves HTML without CSP headers. While it's localhost-only, adding CSP is a
defense-in-depth measure against accidental XSS from rendered API outputs.

**Recommendation:** Add `Content-Security-Policy: default-src 'self'; script-src 'self'`
to HTML responses.

### UI-3. Dashboard golden screenshots only run on Linux (LOW)

Golden screenshot comparison is skipped on Windows with a log message. This means visual
regressions on Windows are never caught.

**Recommendation:** Maintain separate golden baselines per OS, or at least document why
this is acceptable.

---

## 15. Knowledge Base & Retrieval

### KB-1. Context index `INDEX_VERSION` is hardcoded to `"2026-03-28"` (MEDIUM)

`programstart_context.py` line 42 has a stale version string. The index has changed many
times since March 28. A stale version means the cache compatibility check
(`cached_index_is_compatible`) might serve outdated data.

**Recommendation:** Either auto-derive the version from a hash of the index structure, or
bump it whenever the context builder changes.

### KB-2. BM25 retrieval has no relevance threshold (LOW)

`programstart_retrieval.py` returns the top-K results regardless of score. A query with no
good matches still returns K results with low scores, potentially misleading the user.

**Recommendation:** Add a minimum score threshold. Return fewer results when nothing is
relevant.

### KB-3. No way to extend the knowledge base without editing `knowledge-base.json` directly (LOW)

The KB is a single large JSON file. Adding a new stack or pattern requires editing this file
and understanding its structure. There's no `programstart kb add-stack` command.

**Recommendation:** Consider a `programstart kb` subcommand for structured KB additions,
or at minimum a JSON Schema that guides manual edits.

---

## 16. Bootstrap & Factory

### B-1. Bootstrap output stub extraction is fragile (LOW)

`_extract_file_header()` in `programstart_bootstrap.py` extracts content up to the first `---`
separator. If a template file uses `---` for a different purpose (e.g., YAML frontmatter
in a non-header position), the extraction could be wrong.

**Recommendation:** Use a more robust header parsing strategy — e.g., look for the metadata
block pattern (`Purpose:`, `Owner:`, etc.) rather than relying on `---` alone.

### B-2. `programstart create` wraps a lot (1040+ LoC single file) (LOW)

The one-shot factory (`programstart_create.py`) handles recommendation, scaffolding, git init,
GitHub API calls, service provisioning, and VS Code launch in a single 1040-line file. This
makes it the hardest file to test and maintain.

**Recommendation:** Split into focused modules: `create_orchestrator.py`, `github_api.py`,
`service_provisioning.py`. The current file does too much.

---

## 17. Developer Experience

### DX-1. 39 `.py` files in `scripts/` with no namespace organization (MEDIUM)

All scripts are flat in `scripts/`. As the count grows, discoverability suffers.
Related scripts could be grouped: `scripts/cli/`, `scripts/dashboard/`, `scripts/smoke/`.

**Recommendation:** For now, this works. But if the script count grows past 50, split into
subpackages. The import fallback boilerplate (D-3) would need updating.

### DX-2. `pb.ps1` is undocumented (LOW)

`scripts/pb.ps1` is a PowerShell wrapper but is not listed in the CLI reference or docs.
Its behavior relative to `uv run programstart` is not documented.

**Recommendation:** Add a brief section in QUICKSTART.md explaining `pb.ps1` equivalence.

### DX-3. VS Code tasks are numerous but not categorized in the task picker (LOW)

22 tasks are defined in `.vscode/tasks.json`. The task picker shows them as a flat list.
VS Code tasks support `group` and `presentation` properties for organization.

**Recommendation:** Group tasks by function (validate, smoke, build, advance) using
`presentation.group` for visual grouping in the picker.

### DX-4. No `.editorconfig` rule for JSON indentation consistency (LOW)

`.editorconfig` likely exists (listed in bootstrap_assets) but JSON files in the repo use
2-space indentation (some) and mixed (others). No enforced standard.

**Recommendation:** Add `[*.json]` section to `.editorconfig` with `indent_size = 2`.

---

## 18. Structural Debt

### SD-1. `process-registry.json` is 900+ lines and growing (MEDIUM)

The registry is the single most important configuration file and it's nearing the point where
manual editing is error-prone. It contains workflow definitions, sync rules, metadata rules,
integrity configuration, and workflow guidance — all in one file.

**Recommendation:** Consider splitting into multiple JSON files (`sync-rules.json`,
`workflow-guidance.json`, etc.) loaded by the registry loader. Not urgent but prevents future
brittleness.

### SD-2. No explicit versioning contract between `process-registry.json` and scripts (LOW)

Scripts read the registry and assume specific key names exist. If a registry field is renamed,
all scripts break simultaneously with unhelpful `KeyError` messages. The schema doesn't
enforce required fields at the depth scripts actually need.

**Recommendation:** Use Pydantic models for the registry (like `programstart_models.py` does
for the knowledge base). This would give typed access and clear error messages.

### SD-3. `devlog/` directory is exempted from all rules but not gitignored (LOW)

The source-of-truth instruction file exempts `devlog/` from authority checks. This is correct
for its purpose (historical build artifacts), but it means these files will accumulate
indefinitely with no maintenance or pruning schedule.

**Recommendation:** Document the retention policy. Consider a `programstart clean --devlog`
flag that archives old gameplans.

### SD-4. `BACKUPS/` contains a single snapshot from 2026-03-27 (LOW)

The backup directory has one snapshot from initial setup. There's no automated backup
mechanism and no documented schedule for when backups should be taken.

**Recommendation:** Either automate pre-advance backups or document that backups are the
user's responsibility.

---

## Summary Statistics

| Category | Critical | High | Medium | Low | Info |
|---|---|---|---|---|---|
| Code Hardening | 0 | 0 | 1 | 3 | 0 |
| DRY Violations | 0 | 2 | 1 | 0 | 0 |
| Test & Coverage | 0 | 0 | 3 | 4 | 0 |
| Automation & CI | 0 | 0 | 3 | 3 | 0 |
| CLI & Features | 0 | 0 | 2 | 4 | 0 |
| Rule Enforcement | 0 | 0 | 2 | 3 | 1 |
| Documentation | 0 | 0 | 1 | 5 | 0 |
| Sync & Drift | 0 | 0 | 1 | 3 | 0 |
| Prompt System | 0 | 0 | 1 | 4 | 0 |
| Schema & Validation | 0 | 0 | 1 | 3 | 0 |
| Guardrails | 0 | 0 | 1 | 3 | 0 |
| Workflow Model | 0 | 0 | 1 | 3 | 0 |
| Dependencies | 0 | 0 | 1 | 2 | 0 |
| Dashboard & UI | 0 | 0 | 1 | 2 | 0 |
| Knowledge Base | 0 | 0 | 1 | 2 | 0 |
| Bootstrap & Factory | 0 | 0 | 0 | 2 | 0 |
| Developer Experience | 0 | 0 | 1 | 3 | 0 |
| Structural Debt | 0 | 0 | 1 | 3 | 0 |
| **Total** | **0** | **2** | **23** | **52** | **1** |

**Overall assessment:** No critical issues. The system is remarkably well-structured for a solo-
operated project — particularly the authority model, drift detection, and test coverage. The
two HIGH items (D-1 and D-2) are pure DRY violations that are easy to fix and would reduce
maintenance friction immediately. The MEDIUM items cluster around three themes: (1) test coverage
for the most complex modules, (2) CI and automation completeness, and (3) schema strictness.
The LOW items are polish and defense-in-depth — none are urgent but each represents a small
improvement in robustness or developer experience.

---
---

# Part 2 — Strategic Analysis: Standardization, UI, Prompt Builder, Cross-Repo Potential

Date: 2026-04-14
Scope: Deep dive into PROGRAMSTART's standardization model, dashboard necessity analysis,
prompt system portability, and prompt-builder feasibility for external repos.

---

## Table of Contents (Part 2)

19. [How Program Building Is Standardized](#19-how-program-building-is-standardized)
20. [Centralization Model — What Lives Where](#20-centralization-model--what-lives-where)
21. [Dashboard UI — Is It Necessary?](#21-dashboard-ui--is-it-necessary)
22. [Prompt Builder Feasibility](#22-prompt-builder-feasibility)
23. [Cross-Repo Portability Analysis](#23-cross-repo-portability-analysis)
24. [Additional Factors To Consider](#24-additional-factors-to-consider)
25. [Strategic Recommendations](#25-strategic-recommendations)

---

## 19. How Program Building Is Standardized

PROGRAMSTART codifies program building through eight interlocking standardization layers.
Understanding what each layer does — and what it doesn't — reveals where the system is strong,
where it's brittle, and where it could be extended.

### Layer 1: Registry-Driven Configuration

Everything flows from `config/process-registry.json` (~900 lines):
- **Stage order** (11 PROGRAMBUILD stages, each with `main_output`)
- **Phase order** (USERJOURNEY phases, attachment-optional)
- **Sync rules** (16 authority→dependent file pairs)
- **Metadata rules** (required YAML prefixes for all planning docs)
- **Workflow guidance** (per-stage file lists, scripts, prompts)
- **Bootstrap assets** (155+ files to copy when scaffolding a new repo)
- **Command whitelist** (what the dashboard is allowed to execute)

**What this standardizes:** File naming, stage progression, authority ownership, validation
targets, and command surface. A generated repo inherits the same stage/phase structure,
sync rules, and validation expectations as PROGRAMSTART itself.

**What it doesn't standardize:** Content quality within files, implementation architecture
decisions, or how teams actually use the generated structure.

### Layer 2: Knowledge Base Decision Evidence

`config/knowledge-base.json` (~2000 lines) captures curated domain knowledge:
- 150+ technology stacks with strengths, tradeoffs, best-for, avoid-when, pairs-with
- Provisioning services (Supabase, Vercel, Neon, etc.)
- Third-party APIs (OpenAI, Anthropic, etc.)
- Decision rules (if shape=X and need=Y, prefer stack Z)
- Coverage domains (what architectural concerns each stack addresses)
- Research ledger (staleness tracking per entry)

**What this standardizes:** Stack selection is evidence-based, not opinion-based. Every
recommendation includes scores, matched rules, and reasons. Two operators given the same
inputs will get the same recommendation.

**What it doesn't standardize:** The KB is PROGRAMSTART-specific. Generated repos don't get
their own KB — they inherit the recommendation output as a one-time kickoff packet.

### Layer 3: Recommendation Engine

`programstart_recommend.py` (~900 lines) applies a deterministic scoring algorithm:
- Text normalization → capability expansion → shape profiling → scoring → deduplication
- Score composition: shape match (+5), need match (+2-6), decision rule preference (+4),
  comparison bonus (+2), relationship bonus (+1)
- Confidence levels derived from score distribution
- Coverage warnings surfaced when architectural domains are underrepresented

**What this standardizes:** The recommendation is reproducible and auditable. Changing the
KB changes recommendations predictably. The scoring model prevents "vibes-based" stack choice.

**What it doesn't standardize:** The algorithm is opaque to the end user — they see results,
not the scoring internals. No way to override or weight preferences without editing the KB.

### Layer 4: Authority-Before-Dependent Workflow

The sync rules enforce a strict update ordering:
- REQUIREMENTS.md is authority for USER_FLOWS.md, ARCHITECTURE.md, TEST_STRATEGY.md
- ARCHITECTURE.md is authority for DECISION_LOG.md (architecture decisions)
- PROGRAMBUILD_CANONICAL.md is authority for variant files
- Changes to a dependent without changing its authority file = drift violation

**What this standardizes:** Information flows in one direction. Contradictions between docs
are caught by the drift checker. The authority model prevents the classic planning failure
mode where downstream docs evolve independently of the source-of-truth.

**What it doesn't standardize:** Content accuracy within authority files themselves. An
authority doc can contain errors; nothing above it checks for correctness except human review.

### Layer 5: JIT Source-of-Truth Protocol

Prompts enforce a load-before-act discipline:
1. Run `programstart drift` to establish clean baseline
2. Read authority files listed in workflow guidance (not from memory)
3. Update authority files first, dependents second
4. Run `programstart validate` + `drift` after changes

**What this standardizes:** Prevents stale-context errors where an agent (human or AI) acts
on remembered information that no longer matches the authority docs. Forces re-reading.

**What it doesn't standardize:** An operator can skip the protocol with no enforcement beyond
the pre-commit drift hook. The discipline is prompt-encoded, not system-enforced.

### Layer 6: Bootstrap Scaffolding

`programstart_bootstrap.py` stamps out a new repo with:
- All PROGRAMBUILD control files + output stubs (headers only, no template content)
- Selected variant (lite/product/enterprise)
- Registry mutated to `repo_role: "project_repo"` + `provisioning_scope: "project_repo_only"`
- Complete `.github/` directory (copilot-instructions, agents, instructions, prompts)
- Secrets baseline regenerated per-project

**What this standardizes:** Every generated repo starts with the same structure, the same
agent definitions, the same prompt library, and the same validation infrastructure.

**What it doesn't standardize:** Post-bootstrap evolution. Once a repo is created, it's
independent. There's no mechanism for PROGRAMSTART to push updates to generated repos.

### Layer 7: Multi-Variant Gate Model

Three variants scale rigor to project profile:
- **Lite:** Minimal stages, fewer required outputs, faster progression
- **Product:** Full 11-stage pipeline with all gates
- **Enterprise:** Product + additional compliance/audit requirements

**What this standardizes:** Appropriate ceremony for the project's risk profile. A weekend
CLI tool doesn't need the same rigor as a regulated API service.

**What it doesn't standardize:** Which variant to choose. The recommendation engine suggests
one, but the operator can override.

### Layer 8: AI Agent Specialization

Three agents operationalize domain expertise:
- **Discovery & Scoping** — turns ideas into scoped briefs
- **Architecture & Security** — reviews design, contracts, threat model
- **Quality & Release** — assesses test strategy, CI gates, launch readiness

**What this standardizes:** Domain review happens through structured, constrained agents
rather than freehand chat. Agents have explicit constraints (no production code, no overriding
canonical docs) and structured output formats.

**What it doesn't standardize:** Agent behavior is ultimately advisory. Nothing prevents an
operator from ignoring agent findings.

---

## 20. Centralization Model — What Lives Where

| Concern | Where It Lives | Consumed By |
|---|---|---|
| Stage/phase definitions | `process-registry.json` | CLI, dashboard, validate, guide, bootstrap |
| Authority file ownership | `process-registry.json` `sync_rules` | drift check, prompts, validate |
| Technology knowledge | `knowledge-base.json` | recommend, create, prompt-eval, retrieval |
| Prompt discipline | `PROMPT_STANDARD.md` | all `.prompt.md` files, compliance tests |
| Agent behavior constraints | `.github/agents/*.agent.md` | VS Code / Copilot agent mode |
| Workflow state | `PROGRAMBUILD_STATE.json` / `USERJOURNEY_STATE.json` | CLI, dashboard, advance, validate |
| Metadata format | `process-registry.json` `metadata_rules` | validate, parsers |
| Command surface | `process-registry.json` `dashboard_allowed_commands` | dashboard server |
| Bootstrap file list | `process-registry.json` `bootstrap_assets` | bootstrap, validate |
| CI quality gates | `.github/workflows/` + `noxfile.py` | GitHub Actions, local nox |

**Key insight:** `process-registry.json` is the gravitational center. 80% of PROGRAMSTART's
behavior is derived from this one file. This is both a strength (single point of change) and
a risk (single point of failure — see SD-1 in Part 1).

---

## 21. Dashboard UI — Is It Necessary?

### What the Dashboard Actually Does

`programstart_serve.py` is a 2700-line self-contained HTTP server (localhost:7771):
- **67% is inline HTML/CSS/JS** (~1800 lines) — dark-mode Catppuccin design system
- **33% is Python logic** (~900 lines) — state loading, command execution, validation

**API endpoints:**
| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serve full HTML dashboard |
| `/api/state` | GET | Workflow state + catalog metadata as JSON |
| `/api/run` | POST | Execute whitelisted CLI commands |
| `/api/workflow-advance` | POST | Advance stage/phase + record signoff |
| `/api/workflow-signoff` | POST | Save signoff metadata without advancing |
| `/api/uj-phase` | POST | Update USERJOURNEY phase status |
| `/api/uj-slice` | POST | Update USERJOURNEY slice status |
| `/api/doc` | GET | File preview (max 220 lines, max 64 KB) |

**User actions enabled:**
- View active stage/phase with progress percentage
- Advance to next stage with pre-flight checks + signoff modal
- Record hold/blocked/approved decisions with notes
- Tab-based navigation (References → Setup → Execution → Diagnostics)
- Open files in VS Code via `vscode://` deep links
- Preview file content in side panel
- Run validation/drift checks from UI
- Bootstrap new projects with form validation
- Copy subagent prompts to clipboard

### Could CLI Replace It?

**Yes, with significant friction:**

| Function | CLI Alternative | Friction Cost |
|---|---|---|
| State overview | `programstart status --json` | Must parse JSON mentally |
| Stage advance | `programstart advance --system X` | No pre-flight modal, no signoff form |
| Dual-system view | Run two terminal commands | Can't see both simultaneously |
| File preview | Open in editor | Context-switch away from workflow |
| Drift check | `programstart drift` | Output is text wall, not categorized |
| Copy prompts | Manual selection + copy | 3-4 extra steps per prompt |
| Bootstrap | `programstart bootstrap` | No form validation UI, easy to typo paths |

**Estimated operator friction without UI: +30-40% time per session.**

### Assessment

The dashboard is **genuinely valuable but architecturally expensive**. The 1800 lines of inline
HTML/CSS/JS create a maintenance burden that's disproportionate to the functionality. The core
value propositions are:

1. **Parallel state awareness** — seeing both systems simultaneously
2. **Pre-flight modals** — catching mistakes before state-changing operations
3. **Reduced context-switching** — staying in one surface while navigating workflow

These could be delivered via:
- **Option A (current):** Monolithic inline HTML server — works but unmaintainable
- **Option B:** Extracted static files (`dashboard/`) served by the same server — still Python-owned but allows frontend tooling
- **Option C:** VS Code webview extension — integrates natively and eliminates duplicate server
- **Option D:** Enhanced CLI with `--interactive` TUI (textual/rich) — terminal-native, no browser dependency

**Verdict:** The UI is necessary for 8+ hour planning sessions. The delivery mechanism
(inline HTML in a Python string) is not. Options B or D would preserve the value while
reducing maintenance cost. Option C would be the most integrated but requires VS Code
extension development expertise.

---

## 22. Prompt Builder Feasibility

### What Is a Prompt Builder?

A tool that generates repo-specific `.prompt.md` files from a template, parameterized by:
- The repo's stage definitions
- The repo's authority file paths
- The repo's sync rules
- The repo's validation commands

Instead of handwriting 23 prompt files per repo, the builder would generate them from
PROMPT_STANDARD.md + the repo's process-registry.json.

### Current State: Why This Is Feasible

PROGRAMSTART already has the ingredients:

1. **`PROMPT_STANDARD.md`** defines 11 mandatory sections + 3 optional sections. This is
   already a template — it just isn't parameterized.

2. **`process-registry.json`** `workflow_guidance` maps each stage to:
   - `step_files` (authority docs to read)
   - `scripts` (CLI commands to run)
   - `prompts` (prompt file name)
   This is the parameter source.

3. **`sync_rules`** define authority→dependent ordering. The "Output Ordering" section of
   every prompt derives directly from the matching sync rule. This is already computable.

4. **`propagate-canonical-change.prompt.md`** is nearly a parameterized template already —
   it just needs the authority file name and dependent list injected.

5. **`programstart_prompt_eval.py`** already validates generated prompt content against
   expected terms and sections. This is the test harness for a prompt builder.

### What the Builder Would Need

```
Input:
  - process-registry.json (stage order, sync rules, workflow guidance)
  - Optional: knowledge-base.json (for shape-conditioning sections)
  - Target stage name

Output:
  - Complete .prompt.md file conforming to PROMPT_STANDARD.md
```

**Section-by-section generation:**

| Section | Source | Parameterizable? |
|---|---|---|
| YAML frontmatter | Stage name + description | YES — derive from `stage_order` |
| Data Grounding Rule | Static boilerplate | YES — copy verbatim |
| Protocol Declaration | Static per variant | YES — template with variant |
| Pre-flight | Static | YES — copy verbatim |
| Authority Loading | `workflow_guidance[stage].step_files` | YES — list from registry |
| Upstream Verification | Previous stage's `main_output` | YES — derive from `stage_order` |
| Protocol Steps | Stage-specific procedure | PARTIAL — structure templatable, detail is stage-specific |
| Output Ordering | `sync_rules` matching stage files | YES — computable from sync rules |
| DECISION_LOG Mandate | Static | YES — copy verbatim |
| Verification Gate | Static | YES — copy verbatim |
| Workflow Routing | Static | YES — copy verbatim |
| O1: Shape Conditioning | Knowledge base shapes | YES — if KB attached |
| O2: Kill Criteria | Static with stage reference | YES — template |
| O3: Entry Criteria | `entry_criteria` from registry | YES — derive from registry |

**Result: 9 of 11 mandatory sections are fully auto-generatable.** Section 7 (Protocol Steps)
requires human-authored procedure text, but even this could have a structured skeleton
generated from the stage's `main_output` and expected deliverables.

### Prompt Builder Architecture

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

### Cross-Repo Prompt Builder

For **other repos** (not PROGRAMSTART), the builder would need:

1. **The target repo has a `process-registry.json`** (or equivalent config) with:
   - `stage_order` or `phase_order` defining workflow steps
   - `sync_rules` defining file dependencies
   - `workflow_guidance` mapping stages to files

2. **The target repo has authority markdown files** at the paths listed in the registry

3. **The target repo has CLI validation tools** (or the builder generates stubs for them)

**Two operating modes:**

- **Mode A: PROGRAMSTART-bootstrapped repos** — these already have the registry, sync rules,
  and prompt library. The builder regenerates prompts from the inherited registry. Useful
  when the registry evolves (new stages, renamed files).

- **Mode B: Arbitrary repos** — the builder requires a minimal config file defining stages
  and authority files. It generates first-pass prompts that the operator then customizes.
  This is the more ambitious case.

### Effort Estimate

- **Mode A (regenerate for bootstrapped repos):** ~300-400 LoC. Most logic is registry parsing +
  template rendering. Tests can reuse `programstart_prompt_eval.py` patterns.

- **Mode B (arbitrary repos):** ~600-800 LoC. Needs a simplified registry schema, a config
  wizard (`programstart prompt-build --init`), and fallback templates for repos without
  full registry infrastructure.

### Risks

- **Over-abstraction:** Generating prompts from templates could produce generic, hollow prompts
  that miss stage-specific nuance. Section 7 (Protocol Steps) is where domain expertise lives —
  a template can't capture "how to do a feasibility study" from a config file alone.

- **Maintenance inversion:** If the builder generates prompts, but operators then hand-edit
  the generated files, regeneration would overwrite their customizations. Need a strategy
  for "ejected" (manually customized) vs "managed" (auto-generated) prompts.

- **Registry schema coupling:** The builder assumes a specific registry structure. If the
  registry schema evolves, the builder must evolve in lockstep.

---

## 23. Cross-Repo Portability Analysis

### What PROGRAMSTART Exports Today

When `programstart bootstrap` runs, the target repo receives:

| Category | Files Copied | Post-Bootstrap Independence |
|---|---|---|
| Agent definitions | 3 `.agent.md` files | Fully independent — can be edited per-repo |
| Instruction files | 4 `.instructions.md` files | Fully independent |
| Prompts | 23 `.prompt.md` + 15 internal | Fully independent — but stale if PROGRAMSTART evolves |
| Copilot instructions | `copilot-instructions.md` | Independent |
| Registry | `process-registry.json` (mutated) | Independent — `repo_role: "project_repo"` |
| Schemas | 3 JSON schemas | Independent |
| CI workflows | 6 workflow files | Independent |
| PROGRAMBUILD docs | All control + output stubs | Independent |
| USERJOURNEY docs | If attached | Independent |

**Key gap: No update channel.** Once a repo is bootstrapped, it never receives updates from
PROGRAMSTART. If a prompt is improved, a sync rule is added, or an agent is refined, the
generated repo doesn't benefit.

### Component Portability Scores

| Component | LOC | Portability | Notes |
|---|---|---|---|
| `PROMPT_STANDARD.md` | ~180 | **99%** | Pure format spec; works for any registry-based repo |
| Agent definitions | ~50-80 each | **80%** | Constraints and approach are generic; file refs need updating |
| `propagate-canonical-change.prompt.md` | ~80 | **85%** | Only needs sync_rules schema to match |
| `shape-requirements.prompt.md` | ~120 | **75%** | Process is generic; file paths are hardcoded |
| `shape-architecture.prompt.md` | ~120 | **75%** | Architecture review protocol is universal |
| `programstart_prompt_eval.py` | ~450 | **40%** | Framework is generic; scenarios are PROGRAMSTART-specific |
| `programstart_recommend.py` | ~900 | **80%** | Scoring algorithm is generic; KB is specific |
| `programstart_bootstrap.py` | ~350 | **85%** | Template scaffolding pattern is generic |
| `programstart_serve.py` | ~2700 | **30%** | Registry-specific command whitelist, state structure |
| `process-registry.json` | ~900 | **70%** | Schema is generic; content is PROGRAMSTART-specific |

### What Would Make It More Portable

1. **Registry schema as a standalone spec** — define the minimum registry schema that any
   repo must implement to use PROGRAMSTART's prompt/validation/drift toolchain.

2. **Prompt template engine** (see §22) — generate prompts from registry instead of
   handwriting them per-repo.

3. **Update channel** — a `programstart sync --from-template` command that pulls updated
   prompts/agents/instructions from PROGRAMSTART into a generated repo, merging carefully.

4. **Lighter bootstrap variant** — "prompt-only" mode that copies only `.github/` without
   PROGRAMBUILD/USERJOURNEY structure. For repos that want the prompt discipline without
   the full workflow system.

---

## 24. Additional Factors To Consider

### 24.1 Prompt Drift Across Generated Repos

Once 5-10 repos are bootstrapped, each will have its own copy of the prompt library. Some
will customize prompts; others won't. There's no mechanism to:
- Know which repos are running which prompt versions
- Push improvements to all repos at once
- Detect when a repo's prompts have diverged from the template

**Consideration:** This is the "WordPress plugin update" problem. Solutions range from
"accept divergence" (current) to "centralized prompt registry with version pinning" (complex).

### 24.2 Knowledge Base Scope

The KB is comprehensive for the PROGRAMSTART template repo but doesn't help generated repos
with their own domain knowledge. A receipt-processing app (RECEIPTReader) has different
domain knowledge needs than a SaaS dashboard.

**Consideration:** Should generated repos have a mechanism for building their own project-
specific knowledge bases? Or is the KB purely a kickoff-time resource?

### 24.3 Operator Skill Assumptions

The system assumes an operator who:
- Understands git, pre-commit, and CI workflows
- Can read and interpret JSON config files
- Knows how to invoke UV, nox, pytest
- Can evaluate AI agent output critically

**Consideration:** Lower the barrier with `programstart doctor` (see F-2) and more guardrails
for common mistakes. The dashboard helps, but doesn't fully address the learning curve.

### 24.4 Multi-Repo Orchestration

Currently, PROGRAMSTART operates on one repo at a time. If a product has multiple repos
(frontend, backend, infra), there's no mechanism to:
- Track cross-repo stage progression
- Enforce cross-repo sync rules
- Generate coordinated architecture docs across repos

**Consideration:** This is a separate concern from PROGRAMSTART's current scope, but it's
a natural evolution for teams building multi-repo products.

### 24.5 Prompt Testing Beyond Structural Compliance

`test_prompt_compliance.py` checks that prompts have the right sections and frontmatter.
It doesn't test whether a prompt actually produces good output when used. The `prompt-eval`
system tests recommendations, not the prompts themselves.

**Consideration:** True prompt quality testing requires LLM-in-the-loop evaluation — running
each prompt against a model and scoring the output. This is expensive but would catch prompts
that are structurally compliant but practically ineffective.

### 24.6 Versioned Prompt Releases

If PROGRAMSTART ships a prompt builder or serves as a prompt registry for generated repos,
prompts need semantic versioning:
- **Major:** Breaking change (section removed or renamed)
- **Minor:** New optional section or enhanced guidance
- **Patch:** Wording fix, typo correction

**Consideration:** The `PROMPT_STANDARD.md` has no version field. Adding one is prerequisite
for any update channel.

### 24.7 Config vs Code Balance

PROGRAMSTART leans heavily on JSON config (`process-registry.json`, `knowledge-base.json`,
`prompt-eval-scenarios.json`). This is good for declarative authority but creates a secondary
programming language that's harder to debug than Python:
- No IDE autocomplete for registry keys
- No type checking on JSON values
- No stack traces when a registry key is misspelled

**Consideration:** Pydantic models for the registry (see SD-2) would provide typed access,
validation, and IDE support. The investment pays off as registry complexity grows.

### 24.8 Dashboard vs VS Code Extension

The dashboard is a standalone HTTP server that duplicates some VS Code functionality (file
preview, command execution, terminal output). A VS Code webview extension would:
- Eliminate the separate server process
- Integrate with VS Code's existing file preview, terminal, and git support
- Access workspace APIs directly (no HTTP round-trip)
- Ship as a VSIX with the bootstrapped repo

**Consideration:** This is a significant development effort but would be the most natural
integration point. The current tasks.json already demonstrates deep VS Code integration.

### 24.9 Starter Scaffold Completeness

`programstart_starter_scaffold.py` generates first-pass project files dynamically from the
recommendation. But the generated files are thin starters — they don't include:
- Pre-configured CI workflows for the recommended stack
- Stack-specific testing setup (e.g., Playwright config for web apps)
- Environment-specific deployment manifests

**Consideration:** Starter scaffolds could be enriched with stack-specific templates. The
risk is maintenance burden — each new stack needs its own starter template.

### 24.10 Feedback Loop

There's no mechanism for a generated repo to report back to PROGRAMSTART:
- "This recommendation worked well / didn't work"
- "We diverged from the recommended stack at stage 4 because..."
- "The feasibility prompt missed risk X"

**Consideration:** Even a simple `programstart feedback --from <repo>` that collects a
structured retrospective would improve the KB and prompt library over time.

---

## 25. Strategic Recommendations

### Tier 1: High-Value, Low-Effort (do first)

| # | Recommendation | Effort | Impact |
|---|---|---|---|
| S-1 | **Build the prompt builder** (Mode A — regenerate for bootstrapped repos) | ~300 LoC | Eliminates hand-maintaining 23 prompt files per generated repo |
| S-2 | **Add `version:` field to prompt frontmatter** + PROMPT_STANDARD.md | ~50 LoC | Prerequisite for S-1 and any future update channel |
| S-3 | **Extract dashboard HTML/CSS/JS to static files** (Option B from §21) | ~200 LoC refactor | Unblocks frontend tooling + reduces serve.py from 2700 to ~900 lines |
| S-4 | **Add `--json` output to core CLI commands** (status, guide, drift) | ~100 LoC | Enables scripting, piping, and dashboard API simplification |

### Tier 2: High-Value, Medium-Effort (plan next)

| # | Recommendation | Effort | Impact |
|---|---|---|---|
| S-5 | **Prompt builder Mode B** (arbitrary repos with minimal config) | ~500 LoC | Opens PROGRAMSTART's prompt discipline to non-bootstrapped repos |
| S-6 | **Registry Pydantic models** (typed access, validation, IDE support) | ~400 LoC | Eliminates KeyError fragility, enables IDE autocomplete |
| S-7 | **Prompt update channel** (`programstart sync --from-template`) | ~300 LoC | Solves prompt drift across generated repos |
| S-8 | **"Prompt-only" bootstrap mode** (just `.github/`, no PROGRAMBUILD) | ~150 LoC | Lighter adoption path for repos that want prompt discipline without full gates |

### Tier 3: Strategic (evaluate when Tier 1-2 are done)

| # | Recommendation | Effort | Impact |
|---|---|---|---|
| S-9 | **VS Code webview extension** (replace HTTP dashboard) | ~2000 LoC | Most integrated UX, eliminates standalone server |
| S-10 | **Multi-repo orchestration** (cross-repo stage tracking) | ~1000 LoC | Enables coordinated multi-repo products |
| S-11 | **LLM-in-the-loop prompt testing** | ~500 LoC + API costs | Catches structurally compliant but practically ineffective prompts |
| S-12 | **Feedback loop from generated repos** | ~300 LoC | Closes the learning loop for KB and prompt improvement |

### Decision: UI Strategy

The dashboard is necessary. The question is delivery mechanism. Recommended path:

1. **Now:** Extract to static files (S-3). Immediate maintainability win.
2. **Next:** Add `--json` to CLI (S-4). Makes the API layer thinner.
3. **Later:** Evaluate VS Code extension (S-9) once the API surface is stable.

### Decision: Prompt Builder Strategy

Build Mode A first (S-1). This solves the immediate problem of maintaining prompt files
across bootstrapped repos. Mode B (S-5) follows naturally once the template engine is proven.

The prompt builder should:
- Read `process-registry.json` as its only required input
- Generate prompts that pass `test_prompt_compliance.py` out of the box
- Mark generated prompts with `# AUTO-GENERATED — do not edit` header
- Support `--eject` to convert a managed prompt to a manually-maintained one
- Track managed vs ejected state in a `.prompt-manifest.json`

---

---
---

# Part 3 — UI/UX Recommendation Gap Analysis

Date: 2026-04-14
Scope: How PROGRAMSTART decides whether a new program needs UI/UX, why the last two builds
shipped without a frontend, and what the system should do differently.

---

## Table of Contents (Part 3)

26. [The Problem: UI/UX Is Silently Dropped](#26-the-problem-uiux-is-silently-dropped)
27. [Root Cause: Shape-Locked Domain Inference](#27-root-cause-shape-locked-domain-inference)
28. [Gap Inventory: 9 Points Where UI Could Be Surfaced](#28-gap-inventory-9-points-where-ui-could-be-surfaced)
29. [What Other Factors Should We Consider](#29-what-other-factors-should-we-consider)
30. [Recommendations: Fixing the UI Blind Spot](#30-recommendations-fixing-the-ui-blind-spot)

---

## 26. The Problem: UI/UX Is Silently Dropped

When PROGRAMSTART builds a new program with shape "CLI tool" or "API service", the system
**never asks whether the project also needs a user interface**. There is no question, no
detection, no suggestion, and no advisory. The operator walks away with a pure backend
stack and no prompt or scaffold for a companion UI.

This is not a correct-by-default omission — it's a blind spot. Many real-world products
that are "primarily an API" still need:
- An admin dashboard for operators
- A monitoring/status UI
- A web interface for non-technical users
- A settings/configuration panel
- A documentation site with interactive API explorer

The system treats `PRODUCT_SHAPE` as a **mutually exclusive classification** when in
practice it's more like a **primary shape with optional surfaces**.

### How the Current Flow Works

```
User: programstart recommend --product-shape "api service" --need rag --need agents

  1. shape_profile("api service") →
       archetype: "Typed API and automation platform"
       base_stacks: [FastAPI, PostgreSQL, Pydantic, OpenTelemetry, pytest]
       intent_terms: {api contracts, automation, service observability, ...}
       base_domains: ["API, workflow, and backend platforms",
                      "Cloud, infrastructure, and platform operations"]

  2. infer_domain_names() →
       Checks needs against _need_to_domain map
       "rag" → "AI, retrieval, and agent systems"  ✓ added
       "agents" → "AI, retrieval, and agent systems"  (already present)
       NO frontend domain inferred — nothing triggers it

  3. build_stack_candidates() →
       Scores stacks against matched domains
       Frontend stacks (React, Next.js, Vite) never enter the candidate pool
       because "Web and frontend product delivery" domain was never added

  4. Coverage warnings →
       Only warn about domains that WERE matched but have gaps
       "Web and frontend" was never matched, so no warning is generated

  → Result: FastAPI + PostgreSQL + Pydantic + LiteLLM + Instructor + pytest
  → No mention of UI/UX anywhere in the recommendation
  → No coverage warning about missing frontend
```

---

## 27. Root Cause: Shape-Locked Domain Inference

The problem has **four interlocking causes**, not one:

### Cause 1: `shape_profile()` hard-codes domain sets per shape

```python
# "api service" NEVER includes "Web and frontend product delivery"
if product_shape == "api service":
    return (
        "Typed API and automation platform",
        ["FastAPI", "PostgreSQL", ...],
        {"api contracts", "automation", ...},
        ["API, workflow, and backend platforms",
         "Cloud, infrastructure, and platform operations"],  # ← no frontend domain
    )
```

Only "web app" and "mobile app" shapes include frontend domains in their base profile.
This means **the frontend domain can only be reached via capability expansion** — and
there's almost no path to it.

### Cause 2: `CAPABILITY_ALIASES` has only one frontend alias key

```python
"javascript": {"javascript", "typescript", "frontend"},
```

To trigger the frontend domain, a user must explicitly pass `--need javascript`,
`--need typescript`, or `--need frontend`. There are **no aliases for**:
- `"dashboard"` or `"admin dashboard"`
- `"web ui"` or `"web interface"`
- `"admin panel"` or `"management ui"`
- `"monitoring ui"` or `"status page"`
- `"configuration ui"` or `"settings panel"`

A user thinking "my API needs a dashboard" has no natural way to express this.

### Cause 3: `_need_to_domain` maps only `"javascript"` to frontend

```python
"javascript": "Web and frontend product delivery",
```

Even if a user said `--need dashboard`, the term `"dashboard"` has no alias expansion
and no domain mapping. It would be logged as an unrecognized need and **silently ignored**.

### Cause 4: No cross-shape advisory exists

The recommendation engine has `coverage_warnings` — but these only fire for domains that
**were matched and have gaps**. A completely absent domain generates no warning.

There is no logic anywhere that says: "You selected API service, but many API services
also need a management interface. Consider whether you need a web UI."

---

## 28. Gap Inventory: 9 Points Where UI Could Be Surfaced

### GAP-1: Idea Intake has no UI/UX question (HIGH)

`PROGRAMBUILD_IDEA_INTAKE.md` has 7 interview questions. None ask:
- "Will non-technical users interact with this system?"
- "Does this product need a visual interface beyond the terminal?"
- "Is there an admin/operator dashboard requirement?"

**Impact:** The very first structured conversation about the project never surfaces UI needs.

### GAP-2: Kickoff Packet has no UI needs field (HIGH)

The inputs block in `PROGRAMBUILD_KICKOFF_PACKET.md`:
```
PRODUCT_SHAPE:  [web app | mobile app | CLI tool | desktop app | API service | data pipeline | library | other]
```

There is no field for:
```
ADDITIONAL_SURFACES:    [admin dashboard | public web UI | monitoring dashboard | none]
```

The decision matrix explicitly says "API service, CLI tool → no UI guidance" with no
escape hatch.

### GAP-3: `CAPABILITY_ALIASES` missing UI-specific terms (HIGH)

No aliases for: `dashboard`, `admin ui`, `web interface`, `management ui`, `monitoring ui`,
`settings panel`, `portal`, `console`, `web portal`, `status page`.

**Impact:** Users can't express UI needs through the `--need` flag.

### GAP-4: `shape_profile()` treats shapes as mutually exclusive (MEDIUM)

There's no concept of a "composite shape" — e.g., "API service with admin dashboard" or
"CLI tool with web configuration UI". The function returns exactly one archetype, one stack
set, and one domain set.

### GAP-5: No "secondary surface" recommendation field (MEDIUM)

The `ProjectRecommendation` dataclass has no field for `suggested_companion_surfaces` or
`additional_ui_recommendation`. The recommendation output is a flat list of stacks for one
shape.

### GAP-6: Coverage warnings don't fire for absent domains (MEDIUM)

Warnings only generate for matched domains with `status: "partial"` or `"seed"`. A domain
that was **never matched** produces no warning. This means "Web and frontend product delivery"
is invisible when you pick a non-web shape.

### GAP-7: Prompt-eval scenarios don't test cross-shape UI (MEDIUM)

`config/prompt-eval-scenarios.json` has 6 scenarios. None test:
- "API service that also needs an admin dashboard"
- "CLI tool with a web-based configuration UI"
- "Data pipeline with monitoring dashboard"

The recommendation engine is never validated against hybrid-surface scenarios.

### GAP-8: Starter scaffold has no companion-UI option (LOW)

`programstart_starter_scaffold.py` has `cli_tool_plan()`, `api_service_plan()`,
`web_app_plan()`, and `mobile_app_plan()`. There is no `admin_dashboard_plan()` that
could be added to a CLI or API scaffold.

### GAP-9: Factory plan doesn't mention UI/UX considerations (LOW)

`render_factory_plan()` in `programstart_create.py` generates sections for Matched Domains,
Coverage Warnings, Stack Evidence, and Service Evidence. It never says: "This API service
is missing a management UI. Consider running `programstart create` with shape 'web app'
for a companion frontend repo."

---

## 29. What Other Factors Should We Consider

### 29.1 The "API Service + Dashboard" Is the Most Common Real-World Pattern

Most production API services ship with at least one of:
- Admin dashboard (user management, config, monitoring)
- API documentation site (Swagger/Redoc, but also custom docs)
- Status page (uptime, health checks)
- Internal tooling UI (debug tools, data viewers)

By not surfacing this, PROGRAMSTART's recommendation is technically correct but
**practically incomplete**. The user gets a well-recommended backend and then has to
figure out the frontend independently — outside the structured planning process.

### 29.2 UI Complexity Spectrum

Not all projects need a full Next.js app. The system should recognize different UI tiers:

| Tier | Example | Stack Profile |
|---|---|---|
| **None** | Pure library, background worker | No UI needed |
| **Docs only** | API with documentation | MkDocs / Swagger UI (no custom frontend) |
| **Minimal admin** | Internal dashboard, config panel | Vite + React SPA, or server-rendered FastAPI templates |
| **Full product UI** | Customer-facing web app | Next.js / SvelteKit / full SSR framework |

The current system treats this as binary: "web app" (full product UI) or nothing.
The middle tiers are invisible.

### 29.3 USERJOURNEY Attachment Should Consider UI Surface

The decision to attach USERJOURNEY currently depends on whether the project has "real
end-user flows, screens, client auth, or interactive state transitions." But this
assessment only happens at shape selection time. If the shape is "API service" and the
operator doesn't realize their API also needs user-facing flows, USERJOURNEY is never
attached.

### 29.4 Multi-Repo vs Monorepo for API + UI

If an API service gets a companion dashboard, should it be:
- **Same repo** (monorepo with `backend/` and `frontend/` directories)
- **Separate repo** (API repo + UI repo, each with their own PROGRAMBUILD)

The current bootstrap model creates one repo per `programstart create` invocation.
There's no guidance on when to use monorepo vs multi-repo for composite products.

### 29.5 When UI Should Be Explicitly Excluded

Not every project needs a UI, and the system shouldn't over-recommend one. Cases where
"no UI" is correct:
- Pure libraries consumed by other code
- Background workers / cron jobs
- Infrastructure-as-code modules
- Data pipeline stages that feed other systems
- Internal tools where terminal is the right interface

The system should **ask the question** but accept "no" as a valid answer.

### 29.6 UI Decision Timing

When should the UI question be asked?
- **Stage 0 (Idea Intake):** Too early for implementation details, but the right time
  to establish whether users will interact visually
- **Stage 1 (Feasibility):** Good time to assess whether a UI changes the feasibility
  calculus (cost, complexity, team skills)
- **Stage 3 (Requirements):** The latest point where UI surfaces must be identified,
  because architecture (Stage 4) depends on knowing all system boundaries

Current gap: The question is never asked at any stage.

### 29.7 Knowledge Base Frontend Coverage

The KB has strong frontend entries (React, Next.js, Vue, Svelte, Vite, Playwright,
Tailwind), but they're only reachable when the "Web and frontend product delivery"
domain is matched. For non-web shapes, this entire section of the KB is dark.

### 29.8 Shape-Agnostic UI Decision Rules

The KB `decision_rules` could include rules that fire across shapes:
- "If shape is API service AND regulated=true, recommend admin dashboard for audit trail"
- "If shape is data pipeline AND need includes monitoring, recommend status dashboard"
- "If shape is CLI tool AND target user is non-technical, recommend web wrapper"

No such cross-shape UI rules exist today.

---

## 30. Recommendations: Fixing the UI Blind Spot

### Tier 1: Quick Wins (address the silent failure)

| # | Change | Where | Effort |
|---|---|---|---|
| UI-1 | Add `ADDITIONAL_SURFACES` field to kickoff packet inputs block | `PROGRAMBUILD_KICKOFF_PACKET.md` | ~10 lines |
| UI-2 | Add UI question to Idea Intake: "Will end users or operators interact with this system through a visual interface?" | `PROGRAMBUILD_IDEA_INTAKE.md` | ~15 lines |
| UI-3 | Add capability aliases: `"dashboard"`, `"admin ui"`, `"web interface"`, `"portal"`, `"console"`, `"management ui"`, `"monitoring ui"` → mapped to `"javascript"` canonical | `programstart_recommend.py` CAPABILITY_ALIASES | ~10 lines |
| UI-4 | Add `_need_to_domain` entry for `"dashboard"` → `"Web and frontend product delivery"` | `programstart_recommend.py` infer_domain_names | ~3 lines |

### Tier 2: Structural Improvements (address the model gap)

| # | Change | Where | Effort |
|---|---|---|---|
| UI-5 | Add `suggested_companion_surfaces` field to `ProjectRecommendation` dataclass — populate when non-web shape has needs that commonly involve UI (monitoring, admin, config) | `programstart_recommend.py` | ~60 lines |
| UI-6 | Add cross-shape UI advisory logic: when an API/CLI/pipeline recommendation is built, check if the matched domains or needs commonly pair with a UI, and emit a non-blocking advisory in `coverage_warnings` | `programstart_recommend.py` | ~40 lines |
| UI-7 | Add UI-tier classification to shape_profile's output (none / docs-only / minimal-admin / full-product-ui) based on shape + needs | `programstart_recommend.py` | ~30 lines |
| UI-8 | Add prompt-eval scenarios: `api_service_with_admin_dashboard`, `cli_tool_with_web_ui`, `data_pipeline_with_monitoring` | `config/prompt-eval-scenarios.json` | ~60 lines |
| UI-9 | Add cross-shape decision rules to KB: rules that trigger frontend recommendations when non-web shapes have UI-adjacent needs | `config/knowledge-base.json` | ~40 lines |

### Tier 3: Full Solution (address the architecture gap)

| # | Change | Where | Effort |
|---|---|---|---|
| UI-10 | Add `admin_dashboard_plan()` to starter scaffold — a minimal Vite + React SPA scaffold that pairs with any backend shape | `programstart_starter_scaffold.py` | ~80 lines |
| UI-11 | Add monorepo vs multi-repo guidance to factory plan: when companion UI is recommended, advise on whether it belongs in the same repo or a separate one | `programstart_create.py` render_factory_plan | ~40 lines |
| UI-12 | Update `shape-requirements.prompt.md` to include a "UI Surface Assessment" section that checks whether the project needs any visual interface beyond what the primary shape provides | `.github/prompts/shape-requirements.prompt.md` | ~20 lines |
| UI-13 | Update `shape-architecture.prompt.md` to include companion-UI boundary in system topology when `ADDITIONAL_SURFACES` is non-empty | `.github/prompts/shape-architecture.prompt.md` | ~15 lines |

---

## Updated Summary Statistics (Parts 1 + 2 + 3)

| Section | Findings | Strategic Items |
|---|---|---|
| Part 1: Defect Audit (§1-§18) | 78 findings (2H, 23M, 52L, 1I) | — |
| Part 2: Standardization Analysis (§19-§20) | 8 layers documented | — |
| Part 2: UI Necessity (§21) | 1 assessment | 3 options evaluated |
| Part 2: Prompt Builder (§22) | 1 feasibility study | 2 modes defined |
| Part 2: Cross-Repo Portability (§23) | 10 components scored | 4 enablers identified |
| Part 2: Additional Factors (§24) | 10 considerations | — |
| Part 2: Strategic Recommendations (§25) | — | 12 items in 3 tiers |
| Part 3: UI/UX Recommendation Gaps (§26-§28) | 9 gaps (3H, 3M, 3L) | — |
| Part 3: Additional Factors (§29) | 8 considerations | — |
| Part 3: Fix Recommendations (§30) | — | 13 items in 3 tiers |
