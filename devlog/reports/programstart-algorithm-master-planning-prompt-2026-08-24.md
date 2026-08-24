# PROGRAMSTART Algorithm Master Planning / Execution Prompt — 2026-08-24

Status: Reusable launcher / orchestration prompt. **This file is not a game plan, does not replace PROGRAMBUILD authority, and must never become a competing execution spine.**

Use this prompt to continue the PROGRAMSTART algorithm-integration work in a fresh ChatGPT/Codex session.

---

## PROMPT START

Continue the PROGRAMSTART / PROGRAMBUILD planning-and-algorithm improvement work.

Repository:

`GrahamArdent/PROGRAMSTART`

Use the connected GitHub tooling to inspect the repository and verify current state **before making substantive decisions or changes**.

Do not rely solely on this handoff. Repository state, current PRs, current `main`, PROGRAMBUILD authority files, tests, and live validation evidence are authoritative.

## 1. Authority and planning hierarchy

Do **not** create another Master Game Plan, algorithm game plan, roadmap, or parallel execution spine.

PROGRAMBUILD remains the methodology authority. Individual projects created or managed by PROGRAMSTART retain their own project-specific execution authority.

Before implementation, locate and follow the current versions of at least:

- `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md`
- `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md`
- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`
- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`
- `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`
- `PROGRAMBUILD/DECISION_LOG.md`
- `docs/decisions/0023-use-one-strategic-execution-spine-with-bounded-work-packets.md`
- `.github/copilot-instructions.md`
- `.github/instructions/source-of-truth.instructions.md`
- any applicable repository-level agent/instruction files that exist at execution time.

Also inspect the algorithm audit on branch:

`analysis/programstart-algorithm-integration`

File:

`devlog/reports/programstart-algorithm-integration-audit-2026-08-24.md`

Treat that audit as **subordinate evidence only**. It may be stale relative to `main`; reconcile it against current code before acting on any recommendation.

## 2. Current checkpoint to verify

The following was true when this prompt was written, but must be re-verified:

- PR #38 merged the bounded PROGRAMBUILD planning operating model into `main` as commit `f01d4a5978d8b4dce9afba3e099419eb6edd9484`.
- PR #40 had already repaired dormant workflow-template/bootstrap behavior while keeping PROGRAMSTART Actions inactive.
- PR #41 merged the first deterministic algorithm foundation into `main` as commit `9a10b5a785d44457defd43ba06e0138c889c34f6`.
- `scripts/programstart_graph.py` now provides deterministic dependency graph primitives.
- `scripts/programstart_evidence.py` now provides immutable evidence-invalidation primitives.
- Focused isolated execution of the exact new modules/tests produced `23 passed`, but a full repository checkout gate had not yet run in the execution environment.
- GitHub Actions for PROGRAMSTART were intentionally inactive. Do not reactivate recurring Actions merely to obtain validation unless repository policy and explicit user intent have changed.

Verify all of this against live GitHub before proceeding.

## 3. Core design principle

PROGRAMSTART should become **algorithmically precise before algorithmically sophisticated**.

Prefer this architecture:

> LLM/Reasoner interprets ambiguity or generates bounded candidates → deterministic algorithms enforce eligibility, dependencies, impact, evidence validity, verification coverage, budgets, and state transitions → the Reasoner is used only where meaningful ambiguity remains → outputs are observable, explainable, and validated.

Do not use an LLM for a mechanically checkable constraint.

Do not introduce advanced methods simply because they are available.

Keep reinforcement learning, bandits, MCTS, genetic/evolutionary algorithms, graph neural networks, solver-backed scheduling, self-changing weights, and agent swarms deferred unless real telemetry and a measured baseline demonstrate that simpler deterministic methods are inadequate.

Do not introduce a graph database merely because graph algorithms are being used. Prefer the existing relation model and ordinary deterministic data structures until scale or query requirements justify more infrastructure.

## 4. Execution method

Work in **bounded coherent slices**, not one giant algorithm rewrite.

For each slice:

1. inspect live `main` and current open PRs;
2. identify the actual next incomplete justified capability;
3. load only the authority and JIT context needed for that slice;
4. state objective, scope, non-goals, dependencies, acceptance criteria, verification, and invalidation conditions;
5. branch from current `main`;
6. implement the smallest coherent design that improves the system;
7. inspect every consumer of any shared contract you change;
8. add focused tests;
9. update bootstrap assets / coverage / changelog / registry / ADRs only when the repository's existing rules require it;
10. run targeted verification proportional to the touched surface;
11. widen to a convergence gate when the slice changes a shared contract, crosses a meaningful milestone, or is ready to merge;
12. perform a final diff/red-team audit;
13. merge via PR when justified, preferably squash for a coherent slice;
14. update evidence once and reference it rather than duplicating a diary across files;
15. determine the next slice from the new repository state rather than blindly following this prompt.

Do not re-run expensive checks merely because a new session began. Reuse valid evidence until an invalidating change occurs.

CI/full-suite verification is a convergence gate, not a heartbeat. During implementation, prefer targeted checks that cover the changed risk surface.

If full checkout execution is unavailable, do not claim it ran. Use the strongest available substitutes, such as isolated execution of exact changed modules/tests plus connected-repository contract inspection, and document the limitation explicitly.

## 5. Recommended remaining algorithm sequence

The sequence below is a **planning default**, not authority. Re-evaluate it against current `main` each time.

### Slice A — close any outstanding convergence evidence for graph/evidence core

First determine whether commit `9a10b5a...` has since received a full repository validation run.

If a complete checkout/runner is now available, run the appropriate current repository gates, especially the graph/evidence focused tests, Ruff, Pyright, bootstrap validation, and `programstart validate --check all` or the current equivalent.

If no material code changed since the isolated 23-test evidence and no runner is available, do not stall the project indefinitely. Record the remaining verification limitation and continue only where the next change has an independently bounded verification surface.

### Slice B — graph-based blast-radius integration into `programstart impact`

This is the preferred next implementation target unless live repository state shows a stronger prerequisite.

Inspect:

- `scripts/programstart_impact.py`
- `scripts/programstart_context.py`
- `scripts/programstart_graph.py`
- context-index relation models and tests
- command registry / CLI / JSON output contracts
- any dashboard or prompt consumers of impact output.

Goal:

Upgrade impact analysis from related-record discovery to **bounded, explainable dependency-path blast-radius analysis**.

Requirements:

- reuse existing `DependencyGraph`; do not duplicate graph logic;
- distinguish relation propagation semantics explicitly;
- execution dependencies default to `depends_on`;
- impact analysis may include `authority_dependency` when appropriate;
- do not traverse loose semantic relations as hard dependency edges unless a specific rule justifies it;
- support bounded traversal depth or another explicit risk boundary;
- preserve path provenance showing why an item is affected;
- keep existing impact output backward compatible where practical;
- expose machine-readable JSON for affected nodes, relation types, depth/path, and source/provenance;
- classify affected surfaces where current data supports it without inventing unsupported certainty;
- add focused tests for direction, bounds, provenance, duplicate/cyclic safety, and backward compatibility.

Do not immediately turn impact findings into automatic mutation or project-state writes.

### Slice C — evidence invalidation integration

After blast-radius behavior is stable, connect `programstart_evidence.py` to the surfaces that actually change.

Goals:

- answer what evidence remains valid;
- answer what was invalidated;
- explain the changed trigger and propagation path;
- keep time/age as metadata, not automatic expiry;
- preserve unaffected evidence;
- make invalidation deterministic and inspectable.

Start with read-only computation. Do not introduce a persistent evidence cache until the data model, provenance, invalidation semantics, migration story, and source-of-truth ownership are clear.

If persistence becomes justified, determine whether an ADR is required before implementation.

### Slice D — targeted verification-set selector

Turn the PROGRAMBUILD principle “run the smallest verification set that restores confidence” into deterministic behavior.

Model verification checks as sets covering explicit risk surfaces such as:

- requirements/contracts;
- schemas/migrations;
- auth/trust boundaries;
- prompt/registry authority;
- UI flows;
- runtime/deployment surfaces;
- relevant code/module boundaries.

Preferred first algorithm:

A transparent greedy set-cover style selector plus hard-required checks for special risk classes.

Required behavior:

1. determine the changed/at-risk surfaces;
2. invalidate stale evidence precisely;
3. remove checks whose valid evidence still covers unchanged surfaces;
4. choose checks that cover the largest remaining high-value uncovered surface per cost/effort unit;
5. include mandatory checks for designated risk classes;
6. widen to the full convergence gate at stage/release/governance boundaries.

Do not hardcode universal weights as truth. Any defaults must be explicit, explainable, testable, and tunable.

Every selection should expose reason codes explaining why a check was selected or skipped.

### Slice E — deterministic next-work selector

Do not implement ranking before eligibility.

Pipeline:

**1. Eligibility filter**

Exclude work when prerequisites are incomplete, a hard blocker exists, required evidence is invalid/unresolved, necessary tools/access are unavailable, scope is outside the strategic execution spine, or the work would contradict current authority.

**2. Feasibility filter**

Determine what can actually be executed now.

**3. Transparent ranking**

Only rank remaining eligible work using explainable factors such as:

- blocker-removal value;
- dependency unlock value;
- milestone relevance;
- risk reduction;
- information gain;
- estimated effort/cost;
- blast radius;
- real deadline urgency where applicable.

**4. Ambiguity handoff**

If candidates remain meaningfully close or require qualitative judgment, pass only that bounded candidate set and supporting evidence to the Reasoner.

Potential output:

`programstart next-work --json`

with eligible/excluded candidates, reason codes, factor inputs, recommendation, confidence, algorithm version, evidence used, and convergence trigger.

Do not let file ordering become execution priority.

### Slice F — bounded context selection

PROGRAMSTART already has BM25/vector/RRF retrieval. Do not reimplement those.

Retrieval answers: “what is relevant?”

The bounded context selector should answer: “what is the smallest authority/evidence set that must actually be loaded for this work packet under a finite context budget?”

Start with transparent greedy/budgeted selection using factors such as canonical authority, requirement/contract match, dependency relevance, decision relevance, provenance quality, material recency, impact, and redundancy.

Authority required for the task must not be dropped simply because a relevance score is lower.

### Slice G — rolling incremental replanning

Do not continuously regenerate the whole plan and do not use arbitrary calendar intervals as the main trigger.

Recompute the immediate plan when a meaningful event occurs, such as:

- work packet completion;
- blocker appearance/removal;
- dependency change;
- material decision change;
- scope/architecture change;
- evidence invalidation;
- stage/convergence gate;
- material deadline/external-condition change.

Incrementally recompute only the affected dependency subgraph, evidence, eligible work, and ranking. Preserve unaffected decisions and evidence.

### Slice H — recommendation-engine formalization

Only after the preceding execution-state primitives are stable, consider separating `programstart_recommend.py` more explicitly into:

1. hard eligibility/compatibility constraints;
2. soft scoring/ranking;
3. evidence/confidence;
4. alternatives/Pareto tradeoffs;
5. Reasoner escalation for unresolved qualitative choices.

Do not replace transparent recommendation rules with a learned model without a representative evaluation dataset and measured outcome improvement.

## 6. Algorithm observability is mandatory

For every new algorithmic recommendation or selector, expose enough information to reproduce and debug the result:

- algorithm name/version;
- input state/snapshot identifier where available;
- candidates considered;
- candidates excluded + reason codes;
- selected relation types / propagation rules;
- scores/factors where ranking is used;
- selected result;
- evidence used and validity state;
- fallback path;
- whether the Reasoner was invoked;
- validation result;
- later measured outcome when available.

Automation that cannot explain itself is not an improvement for PROGRAMSTART.

## 7. Evaluation requirements

Do not call an algorithmic change an improvement solely because it is more sophisticated.

Where applicable, establish a baseline and measure outcomes such as:

- wrong-next-action rate;
- blocked-task recommendation rate;
- unnecessary verification executions avoided;
- missed invalidation/regression rate;
- context tokens loaded per successful work packet;
- retrieval/context precision and recall;
- time from blocker resolution to useful next work;
- stability under irrelevant context changes;
- provenance/explainability completeness;
- operator override rate and reason;
- defects caused by stale evidence;
- false-positive blast-radius expansion.

If a more complex algorithm does not beat the simpler baseline, prefer the simpler one.

## 8. Project-level algorithm selection guidance

PROGRAMSTART should also help generated projects recognize when their own product problem has a real algorithmic structure.

During Research/Architecture, consider:

- exact lookup/filter/aggregation → database/query/indexing before AI;
- search/retrieval → inverted indexes/BM25/vector/hybrid retrieval;
- ranking/prioritization → hard filters + transparent scoring;
- dependencies/prerequisites → DAG/topological algorithms;
- routing/path selection → graph routing/shortest path where applicable;
- assignment/matching → matching/min-cost matching only when constraints justify it;
- scheduling/resources → greedy/heuristics first, solver only when necessary;
- budgeted selection → knapsack/set-cover approximations where appropriate;
- deduplication/similarity → hashing/similarity/clustering;
- prediction/classification → statistical/ML methods only with meaningful data;
- anomaly detection → statistical baselines first;
- stateful control → explicit state machine before autonomous agent behavior;
- uncertain semantic judgment → bounded Reasoner/LLM with deterministic validation.

If an algorithm materially controls money, access, safety, prioritization, business behavior, or user outcomes, define objective, constraints, baseline, failure modes, complexity/cost, evaluation metrics, fallback behavior, and the appropriate canonical architecture/decision record.

Do not label ordinary application logic an advanced algorithm merely to make the architecture sound sophisticated.

## 9. Non-negotiable anti-bureaucracy rules

- One strategic execution spine per real project.
- PROGRAMBUILD owns reusable methodology, not each project's live execution state.
- A work packet is derived execution context, not a second roadmap.
- Research/audits are evidence, not competing plans.
- Record evidence once; reference it elsewhere.
- Do not create a documentation diary for every micro-step.
- Do not repeat checks just because a session changed.
- Diagnose failures fully before correction; prefer one coherent correction batch over reactive patch loops.
- Do not spawn recurring CI/polling/automation unless it provides real value and is explicitly appropriate for that repository.
- Keep PROGRAMSTART's template repository inactivity decision intact unless the user explicitly changes it.
- Use human escalation for destructive/irreversible/production/credential/security/financial/public-contract/major architecture decisions, not for routine reversible implementation.
- Avoid arbitrary universal numeric thresholds unless evidence supports them.
- Planning rigor should scale with ambiguity, consequence, reversibility, and blast radius.

## 10. End-of-slice reporting

After each coherent slice, report compactly:

- what changed;
- PR/commit status;
- what was actually verified;
- what could not be verified;
- whether any evidence was invalidated;
- whether authority/docs/ADR/registry/changelog were updated and why;
- the actual next incomplete justified slice based on current repository state.

Do not claim background work, future execution, or tests that did not run.

Proceed with the next justified slice after verifying current repository state. Do not stop for unnecessary clarification if repository evidence can resolve the question.

## PROMPT END
