from __future__ import annotations

import argparse
import os
from datetime import date, datetime

try:
    from .programstart_common import (
        extract_numbered_items,
        load_registry,
        load_workflow_state,
        parse_markdown_table,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        extract_numbered_items,
        load_registry,
        load_workflow_state,
        parse_markdown_table,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workspace_path,
    )


def system_is_attached(registry: dict, system_name: str) -> bool:
    system = registry["systems"][system_name]
    root = workspace_path(system["root"])
    return root.exists()


def summarize_programbuild(registry: dict) -> list[str]:
    system = registry["systems"]["programbuild"]
    state = load_workflow_state(registry, "programbuild")
    active_stage = workflow_active_step(registry, "programbuild", state)
    variant = state.get("variant") or "unset"
    missing_control = [path for path in system["control_files"] if not workspace_path(path).exists()]
    missing_outputs = [path for path in system["output_files"] if not workspace_path(path).exists()]
    control_total = len(system["control_files"])
    output_total = len(system["output_files"])

    lines = ["PROGRAMBUILD"]
    lines.append(f"- active stage: {active_stage}")
    lines.append(f"- variant: {variant}")
    lines.append(f"- control files present: {control_total - len(missing_control)}/{control_total}")
    lines.append(f"- output files present: {output_total - len(missing_outputs)}/{output_total}")

    if missing_control:
        lines.append("- next action: restore missing control files before using the workflow")
        lines.append("- missing control files: " + ", ".join(missing_control))
        return lines

    if missing_outputs:
        next_output = missing_outputs[0]
        lines.append(f"- next action: create or restore {next_output}")
        lines.append("- missing output files: " + ", ".join(missing_outputs))
        return lines

    guide_command = f"programstart guide --system programbuild --stage {active_stage}"
    lines.append(f"- next action: run '{guide_command}' and keep PROGRAMBUILD_STATE.json current")
    lines.append("- status: all standard PROGRAMBUILD control and output files are present")
    return lines


def summarize_userjourney(registry: dict) -> list[str]:
    system = registry["systems"]["userjourney"]
    lines = ["USERJOURNEY"]
    if system.get("optional") and not system_is_attached(registry, "userjourney"):
        lines.append("- status: not attached in this repository")
        lines.append(
            "- next action: attach USERJOURNEY separately only if this project needs onboarding, consent, or activation planning"
        )
        return lines

    state = load_workflow_state(registry, "userjourney")
    active_phase = workflow_active_step(registry, "userjourney", state)
    missing_files = [path for path in system["core_files"] if not workspace_path(path).exists()]
    open_questions_path = workspace_path(system["engineering_blocker_file"])
    tracker_path = workspace_path("USERJOURNEY/IMPLEMENTATION_TRACKER.md")
    core_total = len(system["core_files"])

    lines.append(f"- active phase: {active_phase}")
    lines.append(f"- core files present: {core_total - len(missing_files)}/{core_total}")

    if missing_files:
        lines.append("- next action: restore missing core USERJOURNEY files before implementation planning")
        lines.append("- missing files: " + ", ".join(missing_files))
        return lines

    open_items = extract_numbered_items(
        open_questions_path.read_text(encoding="utf-8"),
        "Remaining Operational And Legal Decisions",
    )
    phase_rows = parse_markdown_table(
        tracker_path.read_text(encoding="utf-8"),
        "Phase Overview",
    )
    current_phase = next(
        (row for row in phase_rows if row.get("Status", "").lower() != "completed"),
        None,
    )

    lines.append(f"- unresolved external decisions: {len(open_items)}")
    if current_phase:
        phase_name = current_phase.get("Phase", "unknown")
        phase_goal = current_phase.get("Goal", "")
        phase_blockers = current_phase.get("Blockers", "")
        lines.append(f"- current phase: {phase_name} ({phase_goal})")
        lines.append(f"- phase blockers: {phase_blockers}")
    else:
        lines.append("- current phase: no incomplete phases found in IMPLEMENTATION_TRACKER.md")

    if open_items:
        lines.append(
            "- next action: close or explicitly defer the remaining OPEN_QUESTIONS items before moving deeper into implementation"
        )
        lines.append(
            "- first files to open: USERJOURNEY/OPEN_QUESTIONS.md, "
            "USERJOURNEY/LEGAL_REVIEW_NOTES.md, USERJOURNEY/DELIVERY_GAMEPLAN.md"
        )
    else:
        lines.append(
            "- next action: execute the next incomplete slice from "
            "EXECUTION_SLICES.md and verify it against ACCEPTANCE_CRITERIA.md"
        )
        lines.append(
            "- first files to open: USERJOURNEY/EXECUTION_SLICES.md, "
            "USERJOURNEY/IMPLEMENTATION_TRACKER.md, USERJOURNEY/ACCEPTANCE_CRITERIA.md"
        )

    lines.append(f"- activation event: {system['activation_event']}")
    return lines


def staleness_warnings(
    registry: dict,
    system: str,
    *,
    today: date | None = None,
) -> list[str]:
    """Return staleness warnings if the most recent signoff date is old."""
    state = load_workflow_state(registry, system)
    entry_key = workflow_entry_key(system)
    entries = state.get(entry_key, {})
    latest: date | None = None
    for _step, entry in entries.items():
        raw = (entry.get("signoff") or {}).get("date", "")
        if not raw:
            continue
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            continue
        if latest is None or d > latest:
            latest = d
    if latest is None:
        return []
    ref = today or date.today()
    gap = (ref - latest).days
    lines: list[str] = []
    if gap > 56:
        lines.append(
            f"\033[33m⚠  Last {system} state change was {gap} days ago. "
            "Strongly consider running the Re-Entry Protocol "
            "(PROGRAMBUILD_CHALLENGE_GATE.md) before continuing.\033[0m"
        )
    elif gap > 28:
        lines.append(
            f"\033[33m⚠  Last {system} state change was {gap} days ago. "
            "Consider running the Re-Entry Protocol "
            "(PROGRAMBUILD_CHALLENGE_GATE.md) before continuing.\033[0m"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize current PROGRAMSTART workflow status.")
    parser.add_argument("--system", choices=["all", "programbuild", "userjourney"], default="all")
    parser.add_argument("--skip-staleness-check", action="store_true", help="Suppress staleness warnings.")
    args = parser.parse_args()

    skip_staleness = args.skip_staleness_check or os.environ.get("PROGRAMSTART_SKIP_STALENESS", "") == "1"

    registry = load_registry()
    output: list[str] = []
    if args.system in {"all", "programbuild"}:
        output.extend(summarize_programbuild(registry))
        if not skip_staleness:
            output.extend(staleness_warnings(registry, "programbuild"))
    if args.system == "all":
        output.append("")
    if args.system in {"all", "userjourney"}:
        output.extend(summarize_userjourney(registry))
        if not skip_staleness and system_is_attached(registry, "userjourney"):
            output.extend(staleness_warnings(registry, "userjourney"))

    print("\n".join(output))
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart status' or 'pb status'")
    raise SystemExit(main())
