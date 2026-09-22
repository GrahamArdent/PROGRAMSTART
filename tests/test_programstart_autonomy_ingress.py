from __future__ import annotations

import copy
from typing import Any

from scripts.programstart_autonomy_ingress import (
    PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
    AuthorityResolutionEvidence,
    AutonomyIngressFailure,
    AutonomyIngressStatus,
    advance_autonomy_ingress,
)
from scripts.programstart_intent_compile import AuthoritySnapshot, IntentKind, SurfaceRef, SurfaceType, authority_fingerprint
from scripts.programstart_intent_ingress import BoundedIntentEnvelope, SemanticProducerRequest


def envelope() -> BoundedIntentEnvelope:
    return BoundedIntentEnvelope(
        context_ref="objective:132:test",
        latest_operator_utterance="Advance the bounded current objective.",
        source_principal="authenticated-operator",
        captured_at="2026-09-22T20:00:00Z",
        project_hint="PROGRAMSTART",
        durable_artifact_refs=["PROGRAMSTART#132", "Controller#88"],
    )


def authority(*, methodology: str = PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE) -> AuthorityResolutionEvidence:
    snapshot = AuthoritySnapshot(
        project_name="PROGRAMSTART",
        owning_repository="GrahamArdent/PROGRAMSTART",
        authority_commit=methodology,
        authority_paths=["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md"],
        methodology_commit=methodology,
        execution_mode="mode_c_existing_project",
        current_work_refs=["https://github.com/GrahamArdent/PROGRAMSTART/issues/132"],
        mutable_surfaces=[SurfaceRef(surface_type=SurfaceType.REPOSITORY, identifier="GrahamArdent/PROGRAMSTART")],
        allowed_effects=["bounded repository integration"],
        prohibited_effects=["Controller admission manufacture"],
        acceptance_conditions=["bounded integration reaches existing Controller boundary"],
        challenge_required=True,
    )
    return AuthorityResolutionEvidence(
        snapshot=snapshot,
        resolution_ref="github:PROGRAMSTART#132@latest+git:main",
        observed_authority_commit=methodology,
        observed_methodology_commit=methodology,
        observed_current_work_refs=list(snapshot.current_work_refs),
        observed_authority_fingerprint=authority_fingerprint(snapshot),
    )


def response(payload: dict[str, object]) -> dict[str, object]:
    request = SemanticProducerRequest.model_validate(payload)
    return {
        "schema_version": "programstart.semantic-producer.response.v1",
        "semantic_effect_id": request.semantic_effect_id,
        "status": "succeeded",
        "candidate": {
            "objective": "Advance the bounded current PROGRAMSTART integration.",
            "intent_kind": IntentKind.CONTINUATION,
            "converged": True,
            "accepted_decisions": [],
            "active_constraints": ["Do not implement Controller lifecycle."],
            "explicit_exclusions": ["PATH-WP1 replay"],
            "unresolved_material_ambiguities": [],
            "producer": "execution-node-codex-semantic",
            "producer_version": "v1",
            "confidence": 0.9,
        },
    }


def test_validated_semantics_and_independent_currentness_reach_existing_controller_boundary() -> None:
    submitted: list[dict[str, Any]] = []
    result = advance_autonomy_ingress(
        envelope(),
        authority(),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=response,
        controller_boundary=lambda payload: submitted.append(payload) or {"status": "accepted_for_admission"},
    )

    assert result.status == AutonomyIngressStatus.HANDED_TO_CONTROLLER
    assert result.resolution is not None and result.resolution.packet is not None
    assert result.resolution.packet.admission_hint == "ready_for_controller_admission"
    assert len(submitted) == 1
    assert submitted[0]["authority"]["authority_commit"] == PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE
    source_ref = submitted[0]["harvest"]["objective"]["source_ref"]
    assert "producer-release=b9d6e0bd22ad5868e277fa465cb23ef829046aae" in source_ref
    assert f"programstart-release={PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE}" in source_ref
    assert result.semantic_effect_id in source_ref


def test_stale_authority_never_invokes_producer_or_controller() -> None:
    called: list[str] = []
    result = advance_autonomy_ingress(
        envelope(),
        authority(methodology="0" * 40),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=lambda _: called.append("producer"),
        controller_boundary=lambda _: called.append("controller"),
    )
    assert result.failure == AutonomyIngressFailure.STALE_AUTHORITY
    assert called == []


def test_semantic_authority_manufacture_never_crosses_boundary() -> None:
    submitted: list[dict[str, object]] = []

    def malicious(payload: dict[str, object]) -> dict[str, object]:
        value = response(payload)
        value["candidate"]["execution_permission"] = True  # type: ignore[index]
        return value

    result = advance_autonomy_ingress(
        envelope(),
        authority(),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=malicious,
        controller_boundary=lambda payload: submitted.append(payload),
    )
    assert result.failure == AutonomyIngressFailure.PRODUCER_FAILURE
    assert submitted == []


def test_wrong_producer_provenance_and_provider_failure_fail_closed() -> None:
    def wrong(payload: dict[str, object]) -> dict[str, object]:
        value = response(payload)
        value["candidate"]["producer"] = "other"  # type: ignore[index]
        return value

    result = advance_autonomy_ingress(
        envelope(), authority(), programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE, producer_boundary=wrong
    )
    assert result.failure == AutonomyIngressFailure.PRODUCER_PROVENANCE_MISMATCH

    result = advance_autonomy_ingress(
        envelope(),
        authority(),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=lambda _: (_ for _ in ()).throw(OSError()),
    )
    assert result.failure == AutonomyIngressFailure.PRODUCER_FAILURE


def test_same_effect_and_authority_with_changed_semantics_is_replay_conflict() -> None:
    first = advance_autonomy_ingress(
        envelope(), authority(), programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE, producer_boundary=response
    )
    assert first.replay_receipt is not None

    def changed(payload: dict[str, object]) -> dict[str, object]:
        value = copy.deepcopy(response(payload))
        value["candidate"]["objective"] = "A different objective."  # type: ignore[index]
        return value

    second = advance_autonomy_ingress(
        envelope(),
        authority(),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=changed,
        previous_replay=first.replay_receipt,
    )
    assert second.failure == AutonomyIngressFailure.REPLAY_CONFLICT
    assert second.controller_request is None


def test_ambiguity_and_controller_transport_failure_fail_closed() -> None:
    def ambiguous(payload: dict[str, object]) -> dict[str, object]:
        value = response(payload)
        value["candidate"].update(  # type: ignore[union-attr]
            converged=False,
            unresolved_material_ambiguities=["two owners remain plausible"],
        )
        return value

    result = advance_autonomy_ingress(
        envelope(), authority(), programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE, producer_boundary=ambiguous
    )
    assert result.failure == AutonomyIngressFailure.PRODUCER_FAILURE

    result = advance_autonomy_ingress(
        envelope(),
        authority(),
        programstart_release=PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE,
        producer_boundary=response,
        controller_boundary=lambda _: (_ for _ in ()).throw(TimeoutError()),
    )
    assert result.failure == AutonomyIngressFailure.CONTROLLER_FAILURE
    assert result.controller_request is not None
