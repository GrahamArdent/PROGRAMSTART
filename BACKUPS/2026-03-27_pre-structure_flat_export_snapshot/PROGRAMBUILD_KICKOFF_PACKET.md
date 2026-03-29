# PROGRAMBUILD_KICKOFF_PACKET.md

# Program Build Kickoff Packet

Use this file to start a new project with the same naming conventions, the same critical file set, and the same authority model every time.

Before using this packet:
- read `PROGRAMBUILD_CANONICAL.md`
- use `PROGRAMBUILD_FILE_INDEX.md` as the reference list
- choose one process file: `PROGRAMBUILD_LITE.md`, `PROGRAMBUILD_PRODUCT.md`, or `PROGRAMBUILD_ENTERPRISE.md`

---

## 1. Kickoff File Set

Create these files first:

- `FEASIBILITY.md`
- `RESEARCH_SUMMARY.md`
- `REQUIREMENTS.md`
- `USER_FLOWS.md`
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`
- `TEST_STRATEGY.md`
- `RELEASE_READINESS.md`
- `AUDIT_REPORT.md`

---

## 2. Starter Inputs Block

```text
PROJECT_NAME:
ONE_LINE_DESCRIPTION:
PRIMARY_USER:
SECONDARY_USER:
CORE_PROBLEM:
SUCCESS_METRIC:
FRONTEND_STACK:
BACKEND_STACK:
AUTH_MECHANISM:
HTTP_CLIENT:
DATABASE:
DEPLOYMENT_TARGET:
INTEGRATIONS:
KNOWN_CONSTRAINTS:
OUT_OF_SCOPE:
COMPLIANCE_OR_SECURITY_NEEDS:
TEAM_SIZE:
DELIVERY_TARGET:
```

---

## 3. Stage Startup Checklist

### Feasibility
- define the problem clearly
- state top risks
- define kill criteria
- record go, no-go, or limited-spike recommendation

### Research
- validate the stack
- identify existing solutions
- record compliance concerns
- surface likely failure modes early

### Requirements And UX
- define P0 and P1 scope
- write measurable acceptance criteria
- capture primary user flows
- define loading, empty, error, and retry states

### Architecture And Risk Spikes
- define the API contract table
- define the auth matrix
- define the route contract layer
- run spikes for risky unknowns

### Scaffold And Guardrails
- create route constants
- create auth-aware client and streaming helper
- add structural tests
- create CI with explicit timeouts

### Test Strategy
- define test layers
- define fixture strategy
- define golden policy
- define endpoint-to-test registry

### Release Readiness
- define rollback and migration plan
- define monitoring and alerts
- define release-day smoke checks
- define support ownership

### Audit
- verify route, auth, schema, and drift integrity
- verify planned-route and deprecated-route safety
- record severity, impact, and prevention guardrails

---

## 4. Required Output Rule

Every kickoff file must state:
- its purpose
- its owner
- the date last updated
- any upstream file it depends on
- whether it is canonical or derived

---

Last updated: 2026-03-27
