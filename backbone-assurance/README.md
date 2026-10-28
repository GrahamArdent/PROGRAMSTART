# Backbone assurance

This area holds the backbone audit's protected outcomes, testing surface, coverage gaps and evidence references. It is a cross-project reference under PROGRAMSTART, selected by Graham on 27 October 2026. It does not replace component authority, grant execution permission, or certify a release.

Resume from [the ten-step plan and progress](TEN_STEP_PLAN.md). Start with [the foundation and continuation](FOUNDATION.md), [repository placement](REPOSITORY_PLACEMENT.md), and [implementation status](IMPLEMENTATION.md). [Original validation findings](VALIDATION.md) preserve the failed baseline; [the subsequent repairs](VALIDATION_NEXT_THREE.md) record the successful local gate, ten-track knowledge review and reproducible environment. The editable audit source is [data/register.json](data/register.json). Its four views are [Components](views/01_components.csv), [Outcomes](views/02_outcomes.csv), [Adoption](views/03_adoption.csv), and [Lean](views/04_lean.csv). The workbook is a generated export; Git stores the reviewable source and CSVs.

The initial baseline has 18 journey families, 84 proposed scenarios, six compound failure sequences and 86 inventoried source methods. These are scoped inventories, not ecosystem totals. All proposed E2E scenarios remain NOT_RUN. The Paths pilot and subsequent repair supply narrower source evidence.

## Ownership and update rules

- PROGRAMSTART hosts this audit reference and its methodology links. Each component owns its implementation, regression tests and acceptance.
- Ecosystem Lab owns reusable isolated experiments. Historical pilot observations retained here do not create a competing experiment service.
- Evidence Spine owns canonical evidence/provenance and scoped acceptance where enrolled. Existing receipts retain their current owner; this audit links them and does not declare unenrolled records canonical by assertion.
- Ecosystem Matrix owns its admitted cross-owner projection semantics. Audit snapshots carry observation time and source identity; they are not a replacement live-state feed.
- Changes to outcomes, boundaries, test adequacy or evidence mappings update the register and relevant owner references together. Fixes land with their component first; audit status follows verified evidence.

Use stable IDs, exact source/test identities, explicit substituted boundaries and evidence links. Preserve historical findings and explain supersession. Unknown, skipped, blocked and unrun remain distinguishable. Component or dependency changes invalidate only affected evidence; a saved green result does not remain current indefinitely.

## Local artifact checks

From this directory:

```bash
python3 validate_register.py
python3 -m unittest test_register -v
python3 render_views.py
```

The existing pytest selection now includes `backbone-assurance`, so the register checks and committed-view freshness check run in the normal Nox test session and existing PR validation. These are artifact checks, not ecosystem runtime coverage. PROGRAMSTART maintains this audit reference; component owners retain their tests and acceptance. The default-discovery guard uses the registry's template/project role: generated project repositories do not inherit the populated audit or its audit-selection obligation. These commands validate and generate the audit artifacts. They do not run the ecosystem or authenticate acceptance. No scheduled sweep, hosted job, new service, credential or runtime controller is introduced by this area.

## Extraction criterion

A separate repository remains unselected. Revisit only with demonstrated independent ownership, access-control needs, harness/release lifecycle or measured coordination friction. Preserve component test ownership and canonical evidence links if extraction becomes justified.
