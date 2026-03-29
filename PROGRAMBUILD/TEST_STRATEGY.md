# TEST_STRATEGY.md

Purpose: Test model, fixture strategy, coverage rules, and endpoint-to-test registry.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: REQUIREMENTS.md, USER_FLOWS.md, ARCHITECTURE.md
Authority: Canonical for quality model

---

## Test Pyramid Targets

Use `PRODUCT_SHAPE` to choose the dominant test layers. Not every project needs browser component tests or end-user E2E.

| Layer | Target | Notes |
|---|---|---|
| Unit | | |
| Component | | |
| Purpose | | |
| Golden | | |
| E2E | | |

## PRODUCT_SHAPE Testing Checklist

Choose the rows that apply. Delete the ones that do not fit the project.

| PRODUCT_SHAPE | Testing emphasis |
|---|---|
| web app | component/UI states, authenticated browser flows, route protection, smoke E2E |
| mobile app | device-state flows, offline/retry behavior, navigation, auth/session renewal |
| CLI tool | command parsing, exit codes, stdout/stderr snapshots, fixture-driven integration tests |
| desktop app | window/app lifecycle, packaging/update path, local persistence, crash recovery |
| API service | contract tests, auth/tenancy, schema compatibility, consumer-facing regression tests |
| data pipeline / background automation | job orchestration, idempotency, retry/backfill behavior, data-quality assertions, operator alerts |
| library / SDK | API compatibility, examples/docs tests, version matrix, consumer integration tests |
| other | define the dominant quality risks before selecting coverage layers |

## Unit Test Rules

- rule
- rule

## Component Test Rules

- rule
- rule

## Purpose And Auth Test Rules

- rule
- rule

## Golden Baseline Policy

- rule
- rule

## E2E And Smoke Strategy

If there is no interactive user flow, replace this section with the dominant end-to-end validation mode: scheduled-job smoke run, CLI scenario matrix, service contract probe, or workflow replay.

- smoke
- regression

## Fixture Strategy

| Fixture type | Purpose | Owner |
|---|---|---|
| | | |

## Requirements Traceability Matrix

| Requirement ID | Architecture reference | Test coverage | Status |
|---|---|---|---|
| | | | |

## Endpoint-To-Test Registry

| Endpoint | Purpose test | Component test | E2E | Golden |
|---|---|---|---|---|
| | | | | |

## Gap Analysis

- gap

---
