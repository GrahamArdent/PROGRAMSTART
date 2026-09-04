---
status: accepted
date: 2026-09-04
deciders: [solo operator]
consulted: []
informed: []
---

# 0025. Treat Intent Ingress as a Pre-Entry Profile, Not a New Project Mode

## Context and Problem Statement

PROGRAMSTART already uses mode terminology for more than one concern:

- PROGRAMBUILD project entry distinguishes raw idea, research-backed project, and existing/in-flight project;
- existing-project work is commonly referred to as Mode C;
- Prompt Builder separately uses Mode A/Mode B for registry-backed versus context-driven prompt rendering.

The Intent Compilation V0.1 work introduces a different concern. The operator may express a goal before the owning project, live execution spine, current work packet, parallel mutation owner, or correct project-entry mode has been resolved.

For example, `Keep Resume Creator moving, but don't interfere with the infrastructure work` is not itself a request to select a new project lifecycle. It is an operator-intent ingress request that must first resolve current authority and active ownership, then preserve the correct normal PROGRAMSTART entry/execution mode.

A live parallel-work observation reinforced this distinction: while intent-compilation PR #94 was active, PROGRAMSTART PR #95 independently claimed the deterministic pre-publication quality-gate surface. Intent compilation should detect and represent that active ownership rather than create a second quality lane merely because the operator's wording is broad.

## Decision Drivers

- Let the operator speak naturally before repository/mode details are known.
- Preserve existing PROGRAMBUILD entry modes instead of inventing a competing lifecycle.
- Avoid further overloading `Mode A`, `Mode B`, `Mode C`, or introducing an ambiguous `Mode D`.
- Resolve owner, authority, current work, and parallel conflicts before deriving executable scope.
- Keep Controller admission downstream from interpretation and compilation.
- Keep long-form prompts as target-specific renderings rather than execution truth.
- Allow the same ingress path to route to continuation, audit, architecture evaluation, or bounded execution without changing project lifecycle semantics.

## Considered Options

1. **Add PROGRAMSTART Mode D for intent compilation.** Treat natural-language intent as a fourth project-entry mode.
2. **Extend Prompt Builder Mode B.** Make context-driven prompt generation responsible for authority discovery, work semantics, and admission boundaries.
3. **Define Intent Ingress as an orthogonal pre-entry profile.** Interpret operator intent, resolve current authority/currentness, compile a Work Packet projection, then hand back to the existing project entry/execution mode and Controller admission.

## Decision Outcome

Chosen option: **3 — Intent Ingress is an orthogonal pre-entry profile, not a new project mode.**

The preferred flow is:

`operator intent -> intent ingress -> authority/currentness resolution -> compiled Work Packet -> existing PROGRAMSTART project mode -> Controller admission -> execution`

Where the target project is already mature, the resolved project mode will usually remain existing/in-flight Mode C. Intent Ingress does not replace Mode C; it makes reaching the correct Mode-C context low-friction and machine-inspectable.

### Intent Ingress responsibilities

Intent Ingress may:

- preserve the operator's raw request;
- classify the semantic request family conservatively;
- resolve or consume the resolved owning project and current authority;
- distinguish explicit requirements, inherited defaults, evidence-backed inferences, assumptions, recommendations, and unresolved ambiguity;
- derive expected mutable/read-only surfaces and parallel-work conflicts;
- compile the smallest useful sealed Work Packet projection;
- render target-specific execution briefs after semantic compilation.

Intent Ingress must not:

- grant execution authority;
- replace project authority or PROGRAMSTART project-entry semantics;
- perform Controller admission;
- own durable orchestration, leases, or fencing;
- convert an audit into implementation without authority;
- convert broad natural language into spend, destructive, credential, provider, or security authority;
- revive Prompt Builder prompt text as the canonical execution contract.

### Terminology

Use these terms on separate axes:

- **Project entry mode** — raw idea, research-backed project, existing/in-flight project (Mode C where applicable).
- **Intent ingress profile** — natural-language operator request entering before project context is fully resolved.
- **Intent kind** — continuation, audit, architecture evaluation, bounded execution, or unresolved/unknown semantic family.
- **Renderer mode/target** — ChatGPT, Codex, Controller job, issue/work item, or another presentation/execution client.

Do not call Intent Ingress `Mode D`.

Prompt Builder's historical Mode A/Mode B naming remains compatible but should be treated as renderer/generator-local terminology, not as the global PROGRAMSTART project-mode axis.

### Product-surface sequencing

Do not expose Intent Ingress as a polished top-level `programstart intent-compile` operator command merely because the deterministic compiler exists.

V0.1 still requires a pre-resolved `AuthoritySnapshot`. A top-level command that asks the operator to manually construct that snapshot would expose an implementation seam as if the intended ordinary-language product experience were complete.

Keep the standalone compiler entrypoint as a developer/contract harness until the authority/currentness resolver can supply the snapshot from owning-project authority, active admitted work, parallel ownership, and accepted evidence. Once that resolver exists, a first-class intent-ingress command/API becomes appropriate.

## Consequences

- Good: Graham can give short natural-language commands without learning PROGRAMSTART boilerplate.
- Good: mature-project work still uses normal Mode-C authority and does not restart planning.
- Good: active parallel ownership can be detected before an execution lane is created.
- Good: future operator surfaces can expose the compiled interpretation before Controller admission without becoming another orchestrator.
- Good: target renderers can change without changing semantic authority.
- Bad: a real authority/currentness resolver is still required before fully automatic intent-to-work admission is proven.
- Bad: PROGRAMSTART documentation should gradually disambiguate overloaded uses of the word `mode` when touched for other reasons.
- Neutral: existing Prompt Builder Mode B remains useful as a historical renderer precursor but is not the canonical intent compiler.
- Neutral: the V0.1 standalone compiler CLI remains a test/developer harness rather than the final operator interface.

## Confirmation

This decision is considered implemented for V0.1 when:

- the compiler emits a sealed Work Packet projection rather than treating a long prompt as canonical;
- real continuation, audit, and architecture examples preserve their existing project-entry semantics;
- parallel ownership changes compilation output before Controller admission;
- unresolved intent fails narrow;
- renderer output cannot widen the canonical packet;
- the Controller integration consumes the compiled packet and independently performs admission;
- future operator-facing CLI/product integration prefers an `intent-compile` / intent-ingress operation or subcommand instead of `--mode d` and does not require Graham to hand-author the authority snapshot.

## Links

- [Prompt Builder Mode B decision](0021-prompt-builder-mode-b-context-driven-generation.md)
- [Mode-C authority precedence](0024-rank-current-product-authority-over-legacy-repository-evidence.md)
- [PROGRAMBUILD playbook](../../PROGRAMBUILD/PROGRAMBUILD.md)
- [Intent compilation V0.1 experiment](../experiments/INTENT_COMPILATION_WORK_PACKET_V0.md)
