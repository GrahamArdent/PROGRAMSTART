# CI failure-pattern audit: shift-left quality publication

**Date:** 2026-09-04
**Classification:** systemic methodology improvement / implemented, real retest pending
**Candidate lesson:** `PSL-022`
**Status:** subordinate acceptance evidence; do not treat as validation

## Observation

A recent cross-repository sample shows that GitHub Actions is frequently the first executable surface to discover deterministic failures that the owning repository already knows how to detect locally. The evidence does **not** support a universal linter/toolchain. It supports one semantic publication contract whose concrete checks remain repository-owned.

The failure sample below is deliberately descriptive rather than statistical. It is recent and biased toward active repositories with visible repeated CI work; several entries are successive attempts in the same incident. Historical failure totals are therefore context, not a denominator for extrapolating these percentages across all GrahamArdent repositories.

## Failure taxonomy

- **A — auto-fixable before commit:** deterministic formatter/linter/whitespace mutations.
- **B — deterministically detectable before push:** repository guard, schema, generated-state, build or other deterministic check that should reject publication before GitHub.
- **C — environment-specific but reproducible:** clean-runner/toolchain/setup behavior that may require environment parity rather than an ordinary local hook.
- **D — external/transient:** provider/network/GitHub or another non-deterministic external failure.
- **E — genuine implementation/test-contract failure:** CI is correctly rejecting behavior. These failures are valuable, but when the same deterministic test can run before publication they should normally become a local rejection rather than the first remote red run.

## Recent sample

| Repository | Run | Primary class | Evidence / failure family | Shift-left assessment |
|---|---:|---|---|---|
| `GrahamArdent/PROGRAMSTART` | `33842179952` | A | Ruff fixed 2 lint errors and reformatted 2 files; security/type checks passed | should have been incorporated before publication |
| `GrahamArdent/PROGRAMSTART` | `33842055355` | A | trailing whitespace fixed; Ruff fixed 2 errors and reformatted 2 files | should have been incorporated before publication |
| `GrahamArdent/PROGRAMSTART` | `33841487050` | A+B mixed | whitespace mutation, Ruff mutation/formatting, remaining E501 findings, detect-secrets high-entropy fixture flags | deterministic local gate should have rejected candidate before publication |
| `GrahamArdent/repo-watchtower` | `33434814063` | C | Node/pnpm cache setup failed while resolving pnpm store/package metadata | reproducible toolchain parity issue; not a Ruff/formatting problem |
| `GrahamArdent/repo-watchtower` | `33434691011` | C | toolchain verification failed | same incident family; avoid counting as independent architecture evidence |
| `GrahamArdent/repo-watchtower` | `33434436318` | C | dependency installation failed | same toolchain/dependency incident family |
| `GrahamArdent/programstart-autonomous-controller` | `33842587991` | E | deterministic unit/integration contract failure in rollback-safety expectation | valid failure; same tests should reject locally before publication where executable |
| `GrahamArdent/programstart-autonomous-controller` | `33840141672` | E | unit/integration test stage failed | valid deterministic test rejection |
| `GrahamArdent/execution-node-control` | `33832191409` | B | 254 tests passed, then dangerous-primitive guard referenced a removed file and raised `FileNotFoundError` | deterministic repo guard should reject before publication |
| `GrahamArdent/execution-node-control` | `33831515603` | E | unit tests failed after source compilation | valid deterministic test rejection |
| `GrahamArdent/programstart-compute-spine` | `33841091089` | E | unit/cross-layer tests failed after setup/compile | valid deterministic test rejection |
| `GrahamArdent/evidence-spine` | `33841925649` | E | deterministic tests failed before derived-state verification | valid deterministic test rejection |
| `GrahamArdent/secrets-control-plane` | `33825802706` | E | resolver compiled, resolver tests failed | valid deterministic test rejection |
| `GrahamArdent/GCRM` | `33833880365` | A | setup, drift, typecheck, lint and seed checks passed; format check failed | formatting should be corrected before publication |
| `GrahamArdent/resume-creator-v6` | `33841654586` | E | frontend deterministic unit tests and backend deterministic purpose lane failed | valid deterministic test rejection |
| `GrahamArdent/Dedication` | `33320840960` | E | Android SDK/JDK/Gradle setup passed; debug test/build step failed | valid deterministic build/test rejection |

## Descriptive result

For these **16 sampled failed runs**:

- primary A auto-fixable failures: **3 / 16 = 18.75%**;
- mixed A+B deterministic hygiene/security/lint failure: **1 / 16 = 6.25%**;
- B deterministic repository-guard failure: **1 / 16 = 6.25%**;
- C environment/toolchain failures: **3 / 16 = 18.75%**;
- D external/transient failures: **0 / 16 = 0%**;
- E genuine implementation/test-contract failures: **8 / 16 = 50%**.

Formatting/whitespace or deterministic source mutation was a material component in **4 / 16 = 25%** of the sample.

More importantly, **13 / 16 = 81.25%** of sampled remote-red runs were caused by checks that are deterministic and, in principle, executable before publication using the owning repository's own formatter/linter/test/build/guard contract. This does **not** mean 81.25% of the changes were invalid or trivial: eight were legitimate implementation/test failures. The avoidable waste is making GitHub the first place those deterministic failures are discovered.

The remaining three Watchtower runs are a clustered clean-environment/toolchain incident. They support environment-parity checks but do not justify forcing every repository to reproduce the hosted runner locally.

## Existing tooling / ownership evidence

### PROGRAMSTART

PROGRAMSTART already has the necessary Python hygiene stack rather than a missing-linter problem:

- `.pre-commit-config.yaml` owns EOF/trailing-whitespace, Ruff fix/format, Bandit, detect-secrets, yamllint, Pyright, schema and PROGRAMSTART-specific checks;
- `noxfile.py` exposes `lint`, `typecheck`, `tests`, `validate`, smoke, docs and the existing `gate_safe` local pre-merge confidence gate;
- `CONTRIBUTING.md` already documented local setup and the full `nox -s ci` gate;
- the existing custom `scripts/hooks/pre-push` protected direct pushes to `main` but did not execute quality validation.

The proven gap is therefore **invocation/enforcement before publication**, not the absence of Ruff or another GitHub Action.

### Repository-specific contracts

The ecosystem is intentionally heterogeneous. For example, Watchtower's `package.json` owns a TypeScript contract (`pnpm check` -> typecheck + Vitest + build), while GCRM's hosted quick-quality lane separately runs drift, typecheck, lint, format and tests, Resume Creator has frontend/backend deterministic lanes, and Dedication has an Android/Gradle build-test contract.

That evidence rejects a single cross-repository tool list. Repository ownership of concrete commands must remain intact.

## Architectural decision

**Hypothesis accepted with a narrowing:**

> The ecosystem should have one semantic publication contract, not one universal validation toolchain.

The semantic sequence is:

`edit -> deterministic fix -> local validation -> commit -> pre-push validation -> GitHub authoritative verification`

Rules:

1. The owning repository defines the concrete formatter/linter/type/test/build/guard commands.
2. Deterministic tools that modify files are allowed to do so only before publication; the worker inspects/incorporates the result and reruns the gate.
3. Autonomous auto-fix retries are bounded. Two deterministic mutation passes is the current maximum before diagnosis rather than an unbounded green-seeking loop.
4. Semantic/test failures are never suppressed or converted into formatting noise.
5. GitHub Actions remains independent and authoritative; it is not changed into an arbitrary source-mutating auto-commit bot.
6. Git hooks are enforcement for normal Git CLI paths, not evidence that API/connector mutations were locally validated. API/direct file writers must explicitly run the equivalent repository contract on an executable candidate when that capability exists. If it does not exist, the worker records the limitation and relies truthfully on GitHub CI rather than claiming a local pass.
7. Watchtower may observe/classify recurring CI evidence, but it does not become the CI execution or remediation engine.

## Bounded implementation

Branch: `methodology/shift-left-quality-gate`

Changes:

- `scripts/hooks/pre-push`
  - retains direct-main protection;
  - changes `PROGRAMSTART_ALLOW_MAIN_PUSH=1` to bypass branch policy only, not quality validation;
  - invokes the already-existing `uv run nox -s gate_safe` before publication;
  - blocks publication if the local confidence gate fails.
- `.github/instructions/source-of-truth.instructions.md`
  - owns the semantic clean-candidate publication sequence;
  - keeps concrete validation repository-owned;
  - requires explicit candidate validation for hook-bypassing API/connector paths when an executable surface exists;
  - requires truthful degraded-mode evidence when it does not.
- `.github/copilot-instructions.md`
  - makes the publication rule an always-on worker expectation;
  - bounds deterministic auto-fix to two mutation passes;
  - forbids semantic/test/security/build suppression for green-seeking.
- `QUICKSTART.md`
  - keeps the JIT dependent surface aligned;
  - names PROGRAMSTART's existing `pre-commit` and `gate_safe` commands without universalizing them to other repositories.
- `tests/test_pre_push_quality_gate.py`
  - proves feature publication invokes the repository-owned gate;
  - proves gate failure blocks publication;
  - proves direct-main protection still occurs;
  - proves the main-policy override does not bypass the quality gate;
  - statically proves the worker/JIT/Quick Start surfaces retain the hook-bypassing publication contract.
- `CONTRIBUTING.md`
  - makes deterministic pre-commit preparation explicit;
  - defines bounded deterministic auto-fix behavior;
  - requires `gate_safe` before push;
  - records the API/connector bypass limitation;
  - preserves GitHub as independent authoritative verification.

No new linter, CI service, repository, Watchtower execution responsibility, provider, credential or hosted auto-remediation was added.

## Self-hosting Challenge evidence

The implementation path reproduced the exact defect under investigation. This branch was mutated through the GitHub connector, so the new local Git hook could not run. Initial PR validation then found trailing whitespace and Ruff formatting mutations in the candidate. Subsequent connector corrections removed those deterministic mutations before later validation stages could be exercised.

That does **not** validate `PSL-022`; it demonstrates the API-path boundary. It also disproves the idea that adding only a Git hook could be ecosystem closure. The methodology therefore now makes candidate preparation an execution-path responsibility as well as a normal Git-hook responsibility.

## Challenge before validation

The implementation must be challenged against these failure sequences before promotion:

1. **Expensive-hook escape:** if `gate_safe` is so expensive that workers routinely bypass it, the change has moved friction rather than reduced it. Counterevidence would justify narrowing the pre-push set, but the present sample shows tests/guards account for most deterministic reds, so a formatting-only hook is insufficient.
2. **API bypass:** direct GitHub/API commits never execute `.git/hooks/pre-push`. The JIT and worker instructions now require explicit candidate validation where an executable environment exists and truthful degraded-mode evidence where it does not. This closes the methodology/instruction gap, but a connector with no candidate-execution capability still cannot manufacture a local validation run.
3. **Green-seeking auto-fix loop:** repeated formatter mutation must not become unbounded retries or suppression. The two-pass bound preserves diagnosis.
4. **False CI replacement:** a local pass must not be treated as remote acceptance. Branch protection and `Required PR Gate` remain unchanged.
5. **Wrong universal tools:** Watchtower's pnpm/toolchain evidence proves Ruff cannot be generalized across repositories. Only the semantic contract is shared.
6. **Direct-main override regression:** an authorized branch-policy override must still execute validation; regression tests explicitly cover this case.
7. **Instruction-only false enforcement:** worker instructions are necessary but are not evidence that an execution environment actually ran the repository contract. Future autonomous publication evidence must distinguish instruction availability from executable gate evidence.

## Learning disposition

This is a reusable methodology signal and is reserved as candidate `PSL-022`; `PSL-021` is already in use by the effective-autonomy observation/workstream. `PSL-022` is **implemented / not validated** until a real autonomous publication retest proves that a previously remote-first deterministic failure is stopped before GitHub publication without creating material bypass behavior or excessive friction.

## Real retest condition

Use the next natural PROGRAMSTART-controlled repository publication where:

- a deterministic formatter/linter/test/build/guard failure exists before push;
- the available execution path can run the repository-owned local validation contract;
- the failure is rejected and corrected before remote publication;
- the final candidate then reaches GitHub and is independently verified;
- no worker bypasses the gate merely because it is inconvenient.

For an API/connector-only mutation path, record whether an executable candidate-validation surface exists. If it does not, this change must not be credited with preventing that remote-first failure.