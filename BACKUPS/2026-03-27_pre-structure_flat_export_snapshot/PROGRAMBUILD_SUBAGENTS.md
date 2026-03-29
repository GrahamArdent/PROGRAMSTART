# PROGRAMBUILD_SUBAGENTS.md

# Program Build Subagent Catalog

This file defines the standard subagent roles for the Program Build system.
Use these roles to split work cleanly and reduce shallow analysis.

Every subagent report should contain:
- findings
- risks
- assumptions
- unresolved questions
- recommended next actions

---

## 1. Research Scout

Use for:
- competitor analysis
- technology validation
- compliance scan
- tooling recommendations

Prompt:

```text
Act as the Research Scout.
Research this project domain and return:
1. leading alternatives
2. recommended stack options
3. major compliance or regulatory concerns
4. common implementation failures
5. open questions with confidence levels
```

---

## 2. Product Analyst

Use for:
- scoping
- user stories
- acceptance criteria
- kill criteria

Prompt:

```text
Act as the Product Analyst.
Turn the project concept into:
1. P0, P1, and P2 scope
2. measurable user stories
3. acceptance criteria
4. out-of-scope list
5. assumptions and risks
```

---

## 3. UX Flow Designer

Use for:
- primary workflows
- role-based flows
- loading, empty, error, and retry states
- accessibility-sensitive interactions

Prompt:

```text
Act as the UX Flow Designer.
Map the primary user flows and include:
1. entry points
2. step-by-step user actions
3. failure and recovery states
4. accessibility-sensitive interactions
5. open UX decisions
```

---

## 4. Architecture Reviewer

Use for:
- service boundaries
- API contracts
- auth model
- data ownership

Prompt:

```text
Act as the Architecture Reviewer.
Review the proposed architecture and return:
1. system boundaries
2. contract risks
3. data ownership issues
4. auth and trust-boundary risks
5. recommendations before implementation
```

---

## 5. Risk Spike Agent

Use for:
- auth lifecycle uncertainty
- streaming behavior uncertainty
- AI latency or cost uncertainty
- file processing uncertainty
- external integration risk

Prompt:

```text
Act as the Risk Spike Agent.
For each risky unknown:
1. define the hypothesis
2. define a small proof or experiment
3. define pass and fail criteria
4. summarize results
5. recommend proceed, redesign, or reject
```

---

## 6. Contract Auditor

Use for:
- route alignment
- schema alignment
- auth wrapper usage
- planned-route safety

Prompt:

```text
Act as the Contract Auditor.
Audit this codebase for:
1. route drift
2. schema drift
3. auth wrapper inconsistencies
4. untracked planned or deprecated routes
5. structural tests missing for these concerns
```

---

## 7. Test Planner

Use for:
- unit, component, purpose, golden, and E2E split
- fixture strategy
- smoke vs regression boundaries
- test registry design

Prompt:

```text
Act as the Test Planner.
Create a test strategy covering:
1. test pyramid targets
2. fixture strategy
3. endpoint-to-test registry
4. smoke and regression split
5. release-blocking quality gates
```

---

## 8. Security Reviewer

Use for:
- threat modeling
- auth matrix review
- tenant isolation
- secret handling
- abuse-case review

Prompt:

```text
Act as the Security Reviewer.
Assess this system for:
1. authentication and authorization risks
2. tenancy and access-control gaps
3. secret-management issues
4. abuse or misuse paths
5. required controls before release
```

---

## 9. Release Readiness Reviewer

Use for:
- rollback readiness
- monitoring and alerting
- smoke checks
- ownership and support gaps

Prompt:

```text
Act as the Release Readiness Reviewer.
Evaluate whether this system is ready to launch.
Return:
1. deployment readiness
2. rollback readiness
3. monitoring and alert coverage
4. release-day smoke checks
5. remaining launch blockers
```

---

Last updated: 2026-03-27