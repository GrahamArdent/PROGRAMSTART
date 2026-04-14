from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any, cast

try:
    from .programstart_common import (
        display_workspace_path,
        extract_numbered_items,
        generated_outputs_root,
        has_required_metadata,
        load_registry,
        load_workflow_state,
        metadata_prefixes,
        metadata_value,
        parse_markdown_table,
        system_is_attached,
        warn_direct_script_invocation,
        workflow_active_step,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        display_workspace_path,
        extract_numbered_items,
        generated_outputs_root,
        has_required_metadata,
        load_registry,
        load_workflow_state,
        metadata_prefixes,
        metadata_value,
        parse_markdown_table,
        system_is_attached,
        warn_direct_script_invocation,
        workflow_active_step,
        workspace_path,
    )


def section_programbuild(registry: dict[str, Any]) -> list[str]:
    system = cast(dict[str, Any], registry["systems"]["programbuild"])
    state = load_workflow_state(registry, "programbuild")
    active_stage = workflow_active_step(registry, "programbuild", state)
    control = cast(list[str], system["control_files"])
    outputs = cast(list[str], system["output_files"])
    present_control = [p for p in control if workspace_path(p).exists()]
    present_outputs = [p for p in outputs if workspace_path(p).exists()]
    missing_control = [p for p in control if not workspace_path(p).exists()]
    missing_outputs = [p for p in outputs if not workspace_path(p).exists()]

    prefixes = metadata_prefixes(registry)
    metadata_rules = cast(dict[str, Any], registry.get("metadata_rules", {}))
    owner_placeholder = cast(str, metadata_rules.get("owner_placeholder", "[ASSIGN]"))
    metadata_issues: list[str] = []
    for rel in cast(list[str], system.get("metadata_required", [])):
        path = workspace_path(rel)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        missing = has_required_metadata(text, prefixes)
        if missing:
            metadata_issues.append(f"{rel}: missing {', '.join(missing)}")
            continue
        owner = metadata_value(text, "Owner:")
        if owner in (None, "", owner_placeholder):
            metadata_issues.append(f"{rel}: owner not assigned")

    lines = [
        "## PROGRAMBUILD",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Control files | {len(present_control)}/{len(control)} |",
        f"| Output files | {len(present_outputs)}/{len(outputs)} |",
        f"| Active stage | {active_stage} |",
        f"| Metadata issues | {len(metadata_issues)} |",
        "",
    ]

    if missing_control or missing_outputs:
        lines.append("### Missing Files")
        lines.append("")
        for f in missing_control + missing_outputs:
            lines.append(f"- {f}")
        lines.append("")

    if metadata_issues:
        lines.append("### Metadata Issues")
        lines.append("")
        for issue in metadata_issues:
            lines.append(f"- {issue}")
        lines.append("")

    if not missing_control and not missing_outputs and not metadata_issues:
        lines.append("All PROGRAMBUILD control and output files are present with complete metadata.")
        lines.append("")

    lines.append("### Next Action")
    lines.append("")
    if missing_control:
        lines.append("Restore missing control files before using the workflow.")
    elif missing_outputs:
        lines.append(f"Create or restore `{missing_outputs[0]}`.")
    else:
        lines.append("Run `programstart guide --system programbuild` to inspect the active stage and next authority files.")
    lines.append("")

    return lines


def section_userjourney(registry: dict[str, Any]) -> list[str]:
    system = cast(dict[str, Any], registry["systems"]["userjourney"])
    if system.get("optional") and not system_is_attached(registry, "userjourney"):
        return [
            "## USERJOURNEY",
            "",
            "USERJOURNEY is not attached in this repository.",
            "",
            "Attach it only for projects that require onboarding, consent, "
            "activation, or other interactive end-user journey planning.",
            "",
        ]
    state = load_workflow_state(registry, "userjourney")
    active_phase = workflow_active_step(registry, "userjourney", state)
    core = cast(list[str], system["core_files"])
    present = [p for p in core if workspace_path(p).exists()]
    missing = [p for p in core if not workspace_path(p).exists()]

    prefixes = metadata_prefixes(registry)
    metadata_rules = cast(dict[str, Any], registry.get("metadata_rules", {}))
    owner_placeholder = cast(str, metadata_rules.get("owner_placeholder", "[ASSIGN]"))
    metadata_issues: list[str] = []
    for rel in cast(list[str], system.get("metadata_required", [])):
        path = workspace_path(rel)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        missing_meta = has_required_metadata(text, prefixes)
        if missing_meta:
            metadata_issues.append(f"{rel}: missing {', '.join(missing_meta)}")
            continue
        owner = metadata_value(text, "Owner:")
        if owner in (None, "", owner_placeholder):
            metadata_issues.append(f"{rel}: owner not assigned")

    tracker_path = workspace_path("USERJOURNEY/IMPLEMENTATION_TRACKER.md")
    open_path = workspace_path(system["engineering_blocker_file"])
    open_items = extract_numbered_items(open_path.read_text(encoding="utf-8"), "Remaining Operational And Legal Decisions")
    phase_rows = parse_markdown_table(tracker_path.read_text(encoding="utf-8"), "Phase Overview")
    current_phase = next((row for row in phase_rows if row.get("Status", "").lower() != "completed"), None)

    lines = [
        "## USERJOURNEY",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Core files | {len(present)}/{len(core)} |",
        f"| Active phase | {active_phase} |",
        f"| Metadata issues | {len(metadata_issues)} |",
        f"| Unresolved external decisions | {len(open_items)} |",
        f"| Activation event | `{system['activation_event']}` |",
        "",
    ]

    if current_phase:
        lines.append(f"**Current phase:** {current_phase.get('Phase', '?')} — {current_phase.get('Goal', '')}")
        lines.append("")
        blockers = current_phase.get("Blockers", "none listed")
        lines.append(f"**Blockers:** {blockers}")
        lines.append("")

    if missing:
        lines.append("### Missing Files")
        lines.append("")
        for f in missing:
            lines.append(f"- {f}")
        lines.append("")

    if metadata_issues:
        lines.append("### Metadata Issues")
        lines.append("")
        for issue in metadata_issues:
            lines.append(f"- {issue}")
        lines.append("")

    if open_items:
        lines.append("### Unresolved External Decisions")
        lines.append("")
        for item in open_items:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("### Next Action")
    lines.append("")
    if missing:
        lines.append("Restore missing core files before implementation planning.")
    elif open_items:
        lines.append(
            "Close or explicitly defer the remaining items in `USERJOURNEY/OPEN_QUESTIONS.md` before advancing implementation."
        )
        lines.append("")
        lines.append(
            "First files to open: `USERJOURNEY/OPEN_QUESTIONS.md`, "
            "`USERJOURNEY/LEGAL_REVIEW_NOTES.md`, "
            "`USERJOURNEY/DELIVERY_GAMEPLAN.md`"
        )
    else:
        lines.append("Execute the next incomplete slice from `EXECUTION_SLICES.md` and verify against `ACCEPTANCE_CRITERIA.md`.")
    lines.append("")

    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the PROGRAMSTART status dashboard.")
    parser.add_argument("--output", default=None, help="Output path. Defaults to outputs/STATUS_DASHBOARD.md.")
    args = parser.parse_args()

    registry = load_registry()
    today = date.today().isoformat()

    lines = [
        "# PROGRAMSTART Status Dashboard",
        "",
        f"Generated: {today}",
        "",
        "---",
        "",
    ]
    lines.extend(section_programbuild(registry))
    lines.append("---")
    lines.append("")
    lines.extend(section_userjourney(registry))

    output_path = Path(args.output) if args.output else generated_outputs_root(registry) / "STATUS_DASHBOARD.md"
    if not output_path.is_absolute():
        output_path = workspace_path(str(output_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {display_workspace_path(output_path)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart dashboard' or 'pb dashboard'")
    raise SystemExit(main())
