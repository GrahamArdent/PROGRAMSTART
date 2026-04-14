from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

try:
    from .programstart_common import (
        git_changed_files,
        load_registry,
        load_workflow_state,
        system_is_optional_and_absent,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_state_config,
        workflow_steps,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        git_changed_files,
        load_registry,
        load_workflow_state,
        system_is_optional_and_absent,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_state_config,
        workflow_steps,
        workspace_path,
    )


def load_changed_files(args: argparse.Namespace) -> list[str]:
    if args.changed_file_list:
        path = Path(args.changed_file_list)
        return [line.strip().replace("\\", "/") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.files:
        return [path.replace("\\", "/") for path in args.files]
    return git_changed_files()


def evaluate_drift(registry: dict[str, Any], changed_files: list[str], system: str | None = None) -> tuple[list[str], list[str]]:
    violations: list[str] = []
    notes: list[str] = []

    changed_set = set(changed_files)
    for rule in registry["sync_rules"]:
        if system and rule.get("system", "") not in (system, "cross"):
            continue
        authority = set(rule["authority_files"])
        dependents = set(rule["dependent_files"])
        touched_authority = sorted(changed_set & authority)
        touched_dependents = sorted(changed_set & dependents)

        if touched_dependents and not touched_authority and rule.get("require_authority_when_dependents_change", False):
            violations.append(f"{rule['name']}: dependent files changed without authority files: {', '.join(touched_dependents)}")
        elif touched_authority and not touched_dependents:
            notes.append(f"{rule['name']}: authority files changed without dependent files: {', '.join(touched_authority)}")

    systems = [system] if system else ["programbuild", "userjourney"]
    is_template_repo = registry.get("workspace", {}).get("repo_role") == "template_repo"
    for system_name in systems:
        if system_is_optional_and_absent(registry, system_name):
            continue
        if is_template_repo:
            # Template repos are maintained at any stage — step-order gating does not apply.
            # Sync rules (authority/dependent file pairing) still apply.
            continue
        state = load_workflow_state(registry, system_name)
        config = workflow_state_config(registry, system_name)
        step_order = workflow_steps(registry, system_name)
        active_step = workflow_active_step(registry, system_name, state)
        active_index = step_order.index(active_step)
        entries = cast(dict[str, Any], state["stages" if system_name == "programbuild" else "phases"])
        step_files = cast(dict[str, list[str]], config.get("step_files", {}))
        for changed_file in changed_files:
            owning_step = next((step for step in step_order if changed_file in step_files.get(step, [])), None)
            if not owning_step:
                continue
            owning_index = step_order.index(owning_step)
            if owning_index > active_index:
                violations.append(
                    f"{system_name}: {changed_file} belongs to future step '{owning_step}' while active step is '{active_step}'"
                )
                continue
            for prior_step in step_order[:owning_index]:
                prior_entry = cast(dict[str, Any], entries.get(prior_step, {}))
                prior_status = str(prior_entry.get("status", "planned"))
                prior_decision = str(cast(dict[str, Any], prior_entry.get("signoff", {})).get("decision", ""))
                if prior_status != "completed" or prior_decision not in ("approved", "go", "accepted"):
                    violations.append(
                        f"{system_name}: {changed_file} changed before prior step '{prior_step}' was completed and approved"
                    )
                    break

    return violations, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether canonical planning files changed with their dependents.")
    parser.add_argument("files", nargs="*", help="Changed files to evaluate.")
    parser.add_argument("--changed-file-list", help="Path to a newline-delimited changed files list.")
    parser.add_argument("--system", choices=["programbuild", "userjourney"], help="Only check rules for this system.")
    parser.add_argument("--strict", action="store_true", help="Treat notes as violations (exit 1 if any notes).")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    changed_files = load_changed_files(args)
    if not changed_files:
        if args.json:
            print(json.dumps({"status": "skip", "violations": [], "notes": []}, indent=2))
        else:
            print("No changed files detected. Nothing to check.")
        return 0

    registry = load_registry()
    violations, notes = evaluate_drift(registry, changed_files, args.system)

    if args.json:
        status = "fail" if violations else ("fail" if args.strict and notes else "pass")
        print(json.dumps({"status": status, "violations": violations, "notes": notes}, indent=2))
        return 1 if status == "fail" else 0

    if violations:
        print("Drift check failed:")
        for violation in violations:
            print(f"- {violation}")
        if notes:
            print("Notes:")
            for note in notes:
                print(f"- {note}")
        return 1

    print("Drift check passed.")
    if args.strict and notes:
        print("Drift check failed (strict mode) — notes treated as violations:")
        for note in notes:
            print(f"- {note}")
        return 1
    if notes:
        print("Notes:")
        for note in notes:
            print(f"- {note}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart drift' or 'pb drift'")
    raise SystemExit(main())
