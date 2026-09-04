"""Regression tests for accepted semantic changes during contextual continuation."""

from __future__ import annotations

from scripts.programstart_intent_compile import AuthoritySnapshot, IntentKind, SurfaceRef, SurfaceType, compile_work_packet
from scripts.programstart_intent_ingress import (
    ContextualIntentRequest,
    ContextualTransitionAction,
    ConversationBasisSource,
    ConversationHarvest,
    ConversationState,
    MaterialStatement,
    resolve_contextual_intent,
)


def _authority() -> AuthoritySnapshot:
    return AuthoritySnapshot(
        project_name="Example Existing Project",
        owning_repository="GrahamArdent/example-project",
        authority_commit="project-authority-ref",
        authority_paths=["docs/MASTER_GAMEPLAN.md"],
        methodology_commit="programstart-current-ref",
        execution_mode="mode_c_existing_project",
        mutable_surfaces=[
            SurfaceRef(
                surface_type=SurfaceType.REPOSITORY,
                identifier="GrahamArdent/example-project",
            )
        ],
        allowed_effects=["bounded repository implementation"],
        challenge_required=True,
    )


def _objective(text: str) -> MaterialStatement:
    return MaterialStatement(
        text=text,
        source=ConversationBasisSource.ACCEPTED_CONVERSATION_DECISION,
    )


def test_same_semantics_with_shorter_final_wording_reuses_existing_packet() -> None:
    authority = _authority()
    objective = "Implement the accepted bounded change."
    packet = compile_work_packet(
        objective,
        authority,
        kind=IntentKind.BOUNDED_EXECUTION,
        interpreted_objective=objective,
    )
    harvest = ConversationHarvest(
        context_ref="chat:same-semantics",
        latest_operator_utterance="Proceed.",
        objective=_objective(objective),
        intent_kind=IntentKind.BOUNDED_EXECUTION,
        converged=True,
        execution_underway=True,
        existing_work_packet_ref=packet.specification_id,
    )

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            authority=authority,
            existing_packet=packet,
        )
    )

    assert resolution.state == ConversationState.EXECUTING
    assert resolution.action == ContextualTransitionAction.RESUME_EXISTING_PACKET
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id


def test_new_accepted_constraint_recompiles_even_when_authority_is_unchanged() -> None:
    authority = _authority()
    objective = "Implement the accepted bounded change."
    packet = compile_work_packet(
        objective,
        authority,
        kind=IntentKind.BOUNDED_EXECUTION,
        interpreted_objective=objective,
    )
    new_constraint = MaterialStatement(
        text="Do not deploy this repository in the current slice.",
        source=ConversationBasisSource.EXPLICIT_USER_INSTRUCTION,
    )
    harvest = ConversationHarvest(
        context_ref="chat:new-constraint",
        latest_operator_utterance="Proceed, but don't deploy it yet.",
        objective=_objective(objective),
        intent_kind=IntentKind.BOUNDED_EXECUTION,
        converged=True,
        active_constraints=[new_constraint],
        existing_work_packet_ref=packet.specification_id,
    )

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository="GrahamArdent/example-project",
            authority=authority,
            existing_packet=packet,
        )
    )

    assert resolution.state == ConversationState.EXECUTION_READY
    assert resolution.action == ContextualTransitionAction.RECOMPILE_FOR_ADMISSION
    assert resolution.packet is not None
    assert resolution.packet.specification_id != packet.specification_id
    assert resolution.supersedes_specification_id == packet.specification_id
    assert new_constraint.text in resolution.packet.intent.explicit_constraints


def test_partial_recovery_with_new_constraint_does_not_silently_reuse_or_recompile() -> None:
    authority = _authority()
    objective = "Implement the accepted bounded change."
    packet = compile_work_packet(
        objective,
        authority,
        kind=IntentKind.BOUNDED_EXECUTION,
        interpreted_objective=objective,
    )
    recovered_constraint = MaterialStatement(
        text="Do not deploy this repository in the current slice.",
        source=ConversationBasisSource.EXPLICIT_USER_INSTRUCTION,
    )
    partial_harvest = ConversationHarvest(
        context_ref="chat:truncated-with-new-constraint",
        latest_operator_utterance="Proceed, but don't deploy it yet.",
        objective=None,
        intent_kind=IntentKind.UNKNOWN,
        converged=False,
        active_constraints=[recovered_constraint],
        execution_underway=True,
        existing_work_packet_ref=packet.specification_id,
    )

    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=partial_harvest,
            authority=authority,
            existing_packet=packet,
        )
    )

    assert resolution.state == ConversationState.CONVERGED
    assert resolution.action == ContextualTransitionAction.RECOVER_EXECUTION_STATE
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id
    assert resolution.supersedes_specification_id is None
    assert resolution.operator_intervention_required is False
    assert "recover complete current conversation semantics" in (resolution.next_system_requirement or "")
