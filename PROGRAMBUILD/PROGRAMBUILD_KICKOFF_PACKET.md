# PROGRAMBUILD_KICKOFF_PACKET.md

# Program Build Kickoff Packet

Use this file to start a new project with the same naming conventions, the same critical file set, and the same authority model every time.

Before using this packet:
- read `PROGRAMBUILD_CANONICAL.md`
- use `PROGRAMBUILD_FILE_INDEX.md` as the reference list
- choose one process file: `PROGRAMBUILD_LITE.md`, `PROGRAMBUILD_PRODUCT.md`, or `PROGRAMBUILD_ENTERPRISE.md`

---

## 1. Kickoff File Set

Create these files in the project repository that was bootstrapped from PROGRAMSTART. Keep the template repository clean.

Create these files first:

- `FEASIBILITY.md`
- `DECISION_LOG.md`
- `RESEARCH_SUMMARY.md`
- `REQUIREMENTS.md`
- `USER_FLOWS.md`
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`
- `TEST_STRATEGY.md`
- `RELEASE_READINESS.md`
- `AUDIT_REPORT.md`
- `POST_LAUNCH_REVIEW.md`

---

## 2. Starter Inputs Block

```text
PROJECT_NAME:
ONE_LINE_DESCRIPTION:
PRIMARY_USER:
SECONDARY_USER:
CORE_PROBLEM:
SUCCESS_METRIC:
PRODUCT_SHAPE:            [web app | mobile app | CLI tool | desktop app | API service | data pipeline | library | other]
KNOWN_CONSTRAINTS:
OUT_OF_SCOPE:
COMPLIANCE_OR_SECURITY_NEEDS:
TEAM_SIZE:
DELIVERY_TARGET:
```

Use `PRODUCT_SHAPE` to choose which later-stage guidance applies. Technology choices belong in `ARCHITECTURE.md`, not here.

---

## 3. Stage Startup Checklist

### Kickoff Decision Matrix

Lock these decisions before filling stage outputs so the rest of the workflow inherits the right assumptions.

| Decision | Choose this when | Primary effect |
|---|---|---|
| `PRODUCT_SHAPE` = `web app` or `mobile app` | the product has real end-user flows, screens, client auth, or interactive state transitions | route/UI/state guidance and end-user test layers become primary |
| `PRODUCT_SHAPE` = `API service`, `data pipeline`, `CLI tool`, `desktop app`, or `library` | the dominant value is delivered through service contracts, jobs, commands, packaged runtime behavior, or a reusable API | contract, operator, job, command, or compatibility guidance becomes primary |
| Variant = `lite` | small team, lower blast radius, fast proof needed | lighter evidence and minimum viable guardrails |
| Variant = `product` | standard production delivery with shared contracts and real quality gates | balanced guardrails, explicit decisions, and maintained regression coverage |
| Variant = `enterprise` | regulated, high-consequence, or multi-team delivery | formal sign-off, retained evidence, stronger governance |
| Attach `USERJOURNEY/` | onboarding, consent, activation, or first-run routing must be designed for real end users | add the USERJOURNEY workflow and dependency chain |
| Stay PROGRAMBUILD-only | the product is background automation, a service, a library, a CLI, or otherwise has no meaningful end-user onboarding journey | keep scope inside PROGRAMBUILD and do not inherit UX/legal journey work by default |

### Ownership And Gates
- use the kickoff decision matrix before assigning variant, attachments, or stage owners
- define the file owner for every output or leave `[ASSIGN]` until confirmed
- define gate approvers for product and enterprise work
- define where approval evidence will be retained
- decide whether this project needs ADRs in addition to the decision log
- decide whether this project needs the optional `USERJOURNEY/` attachment based on whether the product includes interactive end-user onboarding, consent, activation, or first-run routing

### Feasibility
- define the problem clearly
- state top risks
- define kill criteria
- estimate rough cost and effort
- record go, no-go, or limited-spike recommendation
- record the decision in `DECISION_LOG.md`

### Research
- validate the stack
- identify existing solutions
- record compliance concerns
- surface likely failure modes early
- log low-confidence decisions and follow-up spikes

### Requirements And UX
- define P0 and P1 scope
- write measurable acceptance criteria
- capture primary user flows if users interact with the system directly
- define loading, empty, error, and retry states where an operator or end user can observe them

### Architecture And Risk Spikes
- apply the `PRODUCT_SHAPE` checklist first so you do not force a web-app contract model onto a CLI, API service, library, or background automation
- define the contract surface: API, command, job, event, or public library API
- define the auth or trust matrix
- define route or execution registration only where it exists
- define external dependencies and fallbacks
- define the dependency heat map
- run spikes for risky unknowns
- promote material architecture changes into ADRs if required

### Scaffold And Guardrails
- create the contract layer that fits the shape: routes, endpoints, commands, job definitions, or public API boundaries
- create the auth-aware client, trusted caller wrapper, operator helper, or equivalent boundary control
- add structural tests
- create CI with explicit timeouts

### Test Strategy
- apply the `PRODUCT_SHAPE` testing checklist before choosing browser E2E, service contract, command, or job-level coverage
- define test layers
- define fixture strategy
- define golden policy
- define requirements-to-test traceability
- define endpoint-to-test registry

### Release Readiness
- define rollback and migration plan
- define monitoring and alerts
- define SLO and SLI targets
- define release-day smoke checks
- define support ownership

### Audit
- verify contract, access-control, schema, and drift integrity
- verify planned-route and deprecated-route safety
- record severity, impact, and prevention guardrails

### Post-Launch Review
- compare actual outcomes to the success metric
- record incidents, support notes, and adoption friction
- capture lessons learned and follow-up owners

---

## 4. RACI Starter

Use this when the project is large enough that ownership cannot stay implicit.

| Stage Or Output | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Feasibility | | | | |
| Research | | | | |
| Requirements And UX | | | | |
| Architecture And Risk | | | | |
| Test Strategy | | | | |
| Release Readiness | | | | |
| Post-Launch Review | | | | |

---

## 5. Required Output Rule

Every kickoff file must state:
- its purpose
- its owner
- the date last updated
- any upstream file it depends on
- whether it is canonical or derived

---

Last updated: 2026-03-27
