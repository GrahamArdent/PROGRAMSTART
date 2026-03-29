# Reusable Patterns

This page captures the design and delivery patterns that should transfer between PROGRAMSTART and the programs it helps create.

The goal is not to copy the entire platform into every generated repo. The goal is to reuse the parts that reduce ambiguity, drift, and low-signal process overhead.

## Patterns Worth Reusing In Built Programs

### 1. Machine-Readable Workflow Registry

PROGRAMSTART keeps workflow structure in a machine-readable registry and then uses scripts, validation, and UI surfaces against that same source.

Portable lesson:

- keep critical workflow structure, allowed variants, required files, and sync rules in data rather than spreading them across prose only

Good fit in built programs:

- release gates
- environment readiness checks
- migration checklists
- operational runbook validation

### 2. Authority File And Dependent File Discipline

PROGRAMSTART separates canonical owner files from dependent summaries and then checks drift.

Portable lesson:

- decide which document or config owns each concern before implementation multiplies interpretations

Good fit in built programs:

- API contract ownership
- auth and consent behavior ownership
- architecture versus test-strategy dependency rules

### 3. Route And State Freeze Before UI Expansion

USERJOURNEY freezes route/state semantics before code planning expands.

Portable lesson:

- define entry conditions, resume rules, skip-state meaning, and activation handoff before building screens around them

Good fit in built programs:

- onboarding flows
- billing and trial conversion flows
- enterprise provisioning flows
- multi-step setup wizards

### 4. Activation As A Measured Milestone

PROGRAMSTART treats activation as a defined event, not as vague user progress.

Portable lesson:

- define the first value event explicitly and align product, routing, analytics, and tests around it

Good fit in built programs:

- first-run experiences
- trial-to-value journeys
- AI-assisted feature adoption

### 5. Purpose-Based Browser Goldens

The platform uses browser smoke plus focused goldens on stable UI regions instead of brittle full-page capture as the only signal.

Portable lesson:

- verify the important contract, not every incidental pixel

Good fit in built programs:

- first-run dashboards
- signoff or approval dialogs
- billing confirmation states
- admin-control panels

### 6. Bootstrap And Validate The Produced Artifact

PROGRAMSTART validates both the template repo and a freshly bootstrapped repo.

Portable lesson:

- test the emitted artifact, not just the source template or generator

Good fit in built programs:

- project generators
- scaffolding tools
- migration helpers
- installer flows

### 7. Thin Operator Surface Over Safe Commands

The local dashboard does not expose arbitrary shell access. It wraps a strict command allowlist.

Portable lesson:

- operational tooling should prefer constrained actions over generic remote execution

Good fit in built programs:

- internal admin dashboards
- support consoles
- self-serve maintenance actions

## Patterns Built Programs Can Feed Back Into PROGRAMSTART

### 1. Real Route Edge Cases

Generated programs can reveal where route/state planning is still too abstract.

Examples:

- callback failure recovery
- consent-version re-prompting
- partial activation after imported data quality issues

Those findings should feed back into route/state authority docs, not just implementation notes.

### 2. Better Activation Definitions

Different products will prove which activation milestones are measurable and defensible.

That can improve how PROGRAMSTART asks kickoff questions for interactive products.

### 3. Better Operator UX Patterns

Real products often build clearer state recovery, audit, and approval experiences than internal tooling starts with.

Those UI patterns can feed back into the PROGRAMSTART dashboard without changing the underlying workflow model.

### 4. Tighter Verification Contracts

Built programs can reveal where smoke tests, artifact capture, or golden tolerance need better defaults.

That feedback should improve the platform's own verification stack.

## What Not To Copy Blindly

These platform traits are useful here but should not be inherited by every built program without a reason:

- the full planning document volume
- the local dashboard's exact HTTP surface
- the repo-specific workflow state format
- the entire USERJOURNEY package as a default attachment

The reusable asset is the pattern, not the exact file tree.

## Recommended Adoption Order

For most generated programs, the highest-value reuse order is:

1. authority ownership and drift discipline
2. route/state freeze for any user lifecycle work
3. explicit activation milestone and analytics alignment
4. bootstrap-or-install smoke verification
5. purpose-based browser goldens where UI state matters
