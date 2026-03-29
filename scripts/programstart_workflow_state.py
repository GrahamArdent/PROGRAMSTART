from __future__ import annotations

import argparse
from datetime import date
from typing import Any, cast

try:
    from . import programstart_drift_check, programstart_validate
    from .programstart_common import (
        clr_bold,
        clr_cyan,
        clr_dim,
        clr_yellow,
        create_default_workflow_state,
        load_registry,
        load_workflow_state,
        save_workflow_state,
        status_color,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_drift_check  # type: ignore
    import programstart_validate  # type: ignore

    from programstart_common import (
        clr_bold,
        clr_cyan,
        clr_dim,
        clr_yellow,
        create_default_workflow_state,
        load_registry,
        load_workflow_state,
        save_workflow_state,
        status_color,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )


def system_is_optional_and_absent(registry: dict[str, Any], system: str) -> bool:
    system_cfg = cast(dict[str, Any], registry["systems"][system])
    return bool(system_cfg.get("optional")) and not workspace_path(cast(str, system_cfg["root"])).exists()


def print_state(system: str, state: dict[str, Any], active_step: str) -> None:
    entry_key = workflow_entry_key(system)
    print(clr_bold(clr_cyan(system.upper())))
    if system == "programbuild":
        print(f"- variant: {clr_dim(state.get('variant', 'product'))}")
        print(f"- active stage: {clr_yellow(active_step)}")
    else:
        print(f"- active phase: {clr_yellow(active_step)}")
    for name, entry in cast(dict[str, Any], state.get(entry_key, {})).items():
        status = cast(dict[str, Any], entry).get("status", "planned")
        decision = cast(dict[str, Any], entry).get("signoff", {}).get("decision", "")
        suffix = f" ({clr_dim(decision)})" if decision else ""
        marker = " <" if name == active_step else ""
        print(f"- {name}: {status_color(str(status))}{suffix}{clr_cyan(marker)}")


def preflight_problems(registry: dict[str, Any], system: str) -> list[str]:
    problems: list[str] = []
    problems.extend(programstart_validate.validate_required_files(registry, system))
    problems.extend(programstart_validate.validate_metadata(registry, system))
    problems.extend(programstart_validate.validate_workflow_state(registry, system))
    if system == "programbuild":
        problems.extend(programstart_validate.validate_authority_sync(registry))

    changed_files = programstart_drift_check.load_changed_files(argparse.Namespace(changed_file_list=None, files=None))
    if changed_files:
        drift_problems, _ = programstart_drift_check.evaluate_drift(registry, changed_files, system)
        problems.extend(drift_problems)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Show or update PROGRAMSTART workflow state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="Show workflow state.")
    show_parser.add_argument(
        "--system",
        choices=["all", "programbuild", "userjourney"],
        default="all",
    )

    init_parser = subparsers.add_parser("init", help="Create default workflow state files if missing.")
    init_parser.add_argument(
        "--system",
        choices=["all", "programbuild", "userjourney"],
        default="all",
    )

    set_parser = subparsers.add_parser("set", help="Set a step or phase status.")
    set_parser.add_argument("--system", choices=["programbuild", "userjourney"], required=True)
    set_parser.add_argument("--step", required=True, help="Stage or phase key.")
    set_parser.add_argument("--status", choices=["planned", "in_progress", "completed", "blocked"], required=True)
    set_parser.add_argument(
        "--decision",
        default="",
        help="Optional sign-off decision, for example approved, hold, blocked.",
    )
    set_parser.add_argument("--date", default="", help="Optional sign-off date.")
    set_parser.add_argument("--notes", default="", help="Optional sign-off notes.")
    set_parser.add_argument(
        "--variant",
        choices=["lite", "product", "enterprise"],
        help="PROGRAMBUILD variant to record.",
    )

    advance_parser = subparsers.add_parser("advance", help="Approve the active step and move the next one in progress.")
    advance_parser.add_argument("--system", choices=["programbuild", "userjourney"], required=True)
    advance_parser.add_argument(
        "--decision",
        default="approved",
        help="Sign-off decision to record for the completed step.",
    )
    advance_parser.add_argument("--date", default=date.today().isoformat(), help="Sign-off date.")
    advance_parser.add_argument("--notes", default="", help="Optional sign-off notes.")
    advance_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what advance would do without writing state.",
    )
    advance_parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip validation and drift preflight checks before advancing.",
    )

    args = parser.parse_args()
    registry = load_registry()

    if args.command == "init":
        systems = [args.system] if args.system != "all" else ["programbuild", "userjourney"]
        for system in systems:
            if system_is_optional_and_absent(registry, system):
                print(f"Skipped optional unattached system: {system}")
                continue
            path = workflow_state_path(registry, system)
            if not path.exists():
                save_workflow_state(registry, system, create_default_workflow_state(registry, system))
                print(f"Initialized {path.relative_to(path.parents[1]).as_posix()}")
            else:
                print(f"Exists: {path.relative_to(path.parents[1]).as_posix()}")
        return 0

    if args.command == "show":
        systems = [args.system] if args.system != "all" else ["programbuild", "userjourney"]
        for system in systems:
            if system_is_optional_and_absent(registry, system):
                print(clr_bold(clr_cyan(system.upper())))
                print(f"- {clr_dim('not attached in this repository')}")
                if system != systems[-1]:
                    print("")
                continue
            state = load_workflow_state(registry, system)
            active_step = workflow_active_step(registry, system, state)
            print_state(system, state, active_step)
            if system != systems[-1]:
                print("")
        return 0

    if args.command == "advance":
        system = args.system
        if system_is_optional_and_absent(registry, system):
            parser.error(f"{system} is optional and not attached in this repository")
        state = load_workflow_state(registry, system)
        active_step = workflow_active_step(registry, system, state)
        steps = workflow_steps(registry, system)
        entry_key = workflow_entry_key(system)
        entries = cast(dict[str, Any], state[entry_key])
        current_entry = cast(dict[str, Any], entries[active_step])
        if str(current_entry.get("status", "planned")) != "in_progress":
            parser.error(f"Active {system} step '{active_step}' is not in_progress")
        current_index = steps.index(active_step)
        dry_run: bool = getattr(args, "dry_run", False)
        if not dry_run and not getattr(args, "skip_preflight", False):
            problems = preflight_problems(registry, system)
            if problems:
                print("Advance preflight failed:")
                for problem in problems:
                    print(f"- {problem}")
                return 1
        if dry_run:
            print(f"[dry-run] Would mark {system} '{active_step}' completed (decision={args.decision!r}, date={args.date!r})")
            if current_index + 1 < len(steps):
                next_step = steps[current_index + 1]
                print(f"[dry-run] Would advance {system} from '{active_step}' → '{next_step}'")
            else:
                print(f"[dry-run] '{active_step}' is the final {system} step — would mark workflow complete")
            return 0
        current_entry["status"] = "completed"
        current_entry["signoff"] = {
            "decision": args.decision,
            "date": args.date,
            "notes": args.notes,
        }
        current_index = steps.index(active_step)
        if current_index + 1 < len(steps):
            next_step = steps[current_index + 1]
            next_entry = cast(dict[str, Any], entries[next_step])
            if str(next_entry.get("status", "planned")) == "planned":
                next_entry["status"] = "in_progress"
            state["active_stage" if system == "programbuild" else "active_phase"] = next_step
            print(f"Advanced {system} from {active_step} to {next_step}")
        else:
            print(f"Completed final {system} step {active_step}")
        save_workflow_state(registry, system, state)
        return 0

    system = args.system
    if system_is_optional_and_absent(registry, system):
        parser.error(f"{system} is optional and not attached in this repository")
    state = load_workflow_state(registry, system)
    valid_steps = workflow_steps(registry, system)
    if args.step not in valid_steps:
        parser.error(f"Unknown {system} step '{args.step}'. Valid options: {', '.join(valid_steps)}")

    entry_key = workflow_entry_key(system)
    entries = cast(dict[str, Any], state[entry_key])
    entry = cast(dict[str, Any], entries[args.step])
    entry["status"] = args.status
    if args.status == "in_progress":
        state["active_stage" if system == "programbuild" else "active_phase"] = args.step
    if args.decision or args.date or args.notes or args.status == "completed":
        signoff = cast(dict[str, Any], entry.get("signoff", {}))
        if args.status == "completed" and not args.decision and not signoff.get("decision"):
            signoff["decision"] = "approved"
        if args.decision:
            signoff["decision"] = args.decision
        if args.date:
            signoff["date"] = args.date
        if args.notes:
            signoff["notes"] = args.notes
        entry["signoff"] = signoff
    if system == "programbuild" and args.variant:
        state["variant"] = args.variant

    save_workflow_state(registry, system, state)
    print(f"Updated {system} {args.step} to {args.status}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart state' or 'pb state'")
    raise SystemExit(main())
