"""Public validation boundaries reject incomplete semantic and authority inputs."""

import pytest
from pydantic import ValidationError

from scripts import programstart_intent_compile as compiler
from scripts import programstart_intent_ingress as ingress
from scripts import programstart_objective_continuation as continuation
from scripts.programstart_resource_preflight import ResourcePreflight, ResourceStep
from tests.test_programstart_authority_resolver import _envelope, _semantic_response
from tests.test_programstart_intent_compile import _cases, binding, matrix_projection
from tests.test_programstart_resource_preflight import _plan


@pytest.mark.parametrize(
    "model,payload,reason",
    [
        (compiler.SurfaceRef, dict(surface_type="repository", identifier=" "), "identifier"),
        (compiler.EffectReadinessRule, dict(completed_effect=" done", ready_effect="next"), "whitespace"),
        (
            compiler.IntentInterpretation,
            dict(raw_intent=" ", normalized_intent="", kind="unknown", interpreted_objective="x"),
            "raw intent",
        ),
        (
            compiler.IntentInterpretation,
            dict(raw_intent="Do work", normalized_intent="wrong", kind="unknown", interpreted_objective="x"),
            "exactly match",
        ),
        (
            compiler.IntentInterpretation,
            dict(raw_intent="work", normalized_intent="work", kind="unknown", interpreted_objective=" "),
            "objective",
        ),
        (ingress.MaterialStatement, dict(text=" ", source="repository_evidence"), "text"),
        (ingress.CurrentnessCorrection, dict(conversation_claim=" ", current_fact="current", evidence_ref="owner#1"), "claim"),
        (
            ingress.HumanConsequenceGate,
            dict(gate_id=" ", owner="owner", required_action="review", acceptance_evidence="owner#1"),
            "requires id",
        ),
        (
            ingress.BoundedIntentEnvelope,
            dict(context_ref=" ", latest_operator_utterance="continue", source_principal="operator", captured_at="now"),
            "requires context",
        ),
        (
            ingress.SemanticInterpretationCandidate,
            dict(objective=" ", intent_kind="continuation", converged=True, producer="p", producer_version="1"),
            "provenance",
        ),
        (ingress.SemanticProducerResponse, dict(semantic_effect_id="id", status="succeeded"), "only a candidate"),
        (ingress.SemanticProducerResponse, dict(semantic_effect_id="id", status="failed"), "only a provider"),
        (ingress.SemanticProducerValidation, dict(accepted=True, semantic_effect_id="id"), "only a candidate"),
        (ingress.SemanticProducerValidation, dict(accepted=False, semantic_effect_id="id"), "only a rejection"),
        (ingress.ConversationHarvest, dict(context_ref=" ", latest_operator_utterance="continue"), "context_ref"),
        (ingress.ConversationHarvest, dict(context_ref="ctx", latest_operator_utterance=" "), "utterance"),
        (
            ingress.ConversationHarvest,
            dict(context_ref="ctx", latest_operator_utterance="continue", durable_artifact_refs=["x\x7f"]),
            "bounded",
        ),
        (ingress.IntentIngressRequest, dict(raw_intent=" "), "raw_intent"),
        (
            continuation.EvidenceDurability,
            dict(status="proven", mechanism="test", verification_ref="test:proof", invalidation_conditions=[" "]),
            "non-empty",
        ),
        (continuation.ObjectiveContinuationDecision, dict(disposition="effect"), "semantic_effect_token"),
        (continuation.ObjectiveContinuationDecision, dict(disposition="wait_machine"), "wait registration"),
    ],
)
def test_public_model_rejects_incomplete_meaning(model, payload, reason):
    with pytest.raises(ValidationError, match=reason):
        model.model_validate(payload)


@pytest.mark.parametrize("field", ["artifact_ref", "projection_identity", "decision_ref", "source_ref", "source_version"])
def test_projection_identity_is_required(field):
    payload = matrix_projection().model_dump(mode="json")
    payload[field] = " "
    with pytest.raises(ValidationError, match="non-empty"):
        compiler.MatrixProjectionBinding.model_validate(payload)


def test_projection_reference_requires_repository_and_exact_commit():
    payload = matrix_projection().model_dump(mode="json")
    payload["artifact_ref"] = "repo@" + "a" * 40 + ":file.json"
    with pytest.raises(ValidationError, match="immutable"):
        compiler.MatrixProjectionBinding.model_validate(payload)
    payload = binding().model_dump(mode="json")
    payload["projection_identity"] = " "
    with pytest.raises(ValidationError, match="exact decision"):
        compiler.DecisionOperationalizationBinding.model_validate(payload)


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"project_name": " "}, "requires project_name"),
        ({"authority_commit": " "}, "commit references"),
        ({"resource_preflight_path": "plan.json"}, "inactive owner gate"),
    ],
)
def test_authority_requires_explicit_current_meaning(updates, reason):
    payload = dict(_cases()[0]["authority"], **updates)
    with pytest.raises(ValidationError, match=reason):
        compiler.AuthoritySnapshot.model_validate(payload)


def test_semantic_request_must_bind_actual_envelope():
    payload = ingress.SemanticProducerRequest.from_envelope(_envelope()).model_dump(mode="json")
    payload["semantic_effect_id"] = "foreign"
    with pytest.raises(ValidationError, match="mechanical envelope"):
        ingress.SemanticProducerRequest.model_validate(payload)
    response = _semantic_response(_envelope())
    response["failure"] = "provider_failure"
    with pytest.raises(ValidationError, match="only a candidate"):
        ingress.SemanticProducerResponse.model_validate(response)


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"task_kind": "mechanical", "execution_class": "approved_default"}, "mechanical"),
        ({"execution_class": "deterministic", "approved_profile_ref": "profile:1"}, "cannot claim"),
        ({"execution_class": "approved_default"}, "approved profile"),
        ({"execution_class": "approved_stronger", "approved_profile_ref": "profile:1"}, "step-down"),
        (
            {"execution_class": "approved_default", "approved_profile_ref": "profile:1", "escalation_reason": "novel_inference"},
            "premium",
        ),
        (
            {"task_kind": "independent_review", "execution_class": "approved_default", "approved_profile_ref": "profile:1"},
            "separate approved",
        ),
    ],
)
def test_resource_class_cannot_bypass_cost_or_review_policy(updates, reason):
    payload = dict(task="inspect", task_kind="bounded_reasoning", execution_class="deterministic")
    payload.update(updates)
    with pytest.raises(ValidationError, match=reason):
        ResourceStep.model_validate(payload)


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"working_set": [" "]}, "bounded non-empty"),
        ({"working_set": ["work.md", "work.md"]}, "unique"),
        ({"policy_ref": "moving/main:policy.md"}, "exact PROGRAMSTART"),
    ],
)
def test_resource_preflight_requires_bounded_exact_references(updates, reason):
    with pytest.raises(ValidationError, match=reason):
        ResourcePreflight.model_validate(_plan(**updates))


def test_blank_intent_is_rejected_before_interpretation():
    with pytest.raises(ValueError, match="raw intent"):
        compiler.interpret_intent(" ")


@pytest.mark.parametrize("change,reason", [("work", "bind current owner work"), ("policy", "policy is stale")])
def test_compilation_rechecks_resource_work_and_methodology_binding(change, reason):
    from tests.test_programstart_objective_continuation import _authority

    plan = ResourcePreflight.model_validate(_plan())
    authority = _authority(
        resource_preflight_required=True,
        resource_preflight_path="plan.json",
        resource_preflight=plan,
        current_work_refs=[] if change == "work" else [plan.work_ref],
    )
    with pytest.raises(ValueError, match=reason):
        compiler.compile_work_packet("Continue", authority, kind=compiler.IntentKind.CONTINUATION)


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("resolution_ref", " ", "durable evidence"),
        ("observed_authority_commit", "foreign", "owning authority"),
        ("observed_methodology_commit", "foreign", "PROGRAMSTART authority"),
        ("observed_current_work_refs", ["foreign"], "current work"),
        ("observed_authority_fingerprint", "0" * 64, "provenance"),
    ],
)
def test_independent_authority_observation_must_match_current_snapshot(field, value, reason):
    from scripts.programstart_autonomy_ingress import AuthorityResolutionEvidence
    from tests.test_programstart_autonomy_ingress import authority

    payload = authority().model_dump(mode="json")
    payload[field] = value
    with pytest.raises(ValidationError, match=reason):
        AuthorityResolutionEvidence.model_validate(payload)


@pytest.mark.parametrize("drift", ["objective", "kind", "evidence", "constraint"])
def test_partial_conversation_drift_cannot_silently_reuse_packet(drift):
    from tests.test_programstart_contextual_semantic_drift import _authority, _objective

    authority = _authority()
    packet = compiler.compile_work_packet("Do bounded work.", authority, kind=compiler.IntentKind.BOUNDED_EXECUTION)
    fields: dict[str, object] = dict(context_ref="chat:partial", latest_operator_utterance="Continue", converged=False)
    if drift == "objective":
        fields["objective"] = _objective("Changed objective")
    elif drift == "kind":
        fields["intent_kind"] = compiler.IntentKind.CONTINUATION
    elif drift == "evidence":
        fields["durable_artifact_refs"] = ["owner:new-evidence"]
    else:
        fields["accepted_constraints"] = [_objective("Preserve customer data")]
    harvest = ingress.ConversationHarvest.model_validate(fields)
    result = ingress.resolve_contextual_intent(
        ingress.ContextualIntentRequest(harvest=harvest, authority=authority, existing_packet=packet)
    )
    assert result.action == ingress.ContextualTransitionAction.RECOVER_EXECUTION_STATE
    assert result.packet == packet


def test_partial_harvest_without_authority_requests_semantics_and_owner():
    from tests.test_programstart_contextual_semantic_drift import _authority

    packet = compiler.compile_work_packet("Do bounded work.", _authority())
    harvest = ingress.ConversationHarvest(context_ref="chat:partial", latest_operator_utterance="Continue")
    result = ingress.resolve_contextual_intent(ingress.ContextualIntentRequest(harvest=harvest, existing_packet=packet))
    assert "complete current conversation semantics" in (result.next_system_requirement or "")


def test_handoff_requires_present_and_integrity_valid_packet():
    from tests.test_programstart_contextual_semantic_drift import _authority

    harvest = ingress.ConversationHarvest(context_ref="chat:partial", latest_operator_utterance="Continue")
    result = ingress.resolve_contextual_intent(ingress.ContextualIntentRequest(harvest=harvest))
    with pytest.raises(ValueError, match="requires a compiled"):
        ingress.render_contextual_handoff(result)
    packet = compiler.compile_work_packet("Do bounded work.", _authority())
    packet.specification_id = "tampered"
    result.packet = packet
    with pytest.raises(ValueError, match="integrity verification failed"):
        ingress.render_contextual_handoff(result)


def test_complete_harvest_with_changed_evidence_recompiles():
    from tests.test_programstart_contextual_semantic_drift import _authority, _objective

    authority = _authority()
    packet = compiler.compile_work_packet("Do bounded work.", authority, kind=compiler.IntentKind.BOUNDED_EXECUTION)
    harvest = ingress.ConversationHarvest(
        context_ref="chat:new-evidence",
        latest_operator_utterance="Continue",
        objective=_objective("Do bounded work."),
        intent_kind=compiler.IntentKind.BOUNDED_EXECUTION,
        converged=True,
        durable_artifact_refs=["owner:new-evidence"],
    )
    result = ingress.resolve_contextual_intent(
        ingress.ContextualIntentRequest(harvest=harvest, authority=authority, existing_packet=packet)
    )
    assert result.packet and result.packet.evidence_context_refs == ["owner:new-evidence"]
    assert result.packet.specification_id != packet.specification_id


def test_partial_harvest_with_authority_drift_recovers_before_recompile():
    from tests.test_programstart_contextual_semantic_drift import _authority

    authority = _authority()
    packet = compiler.compile_work_packet("Do bounded work.", authority)
    authority = authority.model_copy(deep=True, update={"authority_commit": "new-owner-head"})
    harvest = ingress.ConversationHarvest(context_ref="chat:partial", latest_operator_utterance="Continue")
    result = ingress.resolve_contextual_intent(
        ingress.ContextualIntentRequest(harvest=harvest, authority=authority, existing_packet=packet)
    )
    assert "before recompiling the drifted Work Packet" in (result.next_system_requirement or "")


def test_execution_state_recovery_without_packet_reference_stays_generic():
    harvest = ingress.ConversationHarvest(context_ref="chat:lost", latest_operator_utterance="Continue", execution_underway=True)
    result = ingress.resolve_contextual_intent(ingress.ContextualIntentRequest(harvest=harvest))
    assert "recover the durable active Work Packet" in (result.next_system_requirement or "")


def test_incomplete_harvest_cannot_claim_a_material_executable_change():
    from tests.test_programstart_contextual_semantic_drift import _authority

    packet = compiler.compile_work_packet("Do bounded work.", _authority())
    harvest = ingress.ConversationHarvest(context_ref="chat:partial", latest_operator_utterance="Continue")
    assert ingress._harvest_changes_packet(harvest, packet) is False
