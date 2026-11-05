# Required document context implementation plan
> Execute inline, one reviewed task at a time, under the existing approved game plan.
Goal: required exact document bytes affect actual semantic interpretation and retain immutable role metadata through compilation/recovery.
Architecture: version only the existing PROGRAMSTART semantic request; capture through caller-admitted reader, carry bounded bytes through existing carriers, verify at each receiving owner, leave authority/release contracts intact.
Tech stack: existing Python/Pydantic, unittest/pytest, Git, owner release tools.
Spec: ../specs/2026-11-05-required-document-context-design.md

## Global constraints
V1 seven-field envelopes, output bytes and effect identities remain unchanged. V2 is specific to this semantic action. No fetch permission, new registry, generic schema, platform or transport. Four documents maximum; 8192 UTF-8 bytes each; 16384 total; 24576 serialized semantic request bytes, within existing32768 outer carrier bytes. Hash exact text including whitespace. No latest substitution. Record source, CI, installed/native and owner acceptance separately.

## Review focus
- Valid-looking content for the wrong revision must fail before provider; test changed content/digest and wrong-effect response.
- Empty/missing/duplicate/extra documents and escaping/Unicode amplification must fail closed, test actual serialized size.
- V1 canonical digests and legacy packets must remain identical, freeze independent baseline before edits.
- Required role must survive authority recompile and cold reload without another provider call, test actual consumers.
- Reader permission denial must propagate before capture; do not infer document-owner authorization from bundle presence.

### Task 1: PROGRAMSTART owner
Files: scripts/programstart_required_context.py; scripts/programstart_intent_ingress.py; scripts/programstart_intent_compile.py; tests/test_programstart_required_context.py.
Interfaces: RequiredContextDocument(reference:str,text:str); validate_required_context(required_refs,documents,durable_refs); capture_required_context(required_refs,reader)->list[RequiredContextDocument].
RequiredContextIntentEnvelope(BoundedIntentEnvelope) adds required_context_refs and context_documents. parse_bounded_intent_envelope(payload) selects strict V1/V2. Existing SemanticProducerRequest.from_envelope chooses V1/V2 and validates pair/effect/request bound. CompiledWorkPacket.required_context_refs projects existing provenance; compile functions accept optional required_context_refs. Harvest deterministically forwards required refs. Existing caller APIs taking the base accept subclass without dropping fields.
- [ ] Freeze V1 request/effect and packet baseline.
- [ ] Write RED tests for bundle input/refusal/capture and actual compile/recompile/cold reload.
- [ ] Run RED; retain exact output.
- [ ] Implement minimum owner logic preserving V1.
- [ ] Run focused tests and affected owner suites; run repository hygiene and gate_safe before publication.
- [ ] Commit exact candidate with evidence; source-only status until cohort qualified.

### Task 2: paired receiving owners
Files: Controller programstart_autonomy_adapter.py/private_ingress.py/programstart_semantic_transport.py/programstart_objective_adapter.py; Compute spine/worker_bridge_agent.py; EN src/execution_node_control/codex_semantic_producer.py; each owner's existing semantic tests.
Interfaces: same existing actions/profile/carriers; accept exact V1 or V2 field sets, recompute content hashes and effect ID; final EN validates before subprocess and includes verified docs as quoted evidence. Controller uses pinned PS parser; recompile forwards required refs using existing adapter.
- [ ] Write RED valid V2 and malformed/missing/hash-mismatch tests against each actual validator.
- [ ] Implement local validators and prompt clarification, no new shared deployed dependency.
- [ ] Run focused owner regressions and composed actual receiving-consumer fixture; preserve V1 baseline.
- [ ] Create exact commits in dependency order, update pins explicitly, run owner full local gates/review.
- [ ] Publish coherent candidates and one focused CI round; resolve failures, merge only exact qualified revisions.

### Task 3: installation and native oracle
- [ ] Freeze expected read-only audit/literal from decisive fixture doc; generic utterance contains neither.
- [ ] Install exact qualified cohort using existing broker/coordinator; verify hashes/processes/pins/health/rollback.
- [ ] Negative invalid bundles reach zero provider/effect calls; authorized reader denial retains original failure.
- [ ] One declared positive model request; reconcile original effect if pending rather than resubmit.
- [ ] Actual next compiler/continuation adopts audit posture and literal/constraints, required digests survive recompile and cold read, retry makes zero model calls.
- [ ] Save raw evidence, manifest, exact revisions and active coverage update; leave unexercised ACL/currentness/mixed-version and owner-acceptance gates open.

## Material source-review correction
Original candidate was rejected; retain its exact snapshot and findings. V2 must use existing private carriers only, with no Git-origin admission or parent/child/result Git fallback. Private outages retain original identities and uncertainty for private reconciliation. V1 policy stays unchanged.
Nested semantic input is capped at24576 canonical bytes; each owner preflights its actual outer frame before writing raw journals/child state, within the existing32768 ceiling. Nonblank exact text and strict UTF-8 on all V2 strings are mandatory before reader/provider. No normalization or truncation.
Both EN invocations pass V2 content through bounded stdin; document text must not appear in Python/systemd/Codex argv. Raw recovery state files use explicit private creation mode. Preserve the copies and their hashes.
Restore replay receipt conjunction; retain required roles in TRA successor compilation. Schema arrays/objects must raise owner typed rejections without interrupting unrelated queue work.
The private semantic intake remains a new-objective/reinterpretation entry that denies unresolved existing references; positive ordinary continuation uses the separately qualified recorded-packet recovery adapter, with no new model call. This is a documented scope limit, not positive proof for referenced semantic intake.
