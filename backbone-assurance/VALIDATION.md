# Validation and remaining repository findings — 27 October 2026

The Paths repair and the audit artifact checks pass for their declared local scope. **PROGRAMSTART's full local confidence gate failed.** This candidate is retained as a source-only audit draft for the operator's requested durability/review; it is not merge-ready, accepted, installed or a waiver of the failed gate. Normal required remote/owner acceptance remains outstanding.

## Subject and commands

The complete PROGRAMSTART source was reconstructed from 623 blob-verified files at main commit `d3e0f95edc709e779b1632a5861384c97a83c6f9`, tree `1702331d3ed3829e8bc79ef5b81d2483a51d9c9a`. The local Git fixture reproduces that tree but has synthetic local commit metadata. The base comparison used the exact untouched tree in a separate Git-backed directory.

`uv sync --extra dev --frozen` installed the project environment. The completed gate was `uv run nox -s gate_safe --default-venv-backend uv` (900-second outer limit; exit 1). The backend flag changes environment installation, not session selection or assertions. An earlier default-backend attempt did not complete and is not counted as validation. No repository tests, thresholds or gate configuration were removed or weakened.

| Check | Observed result | Scope / implication |
|---|---|---|
| Audit register and negative controls | PASS, 19 manually invoked unittest methods | Structure/retention, not ecosystem behavior or automatic CI discovery |
| Generated views | PASS | 18 components, 84 scenarios, 12 adoption, 12 lean, 86 catalogued methods, 19 boundaries, 13 source records |
| Retention comparison | PASS | 17 register sections unchanged, including cases/journeys/tests/boundaries/adoption/lean/compound failures/retention; original research decompressed bytes match |
| Full lint session | FAIL | Formatting, Ruff, Bandit, secret scan, schemas, drift and prompt lint passed; strict process validation rejected overdue KB tracks |
| Type checking | PASS | Zero errors/warnings |
| Full test session | FAIL during collection | 3,013 items collected with seven import errors; suite execution/coverage did not complete |
| Process validation / CLI smoke | PASS with freshness warnings in non-strict check | Authority/planning/workflow checks, prompt evaluation, CLI smoke and drift passed |
| Browser smoke | BLOCKED before smoke execution | Chromium download produced invalid/truncated ZIP data; no browser result claimed |
| Documentation build | PASS | Strict MkDocs build; informational pre-existing external-to-docs links remain |

## Additional findings and dispositions

**A-G01 — overdue knowledge-base tracks.** All ten tracks were last reviewed 2026-10-19 against a seven-day policy. Strict validation produced the same ten failures on the untouched base. This is not repaired by changing dates without a review. Follow up through the existing knowledge-maintenance owner and revalidate that evidence; it is not a new audit scheduler or a reason to repeat completed Paths work.

**A-G02 — test collection imports.** Six modules import `conftest` as a top-level module; `test_programstart_research_admission.py` imports `test_programstart_objective_proof` likewise. The same seven failures reproduced with the untouched base using the completed gate's test interpreter (`python -m pytest --collect-only -q`). This proves a baseline/runner compatibility gap for the observed environment, not a claim about every GitHub environment or all remaining tests. Correct the import/package contract with the PROGRAMSTART owner, then run the actual full suite and coverage gate. Do not convert collection counts into passes.

**A-G03 — browser installation evidence unavailable.** The Playwright-managed Chromium download failed to unzip. The existing command retried its configured mirrors and failed before the read-only smoke. Qualify the same declared browser dependency in a working runner; no substitute browser was silently credited.

The new audit does not repair these unrelated baseline/environment findings or certify the wider repository. They are retained here with exact subjects and logs. Its own artifact checks and the Paths repair remain valid within their narrower scopes.

## Preparation corrections

- Added ADR-0027 because ACTIVE decision DEC-025 requires an ADR link; registered that ADR in the existing bootstrap and synchronization lists. Generated projects inherit decision provenance, not the filled audit register.
- Removed an unrelated root README pointer instead of modifying the KB authority solely to appease a broad README drift rule. The decision index and PR provide discovery.
- Retained original research and raw validation logs with deterministic gzip so text hooks cannot alter evidence bytes.
- Extended the existing secret baseline only with individually identified Git/content digests flagged by entropy detection. No detector or directory was disabled; the full secret scan passed.
- Marked the old pilot and workbook as historical. The editable Git register, current implementation checkpoint and original source/effect ownership remain distinct.

## Raw evidence

Gzip entries retain exact original bytes. Hashes below refer to **decompressed** content. The full gate log records runtime package/environment versions and all selected session results. No generated browser or dashboard artifact is claimed as accepted evidence.

| Log | Raw bytes | SHA-256 |
|---|---:|---|
| [programstart-gate-safe-final.log](evidence/programstart-gate-safe-final.log.gz) | 60,648 | `5d6df9ce522119833427a2235191b3e3bf98c40df253b9c4041e9fe6700fab71` |
| [programstart-base-validation.log](evidence/programstart-base-validation.log.gz) | 1,214 | `13e56f96228fca33e9d83d36525f78b069c7f5ceab04cf14e4755b8fb5e70bb7` |
| [programstart-base-collection-final.log](evidence/programstart-base-collection-final.log.gz) | 298,989 | `30ad23d5e8b84cde3068bc0f5a0efe1057103e419e390b76d7a596f112db8c79` |
| [audit-artifact-checks.log](evidence/audit-artifact-checks.log.gz) | 1,961 | `f46f973dbf736c7d47141a80ce5a31a41de956b9391581a581304428a048cbc7` |

The [Paths owner-local evidence](https://github.com/GrahamArdent/paths/blob/ff1694e5deff607afd560cc879c28234bf227ce6/docs/evidence/lookup-test-gaps-2026-10-27/README.md) records the 54-method result, four registry command blocks, MCP stdio suite and 12 detected faults separately. All 84 proposed ecosystem scenarios remain NOT_RUN.
