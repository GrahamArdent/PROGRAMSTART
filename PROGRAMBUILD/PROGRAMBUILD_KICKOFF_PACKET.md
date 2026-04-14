# PROGRAMBUILD_KICKOFF_PACKET.md

# Program Build Kickoff Packet

Use this file to start a new project with the same naming conventions, the same critical file set, and the same authority model every time.

Before using this packet:
- run `programstart bootstrap --dest <path/to/new-project> --project-name <name> --variant <lite|product|enterprise>` to create the project repo from this template
- read `PROGRAMBUILD_CANONICAL.md`
- use `PROGRAMBUILD_FILE_INDEX.md` as the reference list
- run `PROGRAMBUILD_IDEA_INTAKE.md` before filling the inputs block — use `programstart recommend` at the end to validate your variant and stack choices
- use `PROGRAMBUILD_GAMEPLAN.md` as the execution sequence guide
- run `PROGRAMBUILD_CHALLENGE_GATE.md` at every stage transition — follow each gate pass with `programstart advance --system programbuild`

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
ADDITIONAL_SURFACES:      [admin dashboard | monitoring UI | public web UI | documentation site | none]
KNOWN_CONSTRAINTS:
OUT_OF_SCOPE:
COMPLIANCE_OR_SECURITY_NEEDS:
TEAM_SIZE:
DELIVERY_TARGET:
```

Use `PRODUCT_SHAPE` to choose which later-stage guidance applies. When `ADDITIONAL_SURFACES` is non-empty and not `none`, include frontend and UI concerns in architecture, testing, and release planning. Technology choices belong in `ARCHITECTURE.md`, not here.

---

## 3. Stage Startup Checklist

### Idea Intake
- run `PROGRAMBUILD_IDEA_INTAKE.md` before filling the inputs block
- answer all 7 challenge questions; do not skip or combine
- review answers against the red flag table
- run `programstart recommend --product-shape "<shape>" --need <need1> --need <need2>` to get KB-backed variant, stack, and coverage recommendations before locking the inputs block
- stop and record why in `DECISION_LOG.md` if the recommendation is "stop"

### Stage Transitions
- run the Challenge Gate from `PROGRAMBUILD_CHALLENGE_GATE.md` at every stage boundary
- Lite minimum: Parts A, C, and F
- Product and Enterprise: all 7 parts (Part G required at Stages 4+)
- if resuming after a pause, run the Re-Entry Protocol instead
- after each gate pass, run `programstart advance --system programbuild` to move workflow state to the next stage
- run `programstart log --system programbuild` at any time to review the full sign-off history
- run `programstart progress --system programbuild` to check checklist completion percentage

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
- run Challenge Gate (Idea Intake → Stage 0), then `programstart advance --system programbuild`
- run Challenge Gate (Stage 0 → Stage 1), then `programstart advance --system programbuild`
- define the problem clearly
- state top risks
- define kill criteria
- estimate rough cost and effort
- record go, no-go, or limited-spike recommendation
- record the decision in `DECISION_LOG.md`

### Research
- run Challenge Gate (Stage 1 → Stage 2), then `programstart advance --system programbuild`
- run `programstart retrieval "<your topic>"` to query the KB before going to external sources — the KB has curated stack guidance, comparisons, and decision rules
- validate the stack
- identify existing solutions
- record compliance concerns
- surface likely failure modes early
- log low-confidence decisions and follow-up spikes

### Requirements And UX
- run Challenge Gate (Stage 2 → Stage 3), then `programstart advance --system programbuild`
- define P0 and P1 scope
- write measurable acceptance criteria
- capture primary user flows if users interact with the system directly
- define loading, empty, error, and retry states where an operator or end user can observe them

### Architecture And Risk Spikes
- run Challenge Gate (Stage 3 → Stage 4), then `programstart advance --system programbuild`
- run `programstart impact "<dependency or concern>"` to see which downstream docs are affected before committing an architecture decision
- apply the `PRODUCT_SHAPE` checklist first so you do not force a web-app contract model onto a CLI, API service, library, or background automation
- define the contract surface: API, command, job, event, or public library API
- define the auth or trust matrix
- define route or execution registration only where it exists
- define external dependencies and fallbacks
- define the dependency heat map
- run spikes for risky unknowns
- promote material architecture changes into ADRs if required

### Scaffold And Guardrails
- run Challenge Gate (Stage 4 → Stage 5), then `programstart advance --system programbuild`
- create the contract layer that fits the shape: routes, endpoints, commands, job definitions, or public API boundaries
- create the auth-aware client, trusted caller wrapper, operator helper, or equivalent boundary control
- add structural tests
- create CI with explicit timeouts

### Test Strategy
- run Challenge Gate (Stage 5 → Stage 6), then `programstart advance --system programbuild`
- apply the `PRODUCT_SHAPE` testing checklist before choosing browser E2E, service contract, command, or job-level coverage
- default to desired-outcome coverage first; treat purpose tests as the primary proof of value delivery
- do not count theatre tests as outcome coverage; use them only when they protect a real contract, structure, or regression class
- define test layers
- define fixture strategy
- define golden policy
- define requirements-to-test traceability
- define endpoint-to-test registry

### Template Quality Standard
- every bootstrapped repo should inherit the same testing rigor as this template: explicit contracts, regression coverage, and validated workflow checks
- desired outcome testing is the highest-priority evidence for product correctness
- golden, structural, smoke, and regression tests support the system, but they do not replace purpose tests tied to real user or operator outcomes

### Release Readiness
- run Challenge Gate (Stage 7 → Stage 8), then `programstart advance --system programbuild`
- define rollback and migration plan
- define monitoring and alerts
- define SLO and SLI targets
- define release-day smoke checks
- define support ownership

### Audit
- run Challenge Gate (Stage 8 → Stage 9), then `programstart advance --system programbuild`
- verify contract, access-control, schema, and drift integrity
- verify planned-route and deprecated-route safety
- record severity, impact, and prevention guardrails

### Post-Launch Review
- run Challenge Gate (Stage 9 → Stage 10), then `programstart advance --system programbuild`
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

Last updated: 2026-03-31
