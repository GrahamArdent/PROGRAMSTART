# TEST_STRATEGY.md

Purpose: Test model, fixture strategy, coverage rules, and endpoint-to-test registry.
Owner: Solo operator
Last updated: 2026-04-14
Depends on: REQUIREMENTS.md, USER_FLOWS.md, ARCHITECTURE.md
Authority: Canonical for quality model

---

## Test Pyramid Targets

PROGRAMSTART is a **CLI tool** with a **local web dashboard** (API service). The dominant test layers reflect both shapes.

| Layer | Target | Notes |
|---|---|---|
| Unit | 400+ pytest tests across 25 files | Core of the pyramid — covers CLI commands, recommendation engine, workflow state, validation, retrieval, drift check, models, prompts |
| Component | Endpoint HTTP integration tests | `test_serve_endpoints.py` — real HTTP server on loopback, exercises all 8 API endpoints |
| Purpose | Prompt-eval scenario suite (9 scenarios) | Deterministic recommendation quality via `config/prompt-eval-scenarios.json` |
| Golden | Playwright pixel-diff screenshots (3 baselines) | `tests/golden/dashboard/` — `absent-shell.png`, `attached-shell.png`, `attached-signoff-modal.png`; MAX_DIFF_PIXELS = 20 |
| E2E | Browser smoke + CLI smoke scripts | `programstart_dashboard_browser_smoke.py` (Playwright headless Chromium), `programstart_cli_smoke.py`, `programstart_dist_smoke.py` |

## PRODUCT_SHAPE Testing Checklist

| PRODUCT_SHAPE | Testing emphasis |
|---|---|
| CLI tool | command parsing, exit codes, stdout/stderr snapshots, fixture-driven integration tests |
| API service | contract tests, schema compatibility, endpoint routing, JSON body parsing, error responses |

Both rows apply. PROGRAMSTART is a CLI tool that also serves a local dashboard with a REST-like API.

## Unit Test Rules

- Every public function in `scripts/` must have at least one test in `tests/`.
- Tests must not depend on network access or external services. Use monkeypatch or tmp_path fixtures for isolation.
- New scripts added to `scripts/` must have a corresponding `tests/test_<name>.py` file and be registered in `config/process-registry.json` bootstrap_assets.
- Prefer testing the function directly over testing via subprocess unless the test specifically validates CLI arg parsing.
- New unified CLI aliases (for example `programstart kb` and `programstart diff`) must have parser/dispatch coverage in `test_programstart_cli.py`; destructive state commands must also have direct workflow-state safety tests.

## Component Test Rules

- Dashboard API endpoint tests (`test_serve_endpoints.py`) must start a real `DashboardHandler` on a loopback port and issue actual HTTP requests.
- Every POST endpoint must test: valid JSON, invalid JSON (400), and at least one business-logic rejection.
- Every GET endpoint must test: successful response, 404 for unknown paths.
- Tests must validate Content-Type headers and HTTP status codes, not just response body.

## Purpose And Auth Test Rules

### What Is A Purpose Test

A purpose test validates a **user outcome or business rule** that was promised in `REQUIREMENTS.md`. If this test fails, a real user or operator loses a real capability.

A purpose test must:
- Reference a specific requirement ID from `REQUIREMENTS.md` (e.g. FR-001).
- Describe the user-visible or operator-visible outcome being protected.
- Fail only when that outcome is broken — not when an implementation detail changes.

### What Is A Theatre Test

A theatre test validates an **implementation detail that no user or operator would notice if it broke.** It exists to satisfy a coverage metric, not to protect a promise.

Signs of a theatre test:
- No requirement ID is referenced.
- The assertion checks internal state, private method signatures, or intermediate data shapes that are not part of any contract.
- Removing the code under test would not break any user-visible behavior.
- The test was written to increase a coverage percentage, not to prevent a recurrence of a real failure.

### The Litmus Test

> If this test fails, does a real user or operator lose a real capability that was promised in REQUIREMENTS.md?

- **Yes** → Purpose test. Keep it. Link it to its requirement ID.
- **No** → Either reclassify it as a structural or regression test with a clear rationale, or delete it.

### Enforcement Rules

- Every P0 requirement must have at least one purpose test. No exceptions.
- Every P1 requirement should have at least one purpose test. Exceptions require a DECISION_LOG.md entry.
- A test without a requirement ID is not a purpose test. It may still be valuable (structural, regression, smoke) but it does not count toward purpose coverage.
- Purpose tests run in CI and block merges. They are never skipped, muted, or marked flaky without a decision log entry.
- Auth tests must verify both the positive case (authorized access works) and the negative case (unauthorized access is denied). An auth test that only checks the happy path is incomplete.
- The dashboard is loopback-only (127.0.0.1). No auth layer exists because the threat model is local-operator-only. If network binding is ever added, auth tests become mandatory.
- Desired outcome testing is the top-level quality bar. Theatre tests may exist, but they never substitute for proof that the promised outcome works.

### Purpose Test Template

```text
Test ID:        PT-[requirement ID]-[sequence]
Requirement:    [FR-XXX or NFR-XXX from REQUIREMENTS.md]
Outcome:        [What the user or operator can do when this works]
Failure Impact: [What breaks for the user or operator if this fails]
Test Type:      [unit / component / integration / E2E]
```

## Template Quality Standard

- New repositories bootstrapped from PROGRAMSTART should inherit the same test discipline: validated contracts, strong regression coverage, and purpose tests tied to real outcomes.
- Purpose-test coverage is the primary indicator that the product works for a real user or operator.
- Structural, smoke, golden, and regression tests are supporting layers. They are useful only when they protect a real contract, failure mode, or user-facing promise.
- Theatre tests do not satisfy coverage gates for P0 or P1 outcomes.

## Golden Baseline Policy

- Golden baselines live in `tests/golden/dashboard/` and are committed to the repository.
- Captures use Playwright headless Chromium at a fixed viewport (1440×1400) with CSS animation/transition freeze injected.
- Pixel diff tolerance: `MAX_DIFF_PIXELS = 20`. Any diff above this threshold fails the check and writes a failure artifact to `outputs/golden-failures/`.
- Golden baselines must be recaptured and committed when intentional UI changes are made. Never update baselines to suppress a real regression.
- CI uploads golden failure artifacts on mismatch for manual review.

## E2E And Smoke Strategy

PROGRAMSTART has no interactive user login flow. The dominant end-to-end validation modes are:

- **CLI smoke** (`programstart_cli_smoke.py`): Exercises the full `programstart` CLI binary with real arguments, validates exit codes and output.
- **Dashboard browser smoke** (`programstart_dashboard_browser_smoke.py`): Launches the dashboard server, opens headless Chromium via Playwright, validates DOM structure, select bindings, and modal behavior.
- **Distribution smoke** (`programstart_dist_smoke.py`): Verifies the installed wheel/editable package exposes the expected entry points.
- **Factory smoke** (`programstart_factory_smoke.py`): End-to-end bootstrap of a new project into a temp directory, validates structure.
- **Dashboard smoke** (`programstart_dashboard_smoke.py`): Lightweight HTTP-level smoke against the running server.
- Smoke scripts are orchestrated by `noxfile.py` sessions and CI workflows (`process-guardrails.yml`, `full-ci-gate.yml`).

## Fixture Strategy

| Fixture type | Purpose | Owner |
|---|---|---|
| `tmp_path` (pytest built-in) | Isolated filesystem for tests that write files (bootstrap, workflow state, golden pixel diff) | pytest |
| `monkeypatch` (pytest built-in) | Stub environment variables, module-level constants, and subprocess calls | pytest |
| `server_url` (module-scoped) | Ephemeral `DashboardHandler` on random loopback port for HTTP endpoint tests | `test_serve_endpoints.py` |
| `config/prompt-eval-scenarios.json` | Deterministic recommendation evaluation: 9 product shapes with expected stack matches | `test_programstart_prompt_eval.py` |
| `config/knowledge-base.json` | 145 technology stacks, 12 decision rules, 15 integration patterns | Multiple test files |
| `tests/golden/dashboard/*.png` | Pixel-perfect screenshot baselines for visual regression | `test_programstart_dashboard_golden.py` |

## Endpoint-To-Test Registry

| Endpoint | HTTP test | Unit test | Browser smoke | Golden |
|---|---|---|---|---|
| `GET /` (index) | `test_serve_endpoints.py::TestGetIndex` | — | Yes (DOM check) | Yes (screenshot) |
| `GET /api/state` | `test_serve_endpoints.py::TestGetApiState` | `TestGetStateJson` | Yes (hydration) | — |
| `GET /api/doc?path=` | `test_serve_endpoints.py::TestGetApiDoc` | `TestGetDocPreview` | — | — |
| `POST /api/run` | `test_serve_endpoints.py::TestPostApiRun` | `test_programstart_serve.py` (5 tests) | — | — |
| `POST /api/uj-phase` | `test_serve_endpoints.py::TestPostUjPhase` | — | — | — |
| `POST /api/uj-slice` | `test_serve_endpoints.py::TestPostUjSlice` | — | — | — |
| `POST /api/workflow-signoff` | `test_serve_endpoints.py::TestPostWorkflowSignoff` | — | — | — |
| `POST /api/workflow-advance` | `test_serve_endpoints.py::TestPostWorkflowAdvance` | — | — | — |
| `POST /api/bootstrap` | `test_serve_endpoints.py::TestPostBootstrap` | — | — | — |

## Desired Outcome Coverage View

This section is derived from `USERJOURNEY/ANALYTICS_AND_OUTCOMES.md`. It distinguishes operator-dashboard coverage from the planned end-user onboarding outcomes.

| Desired outcome | Planned user-facing route anchors | Covered by current operator routes | Covered by current goldens | Covered by current tests | Coverage verdict |
|---|---|---|---|---|---|
| higher signup-to-activation conversion | `/auth/signup`, `/auth/verify-pending`, onboarding route family, `/workspace` | No | No | No | not implemented in this repo |
| lower confusion in the first session | `/auth/login`, `/auth/signup`, `/onboarding/welcome`, `/onboarding/notice` | No | No | No | not implemented in this repo |
| stronger trust through better disclosure | `/onboarding/notice` plus consent checkpoints | No | No | No | not implemented in this repo |
| better separation between account creation and real product activation | `/auth/callback`, onboarding route family, `/workspace` with unactivated skip state | No | No | No | not implemented in this repo |
| cleaner legal audit trail for consent events | signup and AI-notice checkpoints, not a single route | No | No | No | not implemented in this repo |
| operator can inspect workflow state reliably | `/api/state`, `/api/doc` | Yes | Partial | Yes | covered |
| operator can review shell and signoff modal visuals | `/` and modal state inside dashboard | Yes | Yes | Yes | covered |
| operator can run controlled dashboard actions safely | `/api/run`, `/api/bootstrap`, workflow POST routes | Yes | No | Yes | covered at API level, not visually relevant |

## Acceptance-Criteria-To-Test-Case Matrix

Use this matrix when planning or reviewing a project repo. The test case IDs are planning IDs; implementation may rename files, but the coverage intent should remain intact.

| Acceptance criterion reference | Planned test case ID | Primary outcome protected | Minimum proof type |
|---|---|---|---|
| Auth Entry 1 | `TC-AUTH-ENTRY-001` | lower confusion in the first session | browser or component rendering test |
| Auth Entry 2 | `TC-AUTH-ENTRY-002` | lower confusion in the first session | copy assertion tied to product promise |
| Signup 1 | `TC-SIGNUP-001` | higher signup-to-activation conversion | validation test |
| Signup 2 | `TC-SIGNUP-002` | higher signup-to-activation conversion | validation test |
| Signup 3 | `TC-SIGNUP-003` | cleaner legal audit trail for consent events | consent-contract test |
| Signup 4 | `TC-SIGNUP-004` | better separation between account creation and real product activation | route transition test |
| Verification 1 | `TC-VERIFY-001` | better separation between account creation and real product activation | route guard test |
| Verification 2 | `TC-VERIFY-002` | better separation between account creation and real product activation | callback branch test |
| Verification 3 | `TC-VERIFY-003` | better separation between account creation and real product activation | callback branch test |
| Verification 4 | `TC-VERIFY-004` | lower confusion in the first session | recovery-path test |
| Consent 1 | `TC-CONSENT-001` | cleaner legal audit trail for consent events | persistence/versioning test |
| Consent 2 | `TC-CONSENT-002` | stronger trust through better disclosure | notice-gate test |
| Consent 3 | `TC-CONSENT-003` | higher signup-to-activation conversion | signup continuation test |
| Onboarding 1 | `TC-ONBOARD-001` | lower confusion in the first session | route rendering test |
| Onboarding 2 | `TC-ONBOARD-002` | higher signup-to-activation conversion | path-availability test |
| Onboarding 3 | `TC-ONBOARD-003` | better separation between account creation and activation | state-integrity test |
| Onboarding 4 | `TC-ONBOARD-004` | higher signup-to-activation conversion | resume-point test |
| Import 1 | `TC-IMPORT-001` | higher signup-to-activation conversion | file-validation test |
| Import 2 | `TC-IMPORT-002` | higher signup-to-activation conversion | parse-review test |
| Import 3 | `TC-IMPORT-003` | higher signup-to-activation conversion | profile-creation integration test |
| Start-From-Scratch 1 | `TC-SCRATCH-001` | higher signup-to-activation conversion | starter-flow validation test |
| Start-From-Scratch 2 | `TC-SCRATCH-002` | higher signup-to-activation conversion | workspace-handoff test |
| Activation 1 | `TC-ACTIVATION-001` | better separation between account creation and activation | negative activation test |
| Activation 2 | `TC-ACTIVATION-002` | higher signup-to-activation conversion | first-value event test |
| Activation 3 | `TC-ACTIVATION-003` | better separation between account creation and activation | post-activation bypass test |
| Returning User 1 | `TC-RETURN-001` | better separation between account creation and real product activation | returning-user route test |
| Returning User 2 | `TC-RETURN-002` | higher signup-to-activation conversion | partial-onboarding resume test |
| Analytics 1 | `TC-ANALYTICS-001` | better analytics around onboarding drop-off and feature adoption | event emission test |
| Analytics 2 | `TC-ANALYTICS-002` | better analytics around onboarding drop-off and feature adoption | funnel reporting test |
| Outcome And Route Guardrails 1 | `TC-GUARDRAIL-001` | better separation between account creation and activation | activation-event contract test |
| Outcome And Route Guardrails 2 | `TC-GUARDRAIL-002` | better separation between account creation and activation | unactivated-route guard test |
| Outcome And Route Guardrails 3 | `TC-GUARDRAIL-003` | cleaner legal audit trail for consent events | consent-attribution test |
| Outcome And Route Guardrails 4 | `TC-GUARDRAIL-004` | test-model integrity | planning review gate; not executable product test |

## Gap Analysis

- The current golden baseline policy protects the operator dashboard shell only. It does not validate end-user onboarding outcomes because those product routes are not implemented in this template repo.
- Desired USERJOURNEY outcomes are documented and route-mapped, but they currently exist as planning artifacts rather than executable frontend routes in this repository.
- When a project repo implements the onboarding route family, add golden coverage for at least: auth entry, verification pending, onboarding welcome, AI/data notice, import review, minimal unactivated workspace, and activated workspace handoff.
- `REQUIREMENTS.md` still contains template placeholders — purpose tests cannot reference requirement IDs until FR-xxx entries are defined.
- `update_implementation_tracker_phase()` and `update_implementation_tracker_slice()` are tested via HTTP boundary (invalid JSON, invalid params) but do not have happy-path write tests due to side effects on USERJOURNEY tracker files. Consider a fixture-isolated write test.
- `save_workflow_signoff()` and `advance_workflow_with_signoff()` are tested at the HTTP boundary for rejection cases. Happy-path tests exist only through the CLI (`test_programstart_workflow_state.py`). Consider adding direct function-level happy-path tests with tmp_path isolation.
- Browser smoke and golden screenshot comparisons run outside pytest (nox sessions, CI). They are not counted in the 400+ pytest test total. Integrating them as pytest-marked tests (e.g. `@pytest.mark.playwright`) would give unified reporting.

---
