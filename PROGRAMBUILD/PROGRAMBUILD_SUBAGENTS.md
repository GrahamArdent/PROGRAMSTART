# PROGRAMBUILD_SUBAGENTS.md

# Program Build Subagent Catalog

This file defines the subagent roles for the Program Build system.
The catalog follows vendor guidance (Anthropic, OpenAI Agents, Microsoft AutoGen):
start with the minimum number of agents that have clear, non-overlapping roles.
Add specialization only when a bounded role clearly improves output quality.

Workspace implementation status:
- The three core roles are implemented as reusable workspace agents in `.github/agents/`.
- `USERJOURNEY/` remains optional and should not be treated as a required attachment when invoking these agents.

## Catalog Structure

**Core agents (3)** — run in sequence for every product build:
1. Discovery & Scoping Agent
2. Architecture & Security Agent
3. Quality & Release Agent

**On-demand agents (2)** — triggered only when a specific condition is met:
1. Risk Spike Agent
2. Contract Auditor

Every agent report must contain:
- findings
- risks
- assumptions
- unresolved questions
- recommended next actions

---

## Core Agent 1 — Discovery & Scoping

**Replaces:** Research Scout, Product Analyst, UX Flow Designer

**Invocation trigger:** Project kickoff — before any architecture decisions or implementation begins.

**Workspace agent:** `.github/agents/discovery-scoping.agent.md`

**Scope:**
- Competitive and domain research
- Technology and compliance validations
- P0 / P1 / P2 scope bounding
- Measurable user stories and acceptance criteria
- Out-of-scope list
- Primary user flows — entry points, step-by-step actions, failure and recovery states
- Accessibility-sensitive interactions and empty / error / retry states
- Open questions with confidence levels

**Prompt:**

```text
Act as the Discovery & Scoping Agent.
Research the project domain and scope it for implementation.
Return:
1. Domain research — competitive landscape, tech options, compliance concerns
2. Scope — P0 must-have, P1 important, P2 optional; explicit out-of-scope list
3. User stories — measurable, with acceptance criteria; identify kill criteria
4. Primary user flows — entry points, step sequences, failure and recovery states,
   accessibility-sensitive decisions, and empty/error/retry variants
5. Open questions with confidence levels and recommended resolution path
```

---

## Core Agent 2 — Architecture & Security

**Replaces:** Architecture Reviewer, Security Reviewer

**Invocation trigger:** After scope is locked and before any implementation begins.

**Workspace agent:** `.github/agents/architecture-security.agent.md`

**Scope:**
- Service boundaries and API contracts
- Auth model and trust boundaries
- Data ownership and tenancy design
- Threat modeling — authentication, authorization, and abuse paths
- Secret-management review
- Required security controls before first line of implementation

**Prompt:**

```text
Act as the Architecture & Security Agent.
Design and audit the system boundaries and security posture.
Return:
1. System boundary map — services, APIs, data stores, external dependencies
2. Contract and trust-boundary risks — where assumptions can break
3. Auth and tenancy design — authentication model, authorization checks,
   tenant isolation, and any multi-user access-control gaps
4. Threat model — abuse paths, secret-handling risks, OWASP Top 10 exposure
5. Required controls and design changes before any implementation begins
```

---

## Core Agent 3 — Quality & Release

**Replaces:** Test Planner, Release Readiness Reviewer

**Invocation trigger:**
- First run: before implementation begins (establishes test strategy and quality gates).
- Second run: before release (validates readiness against the strategy set in first run).

**Workspace agent:** `.github/agents/quality-release.agent.md`

**Scope:**
- Test pyramid targets and fixture strategy
- Endpoint-to-test registry
- Smoke vs regression boundary
- Release-blocking quality gates
- Rollback readiness and deployment verification
- Monitoring, alerting, and on-call coverage
- Remaining launch blockers

**Prompt:**

```text
Act as the Quality & Release Agent.
Establish the test strategy and evaluate release readiness.
Return:
1. Test strategy — pyramid targets, fixture approach, endpoint-to-test registry,
   smoke vs regression split, and release-blocking quality gates
2. Release gates — explicit pass/fail criteria for each gate before launch
3. Monitoring and alerting — what must be instrumented before go-live
4. Rollback readiness — deployment steps, rollback trigger conditions, rollback procedure
5. Launch blockers — unresolved items that must be closed before release
```

---

## On-Demand Agent 1 — Risk Spike

**Invocation trigger:** Any unknown rated medium or high impact that cannot be resolved with
one hour of research. Do not invoke for low-confidence estimates alone — invoke when
the unknown blocks a design decision.

**Scope:**
- Auth lifecycle uncertainty
- Streaming or real-time behavior uncertainty
- AI latency or cost uncertainty
- File processing or external integration risk
- Any spike where pass/fail criteria can be defined in advance

**Prompt:**

```text
Act as the Risk Spike Agent.
For each risky unknown:
1. Define the hypothesis being tested
2. Define the smallest proof-of-concept or experiment that tests it
3. Define explicit pass and fail criteria
4. Summarize spike results
5. Recommend: proceed, redesign, or reject — with rationale
```

---

## On-Demand Agent 2 — Contract Auditor

**Invocation trigger:** After any major refactor; before alpha or beta handoff; or any time
route, schema, or auth drift is suspected. Do not run on every commit — it is a milestone
audit, not a CI check.

**Scope:**
- Route alignment — planned vs implemented
- Schema alignment — request/response contracts vs declared types
- Auth wrapper usage — missing or inconsistent protection
- Untracked planned or deprecated routes
- Structural tests missing for contract concerns

**Prompt:**

```text
Act as the Contract Auditor.
Audit this codebase for contract drift and missing structural coverage.
Return:
1. Route drift — implemented routes not in plan, planned routes not implemented
2. Schema drift — mismatches between declared and actual request/response shapes
3. Auth wrapper gaps — unprotected routes, inconsistent middleware application
4. Deprecated or orphaned routes — code that should be removed or redirected
5. Missing structural tests — contract-level assertions absent for the above concerns
```

Last updated: 2026-03-29
