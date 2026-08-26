from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Literal

try:
    from .programstart_common import warn_direct_script_invocation
    from .programstart_decision import CONCERNS, RISK_FLAGS, DecisionContext, DecisionRoute, route_decision
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import warn_direct_script_invocation
    from programstart_decision import CONCERNS, RISK_FLAGS, DecisionContext, DecisionRoute, route_decision

Environment = Literal["local", "connected-tools"]
Mode = Literal["a", "b", "c", "unresolved"]


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


def _resolve_environment(environment: str, repo: str, repository: str) -> Environment:
    if repo and repository:
        raise ValueError("Choose either --repo for a local checkout or --repository for a connected remote repository, not both.")
    if environment == "auto":
        return "connected-tools" if repository else "local"
    if environment == "local" and repository:
        raise ValueError("--repository is for connected-tools orchestration; use --repo for a local checkout.")
    if environment == "connected-tools" and repo:
        raise ValueError("--repo is a local checkout path; use --repository with connected-tools orchestration.")
    return environment  # type: ignore[return-value]


def _resolve_mode(mode: str, *, has_target: bool, research_backed: bool) -> tuple[Mode, str]:
    if research_backed and mode not in {"auto", "b"}:
        raise ValueError("--research-backed is compatible only with --mode auto or --mode b.")
    if mode != "auto":
        return mode, "Entry mode was supplied explicitly by the operator."  # type: ignore[return-value]
    if research_backed:
        return "b", "Substantial prior research exists, so the request enters as research-backed planning evidence."
    if has_target:
        return (
            "unresolved",
            "A repository target exists, but repository existence alone does not distinguish a new greenfield repo from an in-flight project.",
        )
    return "a", "No existing target or research-backed evidence was supplied, so start from raw-idea intake."


def _target_label(repo: str, repository: str, environment: Environment) -> str:
    if repo:
        return repo
    if repository:
        return repository
    return "new-project-not-yet-created" if environment == "local" else "new-project-via-connected-tools"


def _authority_loading(mode: Mode, execution_spine: str) -> tuple[str, ...]:
    base = (
        "PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md",
        "PROGRAMBUILD/PROGRAMBUILD_IDEA_INTAKE.md when idea/change shaping is actually needed",
    )
    if mode == "a":
        return (*base, "PROGRAMBUILD/PROGRAMBUILD.md Stage 0 baseline", "PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md")
    if mode == "b":
        return (*base, "Existing research evidence and its provenance/freshness", "PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md")
    if mode == "c":
        spine = execution_spine or "The target project's designated strategic execution spine"
        return (
            "The target repository's stable instructions/authority index, if present",
            spine,
            "Only the project-specific requirements/architecture/decisions affected by this delta",
            "Current implementation/tests/runtime evidence needed to understand actual behavior",
            "PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md as methodology, not replacement authority",
        )
    return (
        "Inspect the target's live authority hierarchy before choosing Mode A/B/C",
        "Do not infer Mode C merely because a repository exists",
        "Load only enough repository evidence to determine whether the project is greenfield, research-backed, or in-flight",
    )


def _orientation_actions(environment: Environment, mode: Mode, target: str, execution_spine: str) -> tuple[str, ...]:
    if environment == "connected-tools":
        if mode == "unresolved":
            return (
                f"Inspect live repository {target} with connected repository tools before substantive decisions.",
                "Determine whether it is truly greenfield, research-backed, or existing/in-flight; then continue under Mode A, B, or C.",
                "Treat repository/runtime state as authoritative for current technical reality and current project authority as authoritative for intent.",
            )
        if mode == "c":
            spine = execution_spine or "the project's designated execution spine"
            return (
                f"Inspect live repository {target} with connected tools before changing it.",
                f"Locate {spine} and the actual next incomplete executable slice.",
                "Load stable repository instructions and only the exact authority/evidence needed for that slice.",
            )
        return (
            "Load the PROGRAMBUILD entry-mode/intake authority needed for the request.",
            "Reuse trustworthy research evidence when present instead of re-asking settled questions.",
            "Do not create implementation structure until the intake/feasibility evidence justifies it.",
        )

    if mode == "unresolved":
        return (
            f"Inspect local target {target} for its existing execution authority and PROGRAMBUILD control surface.",
            "If it is already linked to PROGRAMSTART, use `programstart target --repo <path> status` and `guide --system programbuild` for orientation.",
            "Resolve Mode A/B/C from project maturity and authority evidence before execution; repository existence alone is not enough.",
        )
    if mode == "c":
        return (
            f"Run `programstart target --repo {json.dumps(target)} status` when the target control surface is linked.",
            f"Run `programstart target --repo {json.dumps(target)} guide --system programbuild` for the current methodology baseline.",
            "Locate the target project's execution spine and exact next incomplete slice before editing.",
        )
    return (
        "Run `programstart guide --kickoff` for the current kickoff baseline.",
        "Shape the idea/change with the eight-dimension intake and reuse any trustworthy supplied evidence.",
        "Create or bootstrap the project only after the idea/feasibility decision is accepted.",
    )


def _decision_route(
    *,
    request: str,
    mode: Mode,
    decision: str,
    impact: str,
    uncertainty: str | None,
    reversibility: str,
    evidence_state: str | None,
    volatility: str,
    risks: tuple[str, ...],
    concerns: tuple[str, ...],
    missing_evidence: tuple[str, ...],
    outcome_that_could_change: str,
    minimum_evidence: str,
    stop_condition: str,
) -> DecisionRoute | None:
    router_signals_exist = bool(
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
    if not router_signals_exist or mode == "unresolved":
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
        authority = execution_spine or "the existing project's execution spine"
        required_context = (
            authority,
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
        reusable = ("Trustworthy research findings that directly answer intake or feasibility questions",)
    elif mode == "a":
        required_context = (
            "PROGRAMBUILD entry-mode/intake authority",
            "User problem/outcome/constraints",
            "Cheapest evidence capable of validating or killing the idea",
        )
        reusable = ("Any trustworthy facts supplied with the request",)
    else:
        required_context = (
            "Live target authority sufficient to resolve the entry mode",
            "Do not broaden context until Mode A/B/C is resolved",
        )
        reusable = ("Existing repository evidence that remains trustworthy after authority reconciliation",)

    return WorkPacket(
        objective=request,
        why_now_authority=(
            "Execute the user-requested outcome under the project's existing authority without creating a competing plan."
            if mode == "c"
            else "Convert the request into the smallest justified PROGRAMBUILD-controlled next action."
        ),
        in_scope=(
            "The smallest coherent change or planning slice needed to advance the request",
            "Only decision/research checks that the actual uncertainty and consequence earn",
        ),
        out_of_scope=(
            "A second master plan, lifecycle, or execution spine",
            "Unrelated refactors or broad research for completeness",
            "Remote stage mutation/convergence bypasses that PROGRAMSTART does not yet support safely",
        ),
        required_context=required_context,
        reusable_evidence=reusable,
        invalidation_triggers=(
            "Changed requirements, contracts, runtime behavior, dependencies, or authority",
            "Evidence conflict, material staleness, or a new unknown that could change the next decision",
        ),
        acceptance_criteria=(
            "The requested outcome or bounded next slice is explicit and testable",
            "One authority chain is preserved",
            "Decision-relevant uncertainty is either retired to sufficiency or recorded as a blocker/residual risk",
            "Verification covers every changed or invalidated surface without ritual broadening",
        ),
        targeted_verification=(
            "Verify changed behavior/contracts and directly impacted dependencies",
            "Reuse unaffected prior evidence",
            "Widen only at a meaningful convergence/release boundary or when blast radius requires it",
        ),
        durable_updates_if_needed=(
            "Update the project's existing strategic authority only for accepted durable deltas",
            "Record material decisions/reversals in the project's existing decision mechanism",
            "Do not persist the work packet unless resumability/coordination makes it useful",
        ),
    )


def _execution_handoff(environment: Environment, mode: Mode, target: str) -> tuple[str, ...]:
    if mode == "unresolved":
        return (
            "Resolve entry mode from live authority evidence before implementation.",
            "After mode resolution, continue this same orchestration contract; CLI operators may rerun with explicit --mode.",
        )
    if environment == "connected-tools":
        if mode == "c":
            return (
                "Use connected repository/runtime tools to inspect the live target and execute the bounded delta directly.",
                "Apply the adaptive decision-router rules only when material uncertainty remains; do not claim a local CLI command ran if it did not.",
                "Derive work from the existing execution spine, make the smallest coherent repository change, run targeted verification, then reconcile durable authority/state.",
            )
        return (
            "Use connected tools for any repository/runtime evidence that is actually available.",
            "Shape and validate the request under PROGRAMBUILD, then create/modify implementation assets only when the current gate permits it.",
            "Do not force the user to shuttle a generated prompt between chats when the current environment can execute the next step directly.",
        )
    if mode == "c":
        return (
            f"Use central PROGRAMSTART target commands against {target} for supported orientation, decision, state-read, prompt, and target-local validation operations.",
            "Execute the product-code change in the target repository under its existing authority.",
            "Keep remote `advance`, `closeout`, state mutation, and full template-runtime validation blocked until those paths are explicitly made external-control aware.",
        )
    return (
        "Use the normal PROGRAMSTART factory/kickoff path after idea/feasibility acceptance.",
        "Carry the resulting bounded work packet into implementation rather than creating another plan.",
    )


def build_plan(
    *,
    request: str,
    repo: str = "",
    repository: str = "",
    environment: str = "auto",
    mode: str = "auto",
    research_backed: bool = False,
    execution_spine: str = "",
    decision: str = "",
    impact: str = "medium",
    uncertainty: str | None = None,
    reversibility: str = "costly",
    evidence_state: str | None = None,
    volatility: str = "stable",
    risks: tuple[str, ...] = (),
    concerns: tuple[str, ...] = (),
    missing_evidence: tuple[str, ...] = (),
    outcome_that_could_change: str = "",
    minimum_evidence: str = "",
    stop_condition: str = "",
) -> OrchestrationPlan:
    if not request.strip():
        raise ValueError("request must not be empty")
    resolved_environment = _resolve_environment(environment, repo, repository)
    resolved_mode, mode_reason = _resolve_mode(
        mode,
        has_target=bool(repo or repository),
        research_backed=research_backed,
    )
    if resolved_mode == "c" and not (repo or repository):
        raise ValueError("Mode C requires --repo or --repository so the existing project authority can be inspected.")
    target = _target_label(repo, repository, resolved_environment)
    route = _decision_route(
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
    decision_trigger = (
        "Decision routing is deferred until live orientation resolves Mode A/B/C."
        if resolved_mode == "unresolved"
        else (
            "Adaptive decision routing was activated from the supplied uncertainty/evidence/consequence signals."
            if route is not None
            else "Do not invoke adaptive routing as ceremony; activate it only if live orientation exposes uncertainty or consequence that could change the next action."
        )
    )
    return OrchestrationPlan(
        request=request.strip(),
        environment=resolved_environment,
        mode=resolved_mode,
        mode_reason=mode_reason,
        target=target,
        execution_spine=execution_spine or ("preserve/discover existing spine" if resolved_mode in {"c", "unresolved"} else "PROGRAMBUILD default until project authority is established"),
        authority_loading=_authority_loading(resolved_mode, execution_spine),
        orientation_actions=_orientation_actions(resolved_environment, resolved_mode, target, execution_spine),
        decision_route=route,
        decision_trigger=decision_trigger,
        work_packet=_work_packet(request.strip(), resolved_mode, execution_spine),
        execution_handoff=_execution_handoff(resolved_environment, resolved_mode, target),
        verification_policy=(
            "Narrow while executing; widen while converging.",
            "Use repository/runtime evidence available in the current environment and do not claim unavailable checks were run.",
            "Re-verify only surfaces invalidated by the change, unless a real convergence boundary requires broader proof.",
        ),
        completion_rule=(
            "Complete when the bounded request is executed or handed off with sufficient acceptance evidence and durable project authority/state is reconciled without creating a competing execution spine."
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
        lines.extend(
            [
                f"- decision route: {plan.decision_route.route}",
                f"- research depth: {plan.decision_route.research_depth}",
                "- activated checks: "
                + (", ".join(check.name for check in plan.decision_route.activated_checks) or "none"),
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
        description="Turn a plain-language request into an environment-aware PROGRAMSTART execution contract."
    )
    parser.add_argument("--request", required=True, help="Plain-language project or change request.")
    parser.add_argument("--repo", default="", help="Local checkout path for the target project.")
    parser.add_argument("--repository", default="", help="Connected remote repository identifier, for example owner/name.")
    parser.add_argument("--environment", choices=["auto", "local", "connected-tools"], default="auto")
    parser.add_argument("--mode", choices=["auto", "a", "b", "c"], default="auto")
    parser.add_argument("--research-backed", action="store_true")
    parser.add_argument("--execution-spine", default="", help="Known project execution spine for Mode C.")
    parser.add_argument("--decision", default="", help="Optional material decision to route now.")
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
