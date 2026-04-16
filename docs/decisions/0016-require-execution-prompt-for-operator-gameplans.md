---
status: accepted
date: 2026-04-16
deciders: [Solo operator]
consulted: []
informed: []
---

# 0016. Require execution prompt for operator gameplans

<!-- DEC-013 -->

## Context and Problem Statement

PROGRAMSTART maintains multi-phase gameplans in `devlog/gameplans/`. Some of these gameplans have corresponding `execute-*` operator prompts that enforce JIT protocol, scope guards, verification gates, and governance close-out loops during execution. Others do not.

No written rule defined when a gameplan requires an execution prompt and when it does not. The de facto pattern was that every operator-scoped gameplan got one — but the rationale was implicit, and two categories of gameplan were legitimately exempt without explanation.

During hardening gameplan Phase G, the execution prompt actively impeded work: its verification protocol required all gates to pass, but Phase G exposed that the gate infrastructure itself was broken. The prompt's scope guard forbade "broad cleanup not tied to a hardening finding," so fixing the gates was out of scope — yet the prompt's own Step 6 made Phase G uncompletable without those fixes. A separate gate-repair gameplan was created to escape that deadlock.

This incident demonstrates that execution prompts are not universally beneficial. When a gameplan repairs the systems that an execution prompt's protocol depends on, the prompt creates a circular dependency that actively harms execution.

## Decision Drivers

- Execution prompts enforce JIT, scope guards, and verification — they make multi-phase work predictable and resumable.
- When a gameplan repairs the infrastructure the prompt relies on (gates, prompts, CI), the prompt's protocol creates a deadlock.
- Bootstrap gameplans that create the prompt system itself cannot have a prompt that conforms to a standard that does not yet exist.
- The repo should enforce the pairing automatically, not rely on memory.
- Exempt gameplans should declare their exemption explicitly, not by omission.

## Considered Options

- Option A — Require an execution prompt for every gameplan, with no exceptions.
- Option B — Require an execution prompt for operator gameplans by default; codify explicit exemption criteria; enforce via validation.
- Option C — Continue with the implicit de facto pattern and no enforcement.

## Decision Outcome

Chosen option: **Option B**, because it captures the benefit of execution prompts for the common case while codifying the legitimate exemptions discovered during hardening.

### Approved Decisions

1. **Default: every operator gameplan MUST have an execution prompt.**
   Any multi-phase gameplan in `devlog/gameplans/` that is referenced by an operator prompt entry in `config/registry/prompting.json`, or that describes work of operator scope (maintenance, repair, hardening, migration, audit), MUST have a corresponding `execute-*` prompt registered in `operator_prompt_files`.

2. **Exemption: infrastructure-repair gameplans.**
   A gameplan whose primary purpose is repairing the systems that execution prompts depend on (quality gates, prompt lint, CI pipeline, pre-commit hooks) is EXEMPT. Such gameplans repair the verification surface that every execution prompt's protocol relies on — requiring the prompt to pass its own broken gates creates a circular dependency. The exemption MUST be declared in the gameplan header with the field `Prompt: exempt — infrastructure-repair`.

3. **Exemption: bootstrap gameplans.**
   A gameplan that creates or establishes the prompt system, prompt standard, or prompt architecture for the first time is EXEMPT. The prompt standard cannot govern a prompt that bootstraps the standard itself. The exemption MUST be declared in the gameplan header with the field `Prompt: exempt — bootstrap`.

4. **Exemption: internal stage gameplans.**
   Gameplans scoped to a single PROGRAMBUILD stage (`stage2gameplan.md`, etc.) that use internal `implement-*` prompts in `.github/prompts/internal/` are NOT operator gameplans and are therefore outside the scope of this rule. They are governed by their own internal prompt convention.

5. **Exemption: experimental/working artifacts.**
   Files in `devlog/gameplans/` that are experimental run configurations, mutation test artifacts, or similar working documents — not multi-phase execution plans — are outside scope. These SHOULD be clearly named to avoid confusion (e.g., `*_prompt.md`, `*_config.md`).

6. **Machine-readable enforcement.**
   `config/registry/prompting.json` MUST include a `gameplan_prompt_policy` section that maps gameplan paths to their prompt status. `programstart validate --check prompt-authority` (or a new `--check gameplan-prompt-pairing`) MUST fail when an operator gameplan is missing its execution prompt without a declared exemption.

7. **Exemption field in gameplan header.**
   Exempt gameplans MUST declare the exemption in their metadata header using the pattern:
   ```
   Prompt: exempt — <reason>
   ```
   Valid reasons: `infrastructure-repair`, `bootstrap`.

### Consequences

- Good: Operator gameplans get execution prompts by default, enforcing JIT protocol, scope guards, and verification.
- Good: Legitimate exemptions are codified and machine-checked, not implicit.
- Good: The Phase G deadlock pattern is documented and prevented.
- Good: Internal stage gameplans and experimental artifacts are explicitly excluded.
- Bad: Existing exempt gameplans need a one-time header update.
- Neutral: The validation check adds a small amount of complexity to the validate surface.

## Pros and Cons of the Options

### Option A

- Good, because universally applied rules are simple.
- Bad, because the Phase G deadlock proves the rule cannot be universal — infrastructure-repair gameplans create circular dependencies with their own execution prompt.

### Option B

- Good, because it matches the observed pattern and codifies the exceptions.
- Good, because machine enforcement catches omissions.
- Good, because exemption reasons are explicit and auditable.
- Bad, because it requires a registry addition and header convention.

### Option C

- Good, because it requires no changes.
- Bad, because the pairing is not enforced, gameplans can silently lack prompts, and the next developer has to rediscover the Phase G lesson.

## Related Decisions

- ADR-0011: Separate workflow and operator prompt architecture (defines operator prompt class).
- ADR-0013: Require governance close-out loop for durable operator checkpoints (operator prompts must enforce governance).
- DEC-008: Operator prompt architecture separation (DECISION_LOG.md).
