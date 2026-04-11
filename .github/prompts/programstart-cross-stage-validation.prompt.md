---
description: "Validate that the current stage's outputs are consistent with all previous stage outputs. Use at any stage transition to catch contradictions, scope drift, and assumption decay before they compound."
name: "Cross-Stage Validation"
argument-hint: "Current stage number or name, and the previous outputs to validate against"
agent: "agent"
---
Run the cross-stage validation checks from `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md` for the current stage transition.

Tasks:

1. Identify the current stage and the stage being entered.
2. Open `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md` and locate the Cross-Stage Validation checklist for the target stage.
3. Read each upstream document referenced in the validation (inputs block, FEASIBILITY.md, REQUIREMENTS.md, ARCHITECTURE.md, etc.).
4. For each validation check:
   - State the check.
   - Read the relevant content from both the current stage output and the upstream document.
   - Report whether the check passes, fails, or raises a warning.
   - If it fails, name the specific contradiction and recommend a resolution.
5. Produce a summary table:

| Check | Source | Target | Status | Notes |
|---|---|---|---|---|
| (check description) | (upstream doc) | (current doc) | ✅ / ⚠️ / ❌ | (detail) |

6. If any check is ❌, state clearly: **do not proceed to the next stage until this is resolved.**
7. If all checks pass, confirm the transition is safe.

Do not skip checks. Do not accept "probably fine" as evidence. Read the actual text.
