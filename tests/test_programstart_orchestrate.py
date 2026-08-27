from __future__ import annotations

import json

import pytest

from scripts.programstart_orchestrate import build_plan, main, render_text


def test_new_request_defaults_to_mode_a_without_target() -> None:
    plan = build_plan(request="Build a small API")

    assert plan.environment == "local"
    assert plan.mode == "a"
    assert plan.decision_route is None
    assert plan.blocker_scope == "none"
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
    assert any("classify its scope" in item for item in plan.orientation_actions)
    assert "A second execution spine" in plan.work_packet.out_of_scope[0]


def test_single_repository_packet_preserves_existing_defaults() -> None:
    plan = build_plan(
        request="Continue the already-decided bounded slice",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
    )

    assert plan.related_repositories == ()
    assert plan.authority_graph_policy == ()
    assert plan.cross_repository_guidance == ()
    assert plan.closure_control == ""
    assert plan.work_packet.cross_repository_dependencies == ()
    assert plan.work_packet.manual_boundaries == ()
    assert plan.work_packet.out_of_scope == (
        "A second execution spine",
        "Unrelated refactors or research",
        "Unsupported remote workflow mutation",
    )
    assert plan.work_packet.invalidation_triggers == (
        "Changed authority, contracts, runtime behavior, or dependencies",
        "Material evidence conflict or staleness",
        "A blocked external resource becoming newly visible, inaccessible, deleted, or otherwise materially changed",
    )
    assert "authority graph policy:" not in render_text(plan)
    assert "closure control:" not in render_text(plan)


def test_mutation_gate_keeps_live_action_blocked_but_surfaces_safe_lane_scan() -> None:
    plan = build_plan(
        request="Continue useful R4 work while Vercel mutation is blocked",
        repository="GrahamArdent/GCRM",
        environment="connected-tools",
        mode="c",
        execution_spine="ops/gameplans/GCRM_MASTER_GAMEPLAN_2026-08-22.md",
        blocker_scope="mutation_gate",
    )

    assert plan.blocker_scope == "mutation_gate"
    assert plan.work_packet.blocker_scope == "mutation_gate"
    assert any("Lane A" in item for item in plan.safe_lane_policy)
    assert any("Lane B" in item for item in plan.safe_lane_policy)
    assert any("blocked Lane C mutation" in item for item in plan.safe_lane_policy)
    assert plan.work_packet.safe_lane_policy == plan.safe_lane_policy


def test_external_resource_history_is_not_overwritten_by_current_invisibility() -> None:
    plan = build_plan(
        request="Reconcile a provider resource that is no longer visible",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
    )

    policy = " ".join(plan.evidence_continuity_policy).lower()
    assert "historical existence" in policy
    assert "current visibility" in policy
    assert "does not prove" in policy
    assert "deleted" in policy


def test_calendar_companion_dependency_is_derived_without_becoming_cross_project_authority() -> None:
    plan = build_plan(
        request="Continue Calendar B5 convergence without crossing the credential gate",
        repository="GrahamArdent/Dedication-Calendar-Bridge",
        environment="connected-tools",
        mode="c",
        execution_spine="PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md",
        blocker_scope="milestone",
        related_repository="GrahamArdent/Dedication",
        relationship_type="product_contract",
        related_authority=(
            "product meaning, Integration Gateway contract/runtime, connection/user mapping, and normalized evidence persistence"
        ),
        related_execution_spine="ops/gameplans/DEDICATION_REMAINING_ISSUES_GAMEPLAN_2026-08-20.md",
        dependency_state="partial",
        dependency_evidence=(
            "Dedication PR #46 is open; hosted Calendar contract is deployed and Supabase verification is green.",
            "Calendar Bridge PR #5 is open and Verify Bridge is green.",
        ),
        dependency_invalidation=(
            "Dedication PR #46 changes, merges, closes, or the hosted Calendar contract changes.",
        ),
        manual_boundary="Google OAuth credentials plus real initial and restart/incremental Calendar smoke.",
        closure_control="Calendar Bridge B5 credential gate",
    )

    assert plan.closure_control == "Calendar Bridge B5 credential gate"
    assert len(plan.related_repositories) == 1
    relation = plan.related_repositories[0]
    assert relation.repository == "GrahamArdent/Dedication"
    assert relation.dependency_state == "partial"
    graph = " ".join(plan.authority_graph_policy).lower()
    assert "derived and task-scoped" in graph
    assert "canonical for nothing" in graph
    assert "does not grant multi-repository mutation authority" in graph
    guidance = " ".join(plan.cross_repository_guidance)
    assert "Reuse the proven part" in guidance
    assert "External/manual boundary" in guidance
    assert any("Dedication PR #46" in item for item in plan.work_packet.reusable_evidence)
    assert any("hosted Calendar contract changes" in item for item in plan.work_packet.invalidation_triggers)
    assert plan.work_packet.manual_boundaries == (
        "Google OAuth credentials plus real initial and restart/incremental Calendar smoke.",
    )
    assert "A cross-project Master or portfolio transaction" in plan.work_packet.out_of_scope


def test_cross_repository_metadata_requires_a_related_repository() -> None:
    with pytest.raises(ValueError, match="requires --related-repository"):
        build_plan(
            request="Continue dependency work",
            repository="owner/project",
            environment="connected-tools",
            mode="c",
            dependency_state="partial",
        )


def test_related_repository_is_mode_c_only() -> None:
    with pytest.raises(ValueError, match="only for Mode C"):
        build_plan(
            request="Build a new companion",
            repo="./new-project",
            mode="a",
            related_repository="owner/product",
        )


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


def test_render_text_exposes_authority_blocker_evidence_handoff_and_completion() -> None:
    plan = build_plan(request="Build a small API", blocker_scope="unresolved")
    rendered = render_text(plan)

    assert "PROGRAMSTART Orchestration Contract" in rendered
    assert "environment: local" in rendered
    assert "mode: a" in rendered
    assert "authority loading:" in rendered
    assert "blocker scope: unresolved" in rendered
    assert "safe-lane policy:" in rendered
    assert "evidence continuity:" in rendered
    assert "reusable evidence:" in rendered
    assert "handoff:" in rendered
    assert "completion rule:" in rendered


def test_cli_json_output_is_machine_readable(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(
        [
            "--request",
            "Continue safe preparation",
            "--repository",
            "owner/project",
            "--mode",
            "c",
            "--blocker-scope",
            "mutation_gate",
            "--json",
        ]
    ) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["request"] == "Continue safe preparation"
    assert payload["environment"] == "connected-tools"
    assert payload["mode"] == "c"
    assert payload["blocker_scope"] == "mutation_gate"
    assert payload["safe_lane_policy"]
    assert payload["evidence_continuity_policy"]
    assert payload["authority_loading"]
    assert payload["work_packet"]["blocker_scope"] == "mutation_gate"
    assert payload["work_packet"]["reusable_evidence"]
    assert payload["completion_rule"]


def test_cross_repository_cli_json_output_is_machine_readable(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(
        [
            "--request",
            "Continue Calendar convergence",
            "--repository",
            "GrahamArdent/Dedication-Calendar-Bridge",
            "--mode",
            "c",
            "--blocker-scope",
            "milestone",
            "--related-repository",
            "GrahamArdent/Dedication",
            "--relationship-type",
            "product_contract",
            "--related-authority",
            "product contract/runtime authority",
            "--dependency-state",
            "partial",
            "--dependency-evidence",
            "Dedication contract deployed; companion PR still open.",
            "--dependency-invalidation",
            "Companion PR or hosted contract changes.",
            "--manual-boundary",
            "Google credentials and live smoke.",
            "--closure-control",
            "Calendar B5 credential gate",
            "--json",
        ]
    ) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["request"] == "Continue Calendar convergence"
    assert payload["environment"] == "connected-tools"
    assert payload["mode"] == "c"
    assert payload["blocker_scope"] == "milestone"
    assert payload["closure_control"] == "Calendar B5 credential gate"
    assert payload["related_repositories"][0]["repository"] == "GrahamArdent/Dedication"
    assert payload["related_repositories"][0]["dependency_state"] == "partial"
    assert payload["authority_graph_policy"]
    assert payload["cross_repository_guidance"]
    assert payload["work_packet"]["cross_repository_dependencies"]
    assert payload["work_packet"]["manual_boundaries"]
