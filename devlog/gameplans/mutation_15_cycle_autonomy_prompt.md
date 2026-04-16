# Mutation 15-Cycle Autonomy Prompt

Continue autonomous mutation-hardening work in PROGRAMSTART at `C:\ PYTHON APPS\PROGRAMSTART`.

## Objective

Complete up to 15 additional mutation-hardening cycles against `scripts/programstart_recommend.py` without asking the user for more prompts unless a real blocker prevents progress.

## Current baseline

- Last recorded completed run in `devlog/gameplans/hardeninggameplan.md` is the twelfth completed canonical run.
- Baseline before the next cycle: `total=3281`, `killed=2189`, `survived=1092`, `pending=0`.

## Canonical cycle definition

For each cycle, do all of the following in order:

1. Inspect the latest settled survivor hotspots from `mutants/scripts/programstart_recommend.py.meta`.
2. Pick the highest-value next scenarios from the top hotspot functions.
3. Add narrow exact-output tests in `tests/test_programstart_recommend.py`.
4. Run focused `pytest` for the newly added tests.
5. Run `uv run programstart drift`.
6. Run `uv run programstart validate --check all`.
7. Run the canonical mutation command: `uv run nox -s mutation`.
8. Wait for the mutation run to settle fully.
9. Trust only the settled terminal summary and settled metadata.
10. Update `devlog/gameplans/hardeninggameplan.md` only if the completed run improved the baseline.

## Operating rules

- Do not broaden mutation scope beyond `scripts/programstart_recommend.py`.
- Do not record partial progress snapshots as completed runs.
- Prefer exact-output assertions over loose behavioral checks.
- If a run does not improve the baseline, do not update the gameplan for that run.
- When a run does not improve, use the settled hotspot ordering to drive the next exact-output pass.
- Keep edits minimal and focused.
- Keep going until 15 additional cycles are completed or a genuine blocker stops progress.

## Hotspot guidance

Expect the highest-value survivor surfaces to remain concentrated around functions such as:

- `build_stack_candidates()`
- `build_recommendation()`
- `main()`
- `infer_domain_names()`
- `select_triggered_entries()`
- `re_evaluate_project()`
- `print_recommendation()`

Always recalculate the actual ordering from the latest settled metadata instead of assuming it stayed the same.

## Files in scope

- `scripts/programstart_recommend.py`
- `tests/test_programstart_recommend.py`
- `mutants/scripts/programstart_recommend.py.meta`
- `devlog/gameplans/hardeninggameplan.md`

## Useful commands

- `uv run pytest tests/test_programstart_recommend.py -k "..."`
- `uv run programstart drift`
- `uv run programstart validate --check all`
- `uv run nox -s mutation`

## Final report format

When the full run is finished or blocked, report:

1. Whether all 15 additional cycles were completed.
2. The starting baseline and ending baseline.
3. Per-cycle totals for each completed canonical run.
4. Which files were edited.
5. The final top survivor hotspots.
6. Whether `devlog/gameplans/hardeninggameplan.md` was updated and to what run number.
7. Any blocker if fewer than 15 cycles were completed.
