from __future__ import annotations

import argparse
import json
import re
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, cast

try:
    from .programstart_common import (
        extract_numbered_items,
        has_required_metadata,
        load_registry,
        load_workflow_state,
        metadata_prefixes,
        metadata_value,
        parse_markdown_table,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        extract_numbered_items,
        has_required_metadata,
        load_registry,
        load_workflow_state,
        metadata_prefixes,
        metadata_value,
        parse_markdown_table,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )


def system_is_optional_and_absent(registry: dict, system_name: str) -> bool:
    system = registry["systems"][system_name]
    return bool(system.get("optional")) and not workspace_path(system["root"]).exists()


def validate_registry(registry: dict) -> list[str]:
    problems: list[str] = []
    if "systems" not in registry or "sync_rules" not in registry:
        problems.append("config/process-registry.json is missing top-level systems or sync_rules keys")
    return problems


def clean_md(value: str) -> str:
    return value.strip().strip("`")


def extract_bullets_after_marker(text: str, marker: str) -> list[str]:
    items: list[str] = []
    active = False
    for line in text.splitlines():
        stripped = line.strip()
        if not active and stripped == marker:
            active = True
            continue
        if active:
            if not stripped:
                continue
            if stripped.startswith("##") or stripped.endswith(":"):
                break
            if stripped.startswith("- "):
                items.append(clean_md(stripped[2:]))
    return items


def iter_guidance_sections(registry: dict) -> list[tuple[str, dict[str, Any]]]:
    guidance = cast(dict[str, Any], registry.get("workflow_guidance", {}))
    sections: list[tuple[str, dict[str, Any]]] = []
    kickoff = cast(dict[str, Any], guidance.get("kickoff", {}))
    if kickoff:
        sections.append(("kickoff", kickoff))
    for system in ("programbuild", "userjourney"):
        for step, section in cast(dict[str, Any], guidance.get(system, {})).items():
            sections.append((f"{system}:{step}", cast(dict[str, Any], section)))
    return sections


def planning_reference_rules(registry: dict) -> dict[str, Any]:
    return cast(dict[str, Any], registry.get("planning_reference_rules", {}))


def load_external_reference_allowlist(registry: dict) -> set[str]:
    rules = planning_reference_rules(registry)
    manifest_path = str(rules.get("allowlist_manifest", ""))
    if not manifest_path:
        return set()
    path = workspace_path(manifest_path)
    if not path.exists():
        return set()
    payload = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    return {candidate.replace("\\", "/") for candidate in cast(list[str], payload.get("allowed_external_paths", []))}


def validate_authority_sync(registry: dict) -> list[str]:
    problems: list[str] = []

    canonical_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md").read_text(encoding="utf-8")
    file_index_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md").read_text(encoding="utf-8")

    expected_control = sorted(
        Path(path).name for path in registry["systems"]["programbuild"]["control_files"] if path.endswith(".md")
    )
    expected_outputs = sorted(
        Path(path).name for path in registry["systems"]["programbuild"]["output_files"] if path.endswith(".md")
    )

    canonical_control = sorted(extract_bullets_after_marker(canonical_text, "System control files:"))
    canonical_outputs = sorted(extract_bullets_after_marker(canonical_text, "Project execution outputs:"))
    if canonical_control != expected_control:
        problems.append("PROGRAMBUILD_CANONICAL.md system control file list is out of sync with config/process-registry.json")
    if canonical_outputs != expected_outputs:
        problems.append(
            "PROGRAMBUILD_CANONICAL.md project execution output list is out of sync with config/process-registry.json"
        )

    index_control = sorted(clean_md(row.get("File", "")) for row in parse_markdown_table(file_index_text, "1. Control Files"))
    index_outputs = sorted(
        clean_md(row.get("File", "")) for row in parse_markdown_table(file_index_text, "2. Project Output Files")
    )
    if index_control != expected_control:
        problems.append("PROGRAMBUILD_FILE_INDEX.md control file table is out of sync with config/process-registry.json")
    if index_outputs != expected_outputs:
        problems.append("PROGRAMBUILD_FILE_INDEX.md project output table is out of sync with config/process-registry.json")

    known_programbuild_files = set(expected_control) | set(expected_outputs)
    for row in parse_markdown_table(canonical_text, "3. Authority Map"):
        target = Path(clean_md(row.get("Canonical file", ""))).name
        if target and target not in known_programbuild_files:
            problems.append(f"PROGRAMBUILD_CANONICAL.md authority map references unknown file: {target}")

    declared_files_by_system = {
        "programbuild": set(registry["systems"]["programbuild"]["control_files"])
        | set(registry["systems"]["programbuild"]["output_files"]),
        "userjourney": set(registry["systems"]["userjourney"]["core_files"]),
    }
    for rule in registry.get("sync_rules", []):
        system = rule.get("system", "")
        if system == "cross":
            continue
        if system and system_is_optional_and_absent(registry, system):
            continue
        declared = declared_files_by_system.get(system, set())
        for key in ("authority_files", "dependent_files"):
            for path in rule.get(key, []):
                if path not in declared:
                    problems.append(f"sync rule '{rule['name']}' references undeclared {system} file: {path}")
                elif not workspace_path(path).exists():
                    problems.append(f"sync rule '{rule['name']}' references missing workspace file: {path}")

    for section_name, section in iter_guidance_sections(registry):
        if section_name.startswith("userjourney:") and system_is_optional_and_absent(registry, "userjourney"):
            continue
        for key in ("files", "scripts", "prompts"):
            for path in cast(list[str], section.get(key, [])):
                if not workspace_path(path).exists():
                    problems.append(f"workflow guidance '{section_name}' references missing {key[:-1]}: {path}")

    return problems


def validate_planning_references(registry: dict) -> tuple[list[str], list[str]]:
    problems: set[str] = set()
    warnings: set[str] = set()
    rules = planning_reference_rules(registry)
    docs = cast(
        list[str],
        rules.get(
            "docs",
            [
                "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md",
                "USERJOURNEY/IMPLEMENTATION_PLAN.md",
            ],
        ),
    )
    workspace_prefixes = tuple(
        cast(
            list[str],
            rules.get(
                "workspace_prefixes",
                [
                    ".github/",
                    ".vscode/",
                    "BACKUPS/",
                    "PROGRAMBUILD/",
                    "USERJOURNEY/",
                    "config/",
                    "docs/",
                    "schemas/",
                    "scripts/",
                    "tests/",
                ],
            ),
        )
    )
    allowlisted_external_paths = load_external_reference_allowlist(registry)
    allowlist_manifest = str(rules.get("allowlist_manifest", ""))
    if allowlist_manifest:
        allowlist_path = workspace_path(allowlist_manifest)
        userjourney_root = workspace_path("USERJOURNEY")
        if userjourney_root.exists() and not allowlist_path.exists():
            problems.add(f"planning reference allowlist manifest is missing: {allowlist_manifest}")
    path_pattern = re.compile(r"`([^`\n]+\.[A-Za-z0-9]+)`")

    for relative_doc in docs:
        doc_path = workspace_path(relative_doc)
        if not doc_path.exists():
            continue
        for raw_path in path_pattern.findall(doc_path.read_text(encoding="utf-8")):
            candidate = raw_path.replace("\\", "/")
            if "/" not in candidate:
                continue
            if candidate.startswith(workspace_prefixes):
                if not workspace_path(candidate).exists():
                    problems.add(f"{relative_doc} references missing workspace path: {candidate}")
                continue
            if candidate in allowlisted_external_paths:
                continue
            if any(fnmatch(candidate, pattern) for pattern in allowlisted_external_paths):
                continue
            problems.add(f"{relative_doc} references non-allowlisted external implementation path: {candidate}")

    return sorted(problems), sorted(warnings)


def validate_required_files(registry: dict, system_filter: str | None = None) -> list[str]:
    problems: list[str] = []
    for name, system in registry["systems"].items():
        if system_filter and name != system_filter:
            continue
        if system_is_optional_and_absent(registry, name):
            continue
        for key in ("control_files", "output_files", "core_files"):
            for relative_path in system.get(key, []):
                if not workspace_path(relative_path).exists():
                    problems.append(f"Missing required file: {relative_path}")
    return problems


def validate_metadata(registry: dict, system_filter: str | None = None) -> list[str]:
    prefixes = metadata_prefixes(registry)
    problems: list[str] = []
    for name, system in registry["systems"].items():
        if system_filter and name != system_filter:
            continue
        if system_is_optional_and_absent(registry, name):
            continue
        for relative_path in system.get("metadata_required", []):
            path = workspace_path(relative_path)
            if not path.exists():
                continue
            missing = has_required_metadata(path.read_text(encoding="utf-8"), prefixes)
            if missing:
                problems.append(f"Metadata incomplete in {relative_path}: missing {', '.join(missing)}")
    return problems


def metadata_warnings(registry: dict, system_filter: str | None = None) -> list[str]:
    placeholder = registry.get("metadata_rules", {}).get("owner_placeholder", "[ASSIGN]")
    warnings: list[str] = []
    for name, system in registry["systems"].items():
        if system_filter and name != system_filter:
            continue
        if system_is_optional_and_absent(registry, name):
            continue
        for relative_path in system.get("metadata_required", []):
            path = workspace_path(relative_path)
            if not path.exists():
                continue
            owner = metadata_value(path.read_text(encoding="utf-8"), "Owner:")
            if owner in (None, "", placeholder):
                warnings.append(f"Owner not assigned in {relative_path}")
    return warnings


def validate_engineering_ready(registry: dict) -> list[str]:
    problems = validate_required_files(registry)
    if system_is_optional_and_absent(registry, "userjourney"):
        return problems
    open_questions_file = workspace_path(registry["systems"]["userjourney"]["engineering_blocker_file"])
    open_items = extract_numbered_items(
        open_questions_file.read_text(encoding="utf-8"),
        "Remaining Operational And Legal Decisions",
    )
    if open_items:
        problems.append(
            f"USERJOURNEY is not engineering-ready: {len(open_items)} unresolved items remain in USERJOURNEY/OPEN_QUESTIONS.md"
        )
    return problems


def expected_bootstrap_assets() -> set[str]:
    root = workspace_path(".")
    expected: set[str] = {
        ".secrets.baseline",
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".python-version",
        ".yamllint",
        "pyproject.toml",
        "uv.lock",
        "noxfile.py",
        "mkdocs.yml",
        "CHANGELOG.md",
        "CODEOWNERS",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "requirements.txt",
        "QUICKSTART.md",
        ".github/copilot-instructions.md",
        ".github/dependabot.yml",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".vscode/tasks.json",
    }
    patterns = [
        "config/*.json",
        "docs/*.md",
        "scripts/*.py",
        "schemas/*.json",
        "tests/*.py",
        "tests/golden/dashboard/*",
        ".github/instructions/*.md",
        ".github/prompts/*.md",
        ".github/workflows/*.yml",
        ".github/ISSUE_TEMPLATE/*.md",
    ]
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                expected.add(path.relative_to(root).as_posix())
    return expected


def validate_bootstrap_assets(registry: dict) -> list[str]:
    problems: list[str] = []
    assets = set(cast(list[str], registry.get("workspace", {}).get("bootstrap_assets", [])))
    missing = sorted(expected_bootstrap_assets() - assets)
    if missing:
        problems.append("bootstrap_assets is missing current workspace files: " + ", ".join(missing))
    for asset in sorted(assets):
        if not workspace_path(asset).exists():
            problems.append(f"bootstrap_assets references missing workspace file: {asset}")
    return problems


def validate_workflow_state(registry: dict, system_filter: str | None = None) -> list[str]:
    systems = [system_filter] if system_filter else ["programbuild", "userjourney"]
    problems: list[str] = []
    for system in systems:
        if system_is_optional_and_absent(registry, system):
            continue
        path = workflow_state_path(registry, system)
        if not path.exists():
            problems.append(f"Missing workflow state file: {path.relative_to(path.parents[1]).as_posix()}")
            continue
        state = load_workflow_state(registry, system)
        steps = workflow_steps(registry, system)
        active_step = workflow_active_step(registry, system, state)
        if active_step not in steps:
            problems.append(f"Invalid active step '{active_step}' in {path.name}")
            continue
        entry_key = workflow_entry_key(system)
        entries = cast(dict[str, Any], state.get(entry_key, {}))
        in_progress_steps: list[str] = []
        for step in steps:
            if step not in entries:
                problems.append(f"Missing state entry '{step}' in {path.name}")
        active_index = steps.index(active_step)
        for index, step in enumerate(steps):
            entry = cast(dict[str, Any], entries.get(step, {}))
            status = str(entry.get("status", "planned"))
            decision = str(cast(dict[str, Any], entry.get("signoff", {})).get("decision", ""))
            signoff_date = str(cast(dict[str, Any], entry.get("signoff", {})).get("date", ""))
            if status == "in_progress":
                in_progress_steps.append(step)
            if index < active_index and status != "completed":
                problems.append(f"{system} step '{step}' must be completed before active step '{active_step}'")
            if index < active_index and decision not in ("approved", "go", "accepted"):
                problems.append(f"{system} step '{step}' is missing approved sign-off before active step '{active_step}'")
            if index < active_index and not signoff_date:
                problems.append(f"{system} step '{step}' is missing sign-off date before active step '{active_step}'")
            if index > active_index and status == "completed":
                problems.append(f"{system} step '{step}' cannot be completed after the active step '{active_step}'")
        if len(in_progress_steps) != 1:
            problems.append(f"{system} must have exactly one in_progress step; found {len(in_progress_steps)}")
        elif in_progress_steps[0] != active_step:
            problems.append(f"{system} active step '{active_step}' does not match in_progress step '{in_progress_steps[0]}'")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PROGRAMSTART structure and process metadata.")
    parser.add_argument(
        "--check",
        choices=[
            "all",
            "required-files",
            "metadata",
            "engineering-ready",
            "workflow-state",
            "authority-sync",
            "planning-references",
            "bootstrap-assets",
        ],
        default="all",
    )
    parser.add_argument(
        "--system",
        choices=["programbuild", "userjourney"],
        help="Only validate this system.",
    )
    args = parser.parse_args()

    registry = load_registry()
    problems: list[str] = []
    warnings: list[str] = []

    sf = args.system
    if args.check == "all":
        problems.extend(validate_registry(registry))
        problems.extend(validate_required_files(registry, sf))
        problems.extend(validate_metadata(registry, sf))
        problems.extend(validate_workflow_state(registry, sf))
        problems.extend(validate_authority_sync(registry))
        reference_problems, reference_warnings = validate_planning_references(registry)
        problems.extend(reference_problems)
        warnings.extend(metadata_warnings(registry, sf))
        warnings.extend(reference_warnings)
    elif args.check == "required-files":
        problems.extend(validate_registry(registry))
        problems.extend(validate_required_files(registry, sf))
    elif args.check == "metadata":
        problems.extend(validate_metadata(registry, sf))
        warnings.extend(metadata_warnings(registry, sf))
    elif args.check == "workflow-state":
        problems.extend(validate_workflow_state(registry, sf))
    elif args.check == "authority-sync":
        problems.extend(validate_authority_sync(registry))
    elif args.check == "planning-references":
        reference_problems, reference_warnings = validate_planning_references(registry)
        problems.extend(reference_problems)
        warnings.extend(reference_warnings)
    elif args.check == "bootstrap-assets":
        problems.extend(validate_bootstrap_assets(registry))
    else:
        problems.extend(validate_engineering_ready(registry))

    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"Validation passed for check: {args.check}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart validate' or 'pb validate'")
    raise SystemExit(main())
