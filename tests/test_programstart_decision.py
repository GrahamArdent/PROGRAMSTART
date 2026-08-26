from __future__ import annotations

import json

import pytest

from scripts.programstart_decision import DecisionContext, main, route_decision


def check_names(result) -> set[str]:
    return {check.name for check in result.activated_checks}


def test_trivial_greenfield_utility_executes_without_extra_gates() -> None:
    result = route_decision(
        DecisionContext(
            decision="Choose a local file naming helper",
            mode="a",
            impact="low",
            uncertainty="low",
            reversibility="easy",
            evidence_state="sufficient",
        )
    )
    assert result.route == "execute"
    assert result.research_depth == "none"
    assert result.activated_checks == ()


def test_unfamiliar_external_integration_routes_targeted_contract_runtime_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Choose the provider integration contract",
            impact="medium",
            uncertainty="high",
            reversibility="costly",
            evidence_state="partial",
            concerns=("contract", "runtime", "verification"),
        )
    )
    assert result.route == "investigate"
    assert result.research_depth == "targeted"
    assert {"evidence", "consequence", "boundary", "proof"} <= check_names(result)
    assert result.research_brief is not None
    assert "Stop researching" in result.research_brief.stop_condition


def test_sensitive_auth_activates_risk_contract_proof_without_forcing_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Change the authentication boundary",
            impact="high",
            uncertainty="low",
            reversibility="costly",
            evidence_state="sufficient",
            risks=("authentication", "secrets"),
            concerns=("contract", "verification", "observability"),
        )
    )
    assert result.route == "execute_with_checks"
    assert result.research_depth == "none"
    assert {"consequence", "boundary", "proof"} <= check_names(result)


def test_mode_c_enhancement_stays_delta_oriented_and_does_not_restart_stage_zero() -> None:
    result = route_decision(
        DecisionContext(
            decision="Add one capability to an existing product",
            mode="c",
            impact="low",
            uncertainty="low",
            reversibility="easy",
            evidence_state="sufficient",
        )
    )
    assert result.research_depth == "none"
    assert check_names(result) == {"mode-c-delta"}
    assert "next executable slice" in result.mode_c_return_rule
    assert "Stage-0" in result.mode_c_return_rule


def test_overengineered_proposal_activates_simplicity_and_extraction_checks_not_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Split a small helper into a standalone service",
            impact="low",
            uncertainty="low",
            reversibility="easy",
            evidence_state="sufficient",
            concerns=("architecture-extraction", "complexity", "cost-resource"),
        )
    )
    assert result.research_depth == "none"
    assert result.route == "execute_with_checks"
    assert {"boundary", "simplicity"} <= check_names(result)


def test_stale_fast_changing_evidence_gets_targeted_refresh_not_deep_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Rely on a provider's current API behavior",
            impact="high",
            uncertainty="high",
            reversibility="hard",
            evidence_state="stale",
            volatility="fast",
            concerns=("runtime", "contract"),
        )
    )
    assert result.research_depth == "targeted"
    assert result.evidence_action == "refresh-only-the-time-sensitive-evidence"


def test_deep_research_requires_high_impact_high_uncertainty_absent_or_conflicting_evidence() -> None:
    result = route_decision(
        DecisionContext(
            decision="Choose an irreversible regulated architecture",
            impact="high",
            uncertainty="high",
            reversibility="hard",
            evidence_state="conflicting",
            risks=("compliance",),
            concerns=("contract", "runtime"),
        )
    )
    assert result.research_depth == "deep"
    assert result.route == "investigate"


def test_programstart_self_modification_can_proceed_from_current_mode_c_evidence() -> None:
    result = route_decision(
        DecisionContext(
            decision="Add an adaptive decision router to PROGRAMSTART",
            mode="c",
            impact="high",
            uncertainty="low",
            reversibility="costly",
            evidence_state="sufficient",
            concerns=("verification", "complexity"),
        )
    )
    assert result.research_depth == "none"
    assert result.route == "execute_with_checks"
    assert {"consequence", "proof", "simplicity", "mode-c-delta"} <= check_names(result)


def test_deep_research_is_not_triggered_by_security_risk_alone() -> None:
    result = route_decision(
        DecisionContext(
            decision="Add a permission check",
            impact="high",
            uncertainty="medium",
            reversibility="hard",
            evidence_state="partial",
            risks=("authorization",),
            concerns=("verification",),
        )
    )
    assert result.research_depth == "targeted"


def test_invalid_risk_or_concern_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown risk"):
        DecisionContext(decision="x", risks=("mystery",))
    with pytest.raises(ValueError, match="unknown concern"):
        DecisionContext(decision="x", concerns=("mystery",))


def test_cli_json_contains_research_stop_condition(capsys) -> None:
    assert (
        main(
            [
                "--decision",
                "Verify a volatile provider contract",
                "--evidence",
                "stale",
                "--volatility",
                "fast",
                "--concern",
                "contract",
                "--json",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["research_depth"] == "targeted"
    assert output["research_brief"]["stop_condition"]


def test_partial_evidence_defaults_missing_gap_and_custom_stop_fields_are_preserved() -> None:
    result = route_decision(
        DecisionContext(
            decision="Choose a storage boundary",
            impact="medium",
            uncertainty="medium",
            reversibility="costly",
            evidence_state="partial",
            missing_evidence=("Provider retry semantics", "Provider retry semantics"),
            outcome_that_could_change="Whether the adapter owns retries.",
            minimum_evidence="Authoritative retry documentation plus one runtime check.",
            stop_condition="Stop when retry ownership is unambiguous.",
        )
    )
    assert result.research_brief is not None
    assert result.research_brief.missing_evidence == ("Provider retry semantics",)
    assert result.research_brief.stop_condition == "Stop when retry ownership is unambiguous."


def test_absent_low_impact_evidence_stays_targeted_and_uses_default_missing_evidence() -> None:
    result = route_decision(
        DecisionContext(
            decision="Pick a small library",
            impact="low",
            uncertainty="medium",
            reversibility="easy",
            evidence_state="absent",
        )
    )
    assert result.research_depth == "targeted"
    assert result.research_brief is not None
    assert "Decision-relevant evidence" in result.research_brief.missing_evidence[0]


def test_sufficient_but_high_uncertainty_gets_targeted_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Resolve an unexplained runtime uncertainty",
            impact="medium",
            uncertainty="high",
            reversibility="costly",
            evidence_state="sufficient",
        )
    )
    assert result.research_depth == "targeted"
    assert result.evidence_action == "collect-only-the-evidence-needed-for-the-decision"


def test_fast_but_current_evidence_activates_freshness_check_without_research() -> None:
    result = route_decision(
        DecisionContext(
            decision="Use today's provider limits",
            impact="low",
            uncertainty="low",
            reversibility="easy",
            evidence_state="sufficient",
            volatility="fast",
        )
    )
    assert result.research_depth == "none"
    assert check_names(result) == {"evidence"}


def test_text_renderer_includes_research_brief_and_non_mode_c_return_rule() -> None:
    from scripts.programstart_decision import render_text

    result = route_decision(
        DecisionContext(
            decision="Verify one provider behavior",
            evidence_state="stale",
            concerns=("contract",),
        )
    )
    rendered = render_text(result)
    assert "research brief" in rendered
    assert "decision protected: Verify one provider behavior" in rendered
    assert "does not create a new execution spine" in rendered


def test_decision_requires_non_empty_name() -> None:
    with pytest.raises(ValueError, match="decision must not be empty"):
        DecisionContext(decision="   ")
