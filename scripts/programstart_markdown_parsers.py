"""
Markdown parsing helpers extracted from get_state_json().

Each function is a pure text parser that takes markdown content and returns
structured data.  No side effects, no file I/O.
"""

from __future__ import annotations

import re
from typing import Any


def clean_md(value: str) -> str:
    return value.strip().strip("`")


def extract_bullets(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    items: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("##"):
            current_heading = stripped.lstrip("#").strip()
            if in_section and current_heading != heading:
                break
            in_section = current_heading == heading
            continue

        if in_section and stripped.startswith("- "):
            items.append(stripped[2:].strip())

    return items


def extract_bullets_after_marker(text: str, marker: str) -> list[str]:
    lines = text.splitlines()
    items: list[str] = []
    active = False

    for line in lines:
        stripped = line.strip()
        if not active and stripped == marker:
            active = True
            continue
        if active:
            if stripped == "---" or stripped.startswith("##"):
                break
            if stripped.startswith("- "):
                items.append(stripped[2:].strip())

    return items


def extract_subagents(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    lines = text.splitlines()
    report_requirements: list[str] = []
    agents: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    collecting_use = False
    collecting_prompt = False
    collecting_report = False
    prompt_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        if stripped == "Every subagent report should contain:":
            collecting_report = True
            continue
        if collecting_report:
            if stripped == "---":
                collecting_report = False
            elif stripped.startswith("- "):
                report_requirements.append(stripped[2:].strip())
            continue

        if stripped.startswith("## "):
            if current is not None:
                current["prompt"] = "\n".join(prompt_lines).strip()
                agents.append(current)
            title = re.sub(r"^\d+\.\s*", "", stripped.lstrip("#").strip())
            current = {"name": title, "use_for": [], "prompt": ""}
            collecting_use = False
            collecting_prompt = False
            prompt_lines = []
            continue

        if current is None:
            continue

        if stripped == "Use for:":
            collecting_use = True
            collecting_prompt = False
            continue
        if stripped == "Prompt:":
            collecting_use = False
            continue
        if stripped.startswith("```"):
            collecting_prompt = not collecting_prompt
            continue
        if collecting_use and stripped.startswith("- "):
            current["use_for"].append(stripped[2:].strip())
            continue
        if collecting_prompt:
            prompt_lines.append(line)

    if current is not None:
        current["prompt"] = "\n".join(prompt_lines).strip()
        agents.append(current)

    return agents, report_requirements


def extract_startup_sections(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    in_section = False
    current: dict[str, Any] | None = None
    sections: list[dict[str, Any]] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped.lstrip("#").strip()
            if in_section and heading != "3. Stage Startup Checklist":
                break
            in_section = heading == "3. Stage Startup Checklist"
            continue
        if not in_section:
            continue
        if stripped.startswith("### "):
            if current is not None:
                sections.append(current)
            current = {"title": stripped[4:].strip(), "items": []}
            continue
        if current is not None and stripped.startswith("- "):
            current["items"].append(stripped[2:].strip())

    if current is not None:
        sections.append(current)
    return sections


def extract_slice_sections(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    current: dict[str, Any] | None = None
    sections: list[dict[str, Any]] = []
    current_block: str | None = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Slice "):
            if current is not None:
                sections.append(current)
            current = {"title": stripped[3:].strip(), "outcome": "", "scope": [], "test_scope": [], "risk": ""}
            current_block = None
            continue
        if current is None:
            continue
        if stripped.startswith("### "):
            current_block = stripped[4:].strip().lower()
            continue
        if current_block == "outcome" and stripped and not stripped.startswith("#"):
            current["outcome"] = stripped
            current_block = None
            continue
        if current_block == "primary risk" and stripped and not stripped.startswith("#"):
            current["risk"] = stripped
            current_block = None
            continue
        if current_block == "scope" and re.match(r"^\d+\.\s+", stripped):
            current["scope"].append(re.sub(r"^\d+\.\s+", "", stripped))
            continue
        if current_block == "test scope" and (re.match(r"^\d+\.\s+", stripped) or stripped.startswith("Planning-only")):
            current["test_scope"].append(re.sub(r"^\d+\.\s+", "", stripped))

    if current is not None:
        sections.append(current)
    return sections


def extract_file_checklist_sections(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    current: dict[str, Any] | None = None
    sections: list[dict[str, Any]] = []
    current_block: str | None = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### ") and "`" in stripped:
            if current is not None:
                sections.append(current)
            current = {"file": stripped.strip("# ").strip().strip("`"), "status": "", "items": [], "warning": ""}
            current_block = None
            continue
        if current is None:
            continue
        if stripped.startswith("Status:"):
            current["status"] = stripped.removeprefix("Status:").strip()
            continue
        if stripped == "Checklist:":
            current_block = "checklist"
            continue
        if stripped.lower().startswith("critical warning:"):
            current_block = "warning"
            continue
        if current_block == "checklist" and re.match(r"^\d+\.\s+", stripped):
            current["items"].append(re.sub(r"^\d+\.\s+", "", stripped))
            continue
        if current_block == "warning" and stripped and not stripped.startswith("#"):
            current["warning"] = stripped
            current_block = None

    if current is not None:
        sections.append(current)
    return sections


def system_is_attached(system_name: str, registry: dict[str, Any]) -> bool:
    """Check whether a workflow system's root directory exists on disk."""
    # Import here to avoid circular imports at module level
    try:
        from .programstart_common import workspace_path
    except ImportError:  # pragma: no cover - standalone script execution fallback
        from programstart_common import workspace_path  # type: ignore

    system_cfg = registry.get("systems", {}).get(system_name, {})
    root = system_cfg.get("root", "")
    return bool(root) and workspace_path(root).exists()
