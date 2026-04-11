from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast

try:
    from . import programstart_drift_check, programstart_validate
    from .programstart_common import (
        clr_bold,
        clr_cyan,
        clr_dim,
        clr_yellow,
        create_default_workflow_state,
        generated_outputs_root,
        load_json,
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
        generated_outputs_root,
        load_json,
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


def _check_challenge_gate_log(active_step: str) -> str | None:
    """Return a warning message if no Challenge Gate log entry covers *active_step* as 'From Stage'.

    Returns ``None`` when a matching row is found or the gate file does not exist.
    """
    gate_path = workspace_path("PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md")
    if not gate_path.exists():
        return None
    try:
        text = gate_path.read_text(encoding="utf-8")
    except OSError:
        return None
    # Normalise the step name for fuzzy matching (e.g. "inputs_and_mode_selection" or
    # "Inputs and Mode Selection" should both match the From Stage column).
    normalised = active_step.replace("_", " ").lower().strip()
    in_log_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| From Stage"):
            in_log_table = True
            continue
        if in_log_table and stripped.startswith("|---"):
            continue
        if in_log_table and stripped.startswith("|"):
            # Extract first cell (From Stage).
            cells = [c.strip() for c in stripped.split("|")]
            # cells[0] is '' (before first |), cells[1] is From Stage.
            if len(cells) >= 2:
                from_stage = cells[1].replace("_", " ").lower().strip()
                if from_stage == normalised:
                    return None  # Found a matching row.
        elif in_log_table and not stripped.startswith("|"):
            in_log_table = False
    return (
        f"No Challenge Gate log entry found for stage '{active_step}'. "
        "Run the Challenge Gate protocol and record the result before advancing. "
        "Use --skip-gate-check to bypass this warning."
    )
    problems.extend(programstart_validate.validate_workflow_state(registry, system))
    if system == "programbuild":
        problems.extend(programstart_validate.validate_authority_sync(registry))

    changed_files = programstart_drift_check.load_changed_files(argparse.Namespace(changed_file_list=None, files=None))
    if changed_files:
        drift_problems, _ = programstart_drift_check.evaluate_drift(registry, changed_files, system)
        problems.extend(drift_problems)
    return problems


def _git_head_hash() -> str | None:
    """Return the current HEAD commit hash, or None if git is unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


# ---------------------------------------------------------------------------
# State snapshot and diff
# ---------------------------------------------------------------------------


def _snapshot_dir(registry: dict[str, Any]) -> Path:
    return generated_outputs_root(registry) / "state-snapshots"


def snapshot_state(registry: dict[str, Any], label: str = "") -> Path:
    """Save a timestamped copy of all workflow state files."""
    snap_dir = _snapshot_dir(registry)
    snap_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"_{label}" if label else ""
    snap_name = f"state_{timestamp}{suffix}.json"
    snap_path = snap_dir / snap_name

    payload: dict[str, Any] = {"snapshot_time": timestamp, "label": label, "systems": {}}
    for system_name in registry.get("systems", {}):
        state_path = workflow_state_path(registry, system_name)
        if state_path.exists():
            payload["systems"][system_name] = load_json(state_path)
    snap_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return snap_path


def diff_states(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """Compare two state snapshots and return human-readable diffs."""
    diffs: list[str] = []
    old_systems = old.get("systems", {})
    new_systems = new.get("systems", {})
    all_systems = sorted(set(old_systems) | set(new_systems))
    for sys_name in all_systems:
        old_sys = old_systems.get(sys_name, {})
        new_sys = new_systems.get(sys_name, {})
        entry_key = "stages" if sys_name == "programbuild" else "phases"
        old_entries = old_sys.get(entry_key, {})
        new_entries = new_sys.get(entry_key, {})
        all_steps = sorted(set(old_entries) | set(new_entries))
        for step in all_steps:
            old_e = old_entries.get(step, {})
            new_e = new_entries.get(step, {})
            old_status = old_e.get("status", "absent")
            new_status = new_e.get("status", "absent")
            if old_status != new_status:
                diffs.append(f"{sys_name}.{step}: status {old_status} → {new_status}")
            old_decision = old_e.get("signoff", {}).get("decision", "")
            new_decision = new_e.get("signoff", {}).get("decision", "")
            if old_decision != new_decision:
                diffs.append(f"{sys_name}.{step}: signoff {old_decision or '(none)'} → {new_decision or '(none)'}")
        old_active = old_sys.get("active_stage" if sys_name == "programbuild" else "active_phase", "")
        new_active = new_sys.get("active_stage" if sys_name == "programbuild" else "active_phase", "")
        if old_active != new_active:
            diffs.append(f"{sys_name}: active step {old_active} → {new_active}")
    return diffs


def list_snapshots(registry: dict[str, Any]) -> list[Path]:
    """Return all snapshot files sorted by name (oldest first)."""
    snap_dir = _snapshot_dir(registry)
    if not snap_dir.exists():
        return []
    return sorted(snap_dir.glob("state_*.json"))


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
    advance_parser.add_argument(
        "--skip-gate-check",
        action="store_true",
        help="Skip Challenge Gate log entry check before advancing.",
    )
    advance_parser.add_argument(
        "--skip-cross-stage-check",
        action="store_true",
        help="Skip cross-stage validation advisory before advancing.",
    )

    snapshot_parser = subparsers.add_parser("snapshot", help="Save a timestamped copy of current workflow state.")
    snapshot_parser.add_argument("--label", default="", help="Optional label for the snapshot.")

    diff_parser = subparsers.add_parser("diff", help="Compare two state snapshots or current state vs latest snapshot.")
    diff_parser.add_argument("--old", default="", help="Path to older snapshot (default: latest saved snapshot).")
    diff_parser.add_argument("--new", default="", help="Path to newer snapshot (default: current live state).")

    subparsers.add_parser("snapshots", help="List all saved state snapshots.")

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

    if args.command == "snapshot":
        snap_path = snapshot_state(registry, args.label)
        print(f"Snapshot saved: {snap_path}")
        return 0

    if args.command == "snapshots":
        snaps = list_snapshots(registry)
        if not snaps:
            print("No snapshots found. Run 'programstart state snapshot' to create one.")
            return 0
        print(f"State snapshots ({len(snaps)}):")
        for s in snaps:
            print(f"  {s.name}")
        return 0

    if args.command == "diff":
        snaps = list_snapshots(registry)
        if args.old:
            old_data = load_json(Path(args.old))
        elif snaps:
            old_data = load_json(snaps[-1])
        else:
            print("No snapshots to compare. Run 'programstart state snapshot' first.")
            return 1
        if args.new:
            new_data = load_json(Path(args.new))
        else:
            new_data = {"systems": {}}
            for system_name in registry.get("systems", {}):
                state_path = workflow_state_path(registry, system_name)
                if state_path.exists():
                    new_data["systems"][system_name] = load_json(state_path)
        changes = diff_states(old_data, new_data)
        if not changes:
            print("No changes detected between snapshots.")
        else:
            old_label = args.old or (snaps[-1].name if snaps else "saved")
            new_label = args.new or "current"
            print(f"State diff ({old_label} → {new_label}):")
            for c in changes:
                print(f"  - {c}")
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
                print("")
                print("Tip: If these files were just bootstrapped and have not yet been edited,")
                print("     commit the bootstrapped baseline first ('git add -A && git commit -m ...')")
                print("     so the drift check has a clean starting point.")
                print("     If you have genuinely completed this stage and the check is a false positive,")
                print("     use --skip-preflight and document the reason in DECISION_LOG.md.")
                return 1
        # Challenge Gate log check (programbuild only, warning not blocking).
        if system == "programbuild" and not getattr(args, "skip_gate_check", False):
            gate_warning = _check_challenge_gate_log(active_step)
            if gate_warning:
                print(clr_yellow(f"⚠  {gate_warning}"))
        # Cross-stage validation advisory (programbuild, stages 3+).
        if system == "programbuild" and not getattr(args, "skip_cross_stage_check", False) and current_index >= 3:
            print(
                clr_yellow(
                    "⚠  Tip: Run the cross-stage validation prompt before advancing: @workspace /prompt Cross-Stage Validation"
                )
            )
        if dry_run:
            print(f"[dry-run] Would mark {system} '{active_step}' completed (decision={args.decision!r}, date={args.date!r})")
            if current_index + 1 < len(steps):
                next_step = steps[current_index + 1]
                print(f"[dry-run] Would advance {system} from '{active_step}' → '{next_step}'")
            else:
                print(f"[dry-run] '{active_step}' is the final {system} step — would mark workflow complete")
            return 0
        current_entry["status"] = "completed"
        _commit_hash = _git_head_hash()
        current_entry["signoff"] = {
            "decision": args.decision,
            "date": args.date,
            "notes": args.notes,
            **({"commit_hash": _commit_hash} if _commit_hash else {}),
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
        if args.status == "completed" and not signoff.get("commit_hash"):
            _hash = _git_head_hash()
            if _hash:
                signoff["commit_hash"] = _hash
        entry["signoff"] = signoff
    if system == "programbuild" and args.variant:
        state["variant"] = args.variant

    save_workflow_state(registry, system, state)
    print(f"Updated {system} {args.step} to {args.status}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart state' or 'pb state'")
    raise SystemExit(main())
