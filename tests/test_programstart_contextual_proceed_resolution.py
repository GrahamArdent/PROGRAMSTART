"""Scenario acceptance tests for contextual continuation resolution."""

from __future__ import annotations

import pytest

from scripts.programstart_intent_compile import (
    AuthoritySnapshot,
    IntentKind,
    SurfaceRef,
    SurfaceType,
    compile_work_packet,
)
from scripts.programstart_intent_ingress import (
    ContextualIntentRequest,
    ContextualTransitionAction,
    ConversationBasisSource,
    ConversationHarvest,
    ConversationState,
    CurrentnessCorrection,
    HumanConsequenceGate,
    MaterialStatement,
    render_contextual_handoff,
    resolve_contextual_intent,
)


def _statement(
    text: str,
    source: ConversationBasisSource = ConversationBasisSource.ACCEPTED_CONVERSATION_DECISION,
) -> MaterialStatement:
    return MaterialStatement(text=text, source=source)


def _authority(
    *,
    owner: str = "GrahamArdent/example-project",
    authority_ref: str = "project-authority-ref",
    methodology_ref: str = "programstart-current-ref",
) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        project_name="Example Existing Project",
        owning_repository=owner,
        authority_commit=authority_ref,
        authority_paths=["docs/MASTER_GAMEPLAN.md"],
        methodology_commit=methodology_ref,
        execution_mode="mode_c_existing_project",
        current_work_refs=["CURRENT_WORK_PACKET.md"],
        mutable_surfaces=[SurfaceRef(surface_type=SurfaceType.REPOSITORY, identifier=owner)],
        allowed_effects=["bounded repository implementation"],
        prohibited_effects=["new spend", "destructive provider mutation"],
        human_gate_conditions=["new spend"],
        evidence_requirements=["exact-head verification"],
        acceptance_conditions=["targeted verification passes"],
        challenge_required=True,
    )


def _harvest(
    *,
    utterance: str = "Proceed.",
    objective: str = "Implement the accepted bounded change.",
    kind: IntentKind = IntentKind.BOUNDED_EXECUTION,
    converged: bool = True,
    **updates: object,
) -> ConversationHarvest:
    data: dict[str, object] = {
        "context_ref": "chat:context-123",
        "latest_operator_utterance": utterance,
        "objective": _statement(objective, ConversationBasisSource.ACCEPTED_CONVERSATION_DECISION),
        "intent_kind": kind,
        "converged": converged,
    }
    data.update(updates)
    return ConversationHarvest.model_validate(data)


def test_1_converged_discussion_compiles_without_repeating_the_conversation() -> None:
    harvest = _harvest(
        accepted_decisions=[_statement("Keep the existing owner and reuse its execution spine.")],
        active_constraints=[_statement("Do not create a competing orchestration layer.")],
    )

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository="GrahamArdent/example-project",
            authority=_authority(),
        )
    )

    assert resolution.state == ConversationState.EXECUTION_READY
    assert resolution.action == ContextualTransitionAction.COMPILE_FOR_ADMISSION
    assert resolution.packet is not None
    assert "Keep the existing owner and reuse its execution spine." in resolution.packet.intent.explicit_constraints
    assert "Do not create a competing orchestration layer." in resolution.packet.intent.explicit_constraints


def test_2_active_implementation_reuses_current_packet_instead_of_recompiling() -> None:
    authority = _authority()
    packet = compile_work_packet("Implement the accepted bounded change.", authority, kind=IntentKind.BOUNDED_EXECUTION)
    harvest = _harvest(execution_underway=True, existing_work_packet_ref=packet.specification_id)

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=authority, existing_packet=packet)
    )

    assert resolution.state == ConversationState.EXECUTING
    assert resolution.action == ContextualTransitionAction.RESUME_EXISTING_PACKET
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id
    assert resolution.supersedes_specification_id is None


def test_3_wrong_owner_routes_a_handoff_without_mutating_the_current_repository() -> None:
    owner = "GrahamArdent/existing-remediation-owner"
    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=_harvest(
                objective="Evaluate and implement the accepted remediation under the existing responsibility owner.",
                kind=IntentKind.ARCHITECTURE_EVALUATION,
            ),
            current_repository="GrahamArdent/repo-watchtower",
            authority=_authority(owner=owner),
        )
    )

    assert resolution.state == ConversationState.HANDOFF_READY
    assert resolution.action == ContextualTransitionAction.COMPILE_OWNER_HANDOFF
    assert resolution.handoff_repository == owner
    assert resolution.packet is not None
    assert resolution.packet.owning_repository == owner


def test_4_generic_proceed_never_clears_a_genuine_human_consequence_gate() -> None:
    authority = _authority()
    packet = compile_work_packet("Continue the current slice.", authority, kind=IntentKind.CONTINUATION)
    gate = HumanConsequenceGate(
        gate_id="passkey-registration",
        owner="operator",
        required_action="Register the physical passkey in the owning identity surface.",
        acceptance_evidence="Verifier reports the expected registered credential reference.",
        safe_parallel_work=["continue repository-only documentation reconciliation"],
    )
    harvest = _harvest(kind=IntentKind.CONTINUATION, active_human_gate=gate)

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=authority, existing_packet=packet)
    )

    assert resolution.state == ConversationState.GATED
    assert resolution.action == ContextualTransitionAction.PRESERVE_HUMAN_GATE
    assert resolution.operator_intervention_required is True
    assert resolution.gate == gate
    assert resolution.safe_parallel_work == ["continue repository-only documentation reconciliation"]
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id


def test_5_long_conversation_short_final_message_preserves_only_material_accepted_state() -> None:
    harvest = _harvest(
        utterance="Okay, do it properly.",
        accepted_decisions=[_statement("Use the existing PROGRAMSTART Intent Ingress owner.")],
        rejected_alternatives=[_statement("Create a new prompt-management service.")],
        brainstorming=[_statement("Maybe call it Mode D.")],
        explicit_exclusions=[_statement("Do not create a new orchestration engine.")],
    )
    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository="GrahamArdent/PROGRAMSTART",
            authority=_authority(owner="GrahamArdent/PROGRAMSTART"),
        )
    )

    assert resolution.packet is not None
    assert resolution.packet.intent.raw_intent == "Okay, do it properly."
    assert "Use the existing PROGRAMSTART Intent Ingress owner." in resolution.packet.intent.explicit_constraints
    assert "Explicit exclusion: Do not create a new orchestration engine." in resolution.packet.intent.explicit_constraints
    assert "Create a new prompt-management service." not in resolution.packet.intent.explicit_constraints
    assert "Maybe call it Mode D." not in resolution.packet.intent.explicit_constraints

    handoff = render_contextual_handoff(resolution)
    assert "Create a new prompt-management service." in handoff
    assert "context only; not additional authority" in handoff
    assert "Maybe call it Mode D." not in handoff


def test_6_stale_conversation_recompiles_against_current_authority() -> None:
    old_authority = _authority(methodology_ref="programstart-old-ref")
    old_packet = compile_work_packet("Continue Stage X.", old_authority, kind=IntentKind.CONTINUATION)
    current_authority = _authority(methodology_ref="programstart-current-ref")
    harvest = _harvest(
        kind=IntentKind.CONTINUATION,
        objective="Continue the current Stage Y slice.",
        currentness_corrections=[
            CurrentnessCorrection(
                conversation_claim="Stage X is current.",
                current_fact="Stage X is complete; Stage Y is current.",
                evidence_ref="repo:current-authority-ref:docs/MASTER_GAMEPLAN.md",
            )
        ],
    )

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository="GrahamArdent/example-project",
            authority=current_authority,
            existing_packet=old_packet,
        )
    )

    assert resolution.action == ContextualTransitionAction.RECOMPILE_FOR_ADMISSION
    assert resolution.packet is not None
    assert resolution.packet.specification_id != old_packet.specification_id
    assert resolution.supersedes_specification_id == old_packet.specification_id
    assert resolution.packet.authority.methodology_commit == "programstart-current-ref"
    assert resolution.harvest.currentness_corrections[0].current_fact.startswith("Stage X is complete")


def test_7_safe_reversible_inference_continues_without_an_operator_question() -> None:
    inferred = _statement(
        "Use the repository's existing formatter rather than introduce another formatter.",
        ConversationBasisSource.SYSTEM_INFERENCE,
    )
    harvest = _harvest(active_constraints=[inferred])

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=_authority())
    )

    assert resolution.state == ConversationState.EXECUTION_READY
    assert resolution.operator_intervention_required is False
    assert resolution.packet is not None
    assert inferred.text in resolution.packet.intent.explicit_constraints
    assert resolution.harvest.active_constraints[0].source == ConversationBasisSource.SYSTEM_INFERENCE


def test_8_material_ambiguity_is_the_only_kind_that_requests_operator_judgment() -> None:
    ambiguity = _statement(
        "Two owner choices would create materially different production consequences.",
        ConversationBasisSource.SYSTEM_INFERENCE,
    )
    harvest = _harvest(unresolved_material_ambiguities=[ambiguity])

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=_authority())
    )

    assert resolution.state == ConversationState.EXPLORE
    assert resolution.action == ContextualTransitionAction.REQUEST_MATERIAL_DECISION
    assert resolution.operator_intervention_required is True
    assert resolution.packet is None


def test_9_handoff_renderer_carries_owner_and_exclusions_without_chat_noise() -> None:
    owner = "GrahamArdent/another-owner"
    harvest = _harvest(
        accepted_decisions=[_statement("Preserve the existing controller boundary.")],
        rejected_alternatives=[_statement("Put durable orchestration in the compiler.")],
        brainstorming=[_statement("Maybe make every repository depend on this directly.")],
        explicit_exclusions=[_statement("Do not create a second controller.")],
    )
    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository="GrahamArdent/PROGRAMSTART",
            authority=_authority(owner=owner),
        )
    )

    rendered = render_contextual_handoff(resolution)
    assert resolution.handoff_repository == owner
    assert f"Owner: `{owner}`" in rendered
    assert "Do not create a second controller." in rendered
    assert "Put durable orchestration in the compiler." in rendered
    assert "Maybe make every repository depend on this directly." not in rendered


def test_10_already_complete_context_does_not_invent_more_work() -> None:
    harvest = _harvest(acceptance_met=True)

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=_authority())
    )

    assert resolution.state == ConversationState.COMPLETE
    assert resolution.action == ContextualTransitionAction.REPORT_COMPLETE
    assert resolution.packet is None


def test_exploratory_context_synthesizes_without_fabricating_a_work_packet() -> None:
    harvest = _harvest(
        objective="Compare the strongest current options.",
        kind=IntentKind.UNKNOWN,
        converged=False,
    )

    resolution = resolve_contextual_intent(ContextualIntentRequest(harvest=harvest))

    assert resolution.state == ConversationState.EXPLORE
    assert resolution.action == ContextualTransitionAction.SYNTHESIZE_CURRENT_CONCLUSION
    assert resolution.operator_intervention_required is False
    assert resolution.packet is None


def test_converged_context_without_authority_routes_machine_resolution_not_operator_form_filling() -> None:
    resolution = resolve_contextual_intent(ContextualIntentRequest(harvest=_harvest()))

    assert resolution.state == ConversationState.CONVERGED
    assert resolution.action == ContextualTransitionAction.RESOLVE_CURRENT_AUTHORITY
    assert resolution.operator_intervention_required is False
    assert "authority/currentness" in (resolution.next_system_requirement or "")


def test_execution_underway_without_local_packet_state_recovers_durable_state_instead_of_duplication() -> None:
    harvest = _harvest(execution_underway=True, existing_work_packet_ref="WPK-existing")

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=harvest, authority=_authority())
    )

    assert resolution.state == ConversationState.CONVERGED
    assert resolution.action == ContextualTransitionAction.RECOVER_EXECUTION_STATE
    assert resolution.packet is None
    assert "WPK-existing" in (resolution.next_system_requirement or "")


def test_existing_packet_without_current_authority_is_revalidated_not_regenerated() -> None:
    authority = _authority()
    packet = compile_work_packet("Continue.", authority, kind=IntentKind.CONTINUATION)

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(harvest=_harvest(kind=IntentKind.CONTINUATION), existing_packet=packet)
    )

    assert resolution.action == ContextualTransitionAction.REVALIDATE_EXISTING_PACKET
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id
    assert resolution.next_system_requirement is not None


def test_tampered_existing_packet_is_rejected_before_contextual_resolution() -> None:
    authority = _authority()
    packet = compile_work_packet("Continue.", authority, kind=IntentKind.CONTINUATION)
    tampered = packet.model_copy(update={"semantic_digest": "tampered"})

    with pytest.raises(ValueError, match="integrity"):
        resolve_contextual_intent(
            ContextualIntentRequest(harvest=_harvest(kind=IntentKind.CONTINUATION), authority=authority, existing_packet=tampered)
        )
