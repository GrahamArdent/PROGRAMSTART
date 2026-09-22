"""Owner-bound integration for semantic harvest, currentness, and Controller handoff.

This module composes existing PROGRAMSTART contracts.  It does not discover authority,
invoke a provider SDK, admit Controller work, or persist a second lifecycle.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .programstart_intent_compile import AuthoritySnapshot, CompiledWorkPacket, authority_fingerprint
from .programstart_intent_ingress import (
    BoundedIntentEnvelope,
    ContextualIntentRequest,
    ContextualIntentResolution,
    ContextualTransitionAction,
    ConversationHarvest,
    SemanticInterpretationCandidate,
    SemanticProducerRequest,
    build_trusted_conversation_harvest,
    resolve_contextual_intent,
    validate_semantic_producer_response,
)

PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE = "e5fe99e74c3bbba7003344dd602f4bed26dd9e53"  # pragma: allowlist secret
EXECUTION_NODE_PRODUCER_RELEASE = "b9d6e0bd22ad5868e277fa465cb23ef829046aae"  # pragma: allowlist secret
CONTROLLER_CONTEXTUAL_RELEASE = "731aac5a1c0bdd8cce678032fcd91e587eb817f4"  # pragma: allowlist secret
EXPECTED_PRODUCER = "execution-node-codex-semantic"
EXPECTED_PRODUCER_VERSION = "v1"

SemanticProducerBoundary = Callable[[dict[str, Any]], Any]
ControllerBoundary = Callable[[dict[str, Any]], Any]


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


class AuthorityResolutionEvidence(BaseModel):
    """Evidence emitted by an independent resolver, never by the semantic producer."""

    model_config = ConfigDict(extra="forbid")

    snapshot: AuthoritySnapshot
    resolution_ref: str
    observed_authority_commit: str
    observed_methodology_commit: str
    observed_current_work_refs: list[str] = Field(default_factory=list)
    observed_authority_fingerprint: str

    @model_validator(mode="after")
    def evidence_must_bind_exact_current_snapshot(self) -> AuthorityResolutionEvidence:
        if not self.resolution_ref.strip():
            raise ValueError("authority resolution requires a durable evidence reference")
        if self.snapshot.authority_commit != self.observed_authority_commit:
            raise ValueError("authority snapshot is stale relative to observed owning authority")
        if self.snapshot.methodology_commit != self.observed_methodology_commit:
            raise ValueError("authority snapshot is stale relative to observed PROGRAMSTART authority")
        if self.snapshot.current_work_refs != self.observed_current_work_refs:
            raise ValueError("authority snapshot is stale relative to observed current work")
        if authority_fingerprint(self.snapshot) != self.observed_authority_fingerprint:
            raise ValueError("authority snapshot provenance does not match observed currentness")
        return self


class SemanticReplayReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    semantic_effect_id: str
    authority_fingerprint: str
    semantic_candidate_digest: str


class AutonomyIngressStatus(StrEnum):
    READY_FOR_CONTROLLER = "ready_for_controller"
    HANDED_TO_CONTROLLER = "handed_to_controller"
    FAILED_CLOSED = "failed_closed"


class AutonomyIngressFailure(StrEnum):
    PRODUCER_FAILURE = "producer_failure"
    PRODUCER_PROVENANCE_MISMATCH = "producer_provenance_mismatch"
    STALE_AUTHORITY = "stale_authority"
    REPLAY_CONFLICT = "replay_conflict"
    OWNER_HANDOFF_REQUIRED = "owner_handoff_required"
    NOT_ADMISSION_READY = "not_admission_ready"
    CONTROLLER_FAILURE = "controller_failure"


class AutonomyIngressResult(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    status: AutonomyIngressStatus
    semantic_effect_id: str
    programstart_contract_release: str = PROGRAMSTART_SEMANTIC_CONTRACT_RELEASE
    programstart_authority_release: str
    producer_release: str = EXECUTION_NODE_PRODUCER_RELEASE
    controller_release: str = CONTROLLER_CONTEXTUAL_RELEASE
    authority_resolution_ref: str
    replay_receipt: SemanticReplayReceipt | None = None
    harvest: ConversationHarvest | None = None
    resolution: ContextualIntentResolution | None = None
    controller_request: ContextualIntentRequest | None = None
    controller_evidence: Any | None = None
    failure: AutonomyIngressFailure | None = None


def _semantic_digest(candidate: SemanticInterpretationCandidate) -> str:
    return _digest(candidate.model_dump(mode="json"))


def _bind_semantic_provenance(
    harvest: ConversationHarvest,
    *,
    effect_id: str,
    programstart_release: str,
) -> None:
    source_ref = (
        f"semantic-producer:{EXPECTED_PRODUCER}@{EXPECTED_PRODUCER_VERSION};"
        f"producer-release={EXECUTION_NODE_PRODUCER_RELEASE};"
        f"programstart-release={programstart_release};effect={effect_id}"
    )
    statements = [
        harvest.objective,
        *harvest.accepted_decisions,
        *harvest.active_constraints,
        *harvest.explicit_exclusions,
        *harvest.unresolved_material_ambiguities,
    ]
    for statement in statements:
        if statement is not None:
            statement.source_ref = source_ref


def advance_autonomy_ingress(
    envelope: BoundedIntentEnvelope,
    authority_evidence: AuthorityResolutionEvidence,
    *,
    programstart_release: str,
    producer_boundary: SemanticProducerBoundary,
    controller_boundary: ControllerBoundary | None = None,
    existing_packet: CompiledWorkPacket | None = None,
    previous_replay: SemanticReplayReceipt | None = None,
) -> AutonomyIngressResult:
    """Compose the released producer with existing PROGRAMSTART/Controller boundaries."""

    request = SemanticProducerRequest.from_envelope(envelope)
    common: dict[str, Any] = {
        "semantic_effect_id": request.semantic_effect_id,
        "programstart_authority_release": authority_evidence.observed_methodology_commit,
        "authority_resolution_ref": authority_evidence.resolution_ref,
    }
    if authority_evidence.observed_methodology_commit != programstart_release:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.STALE_AUTHORITY,
            **common,
        )

    try:
        raw_response = producer_boundary(request.model_dump(mode="json"))
    except Exception:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.PRODUCER_FAILURE,
            **common,
        )
    validated = validate_semantic_producer_response(request, raw_response)
    if not validated.accepted or validated.candidate is None:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.PRODUCER_FAILURE,
            **common,
        )
    candidate = validated.candidate
    if candidate.producer != EXPECTED_PRODUCER or candidate.producer_version != EXPECTED_PRODUCER_VERSION:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.PRODUCER_PROVENANCE_MISMATCH,
            **common,
        )

    fingerprint = authority_fingerprint(authority_evidence.snapshot)
    receipt = SemanticReplayReceipt(
        semantic_effect_id=request.semantic_effect_id,
        authority_fingerprint=fingerprint,
        semantic_candidate_digest=_semantic_digest(candidate),
    )
    if previous_replay is not None and (
        previous_replay.semantic_effect_id == receipt.semantic_effect_id
        and previous_replay.authority_fingerprint == receipt.authority_fingerprint
        and previous_replay.semantic_candidate_digest != receipt.semantic_candidate_digest
    ):
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.REPLAY_CONFLICT,
            replay_receipt=receipt,
            **common,
        )

    harvest = build_trusted_conversation_harvest(envelope, candidate)
    _bind_semantic_provenance(
        harvest,
        effect_id=request.semantic_effect_id,
        programstart_release=authority_evidence.observed_methodology_commit,
    )
    contextual_request = ContextualIntentRequest(
        harvest=harvest,
        authority=authority_evidence.snapshot,
        existing_packet=existing_packet,
    )
    resolution = resolve_contextual_intent(contextual_request)
    if resolution.action in {
        ContextualTransitionAction.COMPILE_OWNER_HANDOFF,
        ContextualTransitionAction.RECOMPILE_OWNER_HANDOFF,
    }:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.OWNER_HANDOFF_REQUIRED,
            replay_receipt=receipt,
            harvest=harvest,
            resolution=resolution,
            **common,
        )
    if resolution.packet is None or resolution.packet.admission_hint != "ready_for_controller_admission":
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.NOT_ADMISSION_READY,
            replay_receipt=receipt,
            harvest=harvest,
            resolution=resolution,
            **common,
        )

    if controller_boundary is None:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.READY_FOR_CONTROLLER,
            replay_receipt=receipt,
            harvest=harvest,
            resolution=resolution,
            controller_request=contextual_request,
            **common,
        )
    try:
        evidence = controller_boundary(contextual_request.model_dump(mode="json"))
    except Exception:
        return AutonomyIngressResult(
            status=AutonomyIngressStatus.FAILED_CLOSED,
            failure=AutonomyIngressFailure.CONTROLLER_FAILURE,
            replay_receipt=receipt,
            harvest=harvest,
            resolution=resolution,
            controller_request=contextual_request,
            **common,
        )
    return AutonomyIngressResult(
        status=AutonomyIngressStatus.HANDED_TO_CONTROLLER,
        replay_receipt=receipt,
        harvest=harvest,
        resolution=resolution,
        controller_request=contextual_request,
        controller_evidence=evidence,
        **common,
    )
