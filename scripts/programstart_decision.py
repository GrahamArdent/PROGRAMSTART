from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Literal

Level = Literal["low", "medium", "high"]
Mode = Literal["a", "b", "c"]
Reversibility = Literal["easy", "costly", "hard"]
EvidenceState = Literal["sufficient", "partial", "stale", "absent", "conflicting"]
Volatility = Literal["stable", "changing", "fast"]
ResearchDepth = Literal["none", "targeted", "deep"]
Route = Literal["execute", "execute_with_checks", "investigate"]

RISK_FLAGS = frozenset(
    {
        "authentication",
        "authorization",
        "permissions",
        "secrets",
        "destructive-change",
        "sensitive-data",
        "payments",
        "external-side-effects",
        "security",
        "compliance",
    }
)

CONCERNS = frozenset(
    {
        "contract",
        "runtime",
        "architecture-extraction",
        "build-vs-buy",
        "verification",
        "observability",
        "complexity",
        "cost-resource",
    }
)

BOUNDARY_CONCERNS = frozenset({"contract", "runtime", "architecture-extraction", "build-vs-buy"})
PROOF_CONCERNS = frozenset({"verification", "observability"})
SIMPLICITY_CONCERNS = frozenset({"architecture-extraction", "build-vs-buy", "complexity", "cost-resource"})


@dataclass(frozen=True, slots=True)
class DecisionContext:
    decision: str
    mode: Mode = "a"
    impact: Level = "medium"
    uncertainty: Level = "medium"
    reversibility: Reversibility = "costly"
    evidence_state: EvidenceState = "partial"
    volatility: Volatility = "stable"
    risks: tuple[str, ...] = ()
    concerns: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    outcome_that_could_change: str = ""
    minimum_evidence: str = ""
    stop_condition: str = ""

    def __post_init__(self) -> None:
        if not self.decision.strip():
            raise ValueError("decision must not be empty")
        unknown_risks = sorted(set(self.risks) - RISK_FLAGS)
        if unknown_risks:
            raise ValueError(f"unknown risk flag(s): {', '.join(unknown_risks)}")
        unknown_concerns = sorted(set(self.concerns) - CONCERNS)
        if unknown_concerns:
            raise ValueError(f"unknown concern(s): {', '.join(unknown_concerns)}")


@dataclass(frozen=True, slots=True)
class ActivatedCheck:
    name: str
    reason: str


@dataclass(frozen=True, slots=True)
class ResearchBrief:
    depth: ResearchDepth
    decision_protected: str
    missing_evidence: tuple[str, ...]
    why_it_matters: str
    outcome_that_could_change: str
    minimum_evidence: str
    stop_condition: str


@dataclass(frozen=True, slots=True)
class DecisionRoute:
    route: Route
    research_depth: ResearchDepth
    evidence_action: str
    activated_checks: tuple[ActivatedCheck, ...]
    reasons: tuple[str, ...]
    mode_c_return_rule: str
    research_brief: ResearchBrief | None = None


def _normalized(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _select_research_depth(context: DecisionContext) -> ResearchDepth:
    """Select research depth with qualitative precedence, not a numeric score."""
    evidence = context.evidence_state

    if evidence == "sufficient" and context.uncertainty == "low":
        return "none"

    # Freshness checks are deliberately narrow. Staleness never escalates to a
    # full deep-research cycle by itself.
    if evidence == "stale":
        return "targeted"

    if evidence == "sufficient" and context.uncertainty == "medium":
        return "none"

    high_consequence = bool(context.risks) or context.reversibility == "hard"
    broad_decision_surface = len(set(context.concerns) & (BOUNDARY_CONCERNS | PROOF_CONCERNS)) >= 2
    deep_candidate = (
        context.impact == "high"
        and context.uncertainty == "high"
        and evidence in {"absent", "conflicting"}
        and (high_consequence or broad_decision_surface)
    )
    if deep_candidate:
        return "deep"

    # Any remaining decision-relevant uncertainty should be retired with the
    # smallest bounded research delta rather than a broad knowledge sweep.
    if evidence != "sufficient" or context.uncertainty == "high":
        return "targeted"

    return "none"


def _evidence_action(context: DecisionContext, depth: ResearchDepth) -> str:
    if depth == "none":
        return "reuse-existing-evidence"
    if context.evidence_state == "stale":
        return "refresh-only-the-time-sensitive-evidence"
    if context.evidence_state == "partial":
        return "reuse-valid-evidence-and-fill-only-the-gaps"
    if context.evidence_state == "conflicting":
        return "resolve-the-decision-relevant-conflict"
    return "collect-only-the-evidence-needed-for-the-decision"


def _activated_checks(context: DecisionContext, depth: ResearchDepth) -> tuple[ActivatedCheck, ...]:
    checks: list[ActivatedCheck] = []
    concerns = set(context.concerns)

    if depth != "none" or context.evidence_state != "sufficient" or context.volatility != "stable":
        checks.append(
            ActivatedCheck(
                "evidence",
                "Evidence sufficiency, reuse, freshness, or research depth can affect this decision.",
            )
        )

    if context.impact == "high" or context.reversibility != "easy" or context.risks:
        detail = ", ".join(_normalized(context.risks)) or f"reversibility={context.reversibility}"
        checks.append(ActivatedCheck("consequence", f"Consequences warrant explicit risk/reversibility scrutiny ({detail})."))

    boundary = _normalized(tuple(concerns & BOUNDARY_CONCERNS))
    if boundary:
        checks.append(
            ActivatedCheck(
                "boundary",
                "System-boundary reasoning is relevant: " + ", ".join(boundary) + ".",
            )
        )

    proof = _normalized(tuple(concerns & PROOF_CONCERNS))
    if proof or context.risks or context.impact == "high":
        reason_bits = list(proof)
        if context.risks:
            reason_bits.append("risk-sensitive acceptance evidence")
        if context.impact == "high":
            reason_bits.append("high-impact verification")
        checks.append(ActivatedCheck("proof", "Proof planning is warranted: " + ", ".join(reason_bits) + "."))

    simplicity = _normalized(tuple(concerns & SIMPLICITY_CONCERNS))
    if simplicity:
        checks.append(
            ActivatedCheck(
                "simplicity",
                "Challenge unnecessary architecture or resource cost before adding complexity: "
                + ", ".join(simplicity)
                + ".",
            )
        )

    if context.mode == "c":
        checks.append(
            ActivatedCheck(
                "mode-c-delta",
                "Reuse the existing execution spine, authority, contracts, and valid evidence; "
                "evaluate only the new delta.",
            )
        )

    return tuple(checks)


def _default_missing_evidence(context: DecisionContext) -> tuple[str, ...]:
    if context.missing_evidence:
        return _normalized(context.missing_evidence)
    if context.evidence_state == "stale":
        return ("A current freshness check for the time-sensitive evidence supporting this decision.",)
    if context.evidence_state == "conflicting":
        return ("Evidence that resolves the credible conflict between implementation approaches or factual claims.",)
    if context.evidence_state == "absent":
        return ("Decision-relevant evidence for the material unknowns; broad background knowledge is not required.",)
    if context.evidence_state == "partial":
        return ("Evidence for the remaining material gap not already covered by reusable evidence.",)
    return ("Evidence for the specific unresolved uncertainty that could change this decision.",)


def _research_brief(context: DecisionContext, depth: ResearchDepth) -> ResearchBrief | None:
    if depth == "none":
        return None

    missing = _default_missing_evidence(context)
    outcome = context.outcome_that_could_change.strip() or (
        "The implementation, provider/architecture choice, boundary contract, or decision to proceed could change."
    )
    minimum = context.minimum_evidence.strip() or (
        "Enough current, credible evidence to resolve each named material unknown to the point that no remaining "
        "unknown is likely to change the next decision."
    )
    stop = context.stop_condition.strip() or (
        "Stop researching when the minimum evidence is met and additional research is unlikely to change the "
        "protected decision; record residual uncertainty instead of continuing for completeness."
    )
    why = (
        "Proceeding without this evidence could lock in avoidable rework or risk."
        if context.impact == "high" or context.reversibility == "hard" or context.risks
        else "The missing information is material only because it could change the next implementation decision."
    )
    return ResearchBrief(
        depth=depth,
        decision_protected=context.decision,
        missing_evidence=missing,
        why_it_matters=why,
        outcome_that_could_change=outcome,
        minimum_evidence=minimum,
        stop_condition=stop,
    )


def route_decision(context: DecisionContext) -> DecisionRoute:
    depth = _select_research_depth(context)
    checks = _activated_checks(context, depth)
    if depth != "none":
        route: Route = "investigate"
    elif checks:
        route = "execute_with_checks"
    else:
        route = "execute"

    reasons: list[str] = []
    if depth == "none":
        reasons.append("No decision-relevant evidence gap currently earns additional research.")
    elif depth == "targeted":
        reasons.append("A bounded evidence gap exists, but a focused research delta should be sufficient.")
    else:
        reasons.append(
            "High-impact, high-uncertainty evidence is absent/conflicting across a consequential decision surface; "
            "targeted checking alone may not bound the decision safely."
        )

    if context.evidence_state == "stale":
        reasons.append("Stale/time-sensitive evidence triggers a freshness delta, not automatic deep research.")
    if context.mode == "c":
        reasons.append(
            "Mode C preserves current project authority and returns to the existing execution spine after the "
            "delta is resolved."
        )
    if context.reversibility == "easy" and context.impact == "low":
        reasons.append("Cheap reversibility lowers the amount of rigor the decision must earn.")

    return DecisionRoute(
        route=route,
        research_depth=depth,
        evidence_action=_evidence_action(context, depth),
        activated_checks=checks,
        reasons=tuple(reasons),
        mode_c_return_rule=(
            "Return to the existing project's next executable slice; do not create or advance a fresh Stage-0 lifecycle."
            if context.mode == "c"
            else "Use the current project lifecycle/authority; the router does not create a new execution spine."
        ),
        research_brief=_research_brief(context, depth),
    )


def render_text(result: DecisionRoute) -> str:
    lines = [
        "PROGRAMSTART Adaptive Decision Route",
        f"- route: {result.route}",
        f"- research depth: {result.research_depth}",
        f"- evidence action: {result.evidence_action}",
        "- activated checks: " + (", ".join(check.name for check in result.activated_checks) or "none"),
    ]
    for check in result.activated_checks:
        lines.append(f"  - {check.name}: {check.reason}")
    lines.append("- reasons:")
    lines.extend(f"  - {reason}" for reason in result.reasons)
    lines.append(f"- return rule: {result.mode_c_return_rule}")

    if result.research_brief is not None:
        brief = result.research_brief
        lines.extend(
            [
                "- research brief:",
                f"  - decision protected: {brief.decision_protected}",
                "  - missing evidence:",
                *(f"    - {item}" for item in brief.missing_evidence),
                f"  - why it matters: {brief.why_it_matters}",
                f"  - outcome that could change: {brief.outcome_that_could_change}",
                f"  - minimum evidence: {brief.minimum_evidence}",
                f"  - stop condition: {brief.stop_condition}",
            ]
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Route a decision to the minimum justified PROGRAMBUILD scrutiny/research depth."
    )
    parser.add_argument("--decision", required=True, help="The next important decision being protected.")
    parser.add_argument("--mode", choices=["a", "b", "c"], default="a")
    parser.add_argument("--impact", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--uncertainty", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--reversibility", choices=["easy", "costly", "hard"], default="costly")
    parser.add_argument(
        "--evidence",
        dest="evidence_state",
        choices=["sufficient", "partial", "stale", "absent", "conflicting"],
        default="partial",
    )
    parser.add_argument("--volatility", choices=["stable", "changing", "fast"], default="stable")
    parser.add_argument("--risk", action="append", default=[], choices=sorted(RISK_FLAGS))
    parser.add_argument("--concern", action="append", default=[], choices=sorted(CONCERNS))
    parser.add_argument("--missing-evidence", action="append", default=[])
    parser.add_argument("--outcome-that-could-change", default="")
    parser.add_argument("--minimum-evidence", default="")
    parser.add_argument("--stop-condition", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = route_decision(
        DecisionContext(
            decision=args.decision,
            mode=args.mode,
            impact=args.impact,
            uncertainty=args.uncertainty,
            reversibility=args.reversibility,
            evidence_state=args.evidence_state,
            volatility=args.volatility,
            risks=tuple(args.risk),
            concerns=tuple(args.concern),
            missing_evidence=tuple(args.missing_evidence),
            outcome_that_could_change=args.outcome_that_could_change,
            minimum_evidence=args.minimum_evidence,
            stop_condition=args.stop_condition,
        )
    )
    print(json.dumps(asdict(result), indent=2) if args.json else render_text(result))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
