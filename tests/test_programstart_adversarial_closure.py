from __future__ import annotations

from scripts.programstart_orchestrate import build_plan, render_text


def test_high_risk_packet_activates_post_implementation_adversarial_closure() -> None:
    plan = build_plan(
        request="Harden an Internet-facing webhook receiver",
        repository="owner/watchtower",
        environment="connected-tools",
        mode="c",
        impact="high",
        reversibility="hard",
        risks=("security", "external-side-effects"),
        concerns=("runtime", "verification"),
    )

    review = " ".join(plan.work_packet.adversarial_closure_review).lower()
    assert "actual completed implementation" in review
    assert "failure sequence" in review
    assert "retry/idempotency" in review
    assert "before closure" in review
    assert "adversarial closure review:" in render_text(plan).lower()


def test_low_risk_packet_does_not_receive_explicit_adversarial_ceremony() -> None:
    plan = build_plan(
        request="Correct a small documentation typo",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
        impact="low",
        reversibility="easy",
    )

    assert plan.work_packet.adversarial_closure_review == ()
    assert "adversarial closure review:" not in render_text(plan).lower()


def test_closure_always_rechecks_actual_changed_surface_for_risk_escalation() -> None:
    plan = build_plan(
        request="Implement an ordinary bounded slice",
        repository="owner/project",
        environment="connected-tools",
        mode="c",
        impact="low",
        reversibility="easy",
    )

    verification = " ".join(plan.verification_policy).lower()
    completion = plan.completion_rule.lower()

    assert "actual changed surface" in verification
    assert "persistence" in verification
    assert "idempotency" in verification
    assert "adversarial challenge gate" in verification
    assert "risk-triggered post-implementation adversarial closure review" in completion
