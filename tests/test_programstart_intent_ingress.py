"""Focused tests for the lean PROGRAMSTART Intent Ingress boundary."""

from __future__ import annotations

from scripts.programstart_intent_compile import (
    AuthoritySnapshot,
    IntentKind,
    SurfaceRef,
    SurfaceType,
    interpret_intent,
    verify_integrity,
)
from scripts.programstart_intent_ingress import (
    IntentIngressRequest,
    IntentIngressStatus,
    advance_intent_ingress,
)


def _authority() -> AuthoritySnapshot:
    return AuthoritySnapshot(
        project_name="Example Existing Project",
        owning_repository="GrahamArdent/example-project",
        authority_commit="example-authority-ref",
        authority_paths=["docs/MASTER_GAMEPLAN.md"],
        methodology_commit="example-programstart-ref",
        execution_mode="mode_c_existing_project",
        mutable_surfaces=[
            SurfaceRef(
                surface_type=SurfaceType.REPOSITORY,
                identifier="GrahamArdent/example-project",
            )
        ],
        read_only_surfaces=[
            SurfaceRef(
                surface_type=SurfaceType.REPOSITORY,
                identifier="GrahamArdent/shared-infrastructure",
            )
        ],
        allowed_effects=["bounded repository implementation"],
        prohibited_effects=["new spend", "destructive provider mutation"],
        acceptance_conditions=["targeted verification passes"],
        challenge_required=True,
    )


def test_raw_request_alone_stops_at_interpretation_boundary() -> None:
    request = IntentIngressRequest(raw_intent="Continue the existing project.")

    result = advance_intent_ingress(request)

    assert result.status == IntentIngressStatus.NEEDS_INTERPRETATION
    assert result.packet is None
    assert result.next_required_input == "trusted semantic interpretation"


def test_trusted_interpretation_without_authority_stops_at_authority_boundary() -> None:
    request = IntentIngressRequest(raw_intent="Continue the existing project.")
    interpretation = interpret_intent(
        request.raw_intent,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Continue the current authorized project slice.",
    )

    result = advance_intent_ingress(request, interpretation=interpretation)

    assert result.status == IntentIngressStatus.NEEDS_AUTHORITY
    assert result.packet is None
    assert result.next_required_input == "current owning-project authority snapshot"


def test_resolved_inputs_compile_immediately_without_extra_ingress_state() -> None:
    request = IntentIngressRequest(raw_intent="Continue the existing project.")
    interpretation = interpret_intent(
        request.raw_intent,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Continue the current authorized project slice.",
    )

    result = advance_intent_ingress(
        request,
        interpretation=interpretation,
        authority=_authority(),
    )

    assert result.status == IntentIngressStatus.COMPILED
    assert result.next_required_input is None
    assert result.packet is not None
    assert result.packet.owning_repository == "GrahamArdent/example-project"
    assert verify_integrity(result.packet)


def test_unresolved_semantic_ambiguity_never_falls_through_to_compilation() -> None:
    request = IntentIngressRequest(raw_intent="Do whatever makes sense with the project.")
    interpretation = interpret_intent(
        request.raw_intent,
        kind=IntentKind.UNKNOWN,
        unresolved_ambiguities=["The requested work family is materially unclear."],
    )

    result = advance_intent_ingress(
        request,
        interpretation=interpretation,
        authority=_authority(),
    )

    assert result.status == IntentIngressStatus.NEEDS_INTERPRETATION
    assert result.packet is None


def test_compiler_does_not_extract_constraints_from_english_phrases() -> None:
    raw = "Continue the project, but don't interfere with shared infrastructure."

    interpretation = interpret_intent(raw, kind=IntentKind.CONTINUATION)

    assert interpretation.explicit_constraints == []


def test_trusted_explicit_constraints_are_preserved_without_expanding_authority() -> None:
    raw = "Continue the project, but don't interfere with shared infrastructure."
    request = IntentIngressRequest(raw_intent=raw)
    constraint = "Do not interfere with active shared-infrastructure work."
    interpretation = interpret_intent(
        raw,
        kind=IntentKind.CONTINUATION,
        explicit_constraints=[constraint],
    )

    result = advance_intent_ingress(
        request,
        interpretation=interpretation,
        authority=_authority(),
    )

    assert result.packet is not None
    assert result.packet.intent.explicit_constraints == [constraint]
    assert result.packet.scope.mutable_identifiers == ["GrahamArdent/example-project"]
    assert "GrahamArdent/shared-infrastructure" in result.packet.scope.read_only_identifiers


def test_interpretation_for_different_raw_request_is_rejected() -> None:
    request = IntentIngressRequest(raw_intent="Continue the existing project.")
    interpretation = interpret_intent(
        "Audit the existing project.",
        kind=IntentKind.AUDIT,
    )

    try:
        advance_intent_ingress(request, interpretation=interpretation, authority=_authority())
    except ValueError as exc:
        assert "does not describe the current raw intent" in str(exc)
    else:  # pragma: no cover - explicit failure message is more useful than bare assert False
        raise AssertionError("mismatched interpretation should have been rejected")
