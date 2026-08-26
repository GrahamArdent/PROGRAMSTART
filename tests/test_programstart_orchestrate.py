from __future__ import annotations

from scripts.programstart_orchestrate import build_plan


def test_new_request_defaults_to_mode_a_without_target() -> None:
    plan = build_plan(request="Build a small API")

    assert plan.environment == "local"
    assert plan.mode == "a"
    assert plan.decision_route is None
    assert "PROGRAMBUILD default" in plan.execution_spine


def test_research_backed_request_uses_mode_b() -> None:
    plan = build_plan(request="Turn this research into a product", research_backed=True)

    assert plan.mode == "b"
    assert any("Research evidence" in item for item in plan.authority_loading)


def test_repository_target_does_not_automatically_become_mode_c() -> None:
    plan = build_plan(
        request="Build the next capability",
        repository="GrahamArdent/Dedication-Email-Bridge",
    )

    assert plan.environment == "connected-tools"
    assert plan.mode == "unresolved"
    assert "repository existence alone" in plan.mode_reason
    assert "deferred" in plan.decision_trigger.lower()
    assert any("connected repository tools" in item for item in plan.orientation_actions)


def test_connected_mode_c_preserves_existing_execution_spine_and_does_not_claim_local_cli() -> None:
    plan = build_plan(
        request="Add Gmail OAuth runtime activation",
        repository="GrahamArdent/Dedication-Email-Bridge",
        environment="connected-tools",
        mode="c",
        execution_spine="PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md",
    )

    assert plan.mode == "c"
    assert plan.execution_spine == "PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md"
    assert any("connected repository/runtime tools" in item for item in plan.execution_handoff)
    assert any("do not claim a local CLI command ran" in item for item in plan.execution_handoff)
    assert "A second master plan" in plan.work_packet.out_of_scope[0]


def test_material_uncertainty_routes_through_existing_adaptive_router() -> None:
    plan = build_plan(
        request="Choose an external provider contract",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
        decision="Choose the provider integration contract",
        impact="high",
        uncertainty="high",
        evidence_state="conflicting",
        reversibility="hard",
        concerns=("contract", "verification"),
    )

    assert plan.decision_route is not None
    assert plan.decision_route.route == "investigate"
    assert plan.decision_route.research_depth == "deep"
    assert any(check.name == "mode-c-delta" for check in plan.decision_route.activated_checks)


def test_no_router_ceremony_when_no_material_signal_is_supplied() -> None:
    plan = build_plan(
        request="Implement the already-decided bounded slice",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
    )

    assert plan.decision_route is None
    assert "Do not invoke adaptive routing as ceremony" in plan.decision_trigger


def test_environment_target_mismatch_is_rejected() -> None:
    try:
        build_plan(
            request="Do work",
            repo="./project",
            environment="connected-tools",
        )
    except ValueError as exc:
        assert "--repo is a local checkout path" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected environment/target mismatch to fail")
