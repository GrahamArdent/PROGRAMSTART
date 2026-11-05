# Required document context: bounded P1 correction
Status: implementation proposal under the approved Backbone game plan; no closure claim.
Date: 2026-11-05 UTC.

## Intent
P1/Q01-b,c require a decisive document requirement to reach the actual semantic consumer, with missing, unauthorized or mismatched required bytes refusing the dependent decision. Existing immutable provenance forwarding is retained. Planning coverage is not implementation or owner acceptance.

## Existing owners and approaches
PROGRAMSTART owns semantic input/compilation; Controller owns authenticated intake, replay and its carrier; Compute owns nested typed admission; Execution Node owns final producer validation and prompt construction.
Opaque reference forwarding alone cannot prove use. Adding repository fetch privileges to EN enlarges its authority and leaves capture/currentness ambiguous. Selected implementation choice: capture exact bytes through an already authorized caller reader and carry a bounded verified bundle in a versioned extension of the existing PROGRAMSTART semantic request. This is one specific semantic request, not a universal schema, registry, platform or transport change.

## Input contract
Retain the seven-field V1 BoundedIntentEnvelope and its canonical bytes/effect IDs unchanged.
Add RequiredContextIntentEnvelope, a strict subclass with required_context_refs (ordered unique immutable refs) and context_documents (ordered records with exactly reference/text).
V2 request schema is programstart.semantic-producer.request.v2; fixed profile remains bounded-codex-semantic-v1; output remains response.v1 and current producer v1. V1 admits only V1 envelope; V2 admits only the context envelope. Unknown/mixed versions refuse.
Each required reference ends in :sha256:<64 lowercase hex>, is a subset of durable_artifact_refs, and identifies UTF-8 text exactly including whitespace/newlines. Documents must match required refs one-to-one in order, with no extras or duplicates. At least one and at most four required docs; each <=8192 UTF-8 bytes, total <=16384, full canonical serialized semantic request <=24576 bytes, reserving fixed-wrapper headroom inside the unchanged32768-byte outer carrier limit. Invalid Unicode, hash mismatch, absent bytes, malformed refs and oversized input fail before provider invocation; no truncation or latest substitution.
A capture_required_context helper accepts explicit refs and an owner-admitted callable reader(reference)->bytes. It performs no I/O itself beyond that reader, grants no privileges, propagates permission/missing errors and verifies strict UTF-8 and digest. No caller boolean is accepted as document ACL evidence. The private ingress's existing authenticated principal and owner binding remain mandatory.

## Identity, persistence and currentness
All required roles and text are part of the existing canonical envelope effect digest. A content/reference revision changes the effect ID; a response for another revision refuses. No reference is treated as execution authority.
The actual EN prompt includes verified required text as quoted evidence for interpreting the operator objective and constraints; it cannot grant permission. Source tests inspect the actual prompt boundary and reject invalid input before the subprocess boundary.
PROGRAMSTART harvest carries the deterministic required refs (never model-emitted metadata) into the existing WorkPacket provenance at context.required_context_refs. A property exposes these refs. Compilation requires their inclusion in durable refs. Both roles survive Controller admission, authority recompile and fresh-process packet reload. Existing empty-required legacy output remains byte-compatible.
Ordinary recovery retains the interpreted packet and required digests, without a new provider call. An explicit material revision gets its own required set/effect ID. Live document-owner ACL and supersession policies beyond the supplied authorized reader are not invented here and remain unqualified where not exercised.

## Files
PROGRAMSTART: scripts/programstart_required_context.py (specific bundle validation/capture models), scripts/programstart_intent_ingress.py, scripts/programstart_intent_compile.py; tests/test_programstart_required_context.py and existing ingress/compile suites.
Controller: controller/programstart_autonomy_adapter.py (parse V2 via pinned PS), controller/private_ingress.py, controller/programstart_semantic_transport.py, controller/programstart_objective_adapter.py; narrowly scoped receiving tests.
Compute: spine/worker_bridge_agent.py nested semantic validator and existing semantic bridge tests.
EN: src/execution_node_control/codex_semantic_producer.py final validation/prompt and existing semantic producer tests.
Use owner-local validators; no new shared dependency deployment or schema registry.

## Milestones and gates
1. PROGRAMSTART source: RED required-context tests, minimal implementation, legacy fixtures unchanged, actual compile/recompile/fresh-process tests, repository hygiene and gate_safe. A source-only candidate is not installed closure.
2. Receiving cohort: RED each real owner's boundary with valid and invalid V2; preserve V1 canonical inputs; pair exact PS/Controller/Compute/EN candidates. Add composed test using actual validators and final prompt/actual compiler; only external model I/O may be doubled.
3. Review exact changes, run owner local gates and coherent composed contracts, publish exact branches/PRs, run one bounded focused CI round, reconcile results. Merge only qualified exact candidates; update dependency pins explicitly after hashes exist. Use current owner release brokers/coordinator and retain rollback.
4. Native: freeze oracle before execution, raw utterance generic, decisive fixture document alone says read-only audit of unique literal. One declared provider call only after coherent installed readback. Assert actual provider returns audit plus literal, actual compiler/continuation adopts read-only posture and retains constraints/required refs/digests after cold reload. Missing/wrong hash/substituted docs refuse with zero provider/effect calls. Preserve originals and reconcile pending effect before any retry.

## Independent expected outcomes and residuals
Expected positive: required fixture meaning affects actual receiving decision, metadata survives subsequent compile/reload. Negative: missing, wrong digest, unknown version, out-of-bundle bytes and denied reader stop before provider/dispatch. Original V1 fixtures and output IDs remain unchanged.
Q01-b/c are only qualified for the exercised acquisition/consumer path; no global claim for arbitrary document ACL, live supersession, every consumer or host-loss recovery. All 13 audit items, Q01-Q10 and H01-H05 remain tracked in the single active coverage file. Owner acceptance remains separate.

## Builder-check dispositions
An integrity-checked existing packet owns the required set for ordinary continuation. Missing exact referenced packet or mismatched/removal/downgrade of required roles refuses before producer. Recompile with omitted role metadata preserves recorded roles; a changed nonempty set requires separately admitted material revision, not an invented revision endpoint.
This milestone qualifies authenticated inline content. Hash integrity is not document ACL evidence. The capture helper only acts through an already admitted caller reader; production document-owner ACL/supersession qualification stays open. Fresh builder check found nothing important left after these dispositions.

## Material source-review correction
Original candidate was rejected; retain its exact snapshot and findings. V2 must use existing private carriers only, with no Git-origin admission or parent/child/result Git fallback. Private outages retain original identities and uncertainty for private reconciliation. V1 policy stays unchanged.
Nested semantic input is capped at24576 canonical bytes; each owner preflights its actual outer frame before writing raw journals/child state, within the existing32768 ceiling. Nonblank exact text and strict UTF-8 on all V2 strings are mandatory before reader/provider. No normalization or truncation.
Both EN invocations pass V2 content through bounded stdin; document text must not appear in Python/systemd/Codex argv. Raw recovery state files use explicit private creation mode. Preserve the copies and their hashes.
Restore replay receipt conjunction; retain required roles in TRA successor compilation. Schema arrays/objects must raise owner typed rejections without interrupting unrelated queue work.
The private semantic intake remains a new-objective/reinterpretation entry that denies unresolved existing references; positive ordinary continuation uses the separately qualified recorded-packet recovery adapter, with no new model call. This is a documented scope limit, not positive proof for referenced semantic intake.
