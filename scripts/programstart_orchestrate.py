from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Literal

try:
    from .programstart_common import warn_direct_script_invocation
    from .programstart_decision import (
        CONCERNS,
        RISK_FLAGS,
        DecisionContext,
        DecisionRoute,
        EvidenceState,
        Level,
        Reversibility,
        Volatility,
        route_decision,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import warn_direct_script_invocation
    from programstart_decision import (
        CONCERNS,
        RISK_FLAGS,
        DecisionContext,
        DecisionRoute,
        EvidenceState,
        Level,
        Reversibility,
        Volatility,
        route_decision,
    )

Environment = Literal["local", "connected-tools"]
EnvironmentInput = Literal["auto", "local", "connected-tools"]
Mode = Literal["a", "b", "c", "unresolved"]
ModeInput = Literal["auto", "a", "b", "c"]


@dataclass(frozen=True, slots=True)
class WorkPacket:
    objective: str
    authority: str
    in_scope: tuple[str, ...]
    out_of_scope: tuple[str, ...]
    required_context: tuple[str, ...]
    reusable_evidence: tuple[str, ...]
    invalidation_triggers: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    targeted_verification: tuple[str, ...]
    durable_updates: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrchestrationPlan:
    request: str
    environment: Environment
    mode: Mode
    mode_reason: str
    target: str
    execution_spine: str
    authority_loading: tuple[str, ...]
    orientation_actions: tuple[str, ...]
    decision_route: DecisionRoute | None
    decision_trigger: str
    work_packet: WorkPacket
    execution_handoff: tuple[str, ...]
    verification_policy: tuple[str, ...]
    completion_rule: str


def _resolve_environment(environment: EnvironmentInput, repo: str, repository: str) -> Environment:
    if repo and repository:
        raise ValueError("Choose either --repo or --repository, not both.")
    if environment == "auto":
        return "connected-tools" if repository else "local"
    if environment == "local" and repository:
        raise ValueError("--repository requires connected-tools; use --repo for a local checkout.")
    if environment == "connected-tools" and repo:
        raise ValueError(
            "--repo is a local checkout path; use --repository with connected-tools orchestration."
        )
    return environment


def _resolve_mode(mode: ModeInput, *, has_target: bool, research_backed: bool) -> tuple[Mode, str]:
    if research_backed and mode not in {"auto", "b"}:
        raise ValueError("--research-backed is compatible only with --mode auto or b.")
    if mode != "auto":
        return mode, "Entry mode was supplied explicitly by the operator."
    if research_backed:
        return (
            "b",
            "Prior research exists and should be converted into decisions and scope before execution.",
        )
    if has_target:
        return (
            "unresolved",
            "A repository target exists, but repository existence alone does not distinguish "
            "greenfield from in-flight work.",
        )
    return "a", "No existing target or research-backed evidence was supplied."


def _authority_loading(mode: Mode, execution_spine: str) -> tuple[str, ...]:
    if mode == "c":
        return (
            "Stable target repository instructions or authority index, if present",
            execution_spine or "Target project's designated execution spine",
            "Only affected requirements, architecture, contracts, and decisions",
            "Current implementation, tests, or runtime evidence needed for the delta",
            "PROGRAMBUILD planning operating model as methodology, not replacement authority",
        )
    if mode == "b":
        return (
            "PROGRAMBUILD planning operating model and idea intake when shaping is needed",
            "Existing research evidence, provenance, and freshness",
            "Only unresolved feasibility or requirements evidence",
        )
    if mode == "a":
        return (
            "PROGRAMBUILD planning operating model",
            "PROGRAMBUILD idea intake",
            "PROGRAMBUILD Stage 0 baseline and kickoff packet",
        )
    return (
        "Live target authority sufficient to resolve Mode A, B, or C",
        "No broader context until project maturity and authority are known",
    )


def _orientation(
    environment: Environment,
    mode: Mode,
    target: str,
    execution_spine: str,
) -> tuple[str, ...]:
    if mode == "unresolved":
        surface = "connected tools" if environment == "connected-tools" else "the local checkout"
        return (
            f"Inspect {target} with {surface} before substantive decisions.",
            "Resolve Mode A, B, or C from actual authority and project maturity.",
            "Repository existence alone is not evidence for Mode C.",
        )
    if environment == "connected-tools" and mode == "c":
        return (
            f"Inspect live repository {target} before changing it.",
            f"Locate {execution_spine or 'the designated execution spine'} and its next incomplete slice.",
            "Load only authority and evidence required for that slice.",
        )
    if environment == "local" and mode == "c":
        quoted = json.dumps(target)
        return (
            f"Use `programstart target --repo {quoted} status` when the target is linked.",
            f"Use `programstart target --repo {quoted} guide --system programbuild`.",
            "Locate the existing execution spine and next incomplete slice before editing.",
        )
    return (
        "Load only the PROGRAMBUILD entry-mode and intake authority needed for this request.",
        "Reuse trustworthy supplied or research evidence rather than re-asking settled questions.",
    )


def _route_material_decision(
    request: str,
    mode: Mode,
    *,
    decision: str,
    impact: Level,
    uncertainty: Level | None,
    reversibility: Reversibility,
    evidence_state: EvidenceState | None,
    volatility: Volatility,
    risks: tuple[str, ...],
    concerns: tuple[str, ...],
    missing_evidence: tuple[str, ...],
    outcome_that_could_change: str,
    minimum_evidence: str,
    stop_condition: str,
) -> DecisionRoute | None:
    has_signal = bool(
        decision
        or uncertainty
        or evidence_state
        or risks
        or concerns
        or missing_evidence
        or outcome_that_could_change
        or minimum_evidence
        or stop_condition
    )
    if not has_signal or mode == "unresolved":
        return None

    return route_decision(
        DecisionContext(
            decision=decision or request,
            mode=mode,
            impact=impact,
            uncertainty=uncertainty or "low",
            reversibility=reversibility,
            evidence_state=evidence_state or "sufficient",
            volatility=volatility,
            risks=risks,
            concerns=concerns,
            missing_evidence=missing_evidence,
            outcome_that_could_change=outcome_that_could_change,
            minimum_evidence=minimum_evidence,
            stop_condition=stop_condition,
        )
    )


def _work_packet(request: str, mode: Mode, execution_spine: str) -> WorkPacket:
    if mode == "c":
        required_context = (
            execution_spine or "Existing project execution spine",
            "Exact affected requirements, architecture, contracts, or decisions",
            "Current implementation or runtime evidence for the delta",
        )
        reusable_evidence = (
            "Still-valid project decisions, tests, audits, and runtime evidence",
            "Prior research whose assumptions have not been invalidated",
        )
        authority = "Existing project authority; PROGRAMBUILD remains methodology."
    elif mode == "b":
        required_context = (
            "Research evidence and provenance",
            "PROGRAMBUILD intake",
            "Only unresolved gaps",
        )
        reusable_evidence = (
            "Trustworthy research that already answers intake or feasibility questions",
        )
        authority = "Convert research into decisions and scope before establishing execution authority."
    elif mode == "a":
        required_context = (
            "PROGRAMBUILD intake",
            "Problem, outcome, and constraints",
            "Cheapest validation evidence",
        )
        reusable_evidence = ("Trustworthy facts supplied with the request",)
        authority = "PROGRAMBUILD entry process until project-specific authority is established."
    else:
        required_context = ("Live target authority sufficient to resolve entry mode",)
        reusable_evidence = ("Still-valid repository evidence after authority reconciliation",)
        authority = "Do not implement until entry mode and the authority chain are resolved."

    return WorkPacket(
        objective=request,
        authority=authority,
        in_scope=(
            "Smallest coherent slice needed to advance the request",
            "Only rigor the decision actually earns",
        ),
        out_of_scope=(
            "A second execution spine",
            "Unrelated refactors or research",
            "Unsupported remote workflow mutation",
        ),
        required_context=required_context,
        reusable_evidence=reusable_evidence,
        invalidation_triggers=(
            "Changed authority, contracts, runtime behavior, or dependencies",
            "Material evidence conflict or staleness",
        ),
        acceptance_criteria=(
            "Bounded outcome is explicit and testable",
            "One authority chain is preserved",
            "Material uncertainty is resolved or recorded",
        ),
        targeted_verification=(
            "Verify changed or invalidated surfaces",
            "Reuse unaffected evidence",
            "Widen only at a real convergence boundary",
        ),
        durable_updates=(
            "Update existing authority only for accepted deltas",
            "Record material decisions in the existing decision mechanism",
        ),
    )


def _execution_handoff(environment: Environment, mode: Mode, target: str) -> tuple[str, ...]:
    if mode == "unresolved":
        return ("Resolve entry mode from live evidence before implementation.",)
    if environment == "connected-tools":
        return (
            "Use connected repository or runtime tools directly for the bounded slice.",
            "Do not claim local PROGRAMSTART commands ran when they did not.",
            "Verify narrowly and reconcile durable project authority or state afterward.",
        )
    if mode == "c":
        return (
            f"Use the central PROGRAMSTART target control plane against {target} for supported operations.",
            "Keep remote advance, closeout, state mutation, and full template validation blocked.",
        )
    return ("Use the normal PROGRAMSTART kickoff or factory path after the current gate is satisfied.",)


def build_plan(
    *,
    request: str,
    repo: str = "",
    repository: str = "",
    environment: EnvironmentInput = "auto",
    mode: ModeInput = "auto",
    research_backed: bool = False,
    execution_spine: str = "",
    decision: str = "",
    impact: Level = "medium",
    uncertainty: Level | None = None,
    reversibility: Reversibility = "costly",
    evidence_state: EvidenceState | None = None,
    volatility: Volatility = "stable",
    risks: tuple[str, ...] = (),
    concerns: tuple[str, ...] = (),
    missing_evidence: tuple[str, ...] = (),
    outcome_that_could_change: str = "",
    minimum_evidence: str = "",
    stop_condition: str = "",
) -> OrchestrationPlan:
    request = request.strip()
    if not request:
        raise ValueError("request must not be empty")

    resolved_environment = _resolve_environment(environment, repo, repository)
    resolved_mode, mode_reason = _resolve_mode(
        mode,
        has_target=bool(repo or repository),
        research_backed=research_backed,
    )
    if resolved_mode == "c" and not (repo or repository):
        raise ValueError("Mode C requires --repo or --repository so live project authority can be inspected.")

    target = repo or repository or "new-project-not-yet-created"
    resolved_spine = execution_spine or (
        "preserve/discover existing spine"
        if resolved_mode in {"c", "unresolved"}
        else "PROGRAMBUILD default until project authority is established"
    )
    route = _route_material_decision(
        request,
        resolved_mode,
        decision=decision,
        impact=impact,
        uncertainty=uncertainty,
        reversibility=reversibility,
        evidence_state=evidence_state,
        volatility=volatility,
        risks=risks,
        concerns=concerns,
        missing_evidence=missing_evidence,
        outcome_that_could_change=outcome_that_could_change,
        minimum_evidence=minimum_evidence,
        stop_condition=stop_condition,
    )
    if resolved_mode == "unresolved":
        decision_trigger = "Decision routing is deferred until live orientation resolves Mode A, B, or C."
    elif route is None:
        decision_trigger = (
            "Do not invoke adaptive routing as ceremony; activate it only for a material decision gap."
        )
    else:
        decision_trigger = "Adaptive routing was activated from supplied decision-relevant signals."

    return OrchestrationPlan(
        request=request,
        environment=resolved_environment,
        mode=resolved_mode,
        mode_reason=mode_reason,
        target=target,
        execution_spine=resolved_spine,
        authority_loading=_authority_loading(resolved_mode, execution_spine),
        orientation_actions=_orientation(
            resolved_environment,
            resolved_mode,
            target,
            execution_spine,
        ),
        decision_route=route,
        decision_trigger=decision_trigger,
        work_packet=_work_packet(request, resolved_mode, execution_spine),
        execution_handoff=_execution_handoff(resolved_environment, resolved_mode, target),
        verification_policy=(
            "Narrow while executing; widen while converging.",
            "Do not claim checks or tools that did not actually run.",
            "Re-verify only invalidated surfaces unless a real convergence boundary requires more.",
        ),
        completion_rule=(
            "Complete when the bounded outcome has sufficient acceptance evidence, durable authority or state "
            "is reconciled where needed, and the next executable slice or blocker is explicit."
        ),
    )


def render_text(plan: OrchestrationPlan) -> str:
    route = plan.decision_route
    route_text = "not activated" if route is None else f"{route.route} / research={route.research_depth}"
    packet = plan.work_packet
    fields = (
        ("authority loading", plan.authority_loading),
        ("orientation", plan.orientation_actions),
        ("required context", packet.required_context),
        ("reusable evidence", packet.reusable_evidence),
        ("in scope", packet.in_scope),
        ("out of scope", packet.out_of_scope),
        ("invalidation triggers", packet.invalidation_triggers),
        ("acceptance", packet.acceptance_criteria),
        ("targeted verification", packet.targeted_verification),
        ("durable updates", packet.durable_updates),
        ("handoff", plan.execution_handoff),
        ("verification policy", plan.verification_policy),
    )
    lines = [
        "PROGRAMSTART Orchestration Contract",
        f"- request: {plan.request}",
        f"- environment: {plan.environment}",
        f"- mode: {plan.mode} ({plan.mode_reason})",
        f"- target: {plan.target}",
        f"- execution spine: {plan.execution_spine}",
        f"- work-packet authority: {packet.authority}",
        f"- decision route: {route_text}",
        f"- decision trigger: {plan.decision_trigger}",
    ]
    lines.extend(f"- {label}: " + " | ".join(values) for label, values in fields)
    lines.append(f"- completion rule: {plan.completion_rule}")
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build an environment-aware PROGRAMSTART execution contract."
    )
    parser.add_argument("--request", required=True)
    parser.add_argument("--repo", default="")
    parser.add_argument("--repository", default="")
    parser.add_argument(
        "--environment",
        choices=["auto", "local", "connected-tools"],
        default="auto",
    )
    parser.add_argument("--mode", choices=["auto", "a", "b", "c"], default="auto")
    parser.add_argument("--research-backed", action="store_true")
    parser.add_argument("--execution-spine", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--impact", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--uncertainty", choices=["low", "medium", "high"])
    parser.add_argument("--reversibility", choices=["easy", "costly", "hard"], default="costly")
    parser.add_argument(
        "--evidence",
        dest="evidence_state",
        choices=["sufficient", "partial", "stale", "absent", "conflicting"],
    )
    parser.add_argument("--volatility", choices=["stable", "changing", "fast"], default="stable")
    parser.add_argument("--risk", action="append", default=[], choices=sorted(RISK_FLAGS))
    parser.add_argument("--concern", action="append", default=[], choices=sorted(CONCERNS))
    parser.add_argument("--missing-evidence", action="append", default=[])
    parser.add_argument("--outcome-that-could-change", default="")
    parser.add_argument("--minimum-evidence", default="")
    parser.add_argument("--stop-condition", default="")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        plan = build_plan(
            request=args.request,
            repo=args.repo,
            repository=args.repository,
            environment=args.environment,
            mode=args.mode,
            research_backed=args.research_backed,
            execution_spine=args.execution_spine,
            decision=args.decision,
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
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(asdict(plan), indent=2) if args.json else render_text(plan))
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart orchestrate --request <goal>'")
    raise SystemExit(main())
