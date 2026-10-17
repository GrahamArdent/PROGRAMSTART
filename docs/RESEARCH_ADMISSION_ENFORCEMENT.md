# Research prerequisite admission

Research admission is a companion to objective proof, not a replacement. A heading,
mock fixture, green test or Challenge result does not establish source feasibility.
`PROGRAMBUILD/RESEARCH_EVIDENCE.json` binds the objective contract, current entry
instructions, decision, research findings, source captures and narrowly accepted work
scope. `schemas/research-evidence.schema.json` documents its shape; the runtime also
checks native authority, file identity, currentness and consequence boundaries.

## Admission and currentness

Each selected objective must have research questions. Each question records the
protected boundary, supported/unsupported/unknown/not_applicable disposition,
finding, next action and invalidation conditions. Supported claims require at least
one primary or observed source capture with HTTPS source, observation and expiry
dates, SHA-256, observed capability and limitations. Own repository plans and mocks
must be derived evidence. This is provenance checking, not automatic fact checking:
accepted owner review remains responsible for semantic accuracy, question completeness
and justified not_applicable decisions. Arbitrary third-party URLs cannot prove truth.

The repository owner's immutable native issue comment starts with
`PROGRAMSTART_RESEARCH_ADMISSION_V1` followed by JSON with exactly
`record_sha256`, `previous_sha256`, `result`, `reason`,
`objective_contract_sha256`, and `scope_sha256`. Digests use the objective guard's
canonical JSON function. First acceptance has null previous_sha256; later accepted
records retain the previous accepted digest. A rejection revokes admission. Edited,
foreign, missing or broken-chain receipts fail closed. Current file bindings and
scope must match the accepted record. Relevant changes need refreshed research and
acceptance; unrelated changes inside accepted scope can reuse it until expiry.

## Shared consumers

The actual workflow CLI and dashboard call the objective guard, which calls research
admission before dependent transitions, including skip/dry-run paths. Requirements
and architecture require architecture admission; scaffold, test strategy and
implementation require implementation admission; release/audit/post-launch and
terminal completion require release admission. Implementation entry validation and
`programstart validate research-admission` use the same guard. The guarded merge
consumer verifies its own accepted methodology and research module and incorporates
research admission in the native snapshot. CI copies policy from the accepted base,
never from the PR's proposed guard. Initial policy adoption precedes enrollment.

The merge guard checks native base/head records, actual changed files including
rename sources, accepted scope, source bytes and owner history. Incomplete/truncated
changed-file coverage fails closed. Full objective completion requires all objective
research scope and release admission. Research-only product scope admits documents
and evidence, never application/policy code. Unresolved prerequisites prevent their
dependent product boundary. Explicit experiments can retain unresolved questions
only in accepted isolated scope, cannot merge into the default product branch or
claim product release. Neither profile completes the parent product objective.

## Installation and coverage

New full and lean project entries contain an unaccepted research placeholder; it
must be replaced with actual evidence and native acceptance. Existing records are
preserved. Full projects copy the guard through the asset registry. Lean projects
require an independently qualified accepted external runtime. Existing repositories
without records report UNENROLLED, with product_admitted false: this is compatibility,
not proof of adoption. Installed old runtimes, direct GitHub merge routes, manual
state edits and other callers that bypass these consumers are not intercepted.
Inventory and qualify them individually before making broader enforcement claims.

## Verification

`tests/test_programstart_research_admission.py` exercises native receipt controls,
committed byte bindings, expiry, scope/rename/removal attacks, product/experiment
separation and the real CLI/dashboard transition guard. Its synthetic provider
fixtures prove control behavior only. A real project retest must separately retain
source research, current native acceptance, accepted runtime identity, positive
research-only admission and negative dependent-product admission. Card Vault is
that bounded retest; its product outcomes remain pending until real E2E evidence.
