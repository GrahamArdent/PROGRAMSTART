"""Regression tests for inspect-first audit Work Packet semantics."""

from __future__ import annotations

from scripts.programstart_intent_compile import (
    AuthoritySnapshot,
    IntentKind,
    SurfaceRef,
    SurfaceType,
    compile_work_packet,
)


def _writable_authority() -> AuthoritySnapshot:
    return AuthoritySnapshot(
        project_name="Writable Existing Project",
        owning_repository="GrahamArdent/example-project",
        authority_commit="example-authority-ref",
        authority_paths=["docs/MASTER_GAMEPLAN.md"],
        methodology_commit="example-programstart-ref",
        execution_mode="mode_c_existing_project",
        mutable_surfaces=[
            SurfaceRef(
                surface_type=SurfaceType.REPOSITORY,
                identifier="GrahamArdent/example-project",
                consequential=True,
            )
        ],
        allowed_effects=[
            "repository analysis",
            "bounded repository implementation after findings are reconciled",
        ],
    )


def test_uncontested_audit_packet_has_no_expected_write_set() -> None:
    packet = compile_work_packet(
        "Audit the existing project and identify what should happen next.",
        _writable_authority(),
        kind=IntentKind.AUDIT,
    )

    assert packet.scope.initial_posture == "read_only_until_findings_reconciled"
    assert packet.scope.mutable_identifiers == []
    assert packet.scope.read_only_identifiers == ["GrahamArdent/example-project"]
    assert packet.dependencies.expected_write_set == []
    assert packet.dependencies.conflicts == []
    assert "audit.inspect-first" in packet.transformation_rules


def test_same_authority_remains_mutable_for_bounded_execution_packet() -> None:
    packet = compile_work_packet(
        "Implement the already-authorized bounded repository slice.",
        _writable_authority(),
        kind=IntentKind.BOUNDED_EXECUTION,
    )

    assert packet.scope.initial_posture == "execute_within_authority"
    assert packet.scope.mutable_identifiers == ["GrahamArdent/example-project"]
    assert packet.dependencies.expected_write_set == ["repository:GrahamArdent/example-project"]
