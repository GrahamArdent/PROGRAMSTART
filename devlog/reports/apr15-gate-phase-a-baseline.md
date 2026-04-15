# Gate Repair Phase A Baseline — 2026-04-15

Purpose: Freeze a truthful gate baseline before making any gate-policy or config changes. This report records direct command results, isolated hook results, semantic parity, and failure-bucket assignment for the active gate repair effort.
Status: **Complete** for Phase A evidence freeze.
Authority: Non-canonical working report derived from live command output on 2026-04-15.
Last updated: 2026-04-15

---

## 1. Executive Summary

The repository currently has four distinct gate conditions:

1. `validate` is failing directly and in its isolated pre-commit hook because the newly added `.github/prompts/execute-gate-gameplan.prompt.md` file is not yet registered in bootstrap assets.
2. `drift` is passing directly but failing in the isolated pre-commit hook, which confirms a real semantic mismatch between repo-wide drift and filename-scoped drift hook behavior.
3. `prompt-lint` is failing both directly and in the isolated pre-commit hook when invoked correctly on the real prompt set, which means the repo currently violates the enforced prompt policy.
4. `pyright` is failing directly and in the isolated pre-commit hook with materially the same error classes, which means this is genuine active type/dependency gate debt rather than a hook-only anomaly.

There is also one invalid diagnostic pattern that must not be reused: running `scripts/lint_prompts.py` against a directory path produces a false green because the script only evaluates explicit `.prompt.md` filenames.

---

## 2. Evidence Table

| Gate | Direct command result | Pre-commit hook result | Same semantics? | Notes |
|---|---|---|---|---|
| Validate | Fail | Fail | Yes | Both fail on missing bootstrap asset registration for `.github/prompts/execute-gate-gameplan.prompt.md`. |
| Drift | Pass | Fail | No | Direct `programstart drift --strict` is repo-wide; hook is filename-scoped because `pass_filenames: true`. |
| Prompt lint | Fail | Fail | Yes, when invoked correctly | Direct invocation must pass explicit `.prompt.md` files. A directory-path invocation is a false green and is invalid evidence. |
| Pyright | Fail | Fail | Yes, materially | Direct and hook outputs show the same major classes: missing optional dependencies and real typing issues in repo code. |
| Pytest | Fail | No isolated equivalent captured | N/A | Six failures are downstream of strict validation now failing on bootstrap assets, not fresh feature-regression evidence. |

---

## 3. Command Record

### Direct commands

| Command | Result | Key observation |
|---|---|---|
| `uv run programstart validate --check all --strict` | Fail | `bootstrap_assets is missing current workspace files: .github/prompts/execute-gate-gameplan.prompt.md` |
| `uv run programstart drift --strict` | Pass | Repo-wide drift reports clean state. |
| `uv run pytest --tb=no -q --no-header` | Fail | `6 failed, 1350 passed, 1 warning`; all six failures are validation/bootstrap-asset fallout. |
| `uv run pyright` | Fail | Same core type/dependency error classes as the isolated pre-commit hook. |
| `uv run python scripts/lint_prompts.py (Get-ChildItem .github/prompts -Recurse -Filter *.prompt.md | Select-Object -ExpandProperty FullName)` | Fail | Real prompt corpus violates mandatory section policy in multiple public prompts. |

### Isolated hook commands

| Command | Result | Key observation |
|---|---|---|
| `uv run pre-commit run programstart-validate --all-files` | Fail | Same bootstrap-assets failure as direct validate. |
| `uv run pre-commit run programstart-drift --all-files` | Fail | Fails on authority/dependent drift findings despite direct repo-wide drift passing. |
| `uv run pre-commit run prompt-lint --all-files` | Fail | Same public prompt structural failures as truthful direct invocation. |
| `uv run pre-commit run pyright --all-files` | Fail | Same major error classes as direct pyright. |

### Invalid command pattern captured during Phase A

| Command | Apparent result | Why it is invalid |
|---|---|---|
| `uv run python scripts/lint_prompts.py .github/prompts` | Silent / false green | `lint_prompts.py` skips any path whose basename does not end with `.prompt.md`; a directory path is ignored rather than traversed. |

---

## 4. Failure Bucket Assignment

| Gate or issue | Primary bucket | Reason |
|---|---|---|
| Missing bootstrap asset registration for `.github/prompts/execute-gate-gameplan.prompt.md` | Real repo defect | The repo now contains a tracked prompt file that current strict validation expects to be registered. |
| Downstream pytest failures tied to bootstrap asset checks | Real repo defect | The failing tests are accurately reporting the same repo-state defect exposed by strict validation. |
| Drift direct/hook disagreement | Policy mismatch | The hook invocation semantics do not match the direct command semantics. |
| Prompt corpus failing enforced required sections | Real repo defect | The current public prompt set is non-compliant with the linter policy that is actively enforced. |
| Missing repo-wide prompt structural assertions in tests | Policy mismatch | Tests do not currently model the real enforced prompt policy on the actual corpus. |
| Pyright missing imports for `nox`, `playwright`, `PIL`, and related tooling modules | Environment mismatch | Part of the pyright failure surface is dependency visibility/scope rather than only application logic. |
| Pyright argument and object-shape errors in `programstart_create.py`, `programstart_factory_smoke.py`, and `programstart_recommend.py` | Real repo defect | These failures reproduce outside pre-commit and are not explained by hook isolation alone. |

No active Phase A failure is currently classified as an unrelated in-flight change.

---

## 5. Stable Conclusions

1. The new gate execution prompt introduced one fresh repo-state defect: missing bootstrap-asset registration.
2. Drift parity is genuinely broken. This is the clearest hook-semantic mismatch and should be repaired before any attempt to declare gates trustworthy again.
3. Prompt lint is not merely a hook problem. The prompt corpus currently fails the policy when the direct linter is invoked correctly.
4. Pyright is not merely a pre-commit isolation problem. The gate currently exposes both environment-scope issues and real type debt.
5. Phase A is complete because the active failure inventory is now stable, explicit, and bucketed.

---

## 6. Next Phase Entry Conditions

Phase B may proceed with the following starting assumptions:

1. Fix drift parity first.
2. Do not treat prompt-lint or pyright as hook-only anomalies.
3. Do not bury the bootstrap-assets defect under broader gate cleanup; it is a separate real repo defect that must be repaired explicitly.
