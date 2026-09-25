"""Pure objective continuation decisions from sealed PROGRAMSTART semantics.

This module does not execute effects or bind execution arguments.  It only selects an
already-admitted semantic effect token, reports an explicit wait, or reports root-level
terminality when current, bound evidence proves it.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from .programstart_intent_compile import (
    AuthoritySnapshot,
    CompiledWorkPacket,
    assess_authority_drift,
    authority_fingerprint,
    verify_integrity,
)


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RootObjective(_StrictModel):
    root_id: str = Field(min_length=1, max_length=256)
    objective: str = Field(min_length=1, max_length=16_384)

    @model_validator(mode="after")
    def reject_surrounding_whitespace(self) -> RootObjective:
        if self.root_id != self.root_id.strip() or self.objective != self.objective.strip():
            raise ValueError("root objective fields must not have surrounding whitespace")
        return self


class _BoundEvidence(_StrictModel):
    evidence_id: str = Field(min_length=1, max_length=256)
    status: Literal["accepted", "proven"]
    root_id: str = Field(min_length=1, max_length=256)
    work_packet_specification_id: str = Field(min_length=1, max_length=256)
    authority_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


class CompletedEffectEvidence(_BoundEvidence):
    kind: Literal["effect_completed"] = "effect_completed"
    semantic_effect_token: str = Field(min_length=1, max_length=4096)


class EffectReadyEvidence(_BoundEvidence):
    """Owner-produced proof that one admitted semantic effect is ready."""

    kind: Literal["effect_ready"] = "effect_ready"
    status: Literal["proven"]
    semantic_effect_token: str = Field(min_length=1, max_length=4096)
    preconditions_proven: Literal[True]


class RootTerminalEvidence(_BoundEvidence):
    kind: Literal["root_terminal"] = "root_terminal"
    disposition: Literal["terminal", "impossible"]
    evidence_scope: Literal["root_objective"]
    basis: str = Field(min_length=1, max_length=16_384)


class MachineWaitEvidence(_BoundEvidence):
    kind: Literal["machine_wait"] = "machine_wait"
    condition: str = Field(min_length=1, max_length=4096)
    active: Literal[True]


class HumanWaitEvidence(_BoundEvidence):
    kind: Literal["human_wait"] = "human_wait"
    admitted_gate_condition: str = Field(min_length=1, max_length=4096)
    active: Literal[True]


ObjectiveEvidence = Annotated[
    CompletedEffectEvidence | EffectReadyEvidence | RootTerminalEvidence | MachineWaitEvidence | HumanWaitEvidence,
    Field(discriminator="kind"),
]
OBJECTIVE_EVIDENCE_ADAPTER = TypeAdapter(list[ObjectiveEvidence])


class ContinuationDisposition(StrEnum):
    EFFECT = "effect"
    REORIENT = "reorient"
    WAIT_MACHINE = "wait_machine"
    WAIT_HUMAN = "wait_human"
    TERMINAL = "terminal"
    IMPOSSIBLE = "impossible"


class ObjectiveContinuationDecision(_StrictModel):
    disposition: ContinuationDisposition
    semantic_effect_token: str | None = None

    @model_validator(mode="after")
    def effect_only_for_selection(self) -> ObjectiveContinuationDecision:
        has_effect = self.semantic_effect_token is not None
        if has_effect != (self.disposition == ContinuationDisposition.EFFECT):
            raise ValueError("semantic_effect_token is required only for effect")
        return self


def _reorient() -> ObjectiveContinuationDecision:
    return ObjectiveContinuationDecision(disposition=ContinuationDisposition.REORIENT)


def _is_abstract_effect(token: str) -> bool:
    """Reject execution material that cannot safely be returned as an effect."""

    lowered = token.casefold()
    forbidden_fragments = (
        "://",
        "--",
        "api key",
        "access token",
        "credential",
        "password",
        "workspace id",
        "workspace_id",
        "endpoint",
        "transport",
    )
    command_prefixes = ("git ", "gh ", "uv ", "python ", "python3 ", "curl ", "ssh ", "docker ", "kubectl ")
    sha = re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?:[0-9a-f]{24})?(?![0-9a-f])", lowered)
    return not (
        token != token.strip()
        or any(character in token for character in ("\n", "\r", ";", "|", "`", "$"))
        or any(fragment in lowered for fragment in forbidden_fragments)
        or lowered.startswith(command_prefixes)
        or sha
    )


def evaluate_objective_continuation(
    root_objective: RootObjective,
    packet: CompiledWorkPacket,
    current_authority: AuthoritySnapshot,
    evidence: Sequence[ObjectiveEvidence],
) -> ObjectiveContinuationDecision:
    """Return a deterministic semantic decision without minting authority."""

    if not verify_integrity(packet):
        return _reorient()

    if packet.evidence.authority_fingerprint != authority_fingerprint(packet.authority):
        return _reorient()

    drift = assess_authority_drift(packet, current_authority)
    if drift.status != "unchanged":
        return _reorient()

    current_fingerprint = authority_fingerprint(current_authority)
    expected_binding = (
        root_objective.root_id,
        packet.specification_id,
        current_fingerprint,
    )
    if len({item.evidence_id for item in evidence}) != len(evidence):
        return _reorient()
    if any(
        (
            item.root_id,
            item.work_packet_specification_id,
            item.authority_fingerprint,
        )
        != expected_binding
        for item in evidence
    ):
        return _reorient()

    allowed = packet.scope.allowed_effects
    if len(set(allowed)) != len(allowed):
        return _reorient()
    prohibited = set(packet.scope.prohibited_effects)
    completed_items = [item for item in evidence if isinstance(item, CompletedEffectEvidence)]
    completed = {item.semantic_effect_token for item in completed_items}
    if len(completed) != len(completed_items):
        return _reorient()
    if not completed.issubset(set(allowed)):
        return _reorient()

    ready = [item for item in evidence if isinstance(item, EffectReadyEvidence)]
    if len(ready) > 1:
        return _reorient()
    if ready:
        ready_effect = ready[0].semantic_effect_token
        if ready_effect not in set(allowed):
            return _reorient()
        if ready_effect in prohibited or ready_effect in completed or not _is_abstract_effect(ready_effect):
            return _reorient()

    terminal = [item for item in evidence if isinstance(item, RootTerminalEvidence)]
    if terminal:
        if ready or any(isinstance(item, (MachineWaitEvidence, HumanWaitEvidence)) for item in evidence):
            return _reorient()
        if any(item.status != "proven" for item in terminal):
            return _reorient()
        dispositions = {item.disposition for item in terminal}
        if len(dispositions) != 1:
            return _reorient()
        selected = sorted(terminal, key=lambda item: item.evidence_id)[0]
        return ObjectiveContinuationDecision(
            disposition=ContinuationDisposition(selected.disposition),
        )

    waits = [item for item in evidence if isinstance(item, (MachineWaitEvidence, HumanWaitEvidence))]
    admitted_waits: list[MachineWaitEvidence | HumanWaitEvidence] = []
    for item in waits:
        if ready:
            return _reorient()
        if isinstance(item, HumanWaitEvidence):
            if item.admitted_gate_condition not in packet.autonomy.human_gates:
                return _reorient()
        elif item.condition not in packet.autonomy.temporary_automation_gaps:
            return _reorient()
        admitted_waits.append(item)
    if admitted_waits:
        if len(admitted_waits) != 1:
            return _reorient()
        selected_wait = admitted_waits[0]
        disposition = (
            ContinuationDisposition.WAIT_HUMAN
            if isinstance(selected_wait, HumanWaitEvidence)
            else ContinuationDisposition.WAIT_MACHINE
        )
        return ObjectiveContinuationDecision(
            disposition=disposition,
        )

    if len(ready) != 1:
        return _reorient()

    ready_effect = ready[0].semantic_effect_token
    return ObjectiveContinuationDecision(
        disposition=ContinuationDisposition.EFFECT,
        semantic_effect_token=ready_effect,
    )
