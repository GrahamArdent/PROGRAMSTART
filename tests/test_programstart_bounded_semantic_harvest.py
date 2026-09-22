import pytest
from pydantic import ValidationError

from scripts.programstart_intent_compile import IntentKind
from scripts.programstart_intent_ingress import (
    SEMANTIC_PRODUCER_RESPONSE_VERSION,
    BoundedIntentEnvelope,
    SemanticInterpretationCandidate,
    SemanticProducerRejection,
    SemanticProducerRequest,
    build_trusted_conversation_harvest,
    validate_semantic_producer_response,
)


def _envelope() -> BoundedIntentEnvelope:
    return BoundedIntentEnvelope(
        context_ref="ctx-88",
        latest_operator_utterance="Continue existing work.",
        source_principal="authenticated-operator",
        captured_at="2026-09-22T03:00:00Z",
        existing_work_packet_ref="PATH-WP1",
        durable_artifact_refs=["controller-request:req-path-wp1"],
    )


def _success(request: SemanticProducerRequest) -> dict[str, object]:
    return {
        "schema_version": SEMANTIC_PRODUCER_RESPONSE_VERSION,
        "semantic_effect_id": request.semantic_effect_id,
        "status": "succeeded",
        "candidate": {
            "objective": "Continue current PATH-WP1 through current authority.",
            "intent_kind": "continuation",
            "converged": True,
            "producer": "codex-semantic-profile",
            "producer_version": "v1",
            "confidence": 0.9,
        },
    }


def test_bounded_harvest_preserves_mechanical_context():
    envelope = BoundedIntentEnvelope(
        context_ref="ctx-88",
        latest_operator_utterance="Continue existing work.",
        source_principal="authenticated-operator",
        captured_at="2026-09-22T03:00:00Z",
        existing_work_packet_ref="PATH-WP1",
    )
    semantic = SemanticInterpretationCandidate(
        objective="Continue current PATH-WP1 through current authority.",
        intent_kind=IntentKind.CONTINUATION,
        converged=True,
        producer="test-producer",
        producer_version="v1",
        confidence=0.99,
    )
    harvest = build_trusted_conversation_harvest(envelope, semantic)
    assert harvest.context_ref == envelope.context_ref
    assert harvest.latest_operator_utterance == envelope.latest_operator_utterance
    assert harvest.existing_work_packet_ref == "PATH-WP1"
    assert harvest.objective is not None
    assert harvest.objective.source_ref == "semantic-producer:test-producer@v1"


def test_confidence_does_not_clear_ambiguity():
    envelope = BoundedIntentEnvelope(
        context_ref="ctx",
        latest_operator_utterance="Continue.",
        source_principal="authenticated-operator",
        captured_at="2026-09-22T03:00:00Z",
    )
    semantic = SemanticInterpretationCandidate(
        objective="Continue.",
        intent_kind=IntentKind.CONTINUATION,
        converged=True,
        unresolved_material_ambiguities=["conflicting current references"],
        producer="test-producer",
        producer_version="v1",
        confidence=1.0,
    )
    assert build_trusted_conversation_harvest(envelope, semantic).converged is False


def test_unknown_intent_requires_ambiguity():
    with pytest.raises(ValidationError):
        SemanticInterpretationCandidate(
            objective="Something",
            intent_kind=IntentKind.UNKNOWN,
            converged=False,
            producer="test-producer",
            producer_version="v1",
        )


def test_same_mechanical_input_has_same_semantic_effect_and_accepted_candidate():
    first = SemanticProducerRequest.from_envelope(_envelope())
    second = SemanticProducerRequest.from_envelope(_envelope())

    assert first.semantic_effect_id == second.semantic_effect_id
    first_result = validate_semantic_producer_response(first, _success(first))
    second_result = validate_semantic_producer_response(second, _success(second))
    assert first_result == second_result
    assert first_result.accepted is True


@pytest.mark.parametrize(
    ("raw_response", "rejection"),
    [
        ("not-an-object", SemanticProducerRejection.MALFORMED_SCHEMA),
        (
            {"schema_version": "programstart.semantic-producer.response.v2"},
            SemanticProducerRejection.UNSUPPORTED_VERSION,
        ),
    ],
)
def test_schema_failures_are_deterministic(raw_response: object, rejection: SemanticProducerRejection):
    request = SemanticProducerRequest.from_envelope(_envelope())
    assert validate_semantic_producer_response(request, raw_response).rejection == rejection


def test_extra_candidate_fields_fail_closed():
    request = SemanticProducerRequest.from_envelope(_envelope())
    response = _success(request)
    response["candidate"]["unexpected"] = "value"  # type: ignore[index]

    result = validate_semantic_producer_response(request, response)
    assert result.rejection == SemanticProducerRejection.MALFORMED_SCHEMA


def test_material_ambiguity_fails_closed_even_with_high_confidence():
    request = SemanticProducerRequest.from_envelope(_envelope())
    response = _success(request)
    response["candidate"].update(  # type: ignore[union-attr]
        unresolved_material_ambiguities=["two current owning projects are plausible"],
        confidence=1.0,
    )

    result = validate_semantic_producer_response(request, response)
    assert result.rejection == SemanticProducerRejection.MATERIAL_AMBIGUITY


@pytest.mark.parametrize("key", ["authority_snapshot", "execution_permission", "currentness"])
def test_attempted_authority_manufacture_is_rejected(key: str):
    request = SemanticProducerRequest.from_envelope(_envelope())
    response = _success(request)
    response["candidate"][key] = {"granted": True}  # type: ignore[index]

    result = validate_semantic_producer_response(request, response)
    assert result.rejection == SemanticProducerRejection.ATTEMPTED_AUTHORITY_MANUFACTURE


def test_provider_failure_and_wrong_replay_provenance_fail_closed():
    request = SemanticProducerRequest.from_envelope(_envelope())
    provider_failure = {
        "schema_version": SEMANTIC_PRODUCER_RESPONSE_VERSION,
        "semantic_effect_id": request.semantic_effect_id,
        "status": "failed",
        "failure": "provider_unavailable",
    }
    assert validate_semantic_producer_response(request, provider_failure).rejection == SemanticProducerRejection.PROVIDER_FAILURE

    wrong_replay = _success(request)
    wrong_replay["semantic_effect_id"] = "sha256:" + "0" * 64
    assert validate_semantic_producer_response(request, wrong_replay).rejection == SemanticProducerRejection.PROVENANCE_MISMATCH


def test_mechanical_envelope_rejects_provider_added_semantics():
    payload = _envelope().model_dump()
    payload["execution_authorized"] = True
    with pytest.raises(ValidationError):
        BoundedIntentEnvelope.model_validate(payload)
