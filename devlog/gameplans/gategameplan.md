# Gate Repair Gameplan — Truthful Quality Gates Before More Feature Work

Purpose: Restore trust in PROGRAMSTART's quality gates before any further hardening or feature execution resumes. This plan aligns direct commands, pre-commit hooks, prompt lint policy, pyright scope/environment, and repo-state verification. It exists because the repo currently presents contradictory signals: `validate`, direct `drift`, and pytest pass, while `pre-commit --all-files` fails for reasons that are partly latent policy mismatch rather than newly introduced feature regressions.
Status: **NOT STARTED**
Authority: Non-canonical working plan derived from live gate output on 2026-04-14, `.pre-commit-config.yaml`, `scripts/lint_prompts.py`, `tests/test_lint_prompts.py`, `pyproject.toml`, and `config/process-registry.json` sync rules.
Last updated: 2026-04-14

Recommended operator prompt: `.github/prompts/execute-gate-gameplan.prompt.md`

---

## 1. Problem Statement

PROGRAMSTART does **not** currently have a single trustworthy definition of "green".

Current observed state:

- `uv run programstart validate --check all` passes.
- `uv run programstart drift` passes.
- `uv run pytest --tb=no -q --no-header` passes with **1355 passed, 1 warning**.
- `uv run pre-commit run --all-files` fails.

This is not acceptable. A repo that can be simultaneously green and red depending on which entry point is used has a **gate integrity defect**.

### Root Cause Summary

The current failure is a composite of **three distinct gate mismatches** plus one workflow-control issue:

1. **Drift parity failure**: direct drift and pre-commit drift are not equivalent because the pre-commit hook is filename-scoped.
2. **Prompt lint scope failure**: the linter enforces structural sections on real prompts that the test suite does not verify repo-wide.
3. **Pyright environment/policy failure**: pyright is executed in an environment/scope that does not match the repo's practical runtime/test model.
4. **Dirty-tree amplification**: full `pre-commit --all-files` was run against a very broad mixed worktree, obscuring whether failures are gate debt or feature regressions.

### Operational Consequence

Until this plan is complete, statements such as "the repo is green", "the phase is done", or "all gates passed" are not reliable unless they name the exact command set used.

### Critical Interpretation

The Phase G implementation is **not** the primary problem.
The primary problem is that the repository's gate machinery is currently incapable of giving a single, credible answer.

---

## 2. Non-Negotiable Rules For This Repair

1. **Do not implement new feature work until gate integrity is restored.**
2. **Do not use `Select-Object -Last ...` to diagnose failing gate runs.** Capture the full output or targeted hook output.
3. **Do not fix gate failures by broadening exemptions unless the scope reduction is explicitly justified and documented.**
4. **Do not treat direct command success as proof that the equivalent pre-commit hook is healthy.** Prove parity.
5. **Do not treat pytest success as proof that prompt compliance or type-check policy is healthy.** The current suite does not cover those questions faithfully.
6. **Do not continue Phase H or Phase I work from the hardening gameplan until this gameplan is complete or explicitly superseded.**
7. **One gate problem class per commit.** Do not mix pyright, prompt lint, drift semantics, and unrelated feature changes.
8. **Do not "solve" a failing gate by removing that gate from pre-commit unless the replacement enforcement path is implemented in the same change set.**
9. **Do not silently narrow scope.** Any reduction in prompt-lint or pyright target set MUST be called out as a policy decision, not disguised as cleanup.
10. **Do not update dependent docs or prompts before the controlling policy/config change is decided.** Gate policy first, corpus adjustments second.

### Required Mindset

This plan assumes the repo's current convenience instinct is unsafe.

- A gate that passes only because it no longer checks the hard case is a regression, not a fix.
- A test that passes without exercising the real repo surface is documentation theater.
- A hook that disagrees with the direct command is broken until proven otherwise.
- A clean feature diff inside a dirty tree is still operationally unsafe to judge with `--all-files`.

---

## 3. Success Criteria

This gameplan is complete only when all of the following are true:

1. `uv run programstart validate --check all --strict` passes.
2. `uv run programstart drift --strict` passes.
3. `uv run pytest --tb=no -q --no-header` passes.
4. `uv run pyright` has an explicitly accepted scope and either passes or has an intentional narrowed target documented in config.
5. `uv run pre-commit run --all-files` passes from a clean worktree.
6. The same repo artifacts targeted by prompt lint are validated by tests against the **actual prompt set**, not only temporary fixtures.
7. The drift hook and direct drift command produce equivalent results for the same repo state.
8. Any narrowed pyright or prompt-lint scope is explicitly documented as intentional policy, with rationale, and no longer presented as repo-wide enforcement.
9. The hardening workflow can again use "all gates pass" as a meaningful statement without caveats about which entry point was used.

---

## 4. Scope

### In Scope

- `.pre-commit-config.yaml`
- `scripts/lint_prompts.py`
- `tests/test_lint_prompts.py`
- `tests/test_prompt_compliance.py` if needed for repo-state prompt assertions
- `pyproject.toml` pyright settings
- Prompt files under `.github/prompts/` whose policy scope is genuinely intended to match prompt lint
- Any minimal documentation/config updates required to explain the chosen gate policy
- Minimal hardening tracker updates only if needed to mark gate-repair work as blocking further hardening execution

### Out Of Scope

- New Phase H or Phase I hardening features
- Broad prompt rewrites that are unrelated to enforced lint scope
- General refactors unrelated to gate parity
- Fixing unrelated product behavior under the banner of "while we are here"
- Declaring Phase G complete while gate integrity is still unresolved

---

## 5. Known Evidence Base

The following observations are already established and should not be re-litigated unless a later command disproves them:

1. The prompt linter policy already existed by commit `df7f5e8`.
2. At least one currently failing prompt, `.github/prompts/programstart-stage-guide.prompt.md`, was already structurally non-compliant in that commit.
3. `tests/test_lint_prompts.py` does **not** lint the real prompt set for structural section compliance; it only unit-tests temp fixtures and checks `argument-hint` on actual prompt files.
4. The pre-commit pyright hook currently runs in an environment that does not include the repo's dev/test dependencies.
5. The current worktree contains many unrelated modifications, so `pre-commit --all-files` is not a clean phase-isolation signal.

---

## 6. Repair Sequence

The order below is mandatory. Do not skip ahead.

| Phase | Objective | Why First | Output |
|---|---|---|---|
| A | Freeze evidence and isolate gate surfaces | Prevent further diagnostic corruption | Baseline report and narrowed hook runs |
| B | Repair drift parity | Direct drift vs hook drift must agree before anything else | Consistent drift semantics |
| C | Repair prompt-lint truthfulness | Prompt policy and tests currently disagree | Enforced scope that matches tests and intent |
| D | Repair pyright policy/environment | Type gate is currently half tooling problem, half code debt | Credible pyright target and config |
| E | Re-run from clean tree and close the loop | Final proof that gates are trustworthy | Full all-files pass |

### Stop Conditions

Stop and re-plan if any of these occur:

1. A proposed fix requires weakening more than one gate at once.
2. A proposed fix relies on "we already know this prompt/script is fine" without adding executable proof.
3. A pyright fix starts pulling in broad unrelated typing refactors across feature modules.
4. A drift fix depends on changing registry sync rules without first proving the current hook semantics are wrong.
5. The worktree cannot be reduced to a gate-repair-only diff before final closure.

---

## 7. Detailed Phases

### Phase A: Evidence Freeze And Isolation

**Goal**: Stop diagnosing from mixed signals and establish reproducible per-hook truth.

#### A-1: Capture untailored baseline output

Run each gate directly, with full output saved if needed:

```powershell
uv run programstart validate --check all --strict
uv run programstart drift --strict
uv run pytest --tb=no -q --no-header
uv run pyright
uv run pre-commit run programstart-drift --all-files
uv run pre-commit run prompt-lint --all-files
uv run pre-commit run pyright --all-files
```

**Critical direction**:

- Do **not** tail or truncate these commands for diagnosis.
- For each failing hook, record whether the failure reproduces outside pre-commit.
- If a hook fails only inside pre-commit, treat that as a **hook-design defect candidate**.
- If a direct command fails but the equivalent hook passes, treat that as a **false-green defect candidate**.

**Required output**:

Produce a short evidence table with one row per gate:

| Gate | Direct command result | Pre-commit hook result | Same semantics? | Notes |
|---|---|---|---|---|

Do not proceed to Phase B until this table exists.

#### A-2: Separate dirty-tree noise from gate-policy failures

Before changing gate config, identify which changed files are:

- genuinely related to gate repair,
- unrelated formatting churn,
- in-progress feature work.

**Critical direction**:

- Do not attempt final all-files closure from a dirty mixed tree.
- This phase is complete only when each active failure is assigned to one of these buckets:
  - policy mismatch,
  - environment mismatch,
  - real repo defect,
  - unrelated in-flight change.
- If a failure cannot be assigned confidently, keep it open and do not bury it under a broader bucket like "tooling weirdness".

**Verification**:

- A short written baseline note exists in the commit/PR context or devlog summary.
- Each failing hook has been reproduced in isolation.

**Exit criterion**:

Do not start Phase B until the failure inventory is stable enough that a new command run is not materially changing the diagnosis.

---

### Phase B: Drift Parity Repair

**Goal**: Make direct drift and pre-commit drift mean the same thing.

#### B-1: Inspect hook semantics

Read `.pre-commit-config.yaml` and compare:

- direct drift invocation,
- pre-commit drift invocation,
- `pass_filenames` behavior,
- file regex scope.

Current suspicion: filename-scoped pre-commit drift is producing stricter or materially different behavior than direct drift.

#### B-2: Choose one truth model

Acceptable outcomes are only:

1. **Parity model**: pre-commit drift is changed to evaluate the same repo-wide state as direct drift.
2. **Explicitly narrower model**: pre-commit drift remains scoped, but direct drift is documented as a different diagnostic and tests explicitly verify the divergence.

**Critical direction**:

- Prefer **parity model**.
- Do **not** keep two differently named behaviors under the same "drift" label without explicit documentation and tests.
- Do **not** weaken sync-rule enforcement to make filename-scoped drift appear consistent. Fix invocation semantics first.

#### B-3: Add regression proof

Add or update tests so a future hook config change cannot silently reintroduce drift semantic mismatch.

Minimum proof required:

1. one assertion about hook configuration semantics,
2. one assertion about direct-command behavior,
3. one assertion that the intended relationship between them is stable.

**Verification**:

```powershell
uv run programstart drift --strict
uv run pre-commit run programstart-drift --all-files
```

Expected: both agree for the same clean repo state.

**Exit criterion**:

Do not start Phase C while drift still has two competing meanings.

---

### Phase C: Prompt-Lint Truthfulness Repair

**Goal**: Align prompt lint policy, exempt set, actual prompt corpus, and tests.

#### C-1: Decide intended lint scope

Classify `.github/prompts/*.prompt.md` into categories:

- prompts that **must** follow the full structural standard,
- prompts that are public but utility/operator-facing and should be exempt,
- prompts that need to be upgraded to the standard.

**Critical direction**:

- Do **not** exempt prompts simply because they fail today.
- Exempt only when the prompt's purpose genuinely differs from the enforced structural standard.
- If a prompt is operator-facing and should be governed, fix the prompt rather than weakening the linter.
- If a prompt category is exempted, the exemption reason MUST be stated in the linter code or adjacent test comments in concrete terms, not as "legacy" or "special case".

#### C-2: Make tests check the real repo state

Repair the test gap:

- `tests/test_lint_prompts.py` must validate repo-real structural compliance for the intended lint target set.
- If `tests/test_prompt_compliance.py` is the better home for repo-real assertions, use it, but one test suite must own the real prompt corpus.

**Critical direction**:

- Temp-file unit tests are insufficient.
- A passing pytest suite must mean the real prompt set is compatible with the enforced lint policy.
- The repo-real prompt test MUST enumerate exactly which prompts are governed and why; implicit globbing with hidden exemptions is not sufficient.

#### C-3: Resolve failing prompts intentionally

For each currently failing prompt, choose one of two actions:

1. bring it up to the required structure, or
2. exempt it with written rationale.

No third option.

Selection rule:

- If the prompt is part of `workflow_guidance.kickoff`, `workflow_guidance.cross_cutting_prompts`, or stage/phase guidance in `config/process-registry.json`, default to **upgrade**, not exemption.
- If the prompt is a utility/helper prompt outside the stage protocol model, exemption is acceptable only with rationale.

Additional rule:

- If upgrading a prompt would materially change operator workflow, treat that as a policy decision and record it before editing multiple prompts.

**Verification**:

```powershell
uv run python scripts/lint_prompts.py .github/prompts/*.prompt.md
uv run pytest tests/test_lint_prompts.py tests/test_prompt_compliance.py -q --tb=no
uv run pre-commit run prompt-lint --all-files
```

Expected: direct linter, tests, and hook agree.

---

### Phase D: Pyright Policy And Environment Repair

**Goal**: Make pyright a credible gate instead of a mixed pile of environment noise and latent type debt.

#### D-1: Split failures into categories

Current pyright failures contain at least four classes:

- missing dev/test imports (`pytest`, `nox`),
- missing optional imports (`playwright`, `PIL`, maybe `jsonschema` source resolution),
- genuine type issues in production scripts,
- type looseness or test shim issues.

Do not treat all of these as one problem.

#### D-2: Decide pyright contract

Choose one explicit model:

1. **Full dev-aware model**: pyright runs where dev deps are importable and checks scripts/tests/noxfile.
2. **Narrow production model**: pyright scope excludes tests and optional-tool scripts not intended for strict type enforcement.

**Critical direction**:

- Do not keep a hook that claims to type-check tests if the environment cannot import test dependencies.
- Do not hide real production type errors by broadly excluding `scripts/`.
- Prefer a deliberate production-first scope if full dev-aware pyright is too expensive for pre-commit.
- If the chosen model differs between local development and pre-commit, document that explicitly and rename the gate if needed; do not reuse the unqualified label `pyright` for two different policies.

#### D-3: Make pyright reproducible outside pre-commit

After config changes, the following must tell the same story:

```powershell
uv run pyright
uv run pre-commit run pyright --all-files
```

If they differ, the repair is not complete.

#### D-4: Triage real type debt

Once environment/policy noise is removed, create a separate backlog for remaining real type defects.

**Critical direction**:

- Do not fold broad type-cleanup into this same commit if it expands beyond gate repair.
- If many genuine type errors remain after scope/environment repair, capture them as a follow-on plan instead of hiding them.
- The existence of genuine type debt is acceptable; pretending the current hook is already measuring it accurately is not.

**Verification**:

- direct pyright and pre-commit pyright produce equivalent results,
- the scope is documented in config/comments if narrowed,
- optional dependencies are handled intentionally rather than accidentally.

**Exit criterion**:

Do not start Phase E if pyright still requires verbal caveats like "ignore the missing imports" or "the hook is noisier than the real run".

---

### Phase E: Clean-Tree Closure

**Goal**: Prove that the repaired gates work from a clean and controlled repo state.

#### E-1: Isolate gate-repair changes

Before final verification:

- separate unrelated feature work,
- separate formatter-only churn,
- ensure the working tree contains only gate-repair edits.

#### E-2: Run the full closure set

```powershell
uv run programstart validate --check all --strict
uv run programstart drift --strict
uv run pytest --tb=no -q --no-header
uv run pyright
uv run pre-commit run --all-files
```

**Critical direction**:

- If any command still disagrees materially with its hook counterpart, stop and fix the contract before closing the phase.
- Do not declare success on a subset.
- Record the exact clean-tree SHA or working tree state used for closure so later failures cannot be hand-waved as "probably the same baseline".

**Closure rule**:

- Only after this phase passes may the hardening workflow resume Phase G closure or later phases.
- If the gate repair changes expose substantial follow-on debt, create a new dedicated follow-up plan before returning to normal hardening execution.

---

## 8. Deliverables

This gameplan should produce the following outputs when executed:

1. A repaired `.pre-commit-config.yaml` with explicit, coherent hook semantics.
2. Prompt lint policy and tests that validate the real prompt corpus.
3. A documented pyright contract with matching direct and hook behavior.
4. A clean full-gate pass from a controlled working tree.
5. Updated hardening/gameplan status notes only after the gate layer is trustworthy.
6. A short post-repair note stating which earlier assumptions were false and what guard now prevents recurrence.

---

## 9. Anti-Patterns To Avoid

- "Just exempt the prompt set so pre-commit passes."
- "Just tail the last 40 lines and infer the cause."
- "Just keep using direct drift because it passes."
- "Just ignore pyright because pytest is green."
- "Just continue Phase H/I and circle back later."
- "Just run pre-commit on the dirty feature tree and blame the current phase."
- "Just mark the prompt/helper as exempt because it is easier than deciding the intended policy."
- "Just accept different local and hook behavior because both are useful."
- "Just treat optional dependency import failures as proof that type-checking is working."

Each of these would preserve the exact broken behavior that caused this incident.

---

## 10. Recommended Commit Strategy When Executing This Plan

1. `fix(gates): align drift hook semantics with direct drift`
2. `fix(prompts): align prompt lint scope and repo-real tests`
3. `fix(typecheck): align pyright scope or environment with repo policy`
4. `chore(gates): close gate repair with clean all-files verification`

Do not collapse these into one commit unless the diff is trivially small.

If a separate documentation/policy commit is needed before code changes, prefer:

`docs(gates): define prompt lint and typecheck policy boundaries`

---

## 11. Exit Decision

After this gameplan completes, decide one of two paths:

1. Resume Phase G closure if the gate layer is now trustworthy.
2. If real pyright/type debt remains substantial, create a dedicated type-hardening follow-up before resuming later hardening phases.

The repo should not return to normal feature-phase execution until this decision is explicit.
