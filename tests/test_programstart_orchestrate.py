from __future__ import annotations

import json

import pytest

from scripts.programstart_orchestrate import build_plan, main, render_text


def test_new_request_defaults_to_mode_a_without_target() -> None:
    plan = build_plan(request="Build a small API")

    assert plan.environment == "local"
    assert plan.mode == "a"
    assert plan.decision_route is None
    assert "PROGRAMBUILD default" in plan.execution_spine


def test_research_backed_request_uses_mode_b() -> None:
    plan = build_plan(request="Turn this research into a product", research_backed=True)

    assert plan.mode == "b"
    assert any("research" in item.lower() for item in plan.authority_loading)


def test_repository_target_does_not_automatically_become_mode_c() -> None:
    plan = build_plan(
        request="Build the next capability",
        repository="GrahamArdent/Dedication-Email-Bridge",
    )

    assert plan.environment == "connected-tools"
    assert plan.mode == "unresolved"
    assert "repository existence alone" in plan.mode_reason
    assert "deferred" in plan.decision_trigger.lower()
    assert any("connected tools" in item for item in plan.orientation_actions)


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
    assert any("connected repository" in item for item in plan.execution_handoff)
    assert any("do not claim local programstart" in item.lower() for item in plan.execution_handoff)
    assert "A second execution spine" in plan.work_packet.out_of_scope[0]


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
    with pytest.raises(ValueError, match="--repo is a local checkout path"):
        build_plan(
            request="Do work",
            repo="./project",
            environment="connected-tools",
        )


def test_mode_c_requires_a_target() -> None:
    with pytest.raises(ValueError, match="Mode C requires"):
        build_plan(request="Change the product", mode="c")


def test_render_text_exposes_authority_evidence_handoff_and_completion() -> None:
    plan = build_plan(request="Build a small API")
    rendered = render_text(plan)

    assert "PROGRAMSTART Orchestration Contract" in rendered
    assert "environment: local" in rendered
    assert "mode: a" in rendered
    assert "authority loading:" in rendered
    assert "reusable evidence:" in rendered
    assert "handoff:" in rendered
    assert "completion rule:" in rendered


def test_cli_json_output_is_machine_readable(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--request", "Build a small API", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["request"] == "Build a small API"
    assert payload["environment"] == "local"
    assert payload["mode"] == "a"
    assert payload["authority_loading"]
    assert payload["work_packet"]["reusable_evidence"]
    assert payload["completion_rule"]
