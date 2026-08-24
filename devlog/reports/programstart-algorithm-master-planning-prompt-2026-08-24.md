# PROGRAMSTART Algorithm Planning / Execution Launcher — 2026-08-24

Status: Reusable launcher / orchestration prompt. **Not a game plan, roadmap, or source of project authority.**

Use this prompt to resume PROGRAMSTART algorithm work without loading the full methodology up front.

---

## PROMPT START

Continue work in:

`GrahamArdent/PROGRAMSTART`

Use connected GitHub tooling and current repository state before making substantive decisions.

### 1. Orient from live state

Do not reconstruct the project from chat memory.

First:

1. inspect current `main` and open PRs;
2. read the repository's standing instructions;
3. use the current equivalents of:
   - `programstart status`
   - `programstart guide --system programbuild`
4. identify the **actual next incomplete justified slice**;
5. load only the authority sections and specialist evidence required for that slice.

PROGRAMBUILD owns reusable methodology. A real project owns its own strategic execution spine. Do not create another Master Game Plan, algorithm game plan, roadmap, or parallel execution spine.

### 2. Core execution rules

- Work in one bounded coherent slice at a time.
- Use the lightest planning representation that keeps the slice clear and resumable.
- Treat work packets as logical task context; persist `CURRENT_WORK_PACKET.md` only when multi-session, multi-agent, risk, dependency complexity, or resumability makes a file useful.
- Reuse trustworthy prior evidence until a relevant invalidation trigger occurs.
- Run targeted verification for changed/at-risk surfaces during implementation.
- Widen to the appropriate Challenge Gate / full convergence checks at meaningful boundaries.
- Record durable decisions/evidence once in the correct authority instead of maintaining a diary.
- Diagnose failures before patching; prefer one coherent correction batch.
- Do not reactivate scheduled or recurring CI merely to obtain reassurance.
- Never claim a check ran when it did not.

### 3. Algorithm design rule

PROGRAMSTART should become **algorithmically precise before algorithmically sophisticated**.

Prefer:

> bounded LLM/Reasoner for ambiguity → deterministic eligibility/dependency/impact/evidence/verification/state logic → observable result → deterministic validation.

Do not use an LLM for mechanically checkable constraints.

Keep RL, bandits, MCTS, genetic algorithms, GNNs, solver-heavy scheduling, learned/self-changing policy weights, and agent swarms deferred until measured evidence shows simpler deterministic methods are inadequate.

### 4. Algorithm evidence is JIT context

Only when algorithm work is actually next, consult the current algorithm audit/research evidence and reconcile it against live `main` before acting.

Do **not** load the entire algorithm roadmap merely because this launcher was used.

Current implementation foundation to verify from GitHub:

- dependency graph primitives in `scripts/programstart_graph.py`;
- evidence invalidation primitives in `scripts/programstart_evidence.py`;
- focused graph/evidence tests;
- any later algorithm PRs merged after this launcher was written.

### 5. Default next-capability order

Use this only as a tie-breaker after inspecting live state:

1. close any still-material verification gap on the graph/evidence foundation;
2. integrate bounded provenance-preserving graph blast radius into `programstart impact`;
3. connect evidence invalidation to real changed surfaces;
4. **before** implementing verification-set optimization, confirm PROGRAMSTART has trustworthy machine-readable coverage metadata;
5. **before** implementing next-work ranking, establish a reliable candidate-work model and deterministic eligibility;
6. add ranking only if measured benefit remains after eligibility;
7. consider bounded context optimization only if measurements show current JIT/retrieval is insufficient;
8. use event-driven incremental replanning only after the dependency/evidence/next-work layers justify it.

Do not implement a later item simply because it is listed here.

### 6. Per-slice loop

For the selected slice:

1. state objective and non-goals;
2. identify exact authority and relevant evidence;
3. identify dependencies/blockers;
4. define acceptance criteria;
5. define reusable evidence + invalidation conditions;
6. define the smallest sufficient verification set;
7. branch from current `main`;
8. implement the smallest coherent change;
9. inspect consumers of any shared contract changed;
10. add focused tests;
11. update authority/registry/changelog/ADR only when existing repository rules require it;
12. run targeted verification;
13. widen to convergence before merge when risk/shared-contract/release conditions require it;
14. red-team the final diff;
15. merge when justified;
16. derive the next slice from the new repository state.

### 7. Stop conditions for algorithm complexity

Before adding a selector, optimizer, learned model, or solver, require:

- a clearly defined problem;
- a simpler baseline;
- trustworthy input data/metadata;
- measurable success/failure criteria;
- explainable outputs/reason codes;
- fallback behavior;
- evidence that the added complexity addresses a real bottleneck.

If the complex method does not beat the simpler baseline, keep the simpler method.

### 8. End-of-slice report

Report only:

- what changed;
- PR/commit state;
- what actually passed verification;
- what could not be verified;
- evidence invalidated/reused;
- durable authority updates made and why;
- actual next incomplete justified slice.

Proceed with the next justified slice from live repository state. Do not stop for clarification when repository evidence can resolve the question.

## PROMPT END
