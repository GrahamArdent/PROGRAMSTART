# Prompt Architecture Remediation Gameplan

Purpose: Architecture-first remediation plan for separating workflow prompts, operator prompts, and internal prompts in PROGRAMSTART without weakening source-of-truth guarantees or leaking PROGRAMSTART-only maintenance behavior into future generated repositories.
Status: **COMPLETE**
Authority: Non-canonical working plan derived from [docs/decisions/0011-separate-workflow-and-operator-prompt-architecture.md](../../docs/decisions/0011-separate-workflow-and-operator-prompt-architecture.md), [PROGRAMBUILD/DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md) `DEC-008`, the frozen prompt classification matrix, and current prompt validation wiring.
Last updated: 2026-04-15

---

## 1. Current State

Baseline recorded 2026-04-15:

- `uv run programstart validate --check all` PASSES
- `uv run programstart drift` PASSES
- Prompt architecture decision `ADR-0011` ACCEPTED
- Prompt inventory is fully classified with no miscellaneous bucket
- No prompt requires pre-gameplan splitting

### Frozen Classification

| Class | Count | Disposition |
|---|---|---|
| `workflow` | 21 | Stay workflow; remain eligible for workflow guidance and routing |
| `operator` | 5 | Four frozen operator prompts plus one remediation execution prompt; all remain outside workflow routing |
| `internal` | 15 | Stay internal and exempt from public prompt standards |

### Frozen Borderline Decisions

These classifications are frozen and MUST NOT be reopened during implementation unless validated code or accepted ADRs force a change:

- `.github/prompts/product-jit-check.prompt.md` = `workflow`
- `.github/prompts/propagate-canonical-change.prompt.md` = `workflow`

### Frozen Operator Prompt Set

These prompts are the only prompts that MUST move out of workflow-governed standards and workflow-routing registry semantics:

- `.github/prompts/execute-hardening-gameplan.prompt.md`
- `.github/prompts/execute-gate-gameplan.prompt.md`
- `.github/prompts/execute-enhancement-gameplan.prompt.md`
- `.github/prompts/audit-process-drift.prompt.md`

### Explicit Non-Decisions

- No prompt is split in this remediation plan.
- No prompt is physically moved on disk in the first pass unless a later phase proves the move is necessary.
- `devlog/` remains non-canonical throughout.

---

## 2. Governing Constraints

Implementation MUST follow these accepted constraints from ADR-0011:

1. `workflow`, `operator`, and `internal` are explicit architecture classes.
2. Only `workflow` prompts may participate in workflow routing.
3. Prompt discoverability and workflow routing must be modeled separately.
4. Workflow prompts and operator prompts require separate standards.
5. `devlog/` gameplans remain non-canonical execution artifacts.
6. Prompt class must be machine-enforced through validation.
7. Generated repositories must not inherit PROGRAMSTART-only operator prompts by accident.

If any implementation idea conflicts with these constraints, STOP and update the authority docs first instead of improvising.

---

## 3. Success Criteria

The remediation is complete only when all of the following are true:

1. A documented prompt taxonomy exists and is reflected in repo behavior, not only prose.
2. Workflow routing surfaces expose only workflow prompts.
3. Operator prompts are discoverable without being treated as stage-routing prompts.
4. Workflow and operator prompts are validated against different structural standards.
5. Internal prompts remain exempt and are not accidentally pulled into public prompt compliance checks.
6. The four operator prompts are no longer governed by workflow-only assumptions in standards or registry layout.
7. Generated-repo export/bootstrap logic has an explicit policy boundary for prompt classes.
8. `validate`, `drift`, and prompt-related tests all pass after migration.

---

## 4. Out of Scope

These items are explicitly out of scope unless a later accepted decision changes the boundary:

- Changing PROGRAMBUILD stage order
- Changing USERJOURNEY delivery order
- Changing route/state authority docs for product behavior
- Treating `devlog/` as canonical
- Broad unrelated refactors in `scripts/` or `tests/`
- Splitting prompts without evidence that a split is necessary
- Exporting PROGRAMSTART operator prompts into generated repositories by default

---

## 5. Workstream Sequence

The sequence is architecture-first. Do not reorder it.

| Phase | Workstream | Goal | Primary Outputs |
|---|---|---|---|
| A | Standards split | Separate workflow and operator prompt standards | Updated prompt standard docs |
| B | Registry refactor | Separate prompt discoverability from workflow routing | Updated `config/process-registry.json` model |
| C | Validation refactor | Make prompt class machine-enforced | Updated linter/tests/validation wiring |
| D | Workflow prompt alignment | Align workflow prompts and workflow-facing registry surfaces | Updated workflow prompt metadata and compliance |
| E | Operator prompt alignment | Align operator prompts to operator standard and registry surface | Updated operator prompts and tests |
| F | Inheritance/export boundary | Prevent accidental export of PROGRAMSTART-only operator prompts | Updated bootstrap/factory policy and tests |
| G | Closeout | Final ADR/doc/test consistency check | Green validation and documented completion |

---

## 6. Detailed Phase Instructions

### Phase A: Standards Split

**Status**: COMPLETE
**Result**: Narrowed `.github/prompts/PROMPT_STANDARD.md` to workflow prompts, created `.github/prompts/OPERATOR_PROMPT_STANDARD.md`, and updated `audit-process-drift.prompt.md` to reference the operator standard rather than workflow-standard exemptions.

**Goal**: Replace the current mixed public prompt standard with a clean two-standard model.

**Must do**:

1. Narrow `.github/prompts/PROMPT_STANDARD.md` so it governs `workflow` prompts only.
2. Create a dedicated operator prompt standard for `operator` prompts.
3. Keep internal prompts exempt from both public standards unless a later phase intentionally opts them into some machine-readable metadata requirement.

**Must not do**:

- Do not keep one universal public standard with more carve-outs.
- Do not force operator prompts to retain workflow-routing sections just to satisfy legacy tests.

**Acceptance condition**:

- A reader can tell from standards alone which requirements apply to workflow prompts and which apply to operator prompts.

**Verification**:

```powershell
uv run pytest tests/test_lint_prompts.py tests/test_prompt_compliance.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase B: Registry Refactor

**Status**: COMPLETE
**Result**: Added top-level `prompt_registry` class inventory, renamed workflow cross-cutting surfaces to `cross_cutting_workflow_prompts`, introduced explicit operator discoverability surfaces, and updated `programstart_step_guide.py` plus tests so workflow guidance remains workflow-only by default while `--operator` exposes operator prompts intentionally.

**Goal**: Separate prompt discoverability from workflow routing in `config/process-registry.json`.

**Must do**:

1. Add explicit prompt class modeling to the registry or equivalent deterministic metadata path.
2. Ensure workflow guidance surfaces list only workflow prompts.
3. Add a distinct operator prompt surface for discoverability without stage-routing semantics.
4. Preserve current workflow guide behavior for real workflow prompts.

**Frozen move set**:

- `.github/prompts/execute-hardening-gameplan.prompt.md`
- `.github/prompts/execute-gate-gameplan.prompt.md`
- `.github/prompts/execute-enhancement-gameplan.prompt.md`
- `.github/prompts/audit-process-drift.prompt.md`

These prompts move in registry semantics only unless a later phase proves a file move is necessary.

**Must not do**:

- Do not leave operator prompts in cross-cutting workflow prompt arrays.
- Do not make operator prompt discoverability depend on workflow-stage membership.

**Acceptance condition**:

- `programstart guide` and related workflow surfaces remain workflow-only by default.

**Verification**:

```powershell
uv run pytest tests/test_programstart_step_guide.py tests/test_instruction_enforcement.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase C: Validation Refactor

**Status**: COMPLETE
**Result**: Updated `scripts/lint_prompts.py` to read prompt classes from `prompt_registry`, apply different workflow versus operator structural checks, preserve internal prompt exemption intentionally, and fail operator prompts that still include workflow-stage routing. Expanded prompt tests accordingly and aligned `product-jit-check.prompt.md` plus `execute-enhancement-gameplan.prompt.md` to the new class-aware rules.

**Goal**: Make prompt class a machine-enforced rule.

**Must do**:

1. Update prompt linting so required sections depend on prompt class.
2. Update prompt compliance tests so workflow prompts retain workflow-routing checks and operator prompts do not inherit them.
3. Add or update tests to catch wrong-class registry placement.
4. Preserve internal prompt exemption behavior intentionally rather than incidentally.

**Must not do**:

- Do not solve class differences with filename-only hacks if class metadata exists.
- Do not make operator prompt compliance weaker than necessary; it should be different, not looser by accident.

**Acceptance condition**:

- CI can fail if a workflow prompt is missing workflow routing or if an operator prompt still includes workflow-only structure requirements after migration.

**Verification**:

```powershell
uv run pytest tests/test_lint_prompts.py tests/test_prompt_compliance.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase D: Workflow Prompt Alignment

**Status**: COMPLETE
**Result**: Verified that workflow-classed prompts remain the only prompts participating in workflow guidance surfaces, kept the frozen classification for `product-jit-check` and `propagate-canonical-change`, and aligned `product-jit-check.prompt.md` with workflow prompt structural requirements so the full workflow prompt set is now lint-clean under the class-aware model.

**Goal**: Bring the 21 workflow prompts into explicit alignment with the new class-aware model.

**Workflow prompt set**:

- `shape-*` PROGRAMBUILD prompts
- `shape-uj-*` USERJOURNEY prompts
- `start-programstart-project.prompt.md`
- `programstart-stage-guide.prompt.md`
- `programstart-stage-transition.prompt.md`
- `programstart-cross-stage-validation.prompt.md`
- `programstart-what-next.prompt.md`
- `userjourney-next-slice.prompt.md`
- `product-jit-check.prompt.md`
- `propagate-canonical-change.prompt.md`

**Must do**:

1. Ensure workflow prompts remain the only prompts participating in workflow routing surfaces.
2. Preserve the frozen classification of `product-jit-check` and `propagate-canonical-change` as workflow prompts.
3. Keep current stage/phase semantics intact.

**Must not do**:

- Do not re-open classification unless a real contradiction is found.
- Do not downgrade workflow prompts into operator prompts just because they are occasionally used by developers.

**Acceptance condition**:

- Workflow prompt behavior remains stable while now being class-aware.

**Verification**:

```powershell
uv run pytest tests/test_prompt_compliance.py tests/test_programstart_step_guide.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase E: Operator Prompt Alignment

**Status**: COMPLETE
**Result**: Aligned the long-form operator execution prompts to the operator standard by adding missing scope, resumption, and completion/checkpoint sections where needed, and tightened `scripts/lint_prompts.py` so operator prompts now fail if they are missing the full long-form operator scaffold or if they reintroduce workflow-stage routing.

**Goal**: Move operator prompts onto the new operator standard without changing their core purpose.

**Operator prompt set**:

- `.github/prompts/execute-hardening-gameplan.prompt.md`
- `.github/prompts/execute-gate-gameplan.prompt.md`
- `.github/prompts/execute-enhancement-gameplan.prompt.md`
- `.github/prompts/audit-process-drift.prompt.md`

**Must do**:

1. Align operator prompts to the operator standard.
2. Remove workflow-only assumptions from their compliance surface.
3. Preserve useful operator features already learned in prior work, such as truth hierarchy, full-output diagnosis, and resumption discipline where applicable.

**Must not do**:

- Do not force these prompts to route to `programstart-stage-transition`.
- Do not split these prompts unless implementation reveals a real mixed-purpose defect.

**Acceptance condition**:

- All four operator prompts are structurally compliant under the operator model and absent from workflow-routing surfaces.

**Verification**:

```powershell
uv run pytest tests/test_lint_prompts.py tests/test_prompt_compliance.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase F: Inheritance and Export Boundary

**Status**: COMPLETE
**Result**: Added explicit generated-repo prompt export policy to the registry, filtered bootstrapped prompt assets by allowed prompt class instead of copying every public prompt, rewrote stamped project-repo prompt metadata so operator prompts are no longer advertised by default, and made validation role-aware so project repos do not require PROGRAMSTART-only operator prompt infrastructure.

**Goal**: Make prompt class affect what flows into generated repositories.

**Must do**:

1. Review bootstrap/factory logic for prompt export assumptions.
2. Ensure generated repositories receive only prompts intentionally meant for them.
3. Ensure PROGRAMSTART-only operator prompts are not exported by default.

**Must not do**:

- Do not rely on folder convention alone if export logic can use explicit class metadata.
- Do not assume all public prompts are safe for generated repos.

**Acceptance condition**:

- Generated-repo prompt inheritance is explicit and class-bounded.

**Verification**:

```powershell
uv run pytest tests/test_programstart_bootstrap.py tests/test_programstart_project_factory.py tests/test_programstart_prompt_build.py -q --tb=short
uv run programstart validate --check all
uv run programstart drift
```

---

### Phase G: Closeout

**Status**: COMPLETE
**Result**: Re-read ADR-0011 and confirmed the implementation matches the approved decisions: workflow-only routing, separate workflow versus operator standards, explicit registry class modeling, class-aware validation, and explicit generated-repo export boundaries. Final verification passed with `programstart validate`, `programstart drift`, direct `uv run --extra dev pyright`, the full pytest suite, and `pre-commit run --all-files`.

**Goal**: Verify the prompt architecture remediation is complete and internally consistent.

**Must do**:

1. Re-read ADR-0011 and confirm implementation still matches every approved decision.
2. Confirm the four operator prompts moved only in governance/registry semantics unless a later accepted change required more.
3. Confirm no prompt split was introduced unnecessarily.
4. Confirm docs, registry, validation, and inheritance policy agree.

**Final verification**:

```powershell
uv run programstart validate --check all
uv run programstart drift
uv run --extra dev pyright
uv run pytest --tb=no -q --no-header
uv run pre-commit run --all-files
```

All five MUST pass.

---

## 7. Implementation Notes

### Recommended Commit Shape

Prefer one focused commit per phase or one small pair of tightly coupled phases when separation would be artificial.

### Stop Conditions

STOP and seek clarification if any of the following happen:

- A prompt appears to require splitting to satisfy both workflow and operator requirements.
- Generated-repo inheritance rules conflict with existing factory/bootstrap contracts.
- Registry refactor would break workflow guidance without a clear compatibility path.
- A previously frozen borderline prompt can no longer be justified under its class with evidence from code or accepted docs.

### Anti-Patterns To Reject

- Adding more exemptions to preserve a broken universal prompt model
- Leaving operator prompts in workflow guidance just for discoverability
- Reopening already frozen classification calls without evidence
- Treating `devlog/` gameplans as authority docs
- Exporting PROGRAMSTART-only operator prompts into generated repos by default

---

## 8. Completion Definition

This gameplan is complete when:

- Prompt classes are explicit in repo behavior
- Workflow and operator standards are separate and enforced
- Workflow routing surfaces are workflow-only
- Operator prompts are class-correct and discoverable without route coupling
- Internal prompts remain internal
- Generated-repo prompt inheritance is explicitly bounded
- All final verification commands pass
