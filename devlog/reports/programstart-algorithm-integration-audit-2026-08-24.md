# PROGRAMSTART Algorithm Integration Audit — 2026-08-24

Purpose: Apply the Advanced Algorithms for Practical AI Systems research to PROGRAMSTART/PROGRAMBUILD and identify where algorithms can make the system more precise, efficient, explainable, and reliable without introducing unnecessary sophistication.

Status: Analysis / subordinate evidence. This file is not a game plan, does not replace `PROGRAMBUILD_GAMEPLAN.md`, and does not create execution authority.

Depends on:
- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`
- `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md`
- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`
- `scripts/programstart_context.py`
- `scripts/programstart_retrieval.py`
- `scripts/programstart_impact.py`
- `scripts/programstart_recommend.py`
- `scripts/programstart_status.py`
- `scripts/programstart_step_guide.py`
- `scripts/programstart_workflow_state.py`

---

## 1. Executive conclusion

PROGRAMSTART should become **algorithmically precise before becoming algorithmically sophisticated**.

The strongest architecture is:

> LLM interprets ambiguous evidence or generates candidates → deterministic algorithms enforce eligibility, dependencies, ranking, budgets, verification, and state transitions → the Reasoner is used only where real ambiguity remains → outputs are validated and observable.

PROGRAMSTART already follows much of this philosophy. It has deterministic registries, workflow-state transitions, stage gates, drift rules, schemas, validation, retrieval, and test contracts. The opportunity is therefore not to add advanced algorithms indiscriminately. The opportunity is to strengthen the layer between **canonical project state** and **agent reasoning**.

Highest-value gaps:

1. dependency-aware next-work selection;
2. graph-based blast-radius analysis;
3. minimal verification-set selection;
4. explicit evidence invalidation and reuse;
5. bounded context selection under a context/token budget;
6. rolling replanning after material state changes;
7. transparent recommendation scoring and decision observability.

Advanced methods such as reinforcement learning, bandits, MCTS, genetic algorithms, graph neural networks, constraint-programming solvers, and self-changing weights should remain deferred until simpler deterministic methods are measured and shown inadequate.

---

## 2. What PROGRAMSTART already implements well

### 2.1 Deterministic workflow authority

PROGRAMSTART already gives deterministic code responsibility for:

- registry composition;
- workflow state;
- stage progression;
- required files and metadata;
- source-of-truth drift;
- structural stage gates;
- decision-log coherence;
- ADR coherence;
- prompt classification and linting;
- repository-boundary rules;
- bootstrap validation.

This is the correct placement of deterministic logic. These controls should not be moved into free-form LLM judgment.

### 2.2 Hybrid information retrieval

`scripts/programstart_retrieval.py` already implements meaningful classical information-retrieval algorithms:

- Okapi BM25 lexical retrieval;
- ChromaDB-backed cosine vector retrieval when available;
- Reciprocal Rank Fusion for lexical/vector hybrid retrieval;
- deterministic validation that an LLM citation actually came from retrieved context.

Therefore, adding BM25, embeddings, vector search, or RRF is **not** a new opportunity. They already exist.

Possible future improvements such as diversity-aware reranking should be benchmark-driven rather than assumed useful.

### 2.3 Structured context graph foundation

`scripts/programstart_context.py` already constructs explicit relationships including:

- `depends_on`;
- `canonical_owner`;
- `source_of_truth`;
- `authority_dependency`.

That is an important foundation for graph algorithms. The missing piece is that most current consumers still treat these relationships primarily as searchable records rather than traversable dependency structure.

### 2.4 Deterministic stage gating

`scripts/programstart_workflow_state.py` runs structural preflight checks and blocks stage advancement when required evidence or gate conditions fail. This is a good example of the research principle:

> Do not ask the LLM whether a mechanically checkable constraint is satisfied.

### 2.5 Transparent recommendation inputs

`scripts/programstart_recommend.py` already uses explicit product shapes, capability aliases, rule matching, integration-pattern matching, and knowledge-base evidence rather than asking an LLM to invent a stack from scratch.

The opportunity is to formalize eligibility and scoring, not replace the deterministic foundation.

---

## 3. Immediate consistency findings related to the new planning model

These are not reasons to introduce a large algorithm subsystem. They are places where existing implementation semantics should be brought into alignment with the planning-operating model.

### 3.1 Calendar-only staleness is too authoritative

`scripts/programstart_status.py` currently uses elapsed-time thresholds to label workflow state stale and to recommend the Re-Entry Protocol.

The new canonical Challenge Gate correctly moved away from universal calendar thresholds and now treats re-entry as a function of plausible evidence decay, changed dependencies, changed assumptions, production signals, scope/architecture changes, and other invalidation events.

Recommended adjustment:

- retain elapsed time only as a **weak inactivity signal**;
- do not treat elapsed time by itself as evidence that project truth is stale;
- calculate re-entry need from evidence-invalidation signals where they are available;
- phrase time-based warnings as prompts to inspect validity, not as proof that revalidation is required.

### 3.2 Cross-system stage-distance warning is a heuristic, not a law

`cross_system_health_warning()` warns when PROGRAMBUILD and USERJOURNEY differ by at least two ordinal steps.

That can be useful as a coarse heuristic, but ordinal stage distance is not equivalent to dependency risk. Two workflows can legitimately be several steps apart if the current PROGRAMBUILD work does not depend on the delayed USERJOURNEY state.

Recommended adjustment:

- label ordinal distance as a heuristic only;
- eventually replace or augment it with explicit dependency edges and blocked/unblocked relationships.

### 3.3 `summarize_programbuild()` uses first-missing-file ordering

When outputs are absent, current status behavior selects `missing_outputs[0]` as the next action.

That is simple and predictable, but it is not genuine next-work reasoning. File order can accidentally become execution priority.

Recommended adjustment:

- derive eligibility from active stage and dependencies;
- select the next required output/work item by dependency readiness and project state;
- use ranking only after blockers and hard prerequisites have been applied.

---

## 4. Highest-value algorithmic additions

## 4.1 Dependency DAG and blocker engine — HIGH priority

### Problem

PROGRAMSTART has linear workflow order plus relationship metadata, but it does not yet fully represent implementation/work-packet dependencies as a directed acyclic graph.

### Recommended model

Represent meaningful work items and evidence dependencies as nodes/edges such as:

- requirement → architecture contract;
- architecture contract → implementation slice;
- implementation slice → verification evidence;
- migration → dependent application slice;
- blocker → blocked work packet;
- decision → affected contracts;
- external dependency → evidence whose validity depends on it.

Use deterministic graph algorithms for:

- topological ordering;
- cycle detection;
- immediate blockers;
- newly unlocked work;
- ancestor/descendant impact;
- safe parallelism;
- optional critical-path analysis when real scheduling data exists.

### Why it matters

This would make the work-packet model much stronger. Instead of merely asking an agent what seems next, PROGRAMSTART could mechanically determine what is eligible and what is blocked before the LLM ranks or explains anything.

### Do not overreach

Do not introduce a general graph database initially. The existing context-index relation model plus ordinary adjacency maps is sufficient for an initial deterministic implementation.

---

## 4.2 Deterministic next-work selector — HIGH priority

### Problem

`programstart status` currently reports stage state but does not calculate the best next bounded work item.

### Recommended pipeline

Use a staged decision algorithm:

**Step 1 — eligibility filter**

Exclude candidates when:

- required predecessor is incomplete;
- a blocking Challenge Gate exists;
- the task is outside the strategic execution spine;
- required access/tool/environment is unavailable;
- the task would prospectively contradict current authority;
- prerequisite evidence is invalid or unresolved.

**Step 2 — feasibility filter**

Determine whether the task can actually be executed now.

**Step 3 — transparent ranking**

Rank remaining candidates using understandable factors such as:

- blocker-removal value;
- dependency unlock value;
- milestone relevance;
- risk reduction;
- information gain;
- estimated effort/cost;
- blast radius;
- urgency when a real deadline exists.

No universal fixed weights should be hardcoded as truth. Defaults can exist, but the reason codes and inputs must be visible and tunable.

**Step 4 — ambiguity handoff**

If two or more candidates remain meaningfully close or involve qualitative tradeoffs, give the bounded candidate set and evidence to the Reasoner.

### Output

A future command could return:

```text
programstart next-work --json
```

with:

- eligible candidates;
- excluded candidates + reason codes;
- rank factors;
- selected recommendation;
- confidence;
- algorithm version;
- evidence used;
- next convergence trigger.

This would operationalize the distinction already introduced in the updated What Next prompt between **strategic next** and **immediate next**.

---

## 4.3 Graph-based impact / blast-radius analysis — HIGH priority

### Current state

`scripts/programstart_impact.py` queries the context index and returns related documents, concerns, relations, routes, commands, stack entries, and KB records.

This is useful discovery, but the relation graph can support more.

### Recommended algorithm

Use bounded graph traversal from a changed node:

1. identify direct relations;
2. traverse relevant edge types to an explicit depth/risk boundary;
3. preserve path provenance;
4. classify affected nodes by authority, implementation, test, external dependency, or evidence role;
5. produce a blast-radius summary.

Useful outputs:

- canonical owners potentially affected;
- dependent work packets;
- verification evidence potentially invalidated;
- test surfaces likely required;
- path showing *why* each item is considered affected.

### Important guardrail

Do not blindly traverse every relation. Different edge types should have different propagation semantics. `depends_on` and `authority_dependency` can propagate impact differently from a loose semantic/retrieval relationship.

---

## 4.4 Verification-set selector — HIGH priority

### Problem

The new planning model says to run the smallest verification set that restores confidence, but today the operator/agent still often chooses that set manually.

### Recommended model

Treat verification checks as sets that cover risk surfaces.

Examples of surfaces:

- requirement IDs;
- contracts/endpoints;
- auth/trust boundaries;
- schema/migration surfaces;
- prompt classes;
- registry authority;
- UI flows;
- deployment/runtime surfaces.

Each test/check knows what it covers. After a change, PROGRAMSTART calculates the at-risk surface and selects a minimal useful group of checks.

A greedy set-cover style algorithm is a strong initial approach:

1. list required risk surfaces;
2. select the check covering the most uncovered high-value surfaces per unit cost;
3. repeat until mandatory coverage is met;
4. add hard-required checks for special risk classes;
5. widen to the full convergence gate at stage/release boundaries.

### Why it matters

This directly reduces repeated low-value CI/test work while preserving deterministic justification for what was and was not rerun.

It also converts the current principle “targeted verification” into executable system behavior.

---

## 4.5 Evidence invalidation graph / verification cache — HIGH priority

### Problem

PROGRAMBUILD now correctly says verification evidence should be reused until invalidated, but the invalidation relationship is primarily described in prose/work packets.

### Recommended model

Represent evidence as a cache entry with:

- evidence ID;
- check/test/source;
- scope covered;
- input versions or relevant commit/environment identifiers;
- date as metadata, not sole validity criterion;
- provenance;
- invalidation edges/conditions;
- current validity state.

When a related contract/config/schema/dependency changes, invalidate only the evidence whose dependency graph intersects the changed surface.

### Result

PROGRAMSTART can answer:

- What evidence is still valid?
- Why is it still valid?
- What was invalidated?
- Which smallest check re-establishes it?

This is one of the most direct algorithmic implementations of the new planning model.

---

## 4.6 Bounded context selector — MEDIUM-HIGH priority

### Current state

The repo has strong retrieval algorithms and the new JIT model correctly tells agents not to load every stage file in full.

### Remaining gap

Retrieval returns relevant chunks, but PROGRAMSTART does not yet explicitly solve the problem:

> Given this exact work packet and a finite context budget, what is the smallest authority/evidence set that covers everything needed to execute safely?

### Recommended approach

Use a budgeted selection algorithm over candidate context chunks.

Score candidates by factors such as:

- canonical authority;
- exact requirement/contract match;
- dependency relevance;
- recency where recency is actually material;
- decision relevance;
- provenance quality;
- expected impact;
- redundancy with already-selected chunks.

Then select until required concerns are covered or the context budget is reached.

This can begin as transparent greedy selection. There is no need for an advanced learned context policy initially.

### Retrieval distinction

BM25/vector/RRF answer **what is relevant**.

The context selector answers **what must actually be loaded for this task under a bounded budget**.

Those are different problems.

---

## 4.7 Rolling replanning — MEDIUM-HIGH priority

### Principle

Do not continuously re-plan everything and do not wait for an arbitrary calendar interval.

Recompute the immediate plan when a meaningful invalidation event occurs, such as:

- a work packet completes;
- a blocker clears or appears;
- a dependency changes;
- a material decision changes;
- scope or architecture changes;
- verification evidence becomes invalid;
- a stage/convergence gate is reached;
- a deadline or external condition materially changes.

### Algorithmic behavior

1. update project state;
2. recompute affected dependency subgraph only;
3. invalidate affected evidence;
4. recompute eligible next work;
5. rerank only changed/affected candidates;
6. preserve unaffected decisions/evidence.

This is incremental replanning rather than repeated full-plan regeneration.

---

## 4.8 Recommendation engine formalization — MEDIUM priority

### Current state

`programstart_recommend.py` contains useful explicit heuristics for product shape, capabilities, aliases, stacks, integration patterns, domains, and knowledge-base decision rules.

### Improvement

Separate its logic more explicitly into:

1. hard eligibility/compatibility constraints;
2. soft scoring/ranking;
3. evidence/confidence;
4. alternatives/Pareto tradeoffs;
5. Reasoner escalation for unresolved qualitative choices.

This makes recommendations explainable and benchmarkable.

### Do not prematurely optimize

Do not replace transparent rules with a learned recommender until there is a representative evaluation dataset containing project inputs and measured outcomes.

---

## 4.9 Algorithm observability and versioning — HIGH priority across all additions

Every new algorithmic recommendation should expose:

- algorithm name/version;
- input state or snapshot identifier;
- candidates considered;
- candidates excluded and reason codes;
- scores/factors where ranking is used;
- selected result;
- fallback path;
- whether the Reasoner was invoked;
- validation result;
- later outcome when available.

Without this, PROGRAMSTART could become more opaque as it becomes more automated.

The goal is not merely to automate decisions. It is to make them reproducible and debuggable.

---

## 5. Algorithm selection inside projects created by PROGRAMSTART

PROGRAMSTART should also help a project determine whether **that project's product problem** deserves a specialized algorithm.

This belongs primarily in Research and Architecture, not as a new standalone master-planning hierarchy.

### Suggested algorithm-selection question set

During Stage 2 / Stage 4, explicitly ask whether the core problem contains any of these structures:

| Problem structure | First algorithm family to consider |
|---|---|
| Exact lookup/filter/aggregation | database/query/indexing before AI |
| Search/retrieval | inverted indexes, BM25, vector retrieval, hybrid fusion |
| Ranking/prioritization | rule filters + weighted scoring/ranking |
| Dependencies/prerequisites | DAG/topological algorithms |
| Routing/path selection | graph shortest-path/routing algorithms |
| Assignment/matching | bipartite matching / min-cost matching when constraints justify it |
| Scheduling/resource allocation | greedy/heuristic scheduling first; solver only if constraints justify it |
| Budgeted selection | knapsack/set-cover style approximations where appropriate |
| Deduplication/similarity | hashing, similarity metrics, clustering as appropriate |
| Prediction/classification | statistical/ML model only with meaningful labelled data |
| Anomaly detection | statistical baselines before complex ML |
| Stateful control | explicit state machine before agent autonomy |
| Uncertain semantic judgment | bounded LLM/Reasoner with deterministic validation |

### Architecture decision rule

If an algorithm materially determines business behavior, money, safety, access, prioritization, or user outcomes:

- define the objective;
- define constraints;
- define the baseline;
- define failure modes;
- define complexity/cost;
- define test/evaluation metrics;
- define fallback behavior;
- record it in the project's appropriate canonical architecture/decision authority.

Do not label ordinary application logic an “advanced algorithm” merely to make the architecture sound sophisticated.

---

## 6. Algorithms that should remain deferred by default

The prior research specifically supports restraint here.

### Reinforcement learning / contextual bandits

Defer until there is:

- a repeated decision;
- measurable feedback/reward;
- enough observations;
- safe exploration boundaries;
- a strong static baseline to beat.

Do not use RL for basic task ordering or workflow control.

### Monte Carlo Tree Search

Defer unless PROGRAMSTART eventually faces a genuine large branching planning/search problem where lookahead demonstrably beats deterministic dependency + ranking methods.

### Genetic / evolutionary algorithms

Defer unless there is a measurable optimization space with a costly/non-differentiable objective where simpler search/heuristics fail.

### Graph neural networks

PROGRAMSTART does have graph-shaped data, but graph structure alone does not justify a GNN. Deterministic graph traversal should come first.

### CP-SAT / MILP / constraint solvers

Potentially useful for genuine multi-resource scheduling, allocation, or assignment with hard constraints. Do not introduce them for ordinary work-packet selection until a real optimization problem exists.

### Multi-agent debate / algorithmic agent swarms

Do not use additional agents as a substitute for a clearer deterministic workflow. Use specialists only where decomposed parallel evidence generation is actually beneficial.

### Self-changing weights / autonomous policy learning

Do not allow PROGRAMSTART to silently mutate its own ranking policy. Changes to algorithm configuration should be versioned, observable, evaluated, and governed like other material process changes.

---

## 7. Priority order

### Priority A — align current implementation with current authority

- make status/re-entry warnings invalidation-aware instead of treating calendar age as proof of staleness;
- label ordinal cross-system distance as a heuristic rather than a universal risk rule;
- stop using first-missing-file ordering as a conceptual model of “best next work.”

These items are directly related to the planning-operating-model changes and should be reconciled before claiming the methodology is fully propagated.

### Priority B — build algorithmic primitives with immediate payoff

1. typed dependency graph + cycle/block/unlock detection;
2. bounded blast-radius traversal in `programstart impact`;
3. evidence validity/invalidation model;
4. deterministic next-work eligibility + ranking;
5. verification coverage registry + minimal verification-set selector.

### Priority C — improve context/recommendation efficiency

6. bounded context selection above existing BM25/vector/RRF retrieval;
7. formalize recommendation eligibility/ranking/confidence;
8. incremental rolling replanning.

### Priority D — evaluate before increasing sophistication

Only after enough PROGRAMSTART-managed projects produce real execution telemetry should the project consider learned ranking, solver-backed scheduling, bandits, or other adaptive methods.

---

## 8. Suggested architecture without creating a second planning system

Do not create a parallel “algorithm game plan.”

If implementation is approved later, the likely reusable primitives are small modules integrated into existing commands, for example:

```text
scripts/
  programstart_graph.py          # typed dependency graph / traversal / cycle detection
  programstart_evidence.py       # evidence provenance + invalidation
  programstart_next_work.py      # eligibility + transparent ranking
  programstart_verify_select.py  # risk-surface coverage / targeted check selection
```

Existing consumers would then evolve rather than being replaced:

```text
programstart status
  -> strategic state + blockers + evidence validity + immediate ranked next action

programstart guide
  -> stage baseline + bounded context candidates

programstart impact <target>
  -> graph paths + blast radius + evidence invalidation + likely verification surfaces

programstart recommend
  -> hard constraints + explainable ranking + alternatives

CURRENT_WORK_PACKET.md
  -> consumes selected authority/evidence/verification, remains derived and non-canonical
```

The canonical owner for methodology remains PROGRAMBUILD. Algorithm implementation does not create a second source of project truth.

---

## 9. Evaluation requirements before calling any algorithm an improvement

Each algorithmic change needs an explicit baseline and measurable outcome.

Useful PROGRAMSTART measures include:

- wrong-next-action rate;
- blocked-task recommendation rate;
- unnecessary verification executions avoided;
- missed regression / invalidation rate;
- context tokens loaded per successful work packet;
- retrieval/context precision and recall on an evaluation set;
- time from blocker resolution to useful next action;
- recommendation stability under irrelevant context changes;
- explainability/provenance completeness;
- operator override rate and reason;
- defects attributable to stale evidence;
- false-positive blast-radius expansion.

A sophisticated algorithm that does not outperform the simpler baseline should not survive merely because it is more advanced.

---

## 10. Bottom line

PROGRAMSTART already has strong deterministic foundations and more algorithmic capability than its surface documentation suggests. In particular, retrieval is already meaningfully algorithmic.

The next leap is not “more AI.” It is to make **execution-state reasoning mechanically stronger**:

- graph the dependencies;
- filter what is actually eligible;
- rank transparently;
- invalidate evidence precisely;
- choose the smallest sufficient verification set;
- bound the context;
- replan only when something material changes;
- preserve a Reasoner for ambiguity instead of using it as the default scheduler.

That direction fits the new PROGRAMBUILD planning model and directly addresses the two main operational goals behind it: **move faster without losing authority discipline, and stop spending verification/context budget on work whose underlying evidence has not changed.**
