# PROGRAMBUILD_GAMEPLAN.md

# Execution Gameplan

Purpose: Chained execution sequence that connects every stage to its exact prompt, required inputs, validation checks, and outputs — so execution is deterministic, not improvised.
Owner: Solo Operator or Project Lead
Last updated: 2026-03-31
Depends on: PROGRAMBUILD.md (stage definitions), PROGRAMBUILD_IDEA_INTAKE.md (pre-stage protocol), PROGRAMBUILD_CHALLENGE_GATE.md (transition protocol)
Authority: Canonical for execution sequencing and cross-stage validation

---

## Why This Exists

PROGRAMBUILD.md defines *what* each stage produces. This file defines *how to execute them in sequence* — what feeds into what, what must be validated before proceeding, and what contradictions to check for at every boundary.

Without this, execution drifts into:
- Prompts run out of order or with missing context.
- Outputs from one stage contradict outputs from another.
- Validation happens only at Stage 9 (Audit) — far too late.
- The agent or operator invents the sequence from memory instead of following a canonical path.

---

## How To Use

1. Start at the top. Do not skip ahead.
2. At each step, use the exact inputs listed. Do not substitute from memory.
3. Run the Challenge Gate at every transition. It is built into the sequence.
4. Run the Cross-Stage Validation at the steps where it appears. It catches contradictions that the Challenge Gate cannot.
5. If a step fails validation, do not proceed. Fix the failure, then re-run.

---

## Execution Sequence

### Pre-Stage: Idea Intake

**Trigger:** Someone has an idea.
**Protocol:** `PROGRAMBUILD_IDEA_INTAKE.md`
**Inputs:** The raw idea — verbal, written, or sketched.

```
Steps:
1. Run the Idea Intake interview (all 7 questions).
2. Review answers against the red flag table.
3. Challenge weak answers. Require rewrites for flagged items.
4. Produce the structured output:
   - Clean problem statement
   - Candidate success metric
   - Candidate out-of-scope list
   - Kill criteria candidates
   - Cheapest validation experiment
   - Recommendation: go / investigate / stop
5. If "stop": record why in DECISION_LOG.md. End here.
6. If "investigate": run the cheapest validation experiment. Return to step 4 with new evidence.
7. If "go": proceed to Stage 0.
```

**Output:** Structured intake summary ready to feed into the inputs block.

---

### Stage 0: Inputs And Mode Selection

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Idea Intake → Stage 0).
**Inputs:** Idea Intake output.
**Reference file:** `PROGRAMBUILD.md` Section 2 (Inputs).

```
Steps:
1. Fill the inputs block in PROGRAMBUILD.md using the Idea Intake output.
   - PROJECT_NAME: from intake
   - ONE_LINE_DESCRIPTION: from clean problem statement (not solution language)
   - PRIMARY_USER: from "who has this problem"
   - CORE_PROBLEM: from clean problem statement
   - SUCCESS_METRIC: from intake candidate
   - OUT_OF_SCOPE: from intake candidate list
2. Decide PRODUCT_SHAPE using the conditionals table in PROGRAMBUILD.md.
3. Decide variant: lite, product, or enterprise.
4. Decide whether USERJOURNEY/ is needed (only if real onboarding/consent/activation exists).
5. Record all three decisions in DECISION_LOG.md.
```

**Validation before proceeding:**
- [ ] Every field in the inputs block is populated. No blanks, no "TBD."
- [ ] PRODUCT_SHAPE is explicit and recorded.
- [ ] Variant is chosen and recorded.
- [ ] USERJOURNEY decision is recorded.
- [ ] ONE_LINE_DESCRIPTION does not mention technology or features.
- [ ] SUCCESS_METRIC is a measurable outcome, not a feature shipped.

**Output:** Completed inputs block, DECISION_LOG.md entries.

---

### Stage 1: Feasibility And Kill Criteria

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 0 → Stage 1).
**Inputs:** Completed inputs block, Idea Intake kill criteria candidates.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 8.

```
Steps:
1. Run the feasibility prompt with the inputs block as context.
2. Produce FEASIBILITY.md with all required sections:
   - Problem statement
   - Primary user pain and evidence
   - Alternatives and why insufficient
   - Business viability assumptions
   - Technical feasibility assumptions
   - Top 3 risks
   - Kill criteria (upgraded from intake candidates — must be observable and falsifiable)
   - Rough cost and effort estimate
   - Recommendation: go / limited spike / no-go
3. Record the recommendation in DECISION_LOG.md.
4. If "no-go": stop. Do not proceed to Stage 2.
5. If "limited spike": define the spike scope, run it, return to step 2 with results.
6. If "go": proceed.
```

**Cross-Stage Validation (Stage 1):**
- [ ] Problem statement in FEASIBILITY.md matches the clean problem statement from Idea Intake. If they diverge, reconcile explicitly.
- [ ] Kill criteria are stricter than or equal to the intake candidates. They must not be softened without a decision log entry.
- [ ] Success metric in the inputs block is consistent with the feasibility recommendation.

**Output:** `FEASIBILITY.md`, `DECISION_LOG.md` entry.

---

### Stage 2: Research

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 1 → Stage 2).
**Inputs:** Inputs block + `FEASIBILITY.md`.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 9.

```
Steps:
1. Run the research prompt with inputs block and feasibility outcome as context.
2. Produce RESEARCH_SUMMARY.md with all required sections.
3. End with the decisions table showing confidence levels.
4. Any low-confidence decision must be flagged for spike or explicit approval.
```

**Cross-Stage Validation (Stage 2):**
- [ ] No research finding contradicts a feasibility assumption without being flagged.
- [ ] No technology recommendation contradicts a known constraint from the inputs block.
- [ ] If research reveals a competitor that fully solves the stated problem, re-evaluate FEASIBILITY.md kill criteria before proceeding.
- [ ] Low-confidence decisions are recorded in DECISION_LOG.md, not buried in the research summary.

**Output:** `RESEARCH_SUMMARY.md`, `DECISION_LOG.md` entries for low-confidence decisions.

---

### Stage 3: Requirements And UX

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 2 → Stage 3).
**Inputs:** Inputs block + `FEASIBILITY.md` + `RESEARCH_SUMMARY.md`.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 10.

```
Steps:
1. Run the requirements prompt with all prior context.
2. Produce REQUIREMENTS.md with requirement IDs (FR-001, NFR-001, etc.).
3. Produce USER_FLOWS.md with step-by-step journeys.
4. Every P0 requirement must trace to the core problem in FEASIBILITY.md.
5. Every requirement must have measurable acceptance criteria.
```

**Cross-Stage Validation (Stage 3):**
- [ ] Every P0 requirement traces to the core problem stated in FEASIBILITY.md. If a P0 requirement does not connect to the original problem, challenge it: is this scope creep?
- [ ] No requirement contradicts the out-of-scope list from the inputs block. If it does, either update OUT_OF_SCOPE with a decision log entry or remove the requirement.
- [ ] The success metric from the inputs block is achievable by the P0 requirements alone. If P0 is not sufficient to hit the metric, either the metric or the priorities are wrong.
- [ ] User flows reference users identified in the inputs block, not new personas invented during requirements.
- [ ] Every requirement with "should" or "nice to have" language is P1 or P2, never P0.

**Output:** `REQUIREMENTS.md`, `USER_FLOWS.md`.

---

### Stage 4: Architecture And Risk Spikes

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 3 → Stage 4).
**Inputs:** Inputs block + `REQUIREMENTS.md` + `USER_FLOWS.md` + `RESEARCH_SUMMARY.md`.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 11.

```
Steps:
1. Run the architecture prompt, adapting to PRODUCT_SHAPE.
2. Produce ARCHITECTURE.md with all required sections.
3. Produce RISK_SPIKES.md with top 3–5 unknowns.
4. Run spikes for any unknown rated medium or high impact.
5. Record spike outcomes and decisions.
```

**Cross-Stage Validation (Stage 4):**
- [ ] Every API contract or system boundary in ARCHITECTURE.md serves at least one requirement from REQUIREMENTS.md. Orphan contracts (no requirement) are either scope creep or missing requirements — resolve which.
- [ ] The auth model handles every user role mentioned in USER_FLOWS.md. No role is unaddressed.
- [ ] Technology choices in ARCHITECTURE.md are consistent with the research confidence levels in RESEARCH_SUMMARY.md. A low-confidence technology choice from research that became a committed architecture decision needs a spike or decision log entry.
- [ ] No constraint from the inputs block (KNOWN_CONSTRAINTS, COMPLIANCE_OR_SECURITY_NEEDS) is violated by the architecture.
- [ ] Risk spikes cover the mandatory spike candidates from PROGRAMBUILD.md (auth, streaming, integrations, AI cost, file handling) where applicable.
- [ ] Run `programstart research --status` — any KB research tracks covering chosen technologies must be current. If a track is overdue, run the research delta before committing the architecture.
- [ ] Check the KB for `supersedes_for_new_work` relationships affecting any technology in ARCHITECTURE.md. If a chosen technology has been superseded, record the decision to proceed or switch in DECISION_LOG.md.

**Output:** `ARCHITECTURE.md`, `RISK_SPIKES.md`, `DECISION_LOG.md` entries.

---

### Stage 5: Scaffold And Guardrails

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 4 → Stage 5).
**Inputs:** `ARCHITECTURE.md` + `USER_FLOWS.md`.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 12.

```
Steps:
1. Create the project scaffold adapted to PRODUCT_SHAPE.
2. Implement the contract layer (routes, endpoints, commands, jobs, or public API).
3. Implement the boundary control (auth-aware client, trusted caller, or operator helper).
4. Add structural tests.
5. Create CI with explicit timeouts.
6. Verify all structural tests pass.
```

**Cross-Stage Validation (Stage 5):**
- [ ] Every contract in the scaffold traces to a contract defined in ARCHITECTURE.md. No extra contracts were invented during scaffolding.
- [ ] Structural tests cover alignment, reverse alignment, auth discipline, and no-hardcoded-identifier rules from PROGRAMBUILD.md.
- [ ] The scaffold does not implement product features. If any business logic exists, it was added prematurely.

**Output:** Working skeleton, CI gates, all structural tests green.

---

### Stage 6: Test Strategy

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 5 → Stage 6).
**Inputs:** `REQUIREMENTS.md` + `USER_FLOWS.md` + `ARCHITECTURE.md`.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 13.

```
Steps:
1. Run the test strategy prompt adapted to PRODUCT_SHAPE.
2. Produce TEST_STRATEGY.md with all required sections.
3. Use the purpose test definition and litmus test from the Purpose And Auth Test Rules section.
4. Fill the requirements traceability matrix: every P0 requirement must have at least one planned purpose test.
5. Fill the endpoint-to-test registry for all contracts from ARCHITECTURE.md.
```

**Cross-Stage Validation (Stage 6):**
- [ ] Every P0 requirement in REQUIREMENTS.md appears in the requirements traceability matrix with at least one purpose test planned.
- [ ] Every contract from ARCHITECTURE.md appears in the endpoint-to-test registry.
- [ ] The test strategy does not plan browser E2E for a PRODUCT_SHAPE that has no browser. Adapt layers to shape.
- [ ] The purpose test litmus is applied: every planned test answers "yes" to "if this fails, does a real user lose a real capability?"

**Output:** `TEST_STRATEGY.md` with filled matrices.

---

### Stage 7: Implementation Loop

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 6 → Stage 7).
**Inputs:** Feature user story + relevant `ARCHITECTURE.md` contracts + relevant `USER_FLOWS.md` flow + relevant `TEST_STRATEGY.md` entries.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 14.

```
For each feature:
1. Write purpose tests first. Each must reference a requirement ID.
2. Apply the purpose test litmus: "If this fails, does a real user lose a real capability?"
   If No → reclassify or delete.
3. Write auth tests (positive and negative).
4. Implement the feature following the implementation loop.
5. Re-run structural tests after every feature.
6. Update the endpoint-to-test registry.
7. Update DECISION_LOG.md if any design changed.

Mid-Implementation Challenge Gate (run every 3–5 features or weekly):
- Re-read kill criteria. Any now true?
- Has scope crept? Any features not in REQUIREMENTS.md?
- Are deferred items still tracked?
- Has any assumption weakened?
- Check DECISION_LOG.md for unreconciled reversals.
- Run Part G (Dependency Health) if more than 2 weeks since last check.
```

**Output:** Working features with purpose tests, updated registries.

---

### Stage 8: Release Readiness

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 7 → Stage 8).
**Inputs:** `ARCHITECTURE.md` + `TEST_STRATEGY.md` + implementation status.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 15.

```
Steps:
1. Produce RELEASE_READINESS.md with all required sections.
2. Verify minimum gate: deployment validated, rollback validated, secrets verified, smoke tests pass, monitoring active.
3. Record go/no-go recommendation.
```

**Cross-Stage Validation (Stage 8):**
- [ ] Every P0 requirement from REQUIREMENTS.md is implemented, tested, and passing. Any gap is a launch blocker.
- [ ] The rollback plan references the actual deployment artifacts from the scaffold, not hypothetical procedures.
- [ ] Monitoring covers the SLOs/SLIs defined in ARCHITECTURE.md. No "we'll add monitoring later."
- [ ] Kill criteria from FEASIBILITY.md are re-checked one final time. Any that are now true block release.
- [ ] All decisions in DECISION_LOG.md with status ACTIVE are still valid. No unreconciled reversals remain.
- [ ] Run Part G (Dependency Health) from the Challenge Gate. No deprecated, superseded, or abandoned dependencies remain unaddressed.

**Output:** `RELEASE_READINESS.md`, go/no-go decision.

---

### Stage 9: Audit And Drift Control

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 8 → Stage 9).
**Inputs:** Full codebase + all prior outputs.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 16.

```
Steps:
1. Run the audit prompt.
2. Produce AUDIT_REPORT.md with severity, category, evidence, impact, fix, and prevention.
3. All critical and high findings must have owners.
```

**Cross-Stage Validation (Stage 9):**
- [ ] Every finding traces to a specific contract, rule, or requirement violation — not to a stylistic preference.
- [ ] Audit findings are compared against the challenge gate logs from all previous transitions. Were any ⚠️ warnings from earlier gates realized as actual problems?
- [ ] If the audit reveals drift that the challenge gates should have caught, record a process improvement note.

**Output:** `AUDIT_REPORT.md`, owner assignments.

---

### Stage 10: Post-Launch Review

**Challenge Gate:** Run `PROGRAMBUILD_CHALLENGE_GATE.md` (Stage 9 → Stage 10).
**Inputs:** Success metric + release decision + audit findings + production signals.
**Prompt:** Use the prompt template from `PROGRAMBUILD.md` Section 17.

```
Steps:
1. Produce POST_LAUNCH_REVIEW.md.
2. Compare actual metrics to the success metric from the inputs block.
3. Record lessons learned.
4. Assign follow-up owners.
5. Run the Template Improvement Review (see below).
```

**Cross-Stage Validation (Stage 10):**
- [ ] The success metric comparison uses the exact metric from the inputs block, not a reframed version.
- [ ] Kill criteria from FEASIBILITY.md are reviewed one last time: were any of them correct predictions?
- [ ] Lessons learned are actionable and have owners — not generic platitudes.
- [ ] Any challenge gate ⚠️ that was accepted earlier is reviewed: did the risk materialize?
- [ ] Decision reversals in DECISION_LOG.md are reviewed: were the reversals correct? Would earlier detection have saved work?

**Template Improvement Review:**

After lessons learned are captured, check whether any lesson is *systemic* — meaning it would apply to future projects using this template, not just this specific project.

For each systemic lesson, propose a specific update to one of these PROGRAMBUILD assets:

| Lesson Type | Update Target | Example |
|---|---|---|
| A failure pattern that the Idea Intake should have caught | `PROGRAMBUILD_IDEA_INTAKE.md` — add a new red flag | "We built for a user segment that doesn't exist" → add a red flag for unvalidated user assumptions |
| A risk that the Challenge Gate should have flagged | `PROGRAMBUILD_CHALLENGE_GATE.md` — add a new question to the relevant part | "A dependency was deprecated mid-build" → already covered by Part G, but if Part G missed it, strengthen the check |
| A kill criterion pattern that appears across projects | `FEASIBILITY.md` template — add a suggested kill criterion category | "Third-party API cost exceeded 3x estimate" → add cost blowout as a standard kill criterion candidate |
| A test gap that purpose tests should have prevented | `TEST_STRATEGY.md` — add a new rule or anti-pattern | "Auth bypass was not caught because the test only checked the happy path" → strengthen auth test enforcement |
| A new mandatory spike candidate | `PROGRAMBUILD.md` Stage 4 mandatory spike list | "Webhook delivery reliability was assumed, not tested" → add webhook reliability as a spike candidate |
| A stage that consistently produces low-quality output | `PROGRAMBUILD_GAMEPLAN.md` — strengthen the cross-stage validation for that stage | "Architecture docs said X but implementation did Y" → add a tighter validation check |
| A KB gap that caused a bad technology decision | `config/knowledge-base.json` — add or update the relevant entry, relation, or coverage domain | "Chose a framework the KB didn't cover; it turned out to be unmaintained" → add the framework or mark the coverage domain |

**Template Improvement Log:**

| Lesson | Systemic? | Proposed Update | Target File | Applied? |
|---|---|---|---|---|
| | Yes / No | | | Yes / No / Deferred |

**Rule:** If 3+ projects produce the same systemic lesson, the template update is mandatory, not optional. Repeated lessons that never become template improvements are a system failure.

**Output:** `POST_LAUNCH_REVIEW.md`, follow-up assignments, template improvement proposals.

---

## Cross-Stage Validation Summary

This table shows which validations run at each stage and what they check:

| Stage | Validates Against | Contradiction Being Caught |
|---|---|---|
| 1 (Feasibility) | Idea Intake | Problem drift between intake and feasibility |
| 2 (Research) | Feasibility, Inputs | Research contradicting assumptions or constraints |
| 3 (Requirements) | Feasibility, Inputs, Out-of-scope | Scope creep, phantom requirements, metric mismatch |
| 4 (Architecture) | Requirements, Research, Inputs | Orphan contracts, auth gaps, constraint violations |
| 5 (Scaffold) | Architecture | Premature features, untracked contracts |
| 6 (Test Strategy) | Requirements, Architecture | Untested P0s, shape-inappropriate tests, theatre tests |
| 7 (Implementation) | Requirements, Kill criteria | Scope creep, stale kill criteria, untracked features |
| 8 (Release) | Requirements, Feasibility, Architecture | Unimplemented P0s, missing monitoring, stale kill criteria |
| 9 (Audit) | All prior outputs, Challenge gate logs | Drift the gates should have caught |
| 10 (Post-Launch) | Inputs (success metric), Feasibility (kill criteria), Decision log (reversals), Template history | Outcome vs. promise, prediction accuracy, systemic lesson capture |

---

## Variant Adjustments

| Variant | Gameplan Rigor |
|---|---|
| Lite | Run all steps. Cross-stage validations can be shortened to pass/fail notes. Challenge gates require Parts A, C, and F minimum. |
| Product | Run all steps with full cross-stage validation checklists. Challenge gates require all seven parts. Part G required at Stages 4+. |
| Enterprise | Run all steps with full cross-stage validation. Challenge gate results require approver sign-off. Cross-stage validation evidence is retained. Part G required at all stages. |

---
