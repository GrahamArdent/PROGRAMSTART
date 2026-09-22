from pydantic import ValidationError
import pytest
from scripts.programstart_intent_compile import IntentKind
from scripts.programstart_intent_ingress import BoundedIntentEnvelope, SemanticInterpretationCandidate, build_trusted_conversation_harvest

def test_bounded_harvest_preserves_mechanical_context():
    envelope = BoundedIntentEnvelope(context_ref="ctx-88", latest_operator_utterance="Continue existing work.", source_principal="authenticated-operator", captured_at="2026-09-22T03:00:00Z", existing_work_packet_ref="PATH-WP1")
    semantic = SemanticInterpretationCandidate(objective="Continue current PATH-WP1 through current authority.", intent_kind=IntentKind.CONTINUATION, converged=True, producer="test-producer", producer_version="v1", confidence=0.99)
    harvest = build_trusted_conversation_harvest(envelope, semantic)
    assert harvest.context_ref == envelope.context_ref
    assert harvest.latest_operator_utterance == envelope.latest_operator_utterance
    assert harvest.existing_work_packet_ref == "PATH-WP1"
    assert harvest.objective.source_ref == "semantic-producer:test-producer@v1"

def test_confidence_does_not_clear_ambiguity():
    envelope = BoundedIntentEnvelope(context_ref="ctx", latest_operator_utterance="Continue.", source_principal="authenticated-operator", captured_at="2026-09-22T03:00:00Z")
    semantic = SemanticInterpretationCandidate(objective="Continue.", intent_kind=IntentKind.CONTINUATION, converged=True, unresolved_material_ambiguities=["conflicting current references"], producer="test-producer", producer_version="v1", confidence=1.0)
    assert build_trusted_conversation_harvest(envelope, semantic).converged is False

def test_unknown_intent_requires_ambiguity():
    with pytest.raises(ValidationError):
        SemanticInterpretationCandidate(objective="Something", intent_kind=IntentKind.UNKNOWN, converged=False, producer="test-producer", producer_version="v1")
