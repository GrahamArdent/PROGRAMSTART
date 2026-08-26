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
    why_now_authority: str
    in_scope: tuple[str, ...]
    out_of_scope: tuple[str, ...]
    required_context: tuple[str, ...]
    reusable_evidence: tuple[str, ...]
    invalidation_triggers: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    targeted_verification: tuple[str, ...]
    durable_updates_if_needed: tuple[str, ...]


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


def _resolve_environment(
    environment: EnvironmentInput,
    repo: str,
    repository: str,
) -> Environment:
    if repo and repository:
        raise ValueError(
            "Choose either --repo for a local checkout or --repository for a connected remote repository, not both."
        )
    if environment == "auto":
        return "connected-tools" if repository else "local"
    if environment == "local" and repository:
        raise ValueError(
            "--repository is for connected-tools orchestration; use --repo for a local checkout."
        )
    if environment == "connected-tools" and repo:
        raise ValueError(
            "--repo is a local checkout path; use --repository with connected-tools orchestration."
        )
    return environment


def _resolve_mode(
    mode: ModeInput,
    *,
    has_target: bool,
    research_backed: bool,
) -> tuple[Mode, str]:
    if research_backed and mode not in {"auto", "b"}:
        raise ValueError(
            "--research-backed is compatible only with --mode auto or --mode b."
        )
    if mode != "auto":
        return mode, "Entry mode was supplied explicitly by the operator."
    if research_backed:
        return (
            "b",
            "Substantial prior research exists, so enter as research-backed planning evidence.",
        )
    if has_target:
        return (
            "unresolved",
            "A repository target exists, but repository existence alone does not distinguish greenfield from in-flight work.",
        )
    return (
        "a",
        "No existing target or research-backed evidence was supplied, so start from raw-idea intake.",
    )


def _target_label(
    repo: str,
    repository: str,
    environment: Environment,
) -> str:
    if repo:
        return repo
    if repository:
        return repository
    if environment == "local":
        return "new-project-not-yet-created"
    return "new-project-via-connected-tools"


def _authority_loading(
    mode: Mode,
    execution_spine: str,
) -> tuple[str, ...]:
    if mode == "c":
        spine = execution_spine or "The target project's designated strategic execution spine"
        return (
            "Stable target repository instructions/authority index, if present",
            spine,
            "Only affected project requirements, architecture, contracts, and decisions",
            "Current implementation/tests/runtime evidence needed for the delta",
            "PROGRAMBUILD planning operating model as methodology, not replacement authority",
        )
    if mode == "b":
        return (
            "PROGRAMBUILD planning operating model",
            "PROGRAMBUILD idea intake when shaping is needed",
            "Existing research evidence, provenance, and freshness",
            "Only unresolved feasibility/requirements evidence",
        )
    if mode == "a":
        return (
            "PROGRAMBUILD planning operating model",
            "PROGRAMBUILD idea intake",
            "PROGRAMBUILD Stage 0 baseline and kickoff packet",
        )
    return (
        "Inspect live target authority before choosing Mode A/B/C",
        "Do not infer Mode C merely because a repository exists",
        "Load only enough evidence to resolve project maturity and authority",
    )


def _orientation_actions(
    environment: Environment,
    mode: Mode,
    target: str,
    execution_spine: str,
) -> tuple[str, ...]:
    if environment == "connected-tools":
        if mode == "unresolved":
            return (
                f"Inspect live repository {target} with connected tools before substantive decisions.",
                "Resolve Mode A/B/C from actual authority and project maturity.",
                "Treat runtime/repository state as technical reality and current project authority as intent.",
            )
        if mode == "c":
            spine = execution_spine or "the project's designated execution spine"
            return (
                f"Inspect live repository {target} with connected tools before changing it.",
                f"Locate {spine} and the actual next incomplete executable slice.",
                "Load only the exact authority/evidence required for that slice.",
            )
        return (
            "Load only the PROGRAMBUILD entry-mode/intake authority needed for the request.",
            "Reuse trustworthy research evidence instead of re-asking settled questions.",
        )

    if mode == "unresolved":
        return (
            f"Inspect local target {target} for its authority and PROGRAMBUILD control surface.",
            "If linked, use `programstart target --repo <path> status` and `guide --system programbuild`.",
            "Resolve Mode A/B/C before implementation; repository existence alone is insufficient.",
        )
    if mode == "c":
        quoted = json.dumps(target)
        return (
            f"Run `programstart target --repo {quoted} status` when the target control surface is linked.",
            f"Run `programstart target --repo {quoted} guide --system programbuild`.",
            "Locate the target execution spine and actual next incomplete slice before editing.",
        )
    return (
        "Run `programstart guide --kickoff` for the current kickoff baseline.",
        "Shape the request with the eight-dimension intake and reuse trustworthy evidence.",
    )


def _route_if_earned(
    *,
    request: str,
    mode: Mode,
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


def _work_packet(
    request: str,
    mode: Mode,
    execution_spine: str,
) -> WorkPacket:
    if mode == "c":
        required_context = (
            execution_spine or "Existing project execution spine",
            "Exact affected requirements/architecture/contracts/decisions",
            "Current implementation/runtime evidence for the requested delta",
        )
        reusable = (
            "Still-valid project decisions, tests, audits, and runtime evidence",
            "Prior research whose assumptions have not been invalidated",
        )
    elif mode == "b":
        required_context = (
            "Research evidence and provenance",
            "PROGRAMBUILD entry-mode/intake authority",
            "Only unresolved feasibility/requirements evidence",
        )
        reusable = (
            "Trustworthy research findings that answer intake or feasibility questions",
        )
    elif mode == "a":
        required_context = (
            "PROGRAMBUILD entry-mode/intake authority",
            "User problem, outcome, constraints, and cheapest validation evidence",
        )
        reusable = ("Any trustworthy facts supplied with the request",)
    else:
        required_context = (
            "Live target authority sufficient to resolve entry mode",
            "No broader context until Mode A/B/C is resolved",
        )
        reusable = (
            "Existing repository evidence that remains trustworthy after authority reconciliation",
        )

    why_now = (
        "Execute the requested outcome under the project's existing authority without a competing plan."
        if mode == "c"
        else "Convert the request into the smallest justified PROGRAMBUILD-controlled next action."
    )
    return WorkPacket(
        objective=request,
        why_now_authority=why_now,
        in_scope=(
            "Smallest coherent change or planning slice needed to advance the request",
            "Only decision/research checks earned by actual uncertainty and consequence",
        ),
        out_of_scope=(
            "A second master plan, lifecycle, or execution spine",
            "Unrelated refactors or broad research for completeness",
            "Unsupported remote stage/convergence mutation",
        ),
        required_context=required_context,
        reusable_evidence=reusable,
        invalidation_triggers=(
            "Changed requirements, contracts, runtime behavior, dependencies, or authority",
            "Evidence conflict/staleness or a new unknown that could change the decision",
        ),
        acceptance_criteria=(
            "Requested outcome or bounded next slice is explicit and testable",
            "One authority chain is preserved",
            "Decision-relevant uncertainty is retired or recorded as blocker/residual risk",
            "Verification covers changed or invalidated surfaces without ritual broadening",
        ),
        targeted_verification=(
            "Verify changed behavior/contracts and directly impacted dependencies",
            "Reuse unaffected prior evidence",
            "Widen only at meaningful convergence/release boundaries or material blast radius",
        ),
        durable_updates_if_needed=(
            "Update existing strategic authority only for accepted durable deltas",
            "Record material decisions/reversals in the existing decision mechanism",
            "Persist the work packet only when resumability/coordination earns it",
        ),
    )


def _execution_handoff(
    environment: Environment,
    mode: Mode,
    target: str,
) -> tuple[str, ...]:
    if mode == "unresolved":
        return (
            "Resolve entry mode from live authority evidence before implementation.",
            "Continue the same contract after resolution; CLI users may rerun with explicit --mode.",
        )
    if environment == "connected-tools":
        if mode == "c":
            return (
                "Use connected repository/runtime tools to inspect and execute the bounded delta directly.",
                "Apply adaptive routing only when material uncertainty remains; do not claim a local CLI ran.",
                "Execute from the existing spine, verify narrowly, then reconcile durable authority/state.",
            )
        return (
            "Use connected tools for repository/runtime evidence that is actually available.",
            "Shape and execute under PROGRAMBUILD without forcing a copy/paste handoff to another chat.",
        )
    if mode == "c":
        return (
            f"Use central PROGRAMSTART target commands against {target} for supported external operations.",
            "Execute product changes in the target repository under its existing authority.",
            "Keep remote advance/closeout/state mutation/full template validation blocked.",
        )
    return (
        "Use the normal PROGRAMSTART factory/kickoff path after idea/feasibility acceptance.",
        "Carry the bounded work packet into implementation rather than creating another plan.",
    )


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
        raise ValueError(
            "Mode C requires --repo or --repository so existing project authority can be inspected."
        )

    target = _target_label(repo, repository, resolved_environment)
    route = _route_if_earned(
        request=request,
        mode=resolved_mode,
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
        decision_trigger = "Decision routing is deferred until live orientation resolves Mode A/B/C."
    elif route is not None:
        decision_trigger = (
            "Adaptive routing was activated from supplied uncertainty/evidence/consequence signals."
        )
    else:
        decision_trigger = (
            "Do not invoke adaptive routing as ceremony; activate it only if live orientation exposes a material gap."
        )

    if execution_spine:
        spine = execution_spine
    elif resolved_mode in {"c", "unresolved"}:
        spine = "preserve/discover existing spine"
    else:
        spine = "PROGRAMBUILD default until project authority is established"

    return OrchestrationPlan(
        request=request,
        environment=resolved_environment,
        mode=resolved_mode,
        mode_reason=mode_reason,
        target=target,
        execution_spine=spine,
        authority_loading=_authority_loading(resolved_mode, execution_spine),
        orientation_actions=_orientation_actions(
            resolved_environment,
            resolved_mode,
            target,
            execution_spine,
        ),
        decision_route=route,
        decision_trigger=decision_trigger,
        work_packet=_work_packet(request, resolved_mode, execution_spine),
        execution_handoff=_execution_handoff(
            resolved_environment,
            resolved_mode,
            target,
        ),
        verification_policy=(
            "Narrow while executing; widen while converging.",
            "Use evidence available in the current environment; do not claim unavailable checks ran.",
            "Re-verify invalidated surfaces unless a real convergence boundary requires broader proof.",
        ),
        completion_rule=(
            "Complete when the bounded request is executed or handed off with sufficient evidence and durable "
            "project authority/state is reconciled without creating a competing execution spine."
        ),
    )


def render_text(plan: OrchestrationPlan) -> str:
    lines = [
        "PROGRAMSTART Orchestration Contract",
        f"- request: {plan.request}",
        f"- environment: {plan.environment}",
        f"- mode: {plan.mode}",
        f"- mode reason: {plan.mode_reason}",
        f"- target: {plan.target}",
        f"- execution spine: {plan.execution_spine}",
        "- authority loading:",
        *(f"  - {item}" for item in plan.authority_loading),
        "- orientation:",
        *(f"  - {item}" for item in plan.orientation_actions),
        f"- decision trigger: {plan.decision_trigger}",
    ]
    if plan.decision_route is not None:
        checks = ", ".join(check.name for check in plan.decision_route.activated_checks)
        lines.extend(
            [
                f"- decision route: {plan.decision_route.route}",
                f"- research depth: {plan.decision_route.research_depth}",
                f"- activated checks: {checks or 'none'}",
            ]
        )

    packet = plan.work_packet
    lines.extend(
        [
            "- work packet:",
            f"  - objective: {packet.objective}",
            f"  - why now / authority: {packet.why_now_authority}",
            "  - in scope:",
            *(f"    - {item}" for item in packet.in_scope),
            "  - out of scope:",
            *(f"    - {item}" for item in packet.out_of_scope),
            "  - required context:",
            *(f"    - {item}" for item in packet.required_context),
            "  - reusable evidence:",
            *(f"    - {item}" for item in packet.reusable_evidence),
            "  - invalidation triggers:",
            *(f"    - {item}" for item in packet.invalidation_triggers),
            "  - acceptance criteria:",
            *(f"    - {item}" for item in packet.acceptance_criteria),
            "  - targeted verification:",
            *(f"    - {item}" for item in packet.targeted_verification),
            "  - durable updates if needed:",
            *(f"    - {item}" for item in packet.durable_updates_if_needed),
            "- execution handoff:",
            *(f"  - {item}" for item in plan.execution_handoff),
            "- verification policy:",
            *(f"  - {item}" for item in plan.verification_policy),
            f"- completion rule: {plan.completion_rule}",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Turn a plain-language request into an environment-aware PROGRAMSTART execution contract."
        )
    )
    parser.add_argument(
        "--request",
        required=True,
        help="Plain-language project or change request.",
    )
    parser.add_argument(
        "--repo",
        default="",
        help="Local checkout path for the target project.",
    )
    parser.add_argument(
        "--repository",
        default="",
        help="Connected remote repository identifier, for example owner/name.",
    )
    parser.add_argument(
        "--environment",
        choices=["auto", "local", "connected-tools"],
        default="auto",
    )
    parser.add_argument("--mode", choices=["auto", "a", "b", "c"], default="auto")
    parser.add_argument("--research-backed", action="store_true")
    parser.add_argument(
        "--execution-spine",
        default="",
        help="Known project execution spine for Mode C.",
    )
    parser.add_argument("--decision", default="", help="Optional material decision to route now.")
    parser.add_argument("--impact", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--uncertainty", choices=["low", "medium", "high"])
    parser.add_argument(
        "--reversibility",
        choices=["easy", "costly", "hard"],
        default="costly",
    )
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

    if args.json:
        print(json.dumps(asdict(plan), indent=2))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart orchestrate --request <goal>'")
    raise SystemExit(main())
