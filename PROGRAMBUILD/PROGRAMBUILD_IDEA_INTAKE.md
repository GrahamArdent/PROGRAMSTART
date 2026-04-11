# PROGRAMBUILD_IDEA_INTAKE.md

# Idea Intake Protocol

Purpose: Decompose a raw idea into a structured problem statement before the inputs block is filled.
Owner: Product Lead
Last updated: 2026-03-31
Depends on: none — this is the first step
Authority: Canonical for idea decomposition and pre-feasibility challenge

This protocol runs before Stage 0 (Inputs). Its job is to force clarity about the problem before anyone names a solution, picks a stack, or writes an inputs block.

---

## Why This Exists

Most failed products were not killed by bad engineering. They were killed by building the wrong thing, for the wrong person, with the wrong assumptions — and nobody asked the hard questions early enough.

The inputs block in `PROGRAMBUILD.md` asks *what* you are building. This protocol asks *whether you should*.

---

## When To Use

- Every new idea, before filling the inputs block.
- When someone says "I want to build X" and X is a solution, not a problem.
- When the motivation is a technology ("I want to use Y") rather than a user pain.
- When revisiting a shelved idea to decide if conditions have changed.

---

## The Interview

Answer these in order. Do not skip. Do not combine. Each question is designed to challenge a specific failure pattern.

### 1. State The Problem Without Naming Your Solution

> Describe what is broken, painful, or missing — without mentioning your product idea, proposed technology, or any feature.

Failure pattern this catches: **solution-first thinking.** If you cannot describe the problem without your solution, the problem may not exist independently.

```text
PROBLEM_RAW:
```

### 2. Name The Person Who Has This Problem

> Identify a real person, role, or job title. Not "users" or "everyone." If you cannot name a specific person or role, the problem may be hypothetical.

Failure pattern this catches: **phantom users.** Building for an abstraction guarantees you satisfy nobody.

```text
WHO_HAS_THIS_PROBLEM:
WHY_DO_YOU_KNOW_THEY_HAVE_IT:
```

### 3. How Do They Solve It Today

> Describe their current workaround, tool, process, or coping mechanism. Every real problem has a current solution — even if it is manual, expensive, or ignored.

Failure pattern this catches: **no-alternative delusion.** If they have no workaround, they may not care enough to adopt yours either.

```text
CURRENT_SOLUTION:
COST_OF_CURRENT_SOLUTION:
```

### 4. What Would Solved Look Like — Measurably

> Define the outcome, not features. What metric changes? What time is saved? What error rate drops? What capability exists that did not before?

Failure pattern this catches: **feature lists disguised as success criteria.** "We shipped the dashboard" is not success. "Support tickets dropped 40%" is.

```text
SUCCESS_OUTCOME:
HOW_YOU_WOULD_MEASURE_IT:
```

### 5. What Are You Explicitly Not Building

> Name at least three things that are adjacent, tempting, or frequently requested — that you will not build. If you cannot name exclusions, your scope is unbounded.

Failure pattern this catches: **scope creep by omission.** Undefined boundaries expand silently.

```text
NOT_BUILDING_1:
NOT_BUILDING_2:
NOT_BUILDING_3:
```

### 6. What Would Make You Stop

> Name the specific evidence that would cause you to kill, pause, or substantially redirect this project. These must be observable and falsifiable — not feelings.

Failure pattern this catches: **sunk-cost continuation.** Without pre-committed kill criteria, bad projects survive on momentum.

```text
KILL_SIGNAL_1:
KILL_SIGNAL_2:
KILL_SIGNAL_3:
```

### 7. What Is The Cheapest Way To Test Whether This Problem Is Real

> Before building anything: what is the smallest experiment, conversation, prototype, or data check that would increase or decrease your confidence that this problem is worth solving?

Failure pattern this catches: **building before validating.** The most expensive validation is a shipped product nobody uses.

```text
CHEAPEST_VALIDATION:
EXPECTED_SIGNAL:
TIME_TO_RESULT:
```

---

## Challenge Review

After completing the interview, review the answers against these red flags:

| Red Flag | What It Means |
|---|---|
| Problem statement mentions a technology or feature | You described a solution, not a problem. Rewrite it. |
| "Users" or "everyone" is the target | You have not identified your actual user. Get specific. |
| No current workaround exists | Either the problem is not painful enough or you have not researched it. |
| Success metric is a feature shipped, not an outcome changed | You are measuring output, not impact. Reframe it. |
| Cannot name 3 exclusions | Your scope is undefined. Define it before proceeding. |
| Kill criteria are vague or emotional | "If it feels wrong" is not a kill criterion. Make them observable. |
| Cheapest validation is "build it and see" | You have skipped the cheapest learning. Find a smaller experiment. |

---

## Output

After the interview and challenge review, produce:

1. A clean one-paragraph problem statement (no solution language).
2. A candidate `SUCCESS_METRIC` for the inputs block.
3. A candidate `OUT_OF_SCOPE` list for the inputs block.
4. Kill criteria ready for `FEASIBILITY.md`.
5. A validation experiment recommendation.
6. A go / investigate / stop recommendation.

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

If the recommendation is "go" or "investigate," proceed to Stage 0 (Inputs) and Stage 1 (Feasibility).
If the recommendation is "stop," record why in `DECISION_LOG.md` and do not start the inputs block.

---

## Prompt Template

Use this prompt when running the Idea Intake Protocol with an AI agent:

```text
Act as a critical product advisor. Your job is to stress-test this idea before any planning begins.

Run the Idea Intake Protocol from PROGRAMBUILD_IDEA_INTAKE.md.
For each of the 7 questions:
1. Ask the question.
2. Wait for the answer.
3. Challenge weak, vague, or solution-first answers explicitly. Do not accept "users" as a target, features as success metrics, or "build it and see" as validation.
4. If an answer has a red flag, name the red flag and ask for a rewrite.

After all 7 questions are answered satisfactorily:
- Produce the structured output (problem statement, success metric, exclusions, kill criteria, validation experiment, recommendation).
- If the answers reveal the idea is not ready, say so clearly and recommend investigation or stopping.

Do not be polite at the expense of honesty. A killed idea at this stage costs nothing. A killed product at Stage 7 costs everything.
```

---
