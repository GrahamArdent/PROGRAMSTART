# PROGRAMBUILD_IDEA_INTAKE.md

# Idea Intake Protocol

Purpose: Decompose a raw idea, research-backed opportunity, or existing-project change into a structured problem statement before the inputs block is filled or a planning delta is proposed.
Owner: Product Lead
Last updated: 2026-08-26
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` for entry-mode, authority, adaptive decision/evidence routing, evidence-reuse, and existing-project rules
Authority: Canonical for idea decomposition and pre-feasibility challenge

This protocol normally runs before Stage 0 (Inputs). Its job is to force clarity about the problem before anyone names a solution, picks a stack, or writes an inputs block. For an existing project, it can instead run as a delta-oriented challenge against the project's current authority.

---

## Why This Exists

Most failed products were not killed by bad engineering. They were killed by building the wrong thing, for the wrong person, with the wrong assumptions — and nobody asked the hard questions early enough.

The inputs block in `PROGRAMBUILD.md` asks *what* you are building. This protocol asks *whether you should*.

It must also avoid a different failure: re-asking questions that have already been answered by trustworthy research or an existing project's canonical state. The goal is disciplined challenge, not repetitive ceremony.

---

## Entry Mode

Select the entry mode from `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` before running the interview.

### Mode A — Raw Idea

Use when little reliable planning or evidence exists.

- answer all 8 questions directly
- challenge every red flag
- produce a fresh structured intake output

### Mode B — Research-Backed Project

Use when substantial research already exists but the project has not yet been converted into a durable execution structure.

- use the research to prefill answers where the evidence is clear
- cite or name the evidence used for each prefilled answer
- ask only for missing, ambiguous, stale, or contradictory information
- still challenge all 8 dimensions before proceeding
- treat the research as evidence, not as the execution plan

### Mode C — Existing / In-Flight Project

Use when the work applies to an existing repository, product, or program with current plans and implementation state.

Before running the challenge:

1. identify the project's current canonical authority or execution spine;
2. inspect the current state needed to evaluate the proposed change;
3. reuse still-valid research and verification evidence;
4. apply the 8 questions as a **delta audit** against the proposed change;
5. route only genuinely unresolved decision-relevant uncertainty through additional scrutiny;
6. produce recommendations for the existing plan rather than creating a competing master plan;
7. return to the existing project's next executable slice once the delta is resolved.

If the project already has a clear problem statement, target user, success metric, scope boundary, and kill/stop criteria, do not ask the operator to restate them unless new evidence creates a conflict.

Mode C does not restart at Stage 0 merely because this intake or a research delta was run.

---

## When To Use

- Every genuinely new idea, before filling the inputs block.
- When someone says "I want to build X" and X is a solution, not a problem.
- When the motivation is a technology ("I want to use Y") rather than a user pain.
- When revisiting a shelved idea to decide if conditions have changed.
- When a research document needs to be converted into an executable project structure.
- When new research or a proposed enhancement needs to be evaluated against an existing project's current plan.

---

## The Interview

Challenge these dimensions in order. In Mode A, ask each question. In Modes B and C, prefill from trustworthy evidence and ask only where evidence is missing, stale, ambiguous, or contradictory.

### 1. State The Problem Without Naming Your Solution

> Describe what is broken, painful, or missing — without mentioning your product idea, proposed technology, or any feature.

Failure pattern this catches: **solution-first thinking.** If you cannot describe the problem without your solution, the problem may not exist independently.

```text
PROBLEM_RAW:
EVIDENCE_USED:
```

### 2. Name The Person Who Has This Problem

> Identify a real person, role, or job title. Not "users" or "everyone." If you cannot name a specific person or role, the problem may be hypothetical.

Failure pattern this catches: **phantom users.** Building for an abstraction guarantees you satisfy nobody.

```text
WHO_HAS_THIS_PROBLEM:
WHY_DO_YOU_KNOW_THEY_HAVE_IT:
EVIDENCE_USED:
```

### 3. How Do They Solve It Today

> Describe their current workaround, tool, process, or coping mechanism. Every real problem has a current solution — even if it is manual, expensive, or ignored.

Failure pattern this catches: **no-alternative delusion.** If they have no workaround, they may not care enough to adopt yours either.

```text
CURRENT_SOLUTION:
COST_OF_CURRENT_SOLUTION:
EVIDENCE_USED:
```

### 4. What Would Solved Look Like — Measurably

> Define the outcome, not features. What metric changes? What time is saved? What error rate drops? What capability exists that did not before?

Failure pattern this catches: **feature lists disguised as success criteria.** "We shipped the dashboard" is not success. "Support tickets dropped 40%" is.

```text
SUCCESS_OUTCOME:
HOW_YOU_WOULD_MEASURE_IT:
EVIDENCE_USED:
```

### 5. What Are You Explicitly Not Building

> Name at least three things that are adjacent, tempting, or frequently requested — that you will not build. If you cannot name exclusions, your scope is unbounded.

Failure pattern this catches: **scope creep by omission.** Undefined boundaries expand silently.

```text
NOT_BUILDING_1:
NOT_BUILDING_2:
NOT_BUILDING_3:
EVIDENCE_USED:
```

### 6. What Would Make You Stop

> Name the specific evidence that would cause you to kill, pause, or substantially redirect this project. These must be observable and falsifiable — not feelings.

Failure pattern this catches: **sunk-cost continuation.** Without pre-committed kill criteria, bad projects survive on momentum.

For an existing project, these may be change-specific stop/escalation conditions rather than reasons to kill the entire product.

```text
KILL_SIGNAL_1:
KILL_SIGNAL_2:
KILL_SIGNAL_3:
EVIDENCE_USED:
```

### 7. What Is The Cheapest Way To Test Whether This Problem Is Real

> Before building anything: what is the smallest experiment, conversation, prototype, or data check that would increase or decrease your confidence that this problem is worth solving?

Failure pattern this catches: **building before validating.** The most expensive validation is a shipped product nobody uses.

For Mode C, first ask whether valid evidence already proves this. If yes, reuse it unless an invalidation trigger exists.

If the remaining uncertainty could materially change the next decision, apply the adaptive decision/evidence routing rules from `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`. Research is `none`, `targeted`, or `deep`; do not broaden research until the protected decision, missing evidence, consequence, minimum evidence, and stop condition are clear.

```text
CHEAPEST_VALIDATION:
EXPECTED_SIGNAL:
TIME_TO_RESULT:
EXISTING_EVIDENCE_REUSABLE: [yes | no | partial]
```

### 8. Will End Users Or Operators Need A Visual Interface

> Will end users or operators interact with this system through a visual interface (web dashboard, admin panel, configuration UI)? If yes, describe the audience and their primary tasks.

Failure pattern this catches: **invisible UI assumption.** Backend-first projects often discover late that operators or end users need a dashboard, admin panel, or status page — adding unplanned frontend work.

```text
NEEDS_UI:                 [yes | no | undecided]
UI_AUDIENCE:
UI_PRIMARY_TASKS:
EVIDENCE_USED:
```

---

## Challenge Review

After completing or validating the interview dimensions, review the answers against these red flags:

| Red Flag | What It Means |
|---|---|
| Problem statement mentions a technology or feature | You described a solution, not a problem. Rewrite it. |
| "Users" or "everyone" is the target | You have not identified your actual user. Get specific. |
| No current workaround exists | Either the problem is not painful enough or you have not researched it. |
| Success metric is a feature shipped, not an outcome changed | You are measuring output, not impact. Reframe it. |
| Cannot name 3 exclusions | Your scope is undefined. Define it before proceeding. |
| Kill/stop criteria are vague or emotional | "If it feels wrong" is not a criterion. Make them observable. |
| Cheapest validation is "build it and see" | You have skipped the cheapest learning. Find a smaller experiment. |
| UI need is "undecided" but product shape implies users interact directly | Clarify before architecture. Late UI discovery causes rework. |
| Existing evidence is being re-collected without an invalidation trigger | You are spending verification effort without reducing uncertainty. Reuse the evidence or state why it is stale. |
| Research is broad but the decision it protects or stop condition is undefined | Bound the research around the next decision before gathering more knowledge. |
| Existing project already has an execution spine but this intake creates a new master plan | Convert the result into delta recommendations for the existing authority instead. |

---

## Output

### Mode A or Mode B output

Produce:

1. `ENTRY_MODE` and the material evidence used.
2. A clean one-paragraph problem statement (no solution language).
3. A candidate `SUCCESS_METRIC` for the inputs block.
4. A candidate `OUT_OF_SCOPE` list for the inputs block.
5. Kill criteria ready for `FEASIBILITY.md`.
6. A validation experiment recommendation, noting any reusable existing evidence and research depth if further evidence is actually warranted.
7. A go / investigate / stop recommendation.

Then run `programstart recommend` to get KB-backed variant and stack guidance:

```bash
programstart recommend --product-shape "<your PRODUCT_SHAPE>" --need <need1> --need <need2>
```

The tool maps your product shape and stated needs against the KB (80+ stacks, 11 coverage domains, 11 decision rules) and returns:
- recommended variant (Lite / Product / Enterprise)
- recommended stack profile
- coverage warnings for domains with known gaps
- actionable next commands

Use the output to validate or challenge your variant choice and stack assumptions before filling the inputs block. If the tool's variant recommendation disagrees with your initial assumption, treat that as a signal worth investigating — not a mechanical override.

If the recommendation is "go" or "investigate," proceed through the current lifecycle only as far as the evidence warrants; use the adaptive routing rules before opening broad research.
If the recommendation is "stop," record why in `DECISION_LOG.md` and do not start the inputs block.

### Mode C output

Produce:

1. `ENTRY_MODE: existing_project`.
2. The canonical project authority/execution spine that was found.
3. Existing evidence reused and any invalidation triggers found.
4. The proposed change or research finding being evaluated.
5. Confirmed alignment with the existing problem, user, success metric, and scope — or explicit conflicts.
6. Specific decision deltas, risks, verification implications, and adaptive check families actually activated.
7. Specific recommended edits to the existing execution spine or canonical project artifacts.
8. A proceed / investigate / stop-or-escalate recommendation for the proposed change.
9. The existing project's next executable slice to return to after any bounded investigation.

Do **not** create a new master game plan as the default Mode C output.

---

## Prompt Template

Use this prompt when running the Idea Intake Protocol with an AI agent:

```text
Act as a critical product advisor. Your job is to stress-test this idea, research-backed project, or existing-project change before execution planning proceeds.

Read PROGRAMBUILD_PLANNING_OPERATING_MODEL.md and select the correct entry mode:
- Mode A: raw idea
- Mode B: research-backed project
- Mode C: existing/in-flight project

Run the 8 challenge dimensions from PROGRAMBUILD_IDEA_INTAKE.md.

For Mode A:
1. Ask each of the 8 questions.
2. Wait for the answer.
3. Challenge weak, vague, or solution-first answers explicitly.

For Modes B and C:
1. First use trustworthy existing research and project authority to prefill any dimensions already answered.
2. Do not ask the operator to repeat valid information without an invalidation reason.
3. Ask only about gaps, stale evidence, ambiguity, or contradictions.
4. Still challenge all 8 dimensions before concluding.

For every mode:
- Do not accept "users" as a target, features as success metrics, or "build it and see" as validation.
- If an answer has a red flag, name the red flag and resolve it.
- Distinguish evidence from execution authority.
- If material uncertainty could change the next decision, route it to no/targeted/deep research using the adaptive decision rules; do not research for completeness.
- If Mode C already has a master plan or other execution spine, produce delta recommendations and proposed edits to that authority rather than creating a competing plan.
- If Mode C investigates a delta, return to the existing execution spine rather than restarting Stage 0.

After all 8 dimensions are satisfactory, produce the output defined for the selected mode.

Do not be polite at the expense of accuracy. A killed idea at this stage costs little; an unnecessary research or re-verification cycle also costs real time.
```

---
