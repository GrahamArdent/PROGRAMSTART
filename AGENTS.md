# AGENTS.md — PROGRAMSTART Execution Contract

Status: **ACTIVE**

This file defines **how coding/review agents execute work in a PROGRAMSTART-managed repository**. It is an execution-facing instruction surface for agents such as Codex; it does not replace the repository's project/methodology authority.

In the PROGRAMSTART template repository, reusable methodology authority is indexed by `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`. In a generated or adopted project, the project's current execution spine, decisions, requirements, architecture, live/runtime truth, and any stronger local authority remain primary for their concerns.

The operating principle is:

> **Recover current authority, test the premise before investing heavily, automate everything already authorized that can be verified safely, and consume human attention only for a technically ready human-only boundary.**

---

## 1. Mandatory startup — narrow and current

For substantive work:

1. recover current repository / branch / PR / CI truth;
2. identify the repository's current strategic execution spine and the exact authority owners implicated by the requested change; use `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` as the PROGRAMSTART concern-routing map where applicable;
3. when an existing PR/branch already owns the same mutation surface, continue that owner rather than creating a competing branch/PR unless current repository authority explicitly requires otherwise;
4. load only the PROGRAMSTART protocols triggered by the current work, especially:
   - `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` for current-slice execution semantics;
   - `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` for risk/convergence/post-implementation adversarial review;
   - `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` for autonomy, concept viability, alternative actuation, and human-gate readiness;
   - `docs/PROGRAMSTART_LEARNING_LOOP.md` for reusable methodology learning when that support file is present;
   - `docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md` when a material derived finding is missing from its real owner;
5. use `PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md` or `.github/agents/*.agent.md` only when a bounded specialist role materially improves the result.

Do not load the entire methodology corpus by habit. Reuse still-valid evidence and re-check only plausible invalidation.

---

## 2. Authority and instruction boundary

`AGENTS.md` owns repository execution behavior for compatible agents. It does **not** own project scope, sequencing, architecture, requirements, release status, or provider/runtime truth.

When sources disagree, prefer the strongest current applicable evidence/authority. At minimum:

1. direct system/developer/user instructions that apply to the current agent session;
2. observed live repository/runtime/provider truth for claims about current state;
3. validated code and reproducible tests for implementation behavior;
4. the repository's current strategic execution spine and canonical concern owner, including `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` where applicable;
5. this `AGENTS.md` for execution behavior;
6. supporting/derived evidence and historical material.

A Work Packet, checklist, recommendation, learning observation, audit, chat transcript, or specialist-agent result cannot grant authority merely because it is newer.

A project-local `AGENTS.md` may add stronger repository-specific execution/safety rules. PROGRAMSTART adoption must preserve an existing project-owned `AGENTS.md` rather than overwrite it with the reusable default.

---

## 3. Default execution loop

For a coherent change use:

**Orient → Challenge premise → Decide → Batch → Execute → Verify → Adversarial review when triggered → Reconcile authority → Review outcome**

Prefer one coherent change over a long sequence of tiny mutations.

Before another read/tool/test/retry ask:

1. Is the fact already verified and still valid?
2. Will the next action materially change the decision or confidence?
3. Can related work be batched safely?
4. Is there a smaller discriminating check?
5. If this is another similar attempt, what materially changed and why could that change the outcome?

Do not use repetition as evidence of progress.

---

## 4. Concept viability before implementation persistence

For routine deterministic work with a well-supported mechanism, proceed normally.

When a mechanism is materially uncertain, repeatedly failing, consequential, expensive, recurrent, or approaching a human gate, apply `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` concept-viability rules before investing further.

At minimum establish:

- the concept / mechanism being attempted;
- why current evidence says it should work;
- the smallest meaningful falsification test;
- what result would falsify or materially weaken the premise;
- whether current status is `untested`, `supported`, `inconclusive`, or `falsified`;
- bounded alternatives;
- the evidence/effort boundary for further exploration.

A materially similar retry is allowed only when evidence, mechanism, configuration, environment, hypothesis, implementation, or diagnostic discrimination changed and there is a concrete reason that change could affect the result.

If the concept is falsified, stop forcing it. Pivot, preserve the evidence, or stop truthfully.

Do not use a human as the fallback debugger for a falsified or unvalidated machine premise.

---

## 5. Human attention / credentials / manual boundaries

Human attention is a protected resource.

Before asking the operator for a mechanical action, credential entry, provider-console action, copy/paste relay, or similar transport:

1. classify the boundary as `genuine_human_gate` or `temporary_automation_gap`;
2. if mechanical and already authorized, perform the proportional alternative-actuation search in `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md`;
3. establish `GATE_READINESS: ready` before notifying the operator;
4. identify the exact `HUMAN_ONLY_REMAINDER`.

For a technically ready gate, validate machine-resolvable details before the handoff where applicable:

- current authoritative/provider/runtime procedure;
- exact shell/tool/version/target context;
- command syntax, quoting, spacing, formatting, paths, typed arguments, config shape, and destination;
- owner/permission requirements;
- non-secret/dummy portions when practical and useful;
- secret-sensitive boundary and secure destination;
- post-action verification;
- rollback/removal/recovery when warranted.

Never ask the operator to paste raw secrets into ordinary chat/evidence when a secure owning surface exists. Name the secret/config key and the secure destination instead.

A human action is not acceptance. Run the predefined post-action system verification.

If the operator has to correct machine-resolvable syntax/format/path/permission details after handoff, treat that as evidence the gate was not actually ready; correct the procedure and route reusable learning to the proper owner.

---

## 6. Challenge and closure

Green tests are necessary evidence when applicable, not proof that the chosen approach or trajectory was good enough.

Before merge-ready/accepted/complete status:

- run the narrowest required deterministic checks;
- satisfy repository drift/sync/authority rules;
- if the actual changed surface triggers `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`, challenge the completed implementation with at least one realistic failure sequence against a material invariant;
- inspect materially suspect execution trajectories, including stale-evidence loops, repeated indistinguishable retries, unnecessary human relays, unsafe shortcuts, or accidental success;
- fix or truthfully retain any resulting blocker/warning rather than weakening the gate.

Do not retry a failing CI job unless something relevant changed or the failure is demonstrated transient.

Do not modify requirements/architecture/canonical files merely to silence a drift check. Reconcile them only when the underlying authority actually changed; otherwise correct the dependent change.

---

## 7. PROGRAMSTART learning

At meaningful completion/blocker/correction points, apply `docs/PROGRAMSTART_LEARNING_LOOP.md` when that protocol is part of the repository's managed PROGRAMSTART surface.

A reusable methodology lesson may be earned when, for example:

- an operator was asked to debug a procedure the machine should have validated first;
- repeated attempts persisted after the concept had become unsupported;
- a successful final result hid a materially poor trajectory;
- an execution-facing rule existed only in buried documentation and was not reaching the agent surface;
- a human gate was declared before bounded alternative actuation was challenged.

Do not create learning noise for ordinary local failures. Route behavior-specific learning to the system that owns the behavior.

---

## 8. Specialist agents are not `AGENTS.md`

`PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md` and `.github/agents/*.agent.md` define optional bounded specialist roles when those files exist.

They do not replace this repository-level execution contract, and they do not become project authority.

Use specialist agents for independent evidence/review when helpful; the main execution owner remains responsible for synthesis, current authority, mutation ownership, verification, and closure.

---

## 9. Final self-review requirement

After completing the requested changes, review the completed work against the goals that justified it.

Report truthfully:

- which goals were achieved and the evidence;
- which were not achieved and why;
- any material change of mind and the evidence that caused it;
- any scope/implementation decision that changed during execution and why;
- verification limitations or unresolved blockers;
- whether the result reduced or increased operator work, retry risk, authority ambiguity, and execution complexity.

Do not convert partial implementation into a success claim.
