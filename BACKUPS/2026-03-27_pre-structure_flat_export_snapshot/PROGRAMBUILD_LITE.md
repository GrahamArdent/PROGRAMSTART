# PROGRAMBUILD_LITE.md

# Program Build Lite

Use this version for a solo developer, a prototype, or a very small internal tool.
The goal is speed without abandoning the guardrails that prevent the most common structural mistakes.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files

---

## When To Use

Use this file when:
- the team is 1 to 3 people
- the app is low risk
- the budget or timeline is tight
- the system is not regulated or enterprise-critical

Do not use this file when:
- the app stores sensitive regulated data
- the system needs formal approvals or audit trails
- multiple teams must coordinate contracts

---

## Essential Stages

| Stage | Output | Standard |
|---|---|---|
| Inputs | filled inputs block | must be complete |
| Feasibility | short go/no-go note | 1 page max |
| Requirements | lean requirements and top workflows | focused on P0 only |
| Architecture | one architecture note | only essential contracts |
| Scaffold | route layer, auth client, CI, basic tests | must be green |
| Build | feature loop | one feature at a time |
| Launch check | short readiness checklist | must be explicit |

---

## Non-Negotiables

- one route constants file
- one auth-aware API client
- no hardcoded authenticated URLs in UI code
- one route alignment test
- one auth test per protected endpoint
- one smoke E2E flow for the primary user journey
- one rollback note before first deployment
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention

---

## Suggested Subagents

| Subagent | Use for |
|---|---|
| Research Scout | quick stack and competitor validation |
| UX Flow Designer | primary workflow and empty/error states |
| Contract Auditor | route and auth drift check |
| Test Planner | smoke test plan and fixture list |

---

## Minimal Prompt Pattern

```text
Build a lean but production-conscious plan for this app.

Inputs:
- project inputs block

Produce:
1. short feasibility note
2. P0 requirements only
3. main user workflow
4. basic architecture and API contract
5. scaffold with route constants and auth-aware client
6. essential tests: route alignment, auth, smoke E2E
7. short launch checklist
```

---

## Lite Definition Of Done

- primary workflow works end to end
- protected endpoints reject unauthenticated access
- route alignment test passes
- one smoke Playwright or Chromium test passes
- deployment and rollback steps are written down

---

Last updated: 2026-03-27
