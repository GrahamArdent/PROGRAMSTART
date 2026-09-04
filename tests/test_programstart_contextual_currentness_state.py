"""Regression coverage for contextual currentness transition classification."""

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
    )


def test_existing_packet_without_current_authority_is_converged_pending_revalidation() -> None:
    authority = _authority()
    packet = compile_work_packet("Continue.", authority, kind=IntentKind.CONTINUATION)
    harvest = ConversationHarvest(
        context_ref="chat:authority-currentness-missing",
        latest_operator_utterance="Proceed.",
        objective=MaterialStatement(
            text="Continue.",
            source=ConversationBasisSource.ACCEPTED_CONVERSATION_DECISION,
        ),
        intent_kind=IntentKind.CONTINUATION,
        converged=True,
        existing_work_packet_ref=packet.specification_id,
    )

    resolution = resolve_contextual_intent(ContextualIntentRequest(harvest=harvest, existing_packet=packet))

    assert resolution.state == ConversationState.CONVERGED
    assert resolution.action == ContextualTransitionAction.REVALIDATE_EXISTING_PACKET
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id
    assert resolution.operator_intervention_required is False
    assert "current owning-project authority" in (resolution.next_system_requirement or "")


def test_incomplete_harvest_never_proves_an_existing_packet_safe_to_reuse() -> None:
    authority = _authority()
    packet = compile_work_packet("Continue.", authority, kind=IntentKind.CONTINUATION)
    harvest = ConversationHarvest(
        context_ref="chat:truncated-no-visible-drift",
        latest_operator_utterance="Proceed.",
        objective=None,
        intent_kind=IntentKind.UNKNOWN,
        converged=False,
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

    assert resolution.state == ConversationState.CONVERGED
    assert resolution.action == ContextualTransitionAction.RECOVER_EXECUTION_STATE
    assert resolution.packet is not None
    assert resolution.packet.specification_id == packet.specification_id
    assert resolution.operator_intervention_required is False
    assert "recover complete current conversation semantics" in (resolution.next_system_requirement or "")
