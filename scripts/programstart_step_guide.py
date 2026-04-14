from __future__ import annotations

import argparse
import json
from typing import Any, cast

try:
    from .programstart_common import (
        load_registry,
        load_workflow_state,
        system_is_attached,
        warn_direct_script_invocation,
        workflow_active_step,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        load_registry,
        load_workflow_state,
        system_is_attached,
        warn_direct_script_invocation,
        workflow_active_step,
        workspace_path,
    )


def print_section(title: str, items: list[str]) -> None:
    if not items:
        return
    print(f"{title}:")
    for item in items:
        print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the authoritative files, scripts, and prompts for a workflow step.")
    parser.add_argument(
        "--kickoff",
        action="store_true",
        help="Show the new-project kickoff guidance.",
    )
    parser.add_argument(
        "--system",
        choices=["programbuild", "userjourney"],
        help="Workflow system to guide.",
    )
    parser.add_argument("--stage", help="PROGRAMBUILD stage name from the registry.")
    parser.add_argument("--phase", help="USERJOURNEY phase key, for example phase_0.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    registry = load_registry()
    guidance = cast(dict[str, Any], registry.get("workflow_guidance", {}))

    if args.kickoff:
        section = cast(dict[str, Any], guidance.get("kickoff", {}))
        if args.json:
            print(json.dumps({"type": "kickoff", "description": section.get("description", ""), "files": section.get("files", []), "scripts": section.get("scripts", []), "prompts": section.get("prompts", [])}, indent=2))
        else:
            print("PROGRAMSTART Kickoff")
            print(section.get("description", ""))
            print_section("Files", cast(list[str], section.get("files", [])))
            print_section("Scripts", cast(list[str], section.get("scripts", [])))
            print_section("Prompts", cast(list[str], section.get("prompts", [])))
        return 0

    if args.system == "programbuild":
        stage = args.stage or workflow_active_step(
            registry,
            "programbuild",
            load_workflow_state(registry, "programbuild"),
        )
        section = cast(dict[str, Any], guidance.get("programbuild", {})).get(stage)
        if not section:
            parser.error(f"No guidance found for PROGRAMBUILD stage '{stage}'")
        section = cast(dict[str, Any], section)
        stage_prompts = list(cast(list[str], section.get("prompts", [])))
        cross_cutting = cast(list[str], guidance.get("cross_cutting_prompts", []))
        for p in cross_cutting:
            if p not in stage_prompts:
                stage_prompts.append(p)
        if args.json:
            print(json.dumps({"type": "programbuild", "stage": stage, "files": section.get("files", []), "scripts": section.get("scripts", []), "prompts": stage_prompts}, indent=2))
        else:
            print(f"PROGRAMBUILD Stage: {stage}")
            print_section("Files", cast(list[str], section.get("files", [])))
            print_section("Scripts", cast(list[str], section.get("scripts", [])))
            print_section("Prompts", stage_prompts)
        return 0

    if args.system == "userjourney":
        if registry["systems"]["userjourney"].get("optional") and not system_is_attached(
            registry,
            "userjourney",
        ):
            if args.json:
                print(json.dumps({"type": "userjourney", "attached": False}, indent=2))
            else:
                print("USERJOURNEY is not attached in this repository.")
                print("Attach it separately only if this project needs onboarding, consent, or activation planning.")
            return 0
        phase = args.phase or workflow_active_step(
            registry,
            "userjourney",
            load_workflow_state(registry, "userjourney"),
        )
        section = cast(dict[str, Any], guidance.get("userjourney", {})).get(phase)
        if not section:
            parser.error(f"No guidance found for USERJOURNEY phase '{phase}'")
        section = cast(dict[str, Any], section)
        if args.json:
            print(json.dumps({"type": "userjourney", "phase": phase, "attached": True, "files": section.get("files", []), "scripts": section.get("scripts", []), "prompts": section.get("prompts", [])}, indent=2))
        else:
            print(f"USERJOURNEY Phase: {phase}")
            print_section("Files", cast(list[str], section.get("files", [])))
            print_section("Scripts", cast(list[str], section.get("scripts", [])))
            print_section("Prompts", cast(list[str], section.get("prompts", [])))
        return 0

    parser.error("Provide --kickoff or select a --system; stage and phase can be omitted when state files are current")
    return 1  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart guide' or 'pb guide'")
    raise SystemExit(main())
