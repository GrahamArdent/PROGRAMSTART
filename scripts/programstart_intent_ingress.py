"""Intent Ingress boundaries for natural-language PROGRAMSTART work.

The deterministic layer still does not interpret natural language. A trusted semantic
harvester supplies the conversation facts; a current authority resolver supplies owning
project/currentness. This module deterministically decides whether a short continuation
instruction should synthesize, compile, hand off, reuse/resume an existing Work Packet,
preserve a genuine human gate, or report closure.

Conversation states here are computed ingress classifications, not durable Controller
runtime states. The Autonomous Controller remains the durable execution/admission owner.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from .programstart_intent_compile import (
    AuthoritySnapshot,
    CompiledWorkPacket,
    IntentInterpretation,
    IntentKind,
    assess_authority_drift,
    compile_interpreted_work_packet,
    interpret_intent,
    render_chatgpt_prompt,
    verify_integrity,
)


class IntentIngressStatus(StrEnum):
    NEEDS_INTERPRETATION = "needs_interpretation"
    NEEDS_AUTHORITY = "needs_authority"
    COMPILED = "compiled"


class ConversationState(StrEnum):
    EXPLORE = "EXPLORE"
    CONVERGED = "CONVERGED"
    HANDOFF_READY = "HANDOFF_READY"
    EXECUTION_READY = "EXECUTION_READY"
    EXECUTING = "EXECUTING"
    GATED = "GATED"
    COMPLETE = "COMPLETE"


class ContextualTransitionAction(StrEnum):
    SYNTHESIZE_CURRENT_CONCLUSION = "synthesize_current_conclusion"
    REQUEST_MATERIAL_DECISION = "request_material_decision"
    RESOLVE_CURRENT_AUTHORITY = "resolve_current_authority"
    RECOVER_EXECUTION_STATE = "recover_execution_state"
    REVALIDATE_EXISTING_PACKET = "revalidate_existing_packet"
    CONTINUE_EXISTING_PACKET = "continue_existing_packet"
    RESUME_EXISTING_PACKET = "resume_existing_packet"
    COMPILE_FOR_ADMISSION = "compile_for_admission"
    COMPILE_OWNER_HANDOFF = "compile_owner_handoff"
    RECOMPILE_FOR_ADMISSION = "recompile_for_admission"
    RECOMPILE_OWNER_HANDOFF = "recompile_owner_handoff"
    PRESERVE_HUMAN_GATE = "preserve_human_gate"
    REPORT_COMPLETE = "report_complete"


class ConversationBasisSource(StrEnum):
    EXPLICIT_USER_INSTRUCTION = "explicit_user_instruction"
    ACCEPTED_CONVERSATION_DECISION = "accepted_conversation_decision"
    CURRENT_PROJECT_AUTHORITY = "current_project_authority"
    REPOSITORY_EVIDENCE = "repository_evidence"
    RUNTIME_EVIDENCE = "runtime_evidence"
    PROGRAMSTART_DEFAULT = "programstart_default"
    SYSTEM_INFERENCE = "system_inference"


class MaterialStatement(BaseModel):
    text: str
    source: ConversationBasisSource
    source_ref: str = ""

    @model_validator(mode="after")
    def text_must_be_present(self) -> MaterialStatement:
        if not self.text.strip():
            raise ValueError("material statement text must not be empty")
        return self


class CurrentnessCorrection(BaseModel):
    conversation_claim: str
    current_fact: str
    evidence_ref: str
    disposition: str = "superseded_by_current_evidence"

    @model_validator(mode="after")
    def correction_must_be_grounded(self) -> CurrentnessCorrection:
        if not self.conversation_claim.strip() or not self.current_fact.strip() or not self.evidence_ref.strip():
            raise ValueError("currentness correction requires claim, current fact, and evidence reference")
        return self


class HumanConsequenceGate(BaseModel):
    gate_id: str
    owner: str
    required_action: str
    acceptance_evidence: str
    safe_parallel_work: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def gate_must_be_actionable(self) -> HumanConsequenceGate:
        required = (self.gate_id, self.owner, self.required_action, self.acceptance_evidence)
        if any(not value.strip() for value in required):
            raise ValueError("human consequence gate requires id, owner, action, and acceptance evidence")
        return self


class ConversationHarvest(BaseModel):
    """Trusted semantic harvest of only execution-relevant conversation state.

    The harvester, not this deterministic resolver, decides which conversational material
    is accepted, rejected, speculative, superseded, or materially unresolved.
    """

    context_ref: str
    latest_operator_utterance: str
    objective: MaterialStatement | None = None
    intent_kind: IntentKind = IntentKind.UNKNOWN
    project_hint: str = ""
    converged: bool = False

    accepted_decisions: list[MaterialStatement] = Field(default_factory=list)
    rejected_alternatives: list[MaterialStatement] = Field(default_factory=list)
    brainstorming: list[MaterialStatement] = Field(default_factory=list)
    superseded_items: list[MaterialStatement] = Field(default_factory=list)
    active_constraints: list[MaterialStatement] = Field(default_factory=list)
    explicit_exclusions: list[MaterialStatement] = Field(default_factory=list)
    unresolved_material_ambiguities: list[MaterialStatement] = Field(default_factory=list)
    currentness_corrections: list[CurrentnessCorrection] = Field(default_factory=list)

    execution_underway: bool = False
    acceptance_met: bool = False
    existing_work_packet_ref: str = ""
    active_human_gate: HumanConsequenceGate | None = None

    @model_validator(mode="after")
    def required_context_must_be_present(self) -> ConversationHarvest:
        if not self.context_ref.strip():
            raise ValueError("context_ref must not be empty")
        if not self.latest_operator_utterance.strip():
            raise ValueError("latest_operator_utterance must not be empty")
        return self


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


class ContextualIntentRequest(BaseModel):
    harvest: ConversationHarvest
    current_repository: str = ""
    authority: AuthoritySnapshot | None = None
    existing_packet: CompiledWorkPacket | None = None


class ContextualIntentResolution(BaseModel):
    state: ConversationState
    action: ContextualTransitionAction
    harvest: ConversationHarvest
    packet: CompiledWorkPacket | None = None
    supersedes_specification_id: str | None = None
    handoff_repository: str | None = None
    operator_intervention_required: bool = False
    next_system_requirement: str | None = None
    gate: HumanConsequenceGate | None = None
    safe_parallel_work: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


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


def _execution_constraints(harvest: ConversationHarvest) -> list[str]:
    values = [statement.text for statement in harvest.accepted_decisions]
    values.extend(statement.text for statement in harvest.active_constraints)
    values.extend(f"Explicit exclusion: {statement.text}" for statement in harvest.explicit_exclusions)
    return values


def _interpret_harvest(harvest: ConversationHarvest) -> IntentInterpretation:
    objective = harvest.objective.text if harvest.objective is not None else harvest.latest_operator_utterance
    return interpret_intent(
        harvest.latest_operator_utterance,
        kind=harvest.intent_kind,
        interpreted_objective=objective,
        project_hint=harvest.project_hint,
        explicit_constraints=_execution_constraints(harvest),
        unresolved_ambiguities=[statement.text for statement in harvest.unresolved_material_ambiguities],
    )


def _semantic_gap(harvest: ConversationHarvest) -> bool:
    return not harvest.converged or harvest.objective is None or harvest.intent_kind == IntentKind.UNKNOWN


def _semantic_signature(intent: IntentInterpretation) -> tuple[object, ...]:
    """Compare executable semantics while intentionally ignoring the raw continuation wording."""

    return (
        intent.kind,
        intent.interpreted_objective,
        intent.project_hint,
        tuple(intent.explicit_constraints),
        tuple(intent.unresolved_ambiguities),
    )


def _partial_harvest_changes_packet(harvest: ConversationHarvest, existing: CompiledWorkPacket) -> bool:
    """Detect already-visible material drift without pretending an incomplete harvest is compilable."""

    if harvest.objective is not None and _normalize(harvest.objective.text) != existing.intent.interpreted_objective:
        return True
    if harvest.intent_kind != IntentKind.UNKNOWN and harvest.intent_kind != existing.intent.kind:
        return True
    existing_constraints = set(existing.intent.explicit_constraints)
    return any(value not in existing_constraints for value in _execution_constraints(harvest))


def _harvest_changes_packet(harvest: ConversationHarvest, existing: CompiledWorkPacket) -> bool:
    """Return true only when a complete current harvest materially changes packet semantics."""

    if _semantic_gap(harvest):
        return False
    return _semantic_signature(_interpret_harvest(harvest)) != _semantic_signature(existing.intent)


def _handoff_required(request: ContextualIntentRequest, authority: AuthoritySnapshot) -> bool:
    current = request.current_repository.strip()
    return bool(current and current != authority.owning_repository)


def _recompile_current_harvest(
    request: ContextualIntentRequest,
    existing: CompiledWorkPacket,
    authority: AuthoritySnapshot,
    *,
    note: str,
) -> ContextualIntentResolution:
    packet = compile_interpreted_work_packet(_interpret_harvest(request.harvest), authority)
    handoff = _handoff_required(request, authority)
    return ContextualIntentResolution(
        state=ConversationState.HANDOFF_READY if handoff else ConversationState.EXECUTION_READY,
        action=(
            ContextualTransitionAction.RECOMPILE_OWNER_HANDOFF
            if handoff
            else ContextualTransitionAction.RECOMPILE_FOR_ADMISSION
        ),
        harvest=request.harvest,
        packet=packet,
        supersedes_specification_id=existing.specification_id,
        handoff_repository=authority.owning_repository if handoff else None,
        notes=[note],
    )


def resolve_contextual_intent(request: ContextualIntentRequest) -> ContextualIntentResolution:
    """Resolve how the current conversation should advance without keyword-parsing `proceed`.

    This function assumes conversation semantics and current authority were produced by
    trusted upstream integrations. Missing machine-resolvable context becomes a system
    requirement, not an operator form-filling request.
    """

    harvest = request.harvest
    existing = request.existing_packet
    authority = request.authority

    if existing is not None and not verify_integrity(existing):
        raise ValueError("existing compiled Work Packet failed integrity verification")

    if harvest.active_human_gate is not None:
        return ContextualIntentResolution(
            state=ConversationState.GATED,
            action=ContextualTransitionAction.PRESERVE_HUMAN_GATE,
            harvest=harvest,
            packet=existing,
            operator_intervention_required=True,
            gate=harvest.active_human_gate,
            safe_parallel_work=list(harvest.active_human_gate.safe_parallel_work),
            notes=["Generic continuation language does not satisfy a stronger admitted human consequence gate."],
        )

    if harvest.acceptance_met:
        return ContextualIntentResolution(
            state=ConversationState.COMPLETE,
            action=ContextualTransitionAction.REPORT_COMPLETE,
            harvest=harvest,
            packet=existing,
            notes=["Current acceptance criteria are already met; do not invent another work packet."],
        )

    if harvest.unresolved_material_ambiguities:
        return ContextualIntentResolution(
            state=ConversationState.EXPLORE,
            action=ContextualTransitionAction.REQUEST_MATERIAL_DECISION,
            harvest=harvest,
            packet=existing,
            operator_intervention_required=True,
            notes=["Only material unresolved ambiguity is surfaced to the operator."],
        )

    if harvest.execution_underway and existing is None:
        reference = harvest.existing_work_packet_ref.strip()
        requirement = "recover the durable active Work Packet and current Controller/project execution state"
        if reference:
            requirement = f"recover active Work Packet {reference} and current Controller/project execution state"
        return ContextualIntentResolution(
            state=ConversationState.CONVERGED,
            action=ContextualTransitionAction.RECOVER_EXECUTION_STATE,
            harvest=harvest,
            next_system_requirement=requirement,
            notes=["Do not compile duplicate work merely because the originating conversation lost local packet state."],
        )

    if existing is not None:
        if authority is None:
            return ContextualIntentResolution(
                state=ConversationState.EXECUTING if harvest.execution_underway else ConversationState.EXECUTION_READY,
                action=ContextualTransitionAction.REVALIDATE_EXISTING_PACKET,
                harvest=harvest,
                packet=existing,
                next_system_requirement="resolve current owning-project authority and revalidate the existing Work Packet",
                notes=[
                    "An existing Work Packet is reused; missing currentness is a machine integration boundary, "
                    "not a reason to replan."
                ],
            )

        drift = assess_authority_drift(existing, authority)
        if drift.status == "unchanged":
            if _semantic_gap(harvest) and _partial_harvest_changes_packet(harvest, existing):
                return ContextualIntentResolution(
                    state=ConversationState.CONVERGED,
                    action=ContextualTransitionAction.RECOVER_EXECUTION_STATE,
                    harvest=harvest,
                    packet=existing,
                    next_system_requirement=(
                        "recover complete current conversation semantics before deciding whether the active Work Packet "
                        "must be replaced"
                    ),
                    notes=[
                        "Partial conversation recovery already contains material semantic drift; do not silently reuse "
                        "or recompile from incomplete semantics."
                    ],
                )
            if _harvest_changes_packet(harvest, existing):
                return _recompile_current_harvest(
                    request,
                    existing,
                    authority,
                    note=(
                        "Accepted conversation semantics changed while authority remained current; "
                        "recompile before Controller readmission."
                    ),
                )
            return ContextualIntentResolution(
                state=ConversationState.EXECUTING if harvest.execution_underway else ConversationState.EXECUTION_READY,
                action=(
                    ContextualTransitionAction.RESUME_EXISTING_PACKET
                    if harvest.execution_underway
                    else ContextualTransitionAction.CONTINUE_EXISTING_PACKET
                ),
                harvest=harvest,
                packet=existing,
                notes=["Existing sealed Work Packet remains current; repeated continuation must not create duplicate work."],
            )

        if _semantic_gap(harvest):
            return ContextualIntentResolution(
                state=ConversationState.CONVERGED,
                action=ContextualTransitionAction.RECOVER_EXECUTION_STATE,
                harvest=harvest,
                packet=existing,
                next_system_requirement="recover current conversation semantics before recompiling the drifted Work Packet",
                notes=["Authority drift invalidated the packet; stale chat must not be replayed as current authority."],
            )

        return _recompile_current_harvest(
            request,
            existing,
            authority,
            note="Current authority superseded stale packet inputs; recompile before Controller readmission.",
        )

    if _semantic_gap(harvest):
        return ContextualIntentResolution(
            state=ConversationState.EXPLORE,
            action=ContextualTransitionAction.SYNTHESIZE_CURRENT_CONCLUSION,
            harvest=harvest,
            notes=["Conversation has not converged enough to fabricate executable work."],
        )

    if authority is None:
        return ContextualIntentResolution(
            state=ConversationState.CONVERGED,
            action=ContextualTransitionAction.RESOLVE_CURRENT_AUTHORITY,
            harvest=harvest,
            next_system_requirement="resolve current owning-project authority/currentness and active parallel mutation ownership",
            notes=["Do not ask the operator to hand-author authority fields that the ecosystem should retrieve."],
        )

    packet = compile_interpreted_work_packet(_interpret_harvest(harvest), authority)
    handoff = _handoff_required(request, authority)
    return ContextualIntentResolution(
        state=ConversationState.HANDOFF_READY if handoff else ConversationState.EXECUTION_READY,
        action=(
            ContextualTransitionAction.COMPILE_OWNER_HANDOFF
            if handoff
            else ContextualTransitionAction.COMPILE_FOR_ADMISSION
        ),
        harvest=harvest,
        packet=packet,
        handoff_repository=authority.owning_repository if handoff else None,
        notes=["Compiled packet is ready for the normal PROGRAMSTART/Controller admission boundary."],
    )


def _statement_bullets(values: list[MaterialStatement], empty: str = "none") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(
        f"- {item.text} [source: {item.source.value}{f'; ref: {item.source_ref}' if item.source_ref else ''}]"
        for item in values
    )


def render_contextual_handoff(resolution: ContextualIntentResolution) -> str:
    """Render only the extra conversation context a worker cannot derive from the packet.

    Brainstorming and superseded ideas are intentionally omitted. Rejected alternatives
    are context only and cannot widen the sealed packet.
    """

    packet = resolution.packet
    if packet is None:
        raise ValueError("contextual handoff requires a compiled or reusable Work Packet")
    if not verify_integrity(packet):
        raise ValueError("compiled Work Packet integrity verification failed")

    harvest = resolution.harvest
    correction_lines = [
        (
            f"- conversation: {item.conversation_claim} -> current: {item.current_fact} "
            f"[evidence: {item.evidence_ref}; disposition: {item.disposition}]"
        )
        for item in harvest.currentness_corrections
    ]

    contextual = [
        "<!-- DERIVED CONTEXTUAL HANDOFF: sealed Work Packet remains canonical execution semantics. -->",
        f"Conversation-Context-Ref: {harvest.context_ref}",
        f"Resolved-Conversation-State: {resolution.state.value}",
        "",
        "## Accepted conversation decisions / constraints",
        _statement_bullets([*harvest.accepted_decisions, *harvest.active_constraints, *harvest.explicit_exclusions]),
        "",
        "## Rejected alternatives (context only; not additional authority)",
        _statement_bullets(harvest.rejected_alternatives),
        "",
        "## Currentness corrections",
        "\n".join(correction_lines) if correction_lines else "- none",
        "",
        (
            "The contextual section above preserves decision provenance. It does not expand the Work Packet, "
            "current project authority, or Controller admission."
        ),
        "",
    ]
    return "\n".join(contextual) + render_chatgpt_prompt(packet)