"""Lean pre-entry Intent Ingress scaffold for PROGRAMSTART.

This module is intentionally not an interpreter, authority resolver, Controller, queue,
or durable state machine. It only makes the handoff boundaries explicit:

raw operator intent -> trusted semantic interpretation -> resolved authority -> compile

Missing inputs remain visible instead of being guessed. When both trusted inputs exist,
the existing deterministic Work Packet compiler is invoked immediately.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, model_validator

from .programstart_intent_compile import (
    AuthoritySnapshot,
    CompiledWorkPacket,
    IntentInterpretation,
    IntentKind,
    compile_interpreted_work_packet,
)


class IntentIngressStatus(StrEnum):
    NEEDS_INTERPRETATION = "needs_interpretation"
    NEEDS_AUTHORITY = "needs_authority"
    COMPILED = "compiled"


class IntentIngressRequest(BaseModel):
    raw_intent: str

    @model_validator(mode="after")
    def raw_intent_must_be_present(self) -> IntentIngressRequest:
        if not self.raw_intent.strip():
            raise ValueError("raw_intent must not be empty")
        return self


class IntentIngressResult(BaseModel):
    status: IntentIngressStatus
    request: IntentIngressRequest
    interpretation: IntentInterpretation | None = None
    packet: CompiledWorkPacket | None = None
    next_required_input: str | None = None


def _normalize(value: str) -> str:
    return " ".join(value.strip().split())


def advance_intent_ingress(
    request: IntentIngressRequest,
    *,
    interpretation: IntentInterpretation | None = None,
    authority: AuthoritySnapshot | None = None,
) -> IntentIngressResult:
    """Advance one stateless Intent Ingress step without inventing missing truth."""

    if interpretation is None:
        return IntentIngressResult(
            status=IntentIngressStatus.NEEDS_INTERPRETATION,
            request=request,
            next_required_input="trusted semantic interpretation",
        )

    if interpretation.normalized_intent != _normalize(request.raw_intent):
        raise ValueError("interpretation does not describe the current raw intent")

    if interpretation.kind == IntentKind.UNKNOWN or interpretation.unresolved_ambiguities:
        return IntentIngressResult(
            status=IntentIngressStatus.NEEDS_INTERPRETATION,
            request=request,
            interpretation=interpretation,
            next_required_input="resolved material semantic ambiguity",
        )

    if authority is None:
        return IntentIngressResult(
            status=IntentIngressStatus.NEEDS_AUTHORITY,
            request=request,
            interpretation=interpretation,
            next_required_input="current owning-project authority snapshot",
        )

    packet = compile_interpreted_work_packet(interpretation, authority)
    return IntentIngressResult(
        status=IntentIngressStatus.COMPILED,
        request=request,
        interpretation=interpretation,
        packet=packet,
    )
