"""Required-context regressions exercise real owner parsers and compiler.
Removing bundle validation admits altered bytes; removing provenance forwarding
loses the required role after recompile. No model or final consumer is mocked.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from scripts import programstart_intent_ingress as ingress
from scripts.programstart_intent_compile import (
    AuthoritySnapshot,
    IntentKind,
    compile_work_packet,
    verify_integrity,
)

TEXT = "Only audit the read-only QUARTZ-47 ledger. Do not dispatch work.\n"
REF = "fixture:requirements:sha256:" + hashlib.sha256(TEXT.encode()).hexdigest()


def base() -> dict:
    return dict(
        context_ref="ctx-required",
        latest_operator_utterance="Follow the supplied requirement.",
        source_principal="authenticated-operator",
        captured_at="2026-11-05T05:00:00Z",
        project_hint="",
        existing_work_packet_ref="",
        durable_artifact_refs=[REF],
    )


def bundle() -> dict:
    return dict(base(), required_context_refs=[REF], context_documents=[dict(reference=REF, text=TEXT)])


def parse(payload: dict):
    assert hasattr(ingress, "parse_bounded_intent_envelope"), "required-context parser is missing"
    return ingress.parse_bounded_intent_envelope(payload)


def authority() -> AuthoritySnapshot:
    cases = json.loads((Path(__file__).parent / "fixtures/intent_compilation/real_cases.json").read_text())["cases"]
    return AuthoritySnapshot.model_validate(cases[0]["authority"])


def test_v1_canonical_baseline_is_unchanged():
    expected = json.loads((Path(__file__).parent / "fixtures/required_context_v1_baseline.json").read_text())
    request = ingress.SemanticProducerRequest.from_envelope(ingress.BoundedIntentEnvelope(**base()))
    assert request.model_dump(mode="json") == expected["request"]
    packet = compile_work_packet("Audit the baseline.", authority(), kind=IntentKind.AUDIT, durable_artifact_refs=[REF])
    assert packet.model_dump(mode="json") == expected["packet"]


def test_required_bytes_bound_to_effect_and_round_trip():
    envelope = parse(bundle())
    request = ingress.SemanticProducerRequest.from_envelope(envelope)
    assert request.schema_version == "programstart.semantic-producer.request.v2"
    assert isinstance(request.envelope, ingress.RequiredContextIntentEnvelope)
    assert request.envelope.context_documents[0].text == TEXT
    restored = ingress.SemanticProducerRequest.model_validate_json(request.model_dump_json())
    assert restored == request
    legacy = ingress.SemanticProducerRequest.from_envelope(ingress.BoundedIntentEnvelope(**base()))
    assert request.semantic_effect_id != legacy.semantic_effect_id
    altered = bundle()
    altered["context_documents"][0]["text"] += " "
    with pytest.raises(ValueError):
        parse(altered)


@pytest.mark.parametrize(
    "change",
    [
        lambda v: v.update(context_documents=[]),
        lambda v: v.update(required_context_refs=[]),
        lambda v: v.update(context_documents=v["context_documents"] * 2),
        lambda v: v.update(required_context_refs=[REF, REF]),
        lambda v: v.update(durable_artifact_refs=[]),
        lambda v: v["context_documents"][0].update(reference="fixture:other:sha256:" + "0" * 64),
        lambda v: v["context_documents"][0].update(text="substituted revision"),
        lambda v: v["context_documents"][0].update(text="bad\ud800"),
        lambda v: v["context_documents"][0].update(authorized=True),
        lambda v: v.pop("required_context_refs"),
    ],
)
def test_incomplete_or_substituted_context_refuses(change):
    value = bundle()
    change(value)
    parse_fn = getattr(ingress, "parse_bounded_intent_envelope", None)
    assert parse_fn is not None, "required-context parser is missing"
    with pytest.raises((ValueError, UnicodeError)):
        parse_fn(value)


@pytest.mark.parametrize(
    "text,count",
    [("x" * 8193, 1), ("x" * 6000, 3), ("x", 5), ("\x01" * 6000, 1)],
    ids=["per-document", "total", "count", "escaped-wire"],
)
def test_byte_and_serialized_bounds_refuse(text, count):
    docs = []
    for i in range(count):
        content = text + str(i)
        ref = f"fixture:{i}:sha256:" + hashlib.sha256(content.encode()).hexdigest()
        docs.append(dict(reference=ref, text=content))
    value = dict(
        base(),
        required_context_refs=[d["reference"] for d in docs],
        durable_artifact_refs=[d["reference"] for d in docs],
        context_documents=docs,
    )
    with pytest.raises(ValueError):
        envelope = parse(value)
        ingress.SemanticProducerRequest.from_envelope(envelope)


def test_wrong_request_version_and_response_revision_refuse():
    request = ingress.SemanticProducerRequest.from_envelope(parse(bundle()))
    raw = request.model_dump(mode="json")
    raw["schema_version"] = "programstart.semantic-producer.request.v1"
    with pytest.raises(ValidationError):
        ingress.SemanticProducerRequest.model_validate(raw)
    wrong = {
        "schema_version": ingress.SEMANTIC_PRODUCER_RESPONSE_VERSION,
        "semantic_effect_id": "sha256:" + "0" * 64,
        "status": "failed",
        "failure": "provider_failure",
    }
    result = ingress.validate_semantic_producer_response(request, wrong)
    assert result.rejection == ingress.SemanticProducerRejection.PROVENANCE_MISMATCH


def test_authorized_reader_exact_bytes_and_permission_denial():
    from scripts import programstart_required_context as context

    documents = context.capture_required_context([REF], lambda reference: TEXT.encode())
    assert documents[0].text.encode() == TEXT.encode()
    seen = []

    def denied(reference):
        seen.append(reference)
        raise PermissionError("document owner denies fixture")

    with pytest.raises(PermissionError, match="document owner denies"):
        context.capture_required_context([REF], denied)
    assert seen == [REF]
    with pytest.raises(ValueError):
        context.capture_required_context([REF], lambda reference: b"wrong bytes")


def test_compiler_required_role_survives_cold_recompile(tmp_path):
    packet = compile_work_packet(
        "Audit QUARTZ-47.", authority(), kind=IntentKind.AUDIT, durable_artifact_refs=[REF], required_context_refs=[REF]
    )
    assert packet.required_context_refs == [REF]
    assert packet.scope.initial_posture == "read_only_until_findings_reconciled"
    assert verify_integrity(packet)
    saved = tmp_path / "packet.json"
    saved.write_text(packet.model_dump_json())
    script = """import json,sys
from scripts.programstart_intent_compile import CompiledWorkPacket,compile_interpreted_work_packet,verify_integrity
p=CompiledWorkPacket.model_validate_json(open(sys.argv[1]).read())
q=compile_interpreted_work_packet(p.intent,p.authority,durable_artifact_refs=p.evidence_context_refs,required_context_refs=p.required_context_refs)
assert verify_integrity(q)
assert q.required_context_refs==p.required_context_refs
assert q.semantic_digest==p.semantic_digest
print(q.scope.initial_posture)
"""
    run = subprocess.run([sys.executable, "-c", script, str(saved)], capture_output=True, text=True, check=True)
    assert run.stdout.strip() == "read_only_until_findings_reconciled"
    with pytest.raises(ValueError):
        compile_work_packet("Audit.", authority(), kind=IntentKind.AUDIT, durable_artifact_refs=[], required_context_refs=[REF])


def test_harvest_retains_required_role():
    envelope = parse(bundle())
    candidate = ingress.SemanticInterpretationCandidate(
        objective="Audit QUARTZ-47.", intent_kind=IntentKind.AUDIT, converged=True, producer="test", producer_version="v1"
    )
    harvest = ingress.build_trusted_conversation_harvest(envelope, candidate)
    assert harvest.required_context_refs == [REF]
    result = ingress.resolve_contextual_intent(ingress.ContextualIntentRequest(harvest=harvest, authority=authority()))
    assert result.packet is not None
    assert result.packet.required_context_refs == [REF]
    assert result.packet.intent.interpreted_objective == "Audit QUARTZ-47."


def test_authority_recompile_preserves_recorded_roles_without_provider():
    original = compile_work_packet(
        "Audit QUARTZ-47.", authority(), kind=IntentKind.AUDIT, durable_artifact_refs=[REF], required_context_refs=[REF]
    )
    revised_authority = authority().model_copy(update={"authority_commit": "f" * 40})
    harvest = ingress.ConversationHarvest(
        context_ref="recovery",
        latest_operator_utterance="Continue.",
        objective=ingress.MaterialStatement(
            text="Audit QUARTZ-47.", source=ingress.ConversationBasisSource.SYSTEM_INFERENCE, source_ref="recorded-original"
        ),
        intent_kind=IntentKind.AUDIT,
        converged=True,
        existing_work_packet_ref=original.specification_id,
    )
    result = ingress.resolve_contextual_intent(
        ingress.ContextualIntentRequest(harvest=harvest, existing_packet=original, authority=revised_authority)
    )
    assert result.packet is not None
    assert result.packet.required_context_refs == [REF]
    assert result.packet.evidence_context_refs == [REF]
    assert result.packet.authority.authority_commit == "f" * 40
    assert result.packet.scope.initial_posture == "read_only_until_findings_reconciled"
    assert result.packet.semantic_digest != original.semantic_digest


@pytest.mark.parametrize("mode", ["missing-packet", "downgrade", "wrong-packet"])
def test_existing_required_revision_blocks_before_provider(mode):
    from scripts.programstart_autonomy_ingress import AuthorityResolutionEvidence, advance_autonomy_ingress
    from scripts.programstart_intent_compile import authority_fingerprint

    snapshot = authority()
    evidence_value = AuthorityResolutionEvidence(
        snapshot=snapshot,
        resolution_ref="fixture:owner-authority",
        observed_authority_commit=snapshot.authority_commit,
        observed_methodology_commit=snapshot.methodology_commit,
        observed_current_work_refs=snapshot.current_work_refs,
        observed_authority_fingerprint=authority_fingerprint(snapshot),
    )
    packet = compile_work_packet(
        "Audit QUARTZ-47.",
        evidence_value.snapshot,
        kind=IntentKind.AUDIT,
        durable_artifact_refs=[REF],
        required_context_refs=[REF],
    )
    payload = bundle() if mode != "downgrade" else base()
    payload["existing_work_packet_ref"] = packet.specification_id if mode != "wrong-packet" else "WPK-wrong"
    envelope = parse(payload)
    calls = []
    result = advance_autonomy_ingress(
        envelope,
        evidence_value,
        programstart_release=evidence_value.observed_methodology_commit,
        existing_packet=None if mode == "missing-packet" else packet,
        producer_boundary=lambda value: calls.append(value),
    )
    assert calls == []
    assert result.failure is not None
    assert result.failure.value == "required_context_unavailable"


def test_changed_required_set_needs_explicit_material_revision():
    packet = compile_work_packet(
        "Audit QUARTZ-47.", authority(), kind=IntentKind.AUDIT, durable_artifact_refs=[REF], required_context_refs=[REF]
    )
    other = "fixture:other:sha256:" + "0" * 64
    harvest = ingress.ConversationHarvest(
        context_ref="recovery",
        latest_operator_utterance="Continue.",
        durable_artifact_refs=[REF, other],
        required_context_refs=[other],
    )
    with pytest.raises(ValueError, match="material revision"):
        ingress.resolve_contextual_intent(
            ingress.ContextualIntentRequest(harvest=harvest, existing_packet=packet, authority=authority())
        )


@pytest.mark.parametrize("raw", [b"\xff", "not bytes", b"x" * 8193], ids=["invalid-utf8", "wrong-type", "oversized"])
def test_capture_rejects_invalid_reader_bytes(raw):
    from scripts.programstart_required_context import capture_required_context

    with pytest.raises(ValueError):
        capture_required_context([REF], lambda reference: raw)


def test_capture_rejects_empty_required_declaration_before_reader():
    from scripts.programstart_required_context import capture_required_context

    def forbidden(reference):
        raise AssertionError("reader must not be called")

    with pytest.raises(ValueError):
        capture_required_context([], forbidden)


@pytest.mark.parametrize(
    "field",
    ["context_ref", "latest_operator_utterance", "source_principal", "captured_at", "project_hint", "existing_work_packet_ref"],
)
def test_v2_invalid_unicode_stops_before_semantic_input(field):
    value = bundle()
    value[field] = "invalid\ud800"
    with pytest.raises(ValueError):
        parse(value)


@pytest.mark.parametrize("text", ["", " \n\t"], ids=["empty", "blank"])
def test_meaningless_required_document_refuses(text):
    ref = "fixture:empty:sha256:" + hashlib.sha256(text.encode()).hexdigest()
    value = dict(
        base(), durable_artifact_refs=[ref], required_context_refs=[ref], context_documents=[dict(reference=ref, text=text)]
    )
    with pytest.raises(ValueError):
        parse(value)


def test_surrogate_reference_refuses_before_reader():
    from scripts.programstart_required_context import capture_required_context

    ref = "fixture:\ud800:sha256:" + hashlib.sha256(TEXT.encode()).hexdigest()
    calls = []
    with pytest.raises(ValueError):
        capture_required_context([ref], lambda value: calls.append(value) or TEXT.encode())
    assert calls == []


@pytest.mark.parametrize("identity", ["same", "unrelated"])
def test_identical_or_unrelated_receipt_is_not_a_replay_conflict(identity):
    from scripts.programstart_autonomy_ingress import advance_autonomy_ingress
    from tests.test_programstart_autonomy_ingress import authority as resolved
    from tests.test_programstart_autonomy_ingress import envelope, response

    evidence = resolved()
    first = advance_autonomy_ingress(
        envelope(), evidence, programstart_release=evidence.observed_methodology_commit, producer_boundary=response
    )
    assert first.replay_receipt is not None
    receipt = first.replay_receipt
    if identity == "unrelated":
        receipt = receipt.model_copy(update={"semantic_effect_id": "sha256:" + "0" * 64})
    second = advance_autonomy_ingress(
        envelope(),
        evidence,
        programstart_release=evidence.observed_methodology_commit,
        producer_boundary=response,
        previous_replay=receipt,
    )
    assert second.failure is None
    assert second.status == first.status


def test_valid_unicode_is_preserved_without_normalization():
    effects = []
    for text in ("Audit café 🧭.\n", "Audit cafe\u0301 🧭.\n"):
        ref = "fixture:unicode:sha256:" + hashlib.sha256(text.encode()).hexdigest()
        value = dict(
            base(), durable_artifact_refs=[ref], required_context_refs=[ref], context_documents=[dict(reference=ref, text=text)]
        )
        request = ingress.SemanticProducerRequest.from_envelope(parse(value))
        assert isinstance(request.envelope, ingress.RequiredContextIntentEnvelope)
        assert request.envelope.context_documents[0].text.encode() == text.encode()
        effects.append(request.semantic_effect_id)
    assert effects[0] != effects[1]


def test_exact_nested_frame_limit_accepts_and_next_byte_refuses():
    value = bundle()
    value["durable_artifact_refs"] += [f"p{i:02d}:" + "x" * 508 for i in range(31)]
    value["latest_operator_utterance"] = "u"
    request = ingress.SemanticProducerRequest.from_envelope(parse(value))
    overhead = len(json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode())
    value["latest_operator_utterance"] = "u" * (24576 - overhead + 1)
    request = ingress.SemanticProducerRequest.from_envelope(parse(value))
    assert len(json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode()) == 24576
    value["latest_operator_utterance"] += "u"
    with pytest.raises(ValueError):
        ingress.SemanticProducerRequest.from_envelope(parse(value))


def test_direct_required_document_validator_rejects_unencodable_text():
    from scripts.programstart_required_context import RequiredContextDocument, validate_required_context

    with pytest.raises(ValueError, match="strict UTF-8"):
        validate_required_context([REF], [RequiredContextDocument(reference=REF, text="bad\ud800")], [REF])
