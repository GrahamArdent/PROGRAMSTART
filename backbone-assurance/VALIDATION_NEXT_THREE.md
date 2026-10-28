# Validation repairs — 27 October 2026

This implements the next three operator-selected steps: execute PROGRAMSTART's tests, review the overdue knowledge tracks, and qualify a reproducible local browser/test environment. It follows draft PR257 head `d177ae4a5ee49f7fd5904498159a03b22cfd0818`, tree `125d28d792d3c819193caeaa08ca0c2c4e903970`. The complete local source fixture matched that published tree; its local commit metadata is synthetic. Final Git publication binds the resulting candidate separately.

## Changes and reasons

1. **Execute tests.** Nine test modules now use package-qualified imports, including nested helper imports discovered only after collection was repaired. The first full run collected 3,125 cases but had 15 failures: 14 nested-import failures and one CLI-help side effect. `programstart_precommit_validate --help` now exits through argparse before loading/synchronizing/validating the workspace. The regression check fails if help reaches any of those operations; ordinary invocation still synchronizes prompts and runs strict validation. Class-scoped read-only HTTP fixtures use the supported classmethod form; the unused monkeypatch fixture was removed. Nox builds the local context index so two real-index checks no longer depend on a prior manual setup step. This exposed one previously incidental coverage path: first-run retrieval without an index. An explicit public-API regression test now verifies that a missing index builds usable authority documents and KB entries without relying on test execution order.
2. **Review knowledge.** The [ten-track decision review](../docs/research/2026-10-27-kb-review.md) records official sources, substantive corrections, unchanged recommendations and project-specific follow-ups. All ten dates were updated through the existing review command after review. The seven-day limit and strict freshness gate remain intact.
3. **Qualify the environment.** Nox consumes the existing committed requirements export instead of resolving `.[dev]` afresh. Both smoke sessions install only the headless Chromium shell they actually use. Browser/OS dependencies remain real prerequisites. Browser version, screenshots, visual tolerance, test discovery and coverage exclusions/thresholds were not relaxed.

The 156-case focused regression run passed. The first coherent full suite passed 3,126 tests with zero skips, but the strict coverage gate correctly rejected one missing statement/branch in first-run retrieval. The added missing-index test closes that outcome gap. The final gate below passes.

## Reproduction

On the project's Python 3.12 baseline, from a clean checkout with OS package installation available:

```bash
uv sync --locked --extra dev
uv run python -m playwright install --with-deps --only-shell chromium
uv run nox -s gate_safe --default-venv-backend uv --envdir /tmp/programstart-validation-fresh
```

`uv.lock` and `requirements.txt` must agree. The checked export uses `uv export --locked --format requirements-txt --extra dev --no-hashes`; compare requirement lines after the two generated command-header comments. Updating the lock/export is intentional maintenance, not a side effect of validation. The uv Nox backend changes environment installation, not selected checks. Use a new empty environment directory for qualification; ordinary reuse is appropriate only while the environment remains coherent. On Windows choose an equivalent writable temporary path. Pre-commit hooks retain their declared separate versions.

Observed environment: Linux x86_64, Ubuntu 24.04 userland, glibc 2.39; Python 3.12.14; uv 0.13.4; Nox 2026.2.9; pytest 9.0.3; coverage 7.13.5; Playwright 1.58.0; Pillow 12.2.0. The browser is Playwright's Chromium headless shell 145.0.7632.6, build 1208; FFmpeg build 1011. The system UI font resolves to DejaVu Sans; Arial resolves to Liberation Sans 2.1.5. This is a qualified Linux environment, not a portable pixel-equivalence promise for every OS/font set.

### Observed environment repairs

- The default Chromium CDN returned HTTP 200 with a 195-byte HTML “Site Unavailable” body. Playwright correctly rejected it as an invalid ZIP. Installing the identical managed build from Google's official origin succeeded using the documented download-host override:

  ```bash
  PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST=https://storage.googleapis.com/chrome-for-testing-public \
    uv run python -m playwright install --only-shell chromium
  ```

  This is a session-specific workaround, not a committed global mirror or custom browser executable. TLS verification remained enabled. FFmpeg succeeded on Playwright's built-in alternate Microsoft mirror.
- Reusing previously unlocked Nox environments exposed mixed `filelock` package contents: metadata declared 3.25.2, while eleven installed source files failed their wheel RECORD hashes and imported a missing module from another version. The locked `.venv` passed those same hashes. The failed run retained 53 failures; it is not credited as a pass. The in-place `--reuse-venv never` attempt still exhibited the mismatch and was interrupted; it is not a qualification. A separate empty environment directory produced matching package hashes and restored subprocess imports. Qualification uses that directory rather than altering tests around the broken installation. The precise cause of the in-place refresh failure remains runner-specific and unresolved.
- This container's APT sandbox user-switch operation is unavailable. The missing `fonts-liberation` dependency was downloaded from [Ubuntu's official archive](https://archive.ubuntu.com/ubuntu/pool/main/f/fonts-liberation/fonts-liberation_2.1.5-3_all.deb), extracted without running package scripts and its TTFs placed in the user's font directory, then `fc-cache -f` refreshed discovery. Normal runners should use Playwright's `--with-deps` setup. Before font installation both captures had a one-pixel height mismatch; after installation both original Linux baselines passed unchanged. No font or browser binaries are committed here.

[Playwright's browser documentation](https://playwright.dev/python/docs/browsers) supports the managed-version, system-dependency, headless-shell-only and download-host setup. Headed checks still require full Chromium.

## Scope and continuation

These repairs address local findings A-G01, A-G02 and A-G03 from [the original validation record](VALIDATION.md). They do not execute the 84 proposed ecosystem scenarios, establish hosted selector adequacy, qualify installed/native consumers or remove existing hosted holds. Paths PR81 and its local evidence are unchanged. The next ecosystem work remains outcome-first EN/Compute mapping and admitted owner-bound installed proof, following the existing [implementation continuation](IMPLEMENTATION.md).

No tests were deleted to hide a failure, no assertions were loosened, no dates were advanced without review, and no screenshot baseline was regenerated. A passing local gate must not be described as hosted CI or production acceptance.

## Final observed result

Command: `uv run nox -s gate_safe --default-venv-backend uv --envdir /tmp/programstart-validation-20261027`; exit **0**. All six selected validation sessions passed. The environment directory was created separately from the inconsistent default `.nox` environments.

| Check | Result | Limit |
|---|---|---|
| Full pytest suite | 3,127 passed; zero failed or skipped; two expected diagnostic warnings | Local Python/Linux behavior |
| Production coverage | 67/67 configured modules present; 13,622 statements and 5,054 branch exits covered; zero raw gaps | Four existing excluded lines and existing source scope remain unchanged |
| New outcome fault probes | Both deliberately broken variants rejected by the new assertions | In-process test faults; no production mutation |
| Lint and type checking | All hooks pass; zero type errors/warnings | Includes secret scan, schemas, strict process validation and drift |
| Process/CLI validation | Selected process, prompt, workflow, guide and CLI smoke checks pass | No external provider effect |
| Read-only dashboard | Six HTTP checks, 16 browser checks, two original Linux image baselines pass | Attached USERJOURNEY mode; no isolated mutation or Windows/browser-matrix claim |
| Documentation | Strict MkDocs build passes | Existing informational links outside the documentation tree remain |

The two pytest warnings are intentionally exercised missing-registry/version and workspace-root fallback diagnostics. Pytest fixture deprecation warnings are resolved. Neither test success nor 100% configured coverage establishes adequacy for the full ecosystem. All 84 proposed ecosystem scenarios remain NOT_RUN.

Review of the final code diff confirms package imports use the existing repository pattern, help exits before workspace work, normal hook validation stays strict, and the missing-index test checks useful returned context. Nox session selection, production guards, coverage scope/floor and screenshot thresholds are unchanged. The secret baseline changes only an existing finding's line number and scan timestamp. No independent reviewer or owner acceptance is implied.

## Retained evidence

Logs use deterministic gzip; hashes below describe decompressed bytes. [The coverage summary](evidence/next3-coverage-summary.json) retains per-module raw counters from the successful Nox report. The diagnostic bundle includes package RECORD failures, font before/after, primary browser download failure, review commands, focused tests and both fault probes. The installation-only diagnostic attempt did not run tests and is not credited as validation.

| Log | Raw bytes | SHA-256 |
|---|---:|---|
| [next3-diagnostics.log.gz](evidence/next3-diagnostics.log.gz) | 80,293 | `fee6dda88e950616292ae2acd9ca5dc7db61bb5842bba63effacbcabbf7cd4bf` |
| [next3-first-gate.log.gz](evidence/next3-first-gate.log.gz) | 277,134 | `2a44f56b5d96fbd2939b723c9d79ae2363b9c4bb39357e2406b22641c37cb92f` |
| [next3-pre-fallback-coverage.log.gz](evidence/next3-pre-fallback-coverage.log.gz) | 23,512 | `66c08d28727ce58d16c1e10a401d9d500972d1b09b00220b0009420adaf9b600` |
| [next3-final-gate.log.gz](evidence/next3-final-gate.log.gz) | 69,216 | `41a310ffe977081d7b0eb6d4462b3db76bfde5b228bb6b0e257374a45d1654ef` |
