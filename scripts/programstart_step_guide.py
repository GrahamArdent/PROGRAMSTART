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
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        load_registry,
        load_workflow_state,
        system_is_attached,
        warn_direct_script_invocation,
        workflow_active_step,
    )


def print_section(title: str, items: list[str]) -> None:
    if not items:
        return
    print(f"{title}:")
    for item in items:
        print(f"- {item}")


def workflow_prompt_set(registry: dict[str, Any]) -> set[str]:
    prompt_registry = cast(dict[str, Any], registry.get("prompt_registry", {}))
    return set(cast(list[str], prompt_registry.get("workflow_prompt_files", [])))


def filter_workflow_prompts(registry: dict[str, Any], prompts: list[str]) -> list[str]:
    allowed = workflow_prompt_set(registry)
    if not allowed:
        return prompts
    return [prompt for prompt in prompts if prompt in allowed]


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the authoritative files, scripts, and prompts for a workflow step.")
    parser.add_argument(
        "--kickoff",
        action="store_true",
        help="Show the new-project kickoff guidance.",
    )
    parser.add_argument(
        "--operator",
        action="store_true",
        help="Show operator prompt surfaces without workflow-routing semantics.",
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

    if args.operator:
        operator_sections = cast(dict[str, Any], guidance.get("operator", {}))
        if args.json:
            payload = {
                "type": "operator",
                "sections": {
                    name: {
                        "description": section.get("description", ""),
                        "prompts": section.get("prompts", []),
                    }
                    for name, section in operator_sections.items()
                },
            }
            print(json.dumps(payload, indent=2))
        else:
            print("PROGRAMSTART Operator Prompts")
            for name, section in operator_sections.items():
                typed_section = cast(dict[str, Any], section)
                print(typed_section.get("description", ""))
                print_section(name.replace("_", " ").title(), cast(list[str], typed_section.get("prompts", [])))
        return 0

    if args.kickoff:
        section = cast(dict[str, Any], guidance.get("kickoff", {}))
        prompts = filter_workflow_prompts(registry, list(cast(list[str], section.get("prompts", []))))
        if args.json:
            print(
                json.dumps(
                    {
                        "type": "kickoff",
                        "description": section.get("description", ""),
                        "files": section.get("files", []),
                        "scripts": section.get("scripts", []),
                        "prompts": prompts,
                    },
                    indent=2,
                )
            )
        else:
            print("PROGRAMSTART Kickoff")
            print(section.get("description", ""))
            print_section("Files", cast(list[str], section.get("files", [])))
            print_section("Scripts", cast(list[str], section.get("scripts", [])))
            print_section("Prompts", prompts)
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
        stage_prompts = filter_workflow_prompts(registry, list(cast(list[str], section.get("prompts", []))))
        cross_cutting = filter_workflow_prompts(registry, cast(list[str], guidance.get("cross_cutting_workflow_prompts", [])))
        for p in cross_cutting:
            if p not in stage_prompts:
                stage_prompts.append(p)
        if args.json:
            print(
                json.dumps(
                    {
                        "type": "programbuild",
                        "stage": stage,
                        "files": section.get("files", []),
                        "scripts": section.get("scripts", []),
                        "prompts": stage_prompts,
                    },
                    indent=2,
                )
            )
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
        prompts = filter_workflow_prompts(registry, list(cast(list[str], section.get("prompts", []))))
        if args.json:
            print(
                json.dumps(
                    {
                        "type": "userjourney",
                        "phase": phase,
                        "attached": True,
                        "files": section.get("files", []),
                        "scripts": section.get("scripts", []),
                        "prompts": prompts,
                    },
                    indent=2,
                )
            )
        else:
            print(f"USERJOURNEY Phase: {phase}")
            print_section("Files", cast(list[str], section.get("files", [])))
            print_section("Scripts", cast(list[str], section.get("scripts", [])))
            print_section("Prompts", prompts)
        return 0

    parser.error(
        "Provide --kickoff, --operator, or select a --system; stage and phase can be omitted when state files are current"
    )
    return 1  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart guide' or 'pb guide'")
    raise SystemExit(main())
