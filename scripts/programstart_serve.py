"""
PROGRAMSTART local web dashboard.

Starts a self-contained HTTP server on 127.0.0.1 that provides a
browser-based UI for viewing state, running guide commands, and
advancing workflow stages/phases.

Usage:
    python programstart_serve.py               # default port 7771
    python programstart_serve.py --port 8080
    python programstart_serve.py --no-open     # don't open browser

Security:
    - Binds to 127.0.0.1 only (loopback, not network-accessible).
    - POST /api/run uses a strict command whitelist — no arbitrary shell execution.
    - subprocess is called with a list of arguments, never shell=True.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, cast
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SCRIPTS = Path(__file__).resolve().parent

try:
    from .programstart_command_registry import dashboard_allowed_commands
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_command_registry import dashboard_allowed_commands

# ---------------------------------------------------------------------------
# Allowed commands — strict whitelist, no shell interpolation possible
# ---------------------------------------------------------------------------
ALLOWED_COMMANDS: dict[str, list[str]] = dashboard_allowed_commands(PYTHON, SCRIPTS)

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def run_command(command_key: str, extra_args: list[str] | None = None) -> dict[str, Any]:
    """Run an allowed command and return {output, exit_code}."""
    if command_key not in ALLOWED_COMMANDS:
        return {"output": f"Error: unknown command '{command_key}'", "exit_code": 1}
    cmd = ALLOWED_COMMANDS[command_key][:]
    if extra_args:
        allowed_extras = {"--decision", "--notes", "--date", "--system", "approved", "hold", "blocked"}
        for arg in extra_args:
            if arg not in allowed_extras:
                return {"output": f"Error: extra arg '{arg}' not permitted", "exit_code": 1}
        cmd.extend(extra_args)
    env = {**os.environ, "NO_COLOR": "1"}
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, env=env)
    output = result.stdout + (f"\nSTDERR:\n{result.stderr}" if result.stderr.strip() else "")
    return {"output": strip_ansi(output.strip()), "exit_code": result.returncode}


# ---------------------------------------------------------------------------
# Bootstrap — validated separately; accepts user-supplied path and name
# ---------------------------------------------------------------------------
_SAFE_PATH_RE = re.compile(r"^[A-Za-z]:[/\\][A-Za-z0-9 /\\._-]{1,259}$")
_SAFE_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
_SAFE_VARIANTS = frozenset({"lite", "product", "enterprise"})


def run_bootstrap(
    dest: str,
    project_name: str,
    variant: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Scaffold a new project with strictly validated inputs. Never uses shell=True."""
    if not dest or not _SAFE_PATH_RE.match(dest):
        return {
            "output": "Error: destination path is invalid.\nExpected format: C:\\Projects\\MyApp\n(letters, numbers, spaces, hyphens, underscores, dots only)",
            "exit_code": 1,
        }
    if not project_name or not _SAFE_NAME_RE.match(project_name):
        return {
            "output": "Error: project name must start with a letter and contain only letters, numbers, hyphens, or underscores (max 64 chars).",
            "exit_code": 1,
        }
    if variant not in _SAFE_VARIANTS:
        return {"output": f"Error: variant must be one of: {', '.join(sorted(_SAFE_VARIANTS))}", "exit_code": 1}
    dest_path = Path(dest).resolve()
    cmd = [
        PYTHON,
        str(SCRIPTS / "programstart_bootstrap.py"),
        "--dest",
        str(dest_path),
        "--project-name",
        project_name,
        "--variant",
        variant,
    ]
    if dry_run:
        cmd.append("--dry-run")
    env = {**os.environ, "NO_COLOR": "1"}
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, env=env)
    output = result.stdout + (f"\nSTDERR:\n{result.stderr}" if result.stderr.strip() else "")
    return {"output": strip_ansi(output.strip()), "exit_code": result.returncode}


def get_state_json() -> dict[str, Any]:
    """Return both workflow states as JSON-serialisable dicts plus guidance metadata."""
    try:
        sys.path.insert(0, str(SCRIPTS))
        try:
            from .programstart_common import (  # noqa: PLC0415
                extract_numbered_items,
                load_registry,
                load_workflow_state,
                parse_markdown_table,
                workflow_active_step,
                workflow_entry_key,
                workflow_steps,
                workspace_path,
            )
        except ImportError:
            from programstart_common import (  # noqa: PLC0415
                extract_numbered_items,
                load_registry,
                load_workflow_state,
                parse_markdown_table,
                workflow_active_step,
                workflow_entry_key,
                workflow_steps,
                workspace_path,
            )

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

        registry = load_registry()

        def system_is_attached(system_name: str) -> bool:
            system_cfg = registry.get("systems", {}).get(system_name, {})
            root = system_cfg.get("root", "")
            return bool(root) and workspace_path(root).exists()

        guidance = registry.get("workflow_guidance", {})
        result: dict[str, Any] = {}
        for system in ("programbuild", "userjourney"):
            system_cfg = registry.get("systems", {}).get(system, {})
            attached = system_is_attached(system)
            if system_cfg.get("optional") and not attached:
                result[system] = {
                    "active": "not attached",
                    "variant": "",
                    "steps": [],
                    "entries": {},
                    "completed": 0,
                    "blocked": 0,
                    "total": 0,
                    "descriptions": {},
                    "attached": False,
                    "open_questions": 0,
                }
                continue
            state = load_workflow_state(registry, system)
            active = workflow_active_step(registry, system, state)
            steps = workflow_steps(registry, system)
            entry_key = workflow_entry_key(system)
            entries = state.get(entry_key, {})
            completed = sum(1 for e in entries.values() if e.get("status") == "completed")
            blocked = sum(1 for e in entries.values() if e.get("status") == "blocked")
            sys_guidance = guidance.get(system, {})
            descriptions: dict[str, str] = {}
            for step in steps:
                g = sys_guidance.get(step, {})
                descriptions[step] = g.get("description", "")
            sys_data: dict[str, Any] = {
                "active": active,
                "variant": state.get("variant", ""),
                "steps": steps,
                "entries": entries,
                "completed": completed,
                "blocked": blocked,
                "total": len(steps),
                "descriptions": descriptions,
                "attached": attached,
            }
            if system == "userjourney":
                uj_cfg = registry.get("systems", {}).get("userjourney", {})
                oq_path = workspace_path(uj_cfg.get("engineering_blocker_file", ""))
                try:
                    oq = extract_numbered_items(
                        oq_path.read_text(encoding="utf-8"),
                        "Remaining Operational And Legal Decisions",
                    )
                    sys_data["open_questions"] = len(oq)
                except Exception:
                    sys_data["open_questions"] = 0
            result[system] = sys_data

        file_index_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md").read_text(encoding="utf-8")
        kickoff_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md").read_text(encoding="utf-8")
        subagents_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md").read_text(encoding="utf-8")
        playbook_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD.md").read_text(encoding="utf-8")
        lite_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_LITE.md").read_text(encoding="utf-8")
        product_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_PRODUCT.md").read_text(encoding="utf-8")
        enterprise_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_ENTERPRISE.md").read_text(encoding="utf-8")
        userjourney_attached = system_is_attached("userjourney")
        execution_slices_text = (
            workspace_path("USERJOURNEY/EXECUTION_SLICES.md").read_text(encoding="utf-8") if userjourney_attached else ""
        )
        implementation_tracker_text = (
            workspace_path("USERJOURNEY/IMPLEMENTATION_TRACKER.md").read_text(encoding="utf-8") if userjourney_attached else ""
        )
        file_checklist_text = (
            workspace_path("USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md").read_text(encoding="utf-8")
            if userjourney_attached
            else ""
        )

        control_docs: list[dict[str, str]] = []
        for row in parse_markdown_table(file_index_text, "1. Control Files"):
            filename = clean_md(row.get("File", ""))
            if not filename:
                continue
            control_docs.append(
                {
                    "file": f"PROGRAMBUILD/{filename}",
                    "name": filename,
                    "type": clean_md(row.get("Type", "")),
                    "status": clean_md(row.get("Status", "")),
                    "purpose": clean_md(row.get("Purpose", "")),
                    "canonical_for": clean_md(row.get("Canonical for", "")),
                }
            )

        subagents, report_requirements = extract_subagents(subagents_text)
        canonical_names = {item["name"] for item in subagents}

        variant_subagents = {
            "lite": [
                clean_md(row.get("Subagent", ""))
                for row in parse_markdown_table(lite_text, "Suggested Subagents")
                if clean_md(row.get("Subagent", ""))
            ],
            "product": [
                clean_md(row.get("Subagent", ""))
                for row in parse_markdown_table(product_text, "Suggested Subagents")
                if clean_md(row.get("Subagent", ""))
            ],
            "enterprise": [
                clean_md(row.get("Subagent", ""))
                for row in parse_markdown_table(enterprise_text, "Suggested Subagents")
                if clean_md(row.get("Subagent", ""))
            ],
        }

        variant_gate_model: dict[str, dict[str, str]] = {}
        for row in parse_markdown_table(playbook_text, "7. Gate Model By Variant"):
            variant = clean_md(row.get("Variant", "")).lower()
            if not variant:
                continue
            variant_gate_model[variant] = {
                "gate_style": clean_md(row.get("Gate style", "")),
                "evidence_expectation": clean_md(row.get("Evidence expectation", "")),
            }

        stage_subagents = {
            "inputs_and_mode_selection": ["Product Analyst"],
            "feasibility": ["Research Scout", "Product Analyst"],
            "research": ["Research Scout"],
            "requirements_and_ux": ["Product Analyst", "UX Flow Designer"],
            "architecture_and_risk_spikes": ["Architecture Reviewer", "Risk Spike Agent", "Security Reviewer"],
            "scaffold_and_guardrails": ["Contract Auditor"],
            "test_strategy": ["Test Planner"],
            "implementation_loop": ["Contract Auditor", "Test Planner"],
            "release_readiness": ["Release Readiness Reviewer"],
            "audit_and_drift_control": ["Contract Auditor", "Security Reviewer"],
            "post_launch_review": ["Release Readiness Reviewer"],
        }

        result["catalog"] = {
            "control_docs": control_docs,
            "subagents": subagents,
            "subagent_report_requirements": report_requirements,
            "variant_subagents": variant_subagents,
            "variant_only_subagents": {
                key: [name for name in names if name not in canonical_names] for key, names in variant_subagents.items()
            },
            "variant_gate_model": variant_gate_model,
            "stage_subagents": stage_subagents,
            "kickoff": {
                "preflight": extract_bullets_after_marker(kickoff_text, "Before using this packet:"),
                "files": extract_bullets(kickoff_text, "1. Kickoff File Set"),
                "decision_matrix": parse_markdown_table(kickoff_text, "Kickoff Decision Matrix"),
                "startup_sections": extract_startup_sections(kickoff_text),
            },
            "userjourney_execution": {
                "attached": userjourney_attached,
                "phase_overview": parse_markdown_table(implementation_tracker_text, "Phase Overview")
                if userjourney_attached
                else [],
                "slice_readiness": parse_markdown_table(implementation_tracker_text, "Slice Readiness")
                if userjourney_attached
                else [],
                "critical_risks": parse_markdown_table(implementation_tracker_text, "Critical Risk Register")
                if userjourney_attached
                else [],
                "slice_sections": extract_slice_sections(execution_slices_text) if userjourney_attached else [],
                "slice_mapping": parse_markdown_table(file_checklist_text, "Slice Mapping") if userjourney_attached else [],
                "file_sections": extract_file_checklist_sections(file_checklist_text) if userjourney_attached else [],
            },
            "drift": build_drift_summary(),
        }
        return result
    except Exception as exc:
        return {"error": str(exc)}


def get_doc_preview(relative_path: str) -> dict[str, Any]:
    """Return a safe doc preview for a workspace-relative text file."""
    normalized = relative_path.replace("\\", "/").strip().lstrip("/")
    if not normalized:
        return {"error": "missing path"}
    allowed_prefixes = ("PROGRAMBUILD/", "USERJOURNEY/", "scripts/", "config/", ".vscode/")
    if not normalized.startswith(allowed_prefixes):
        return {"error": "path not allowed"}
    target = (ROOT / normalized).resolve()
    if ROOT.resolve() not in target.parents and target != ROOT.resolve():
        return {"error": "path escapes workspace"}
    if not target.exists() or not target.is_file():
        return {"error": "file not found"}
    if target.suffix.lower() not in {".md", ".txt", ".json", ".py", ".ps1", ".yml", ".yaml"}:
        return {"error": "file type not previewable"}
    text = target.read_text(encoding="utf-8")
    lines = text.splitlines()
    return {
        "path": normalized,
        "line_count": len(lines),
        "truncated": len(lines) > 220,
        "content": "\n".join(lines[:220]),
    }


def update_implementation_tracker_phase(phase: str, status: str, blockers: str) -> dict[str, Any]:
    """Update the USERJOURNEY implementation tracker phase overview row."""
    if not (ROOT / "USERJOURNEY").exists():
        return {"output": "Error: USERJOURNEY is not attached in this repository.", "exit_code": 1}
    valid_statuses = {"Planned", "In Progress", "Blocked", "Completed"}
    phase = phase.strip()
    status = status.strip()
    blockers = blockers.strip()
    if phase not in {str(i) for i in range(9)}:
        return {"output": "Error: phase must be 0-8.", "exit_code": 1}
    if status not in valid_statuses:
        return {"output": f"Error: status must be one of: {', '.join(sorted(valid_statuses))}", "exit_code": 1}

    tracker_path = ROOT / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    text = tracker_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    target_prefix = f"| {phase} |"
    updated = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(target_prefix):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 6:
            return {"output": f"Error: phase row for {phase} has unexpected shape.", "exit_code": 1}
        cells[1] = status
        cells[4] = blockers or cells[4]
        lines[idx] = "| " + " | ".join(cells) + " |"
        updated = True
        break

    if not updated:
        return {"output": f"Error: phase {phase} not found in IMPLEMENTATION_TRACKER.md", "exit_code": 1}

    for idx, line in enumerate(lines[:10]):
        if line.startswith("Last updated:"):
            lines[idx] = f"Last updated: {date.today().isoformat()}"
            break

    tracker_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output": f"Updated USERJOURNEY phase {phase} to {status}", "exit_code": 0}


def update_implementation_tracker_slice(slice_name: str, status: str, notes: str) -> dict[str, Any]:
    """Update the USERJOURNEY implementation tracker slice readiness row."""
    if not (ROOT / "USERJOURNEY").exists():
        return {"output": "Error: USERJOURNEY is not attached in this repository.", "exit_code": 1}
    valid_statuses = {"Pending", "Selected", "Ready", "Blocked", "Completed"}
    slice_name = slice_name.strip()
    status = status.strip()
    notes = notes.strip()
    if slice_name not in {f"Slice {i}" for i in range(1, 10)}:
        return {"output": "Error: slice must be Slice 1 through Slice 9.", "exit_code": 1}
    if status not in valid_statuses:
        return {"output": f"Error: status must be one of: {', '.join(sorted(valid_statuses))}", "exit_code": 1}

    tracker_path = ROOT / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    lines = tracker_path.read_text(encoding="utf-8").splitlines()
    target_prefix = f"| {slice_name} |"
    updated = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(target_prefix):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 4:
            return {"output": f"Error: slice row for {slice_name} has unexpected shape.", "exit_code": 1}
        cells[1] = status
        cells[3] = notes
        lines[idx] = "| " + " | ".join(cells) + " |"
        updated = True
        break

    if not updated:
        return {"output": f"Error: {slice_name} not found in IMPLEMENTATION_TRACKER.md", "exit_code": 1}

    for idx, line in enumerate(lines[:10]):
        if line.startswith("Last updated:"):
            lines[idx] = f"Last updated: {date.today().isoformat()}"
            break

    tracker_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output": f"Updated {slice_name} to {status}", "exit_code": 0}


def save_workflow_signoff(system: str, decision: str, signoff_date: str, notes: str) -> dict[str, Any]:
    """Save signoff metadata for the active workflow step without advancing."""
    if system not in {"programbuild", "userjourney"}:
        return {"output": "Error: unknown system.", "exit_code": 1}

    sys.path.insert(0, str(SCRIPTS))
    try:
        from .programstart_common import (  # noqa: PLC0415
            load_registry,
            load_workflow_state,
            save_workflow_state,
            workflow_active_step,
            workflow_entry_key,
        )
    except ImportError:
        from programstart_common import (  # noqa: PLC0415
            load_registry,
            load_workflow_state,
            save_workflow_state,
            workflow_active_step,
            workflow_entry_key,
        )

    registry = load_registry()
    state = load_workflow_state(registry, system)
    active_step = workflow_active_step(registry, system, state)
    entry_key = workflow_entry_key(system)
    entries = cast(dict[str, Any], state[entry_key])
    entry = cast(dict[str, Any], entries[active_step])
    signoff_record = {
        "decision": decision.strip(),
        "date": signoff_date.strip(),
        "notes": notes.strip(),
        "saved_at": date.today().isoformat(),
    }
    entry["signoff"] = signoff_record
    entry.setdefault("signoff_history", []).append(signoff_record)
    save_workflow_state(registry, system, state)
    return {"output": f"Saved signoff metadata for {system} {active_step}", "exit_code": 0}


def advance_workflow_with_signoff(
    system: str,
    decision: str,
    signoff_date: str,
    notes: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Advance a workflow while recording explicit signoff metadata."""
    if system not in {"programbuild", "userjourney"}:
        return {"output": "Error: unknown system.", "exit_code": 1}

    sys.path.insert(0, str(SCRIPTS))
    try:
        from .programstart_common import (  # noqa: PLC0415
            load_registry,
            load_workflow_state,
            save_workflow_state,
            workflow_active_step,
            workflow_entry_key,
            workflow_steps,
        )
    except ImportError:
        from programstart_common import (  # noqa: PLC0415
            load_registry,
            load_workflow_state,
            save_workflow_state,
            workflow_active_step,
            workflow_entry_key,
            workflow_steps,
        )

    registry = load_registry()
    state = load_workflow_state(registry, system)
    active_step = workflow_active_step(registry, system, state)
    steps = workflow_steps(registry, system)
    entry_key = workflow_entry_key(system)
    entries = cast(dict[str, Any], state[entry_key])
    current_entry = cast(dict[str, Any], entries[active_step])
    if str(current_entry.get("status", "planned")) != "in_progress":
        return {"output": f"Error: active {system} step '{active_step}' is not in_progress", "exit_code": 1}

    decision_value = decision.strip() or "approved"
    date_value = signoff_date.strip() or date.today().isoformat()
    notes_value = notes.strip()
    current_index = steps.index(active_step)
    if dry_run:
        if current_index + 1 < len(steps):
            next_step = steps[current_index + 1]
            output = (
                f"[dry-run] Would mark {system} '{active_step}' completed "
                f"(decision={decision_value!r}, date={date_value!r})\n"
                f"[dry-run] Would advance {system} from '{active_step}' -> '{next_step}'"
            )
        else:
            output = (
                f"[dry-run] Would mark final {system} step '{active_step}' completed "
                f"(decision={decision_value!r}, date={date_value!r})"
            )
        return {"output": output, "exit_code": 0}

    advance_record = {
        "decision": decision_value,
        "date": date_value,
        "notes": notes_value,
        "saved_at": date.today().isoformat(),
    }
    current_entry["status"] = "completed"
    current_entry["signoff"] = advance_record
    current_entry.setdefault("signoff_history", []).append(advance_record)
    if current_index + 1 < len(steps):
        next_step = steps[current_index + 1]
        next_entry = cast(dict[str, Any], entries[next_step])
        if str(next_entry.get("status", "planned")) == "planned":
            next_entry["status"] = "in_progress"
        state["active_stage" if system == "programbuild" else "active_phase"] = next_step
        output = f"Advanced {system} from {active_step} to {next_step}"
    else:
        output = f"Completed final {system} step {active_step}"

    save_workflow_state(registry, system, state)
    return {"output": output, "exit_code": 0}


def build_drift_summary() -> dict[str, Any]:
    """Return a dashboard-friendly drift summary based on current changed files and sync rules."""
    sys.path.insert(0, str(SCRIPTS))
    try:
        from .programstart_common import (  # noqa: PLC0415
            git_changed_files,
            load_registry,
            load_workflow_state,
            workflow_active_step,
            workflow_state_config,
            workflow_steps,
            workspace_path,
        )
    except ImportError:
        from programstart_common import (  # noqa: PLC0415
            git_changed_files,
            load_registry,
            load_workflow_state,
            workflow_active_step,
            workflow_state_config,
            workflow_steps,
            workspace_path,
        )

    registry = load_registry()
    changed_files = git_changed_files()
    changed_set = set(changed_files)
    violations: list[str] = []
    notes: list[str] = []
    sync_rows: list[dict[str, Any]] = []

    for rule in registry.get("sync_rules", []):
        authority = set(rule["authority_files"])
        dependents = set(rule["dependent_files"])
        touched_authority = sorted(changed_set & authority)
        touched_dependents = sorted(changed_set & dependents)
        if touched_dependents and not touched_authority and rule.get("require_authority_when_dependents_change", False):
            violations.append(f"{rule['name']}: dependent files changed without authority files: {', '.join(touched_dependents)}")
        elif touched_authority and not touched_dependents:
            notes.append(f"{rule['name']}: authority files changed without dependent files: {', '.join(touched_authority)}")
        sync_rows.append(
            {
                "name": rule["name"],
                "system": rule.get("system", ""),
                "authority_files": rule["authority_files"],
                "dependent_files": rule["dependent_files"],
                "touched_authority": touched_authority,
                "touched_dependents": touched_dependents,
            }
        )

    for system in ("programbuild", "userjourney"):
        system_cfg = registry.get("systems", {}).get(system, {})
        root = system_cfg.get("root", "")
        if system_cfg.get("optional") and root and not workspace_path(root).exists():
            continue
            state = load_workflow_state(registry, system)
            config = workflow_state_config(registry, system)
            step_order = workflow_steps(registry, system)
            active_step = workflow_active_step(registry, system, state)
            active_index = step_order.index(active_step)
            step_files = config.get("step_files", {})
            for changed_file in changed_files:
                owning_step = next((step for step in step_order if changed_file in step_files.get(step, [])), None)
                if owning_step is None:
                    continue
                owning_index = step_order.index(owning_step)
                if owning_index > active_index:
                    violations.append(
                        f"{system}: {changed_file} belongs to future step '{owning_step}' while active step is '{active_step}'"
                    )

    return {
        "changed_files": changed_files,
        "violations": violations,
        "notes": notes,
        "sync_rules": sync_rows,
        "status": "failed" if violations else "passed",
    }


# ---------------------------------------------------------------------------
# Embedded HTML dashboard
# ---------------------------------------------------------------------------
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PROGRAMSTART Dashboard</title>
<style>
  :root {
    --bg: #1e1e2e; --surface: #24273a; --surface2: #1a1b26; --border: #363a4f;
    --text: #cad3f5; --dim: #6e738d; --accent: #8aadf4;
    --green: #a6da95; --yellow: #eed49f; --red: #ed8796;
    --cyan: #8bd5ca; --mauve: #c6a0f6; --peach: #f5a97f;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-size: 14px; }

  /* Header */
  header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 10px 20px; display: flex; align-items: center; gap: 12px; }
  header h1 { font-size: 15px; font-weight: 600; color: var(--accent); letter-spacing: 1px; }
  header .sub { font-size: 11px; color: var(--dim); }
  header .spacer { flex: 1; }

  /* Buttons */
  .btn { background: var(--border); border: 1px solid var(--border); color: var(--text); padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; transition: background 0.15s; white-space: nowrap; }
  .btn:hover { background: #454858; }
  .btn:disabled { opacity: 0.4; cursor: default; }
  .btn.primary { background: var(--accent); color: #1e1e2e; border-color: var(--accent); font-weight: 600; }
  .btn.primary:hover { background: #9bb8f7; }
  .btn.danger { background: transparent; border-color: var(--red); color: var(--red); }
  .btn.danger:hover { background: rgba(237,135,150,0.1); }
  .btn.warning { border-color: var(--yellow); color: var(--yellow); background: transparent; }
  .btn.warning:hover { background: rgba(238,212,159,0.1); }
  .btn.ghost { border-color: transparent; color: var(--dim); background: transparent; }
  .btn.ghost:hover { color: var(--text); border-color: var(--border); }
  .btn.success { border-color: var(--green); color: var(--green); background: transparent; }
  .btn.success:hover { background: rgba(166,218,149,0.08); }

  /* Layout */
  main { padding: 16px 20px; display: flex; flex-direction: column; gap: 14px; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

  /* Cards */
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
  .card h2 { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; color: var(--cyan); display: flex; align-items: center; gap: 8px; }
  .meta { font-size: 11px; color: var(--dim); }

  /* Badges */
  .badge { display: inline-block; border-radius: 20px; padding: 1px 8px; font-size: 10px; font-weight: 500; }
  .badge.active { background: rgba(238,212,159,0.15); border: 1px solid var(--yellow); color: var(--yellow); }
  .badge.blocker { background: rgba(237,135,150,0.12); border: 1px solid var(--red); color: var(--red); }
  .badge.ok { background: rgba(166,218,149,0.12); border: 1px solid var(--green); color: var(--green); }
  .badge.variant { background: rgba(198,160,246,0.12); border: 1px solid var(--mauve); color: var(--mauve); }

  /* Progress */
  .progress-bar { background: var(--border); border-radius: 4px; height: 5px; margin: 6px 0 10px; }
  .progress-fill { height: 100%; border-radius: 4px; transition: width 0.4s ease; }
  .progress-fill.green { background: var(--green); }
  .progress-fill.yellow { background: var(--yellow); }

  /* Step list */
  .steps { display: flex; flex-direction: column; gap: 2px; max-height: 320px; overflow-y: auto; padding-right: 4px; }
  .steps::-webkit-scrollbar { width: 3px; }
  .steps::-webkit-scrollbar-track { background: transparent; }
  .steps::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  .step { display: grid; grid-template-columns: 10px 1fr auto; gap: 6px; align-items: baseline; padding: 4px 6px; border-radius: 4px; cursor: default; }
  .step:hover { background: rgba(202,211,245,0.03); }
  .step.active { background: rgba(238,212,159,0.06); border-left: 2px solid var(--yellow); padding-left: 4px; }
  .step-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 4px; }
  .step-dot.completed { background: var(--green); }
  .step-dot.in_progress { background: var(--yellow); box-shadow: 0 0 6px var(--yellow); }
  .step-dot.planned { background: var(--dim); opacity: 0.5; }
  .step-dot.blocked { background: var(--red); }
  .step-body { min-width: 0; }
  .step-name { font-size: 12px; }
  .step-name.active { color: var(--yellow); font-weight: 500; }
  .step-desc { font-size: 10px; color: var(--dim); line-height: 1.3; margin-top: 1px; }
  .step-signoff { font-size: 10px; color: var(--dim); white-space: nowrap; }

  /* Action bar */
  .actions { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); }

  /* Guide section */
  .section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
  .section h2 { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; color: var(--mauve); display: flex; align-items: center; gap: 8px; }
  .guide-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .guide-block h3 { font-size: 11px; color: var(--cyan); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
  .guide-block .guide-desc { font-size: 11px; color: var(--peach); margin-bottom: 8px; line-height: 1.4; font-style: italic; }
  .guide-items { display: flex; flex-direction: column; gap: 3px; }
  .guide-item { font-size: 11px; }
  .guide-item a { color: var(--accent); text-decoration: none; }
  .guide-item a:hover { text-decoration: underline; }
  .guide-label { font-size: 10px; color: var(--dim); text-transform: uppercase; letter-spacing: 0.5px; margin: 6px 0 3px; font-weight: 600; }

  /* Terminal */
  .terminal { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 10px 12px; font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace; font-size: 11px; line-height: 1.5; min-height: 60px; max-height: 400px; overflow-y: auto; white-space: pre-wrap; color: #cad3f5; }
  .terminal.hidden { display: none; }
  .terminal.error { border-color: var(--red); }
  .terminal.success { border-color: var(--green); }
  .terminal-bar { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; flex-wrap: wrap; }
  .terminal-bar .label { font-size: 11px; color: var(--dim); flex: 1; min-width: 140px; }
  .spinner { display: none; width: 12px; height: 12px; border: 2px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.7s linear infinite; }
  .spinner.active { display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Modal */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 100; }
  .modal-overlay.hidden { display: none; }
  .modal { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; width: 420px; max-width: 90vw; }
  .modal h3 { font-size: 14px; color: var(--accent); margin-bottom: 12px; }
  .modal label { display: block; font-size: 11px; color: var(--dim); margin: 8px 0 3px; text-transform: uppercase; letter-spacing: 0.5px; }
  .modal input, .modal textarea { width: 100%; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 6px 8px; font-size: 12px; font-family: inherit; }
  .modal input:focus, .modal textarea:focus { outline: none; border-color: var(--accent); }
  .modal textarea { resize: vertical; min-height: 50px; }
  .modal .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 14px; }

  .status-bar { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .status-bar .status-item { font-size: 11px; color: var(--dim); }
  .status-bar .status-item strong { color: var(--text); font-weight: 500; }
  .status-bar .dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 4px; }
  .status-bar .dot.green { background: var(--green); }
  .status-bar .dot.yellow { background: var(--yellow); }
  .status-bar .dot.red { background: var(--red); }

  .variant-opt { display: flex; align-items: center; gap: 7px; font-size: 12px; cursor: pointer; padding: 4px 6px; border-radius: 4px; }
  .variant-opt:hover { background: rgba(202,211,245,0.04); }
  .variant-opt input[type="radio"], .variant-opt input[type="checkbox"] { accent-color: var(--accent); cursor: pointer; flex-shrink: 0; }
  .variant-opt strong { color: var(--text); min-width: 72px; }
  .variant-opt .meta { margin: 0; }
  .catalog-list, .subagent-list, .handoff-list { display: flex; flex-direction: column; gap: 8px; }
  .catalog-item, .subagent-card, .handoff-card { background: rgba(202,211,245,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
  .catalog-item h3, .subagent-card h3, .handoff-card h3 { font-size: 11px; color: var(--cyan); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .catalog-item p, .subagent-card p, .handoff-card p { font-size: 11px; color: var(--text); line-height: 1.45; }
  .catalog-meta, .subagent-meta { font-size: 10px; color: var(--dim); margin-top: 3px; }
  .pill-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  .pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 10px; border: 1px solid var(--border); color: var(--text); background: rgba(202,211,245,0.04); }
  .pill.rec { border-color: var(--yellow); color: var(--yellow); background: rgba(238,212,159,0.08); }
  .pill.variant { border-color: var(--mauve); color: var(--mauve); background: rgba(198,160,246,0.08); }
  .pill.dim { color: var(--dim); }
  .link-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  details.doc-details, details.subagent-details, details.kickoff-details { margin-top: 8px; }
  details.doc-details summary, details.subagent-details summary, details.kickoff-details summary { cursor: pointer; color: var(--accent); font-size: 11px; }
  .inline-code { font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace; font-size: 10px; color: var(--peach); }
  .exec-grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 14px; }
  .table-ish { display: flex; flex-direction: column; gap: 8px; }
  .table-row { display: grid; grid-template-columns: 1fr 1fr 1.3fr; gap: 8px; align-items: start; background: rgba(202,211,245,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
  .table-row.phase { grid-template-columns: 0.6fr 0.7fr 1.3fr 1fr; }
  .table-row .label { font-size: 10px; color: var(--dim); text-transform: uppercase; letter-spacing: 0.5px; }
  .table-row .value { font-size: 11px; color: var(--text); line-height: 1.4; }
  .doc-preview { position: fixed; top: 0; right: 0; width: min(760px, 92vw); height: 100vh; background: var(--surface2); border-left: 1px solid var(--border); z-index: 120; display: flex; flex-direction: column; box-shadow: -10px 0 40px rgba(0,0,0,0.35); }
  .doc-preview.hidden { display: none; }
  .doc-preview-header { padding: 12px 14px; border-bottom: 1px solid var(--border); display: flex; gap: 8px; align-items: center; }
  .doc-preview-title { flex: 1; min-width: 0; font-size: 12px; color: var(--accent); }
  .doc-preview-body { padding: 12px 14px; overflow: auto; white-space: pre-wrap; font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace; font-size: 11px; line-height: 1.5; }
  .launcher-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
  .launcher-card { background: rgba(202,211,245,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
  .launcher-card h4 { font-size: 11px; color: var(--cyan); margin-bottom: 6px; }
  .mini-form { display: grid; grid-template-columns: 0.5fr 0.8fr 1.7fr auto; gap: 8px; align-items: end; margin-top: 10px; }
  .mini-form label { display: block; font-size: 10px; color: var(--dim); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .mini-form select, .mini-form input { width: 100%; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 6px 8px; font-size: 12px; }
  .recent-projects { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
  .recent-project { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; background: rgba(202,211,245,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
  .recent-project .title { font-size: 11px; color: var(--text); min-width: 160px; }
  .recent-project .path { font-size: 10px; color: var(--dim); flex: 1; min-width: 220px; }
  @media (max-width: 900px) { .exec-grid, .launcher-grid, .table-row, .table-row.phase { grid-template-columns: 1fr; } }
  @media (max-width: 900px) { .mini-form { grid-template-columns: 1fr; } }
  @media (max-width: 700px) { .row, .guide-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>PROGRAMSTART</h1>
  <span class="sub">Local Workflow Dashboard</span>
  <span class="spacer"></span>
  <span id="lastUpdated" class="sub"></span>
  <button class="btn" onclick="loadAll()">Refresh</button>
  <button class="btn primary" onclick="openBootstrapModal()">+ New Project</button>
</header>

<main>
  <!-- Status bar -->
  <div class="status-bar">
    <div class="status-item"><span id="dot-pb" class="dot yellow"></span> PB: <strong id="sb-pb">...</strong></div>
    <div class="status-item"><span id="dot-uj" class="dot yellow"></span> UJ: <strong id="sb-uj">...</strong></div>
    <div class="status-item" id="sb-blockers"></div>
    <div style="flex:1"></div>
    <div class="status-item" id="sb-updated"></div>
  </div>

  <!-- System cards -->
  <div class="row">
    <div class="card" id="card-pb">
      <h2>PROGRAMBUILD <span id="pb-variant" class="badge variant"></span></h2>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
        <span id="pb-active" class="badge active">...</span>
        <span id="pb-progress-label" class="meta"></span>
      </div>
      <div class="progress-bar"><div id="pb-bar" class="progress-fill green" style="width:0%"></div></div>
      <div id="pb-steps" class="steps"></div>
      <div class="actions">
        <button class="btn ghost" onclick="runCmd('guide.programbuild')">Guide</button>
        <button class="btn ghost" onclick="runCmd('drift')">Drift Check</button>
        <button class="btn ghost" onclick="runCmd('progress')">Progress</button>
        <button class="btn ghost" onclick="openAdvanceModal('programbuild', 'signoff')">Signoff</button>
        <button class="btn warning" onclick="runCmd('advance.programbuild.dry')">Dry-run</button>
        <button class="btn primary" onclick="openAdvanceModal('programbuild', 'advance')">Advance</button>
      </div>
    </div>

    <div class="card" id="card-uj">
      <h2>USERJOURNEY <span id="uj-blockers" class="badge blocker" style="display:none"></span></h2>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
        <span id="uj-active" class="badge active">...</span>
        <span id="uj-progress-label" class="meta"></span>
      </div>
      <div class="progress-bar"><div id="uj-bar" class="progress-fill green" style="width:0%"></div></div>
      <div id="uj-steps" class="steps"></div>
      <div class="actions">
        <button class="btn ghost" onclick="runCmd('guide.userjourney')">Guide</button>
        <button class="btn ghost" onclick="runCmd('drift')">Drift Check</button>
        <button class="btn ghost" onclick="runCmd('status')">Status</button>
        <button class="btn ghost" onclick="openAdvanceModal('userjourney', 'signoff')">Signoff</button>
        <button class="btn warning" onclick="runCmd('advance.userjourney.dry')">Dry-run</button>
        <button class="btn primary" onclick="openAdvanceModal('userjourney', 'advance')">Advance</button>
      </div>
    </div>
  </div>

  <!-- Guide panels -->
  <div class="section" id="guide-section">
    <h2>Active Step Guide <button class="btn ghost" style="margin-left:auto" onclick="runCmd('guide.kickoff')">Kickoff Guide</button></h2>
    <div class="guide-grid">
      <div class="guide-block">
        <h3 id="guide-pb-title">PROGRAMBUILD</h3>
        <div id="guide-pb-desc" class="guide-desc" style="display:none"></div>
        <div id="guide-pb-content"><span class="meta">Loading guide...</span></div>
      </div>
      <div class="guide-block">
        <h3 id="guide-uj-title">USERJOURNEY</h3>
        <div id="guide-uj-desc" class="guide-desc" style="display:none"></div>
        <div id="guide-uj-content"><span class="meta">Loading guide...</span></div>
      </div>
    </div>
  </div>

  <div class="row">
    <div class="section" id="control-section">
      <h2>Control Docs</h2>
      <div id="control-meta" class="meta">Loading control docs...</div>
      <div id="control-docs-list" class="catalog-list"><span class="meta">Loading...</span></div>
    </div>

    <div class="section" id="subagent-section">
      <h2>Subagents <span id="subagent-variant-badge" class="badge variant" style="display:none"></span></h2>
      <div id="subagent-summary" class="meta">Loading subagent catalog...</div>
      <div id="subagent-report-req" class="pill-row"></div>
      <div id="subagent-cards" class="subagent-list"><span class="meta">Loading...</span></div>
    </div>
  </div>

  <div class="section" id="kickoff-section">
    <h2>Kickoff Handoff</h2>
    <div id="kickoff-summary" class="meta">Loading kickoff packet...</div>
    <div class="row">
      <div class="guide-block">
        <h3>Kickoff File Set</h3>
        <div id="kickoff-files" class="handoff-list"><span class="meta">Loading...</span></div>
      </div>
      <div class="guide-block">
        <h3>Stage Startup Checklist</h3>
        <div id="kickoff-checklist" class="handoff-list"><span class="meta">Loading...</span></div>
      </div>
    </div>
    <div id="kickoff-last-project" class="handoff-card" style="margin-top:10px"></div>
    <div class="guide-block" style="margin-top:12px">
      <h3>Recent Projects</h3>
      <div id="recent-projects" class="recent-projects"><span class="meta">No recent projects yet.</span></div>
    </div>
  </div>

  <div class="section" id="uj-execution-section">
    <h2>USERJOURNEY Execution</h2>
    <div id="uj-exec-summary" class="meta">Loading execution tracker...</div>
    <div class="mini-form">
      <div>
        <label>Phase</label>
        <select id="uj-phase-select"></select>
      </div>
      <div>
        <label>Status</label>
        <select id="uj-phase-status">
          <option>Planned</option>
          <option>In Progress</option>
          <option>Blocked</option>
          <option>Completed</option>
        </select>
      </div>
      <div>
        <label>Blockers</label>
        <input id="uj-phase-blockers" placeholder="unresolved open questions">
      </div>
      <div>
        <button class="btn primary" onclick="updateUserJourneyPhase()">Save Phase</button>
      </div>
    </div>
    <div class="mini-form">
      <div>
        <label>Current Slice</label>
        <select id="uj-slice-select"></select>
      </div>
      <div>
        <label>Status</label>
        <select id="uj-slice-status">
          <option>Pending</option>
          <option>Selected</option>
          <option>Ready</option>
          <option>Blocked</option>
          <option>Completed</option>
        </select>
      </div>
      <div>
        <label>Notes</label>
        <input id="uj-slice-note" placeholder="why this slice is current, ready, or blocked">
      </div>
      <div>
        <button class="btn ghost" onclick="updateUserJourneySlice()">Save Slice</button>
      </div>
    </div>
    <div class="exec-grid">
      <div class="guide-block">
        <h3>Phase Overview</h3>
        <div id="uj-phase-overview" class="table-ish"><span class="meta">Loading...</span></div>
      </div>
      <div class="guide-block">
        <h3>Current Slice Path</h3>
        <div id="uj-slice-focus" class="catalog-list"><span class="meta">Loading...</span></div>
      </div>
    </div>
    <div class="exec-grid" style="margin-top:12px">
      <div class="guide-block">
        <h3>File Review Targets</h3>
        <div id="uj-file-review" class="catalog-list"><span class="meta">Loading...</span></div>
      </div>
      <div class="guide-block">
        <h3>Critical Risks</h3>
        <div id="uj-risks" class="catalog-list"><span class="meta">Loading...</span></div>
      </div>
    </div>
  </div>

  <div class="section" id="drift-section">
    <h2>Sync And Drift</h2>
    <div id="drift-summary" class="meta">Loading drift summary...</div>
    <div class="exec-grid">
      <div class="guide-block">
        <h3>Violations And Notes</h3>
        <div id="drift-violations" class="catalog-list"><span class="meta">Loading...</span></div>
      </div>
      <div class="guide-block">
        <h3>Changed Files</h3>
        <div id="drift-files" class="catalog-list"><span class="meta">Loading...</span></div>
      </div>
    </div>
    <div class="guide-block" style="margin-top:12px">
      <h3>Sync Rules</h3>
      <div id="drift-rules" class="catalog-list"><span class="meta">Loading...</span></div>
    </div>
  </div>

  <!-- Command output -->
  <div class="section">
    <h2>Command Output</h2>
    <div class="terminal-bar">
      <span class="label" id="cmd-label">Ready</span>
      <div id="cmd-spinner" class="spinner"></div>
      <button class="btn ghost" onclick="clearOutput()">Clear</button>
      <button class="btn success" onclick="preflightCheck()">Pre-flight Check</button>
      <button class="btn ghost" onclick="runCmd('validate')">Validate</button>
      <button class="btn ghost" onclick="runCmd('smoke.dashboard')">Smoke</button>
      <button class="btn ghost" onclick="runCmd('smoke.browser')">Browser</button>
      <button class="btn ghost" onclick="runCmd('validate.workflow-state')">State Check</button>
      <button class="btn ghost" onclick="runCmd('drift')">Drift</button>
      <button class="btn ghost" onclick="runCmd('status')">Status</button>
      <button class="btn ghost" onclick="runCmd('log')">Log</button>
      <button class="btn ghost" onclick="runCmd('progress')">Progress</button>
    </div>
    <div id="output" class="terminal hidden"></div>
  </div>
</main>

<div id="doc-preview" class="doc-preview hidden">
  <div class="doc-preview-header">
    <div id="doc-preview-title" class="doc-preview-title">Document preview</div>
    <button class="btn ghost" id="doc-preview-open">Open</button>
    <button class="btn ghost" onclick="closeDocPreview()">Close</button>
  </div>
  <div id="doc-preview-meta" class="meta" style="padding:8px 14px 0 14px"></div>
  <div id="doc-preview-body" class="doc-preview-body">Loading...</div>
</div>

<!-- Advance modal -->
<div id="advance-modal" class="modal-overlay hidden">
  <div class="modal">
    <h3 id="modal-title">Advance Stage</h3>
    <p class="meta" id="modal-desc">This will mark the active step as completed and move the next step to in_progress.</p>
    <div id="modal-preflight" style="margin:8px 0;font-size:11px;color:var(--dim)"></div>
    <label>Decision</label>
    <input id="modal-decision" value="approved" placeholder="approved, hold, blocked">
    <label>Date</label>
    <input id="modal-date" value="2026-03-27" placeholder="YYYY-MM-DD">
    <label>Notes (optional)</label>
    <textarea id="modal-notes" placeholder="Why is this stage being completed?"></textarea>
    <div id="modal-history-section" style="display:none;margin-top:8px">
      <label>Signoff History</label>
      <div id="modal-history" style="font-size:11px;max-height:110px;overflow-y:auto;background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:6px 8px;color:var(--dim)"></div>
    </div>
    <div class="modal-actions">
      <button class="btn ghost" onclick="closeAdvanceModal()">Cancel</button>
      <button class="btn warning" id="modal-dry-btn" onclick="dryRunFromModal()">Dry-run</button>
      <button class="btn primary" id="modal-confirm-btn" onclick="confirmAdvanceFromModal()">Advance</button>
    </div>
  </div>
</div>

<!-- Bootstrap / New Project modal -->
<div id="bootstrap-modal" class="modal-overlay hidden">
  <div class="modal" style="width:500px;max-width:95vw">
    <h3>New Project</h3>
    <p class="meta" style="margin-bottom:10px">Bootstrap a fresh planning package into a new folder. This workspace stays as the template.</p>
    <label>Project name</label>
    <input id="bs-name" placeholder="MyNewApp" autocomplete="off" oninput="bsNameChanged(this)">
    <label>Destination folder</label>
    <input id="bs-dest" placeholder="C:\Projects\MyNewApp" autocomplete="off" oninput="this.dataset.manual='1';document.getElementById('bs-create-btn').disabled=true">
    <label style="display:block;margin-top:10px">Variant</label>
    <div style="display:flex;flex-direction:column;gap:3px;margin-top:5px">
      <label class="variant-opt"><input type="radio" name="bsVariant" value="lite"> <strong>lite</strong> <span class="meta">solo / quick idea validation</span></label>
      <label class="variant-opt"><input type="radio" name="bsVariant" value="product" checked> <strong>product</strong> <span class="meta">standard full build</span></label>
      <label class="variant-opt"><input type="radio" name="bsVariant" value="enterprise"> <strong>enterprise</strong> <span class="meta">full + audit trail + compliance track</span></label>
    </div>
    <label class="variant-opt" style="margin-top:10px">
      USERJOURNEY is attached separately only when the project needs onboarding, consent, activation, or first-run routing.
    </label>
    <div id="bs-preview-wrap" style="display:none;margin-top:10px">
      <div class="guide-label">Dry-run preview</div>
      <div id="bs-preview-out" class="terminal" style="max-height:180px;margin-top:4px;font-size:10px;line-height:1.4"></div>
    </div>
    <div class="modal-actions">
      <button class="btn ghost" onclick="closeBootstrapModal()">Cancel</button>
      <button class="btn warning" onclick="previewBootstrap()">Dry-run Preview</button>
      <button class="btn primary" id="bs-create-btn" onclick="createProject()" disabled>Create Project</button>
    </div>
  </div>
</div>

<script>
// ROOT injected server-side, safe const
const ROOT = '__ROOT__';
let _advanceSystem = null;
let _cmdQueue = Promise.resolve(); // serialise commands to avoid race conditions
let _cachedState = null;
let _subagentMap = {};
let _docPreviewPath = null;
let _advanceMode = 'advance';

function getRecentProjects() {
  return JSON.parse(localStorage.getItem('programstartRecentProjects') || '[]');
}

function setRecentProjects(items) {
  localStorage.setItem('programstartRecentProjects', JSON.stringify(items));
}

function currentStepEntry(system) {
  const sys = _cachedState?.[system];
  if (!sys) return null;
  return { step: sys.active, entry: sys.entries?.[sys.active] || {} };
}

function sliceStatusBadge(status) {
  const value = String(status || 'Pending');
  if (value === 'Ready' || value === 'Completed') return `<span class="badge ok">${esc(value)}</span>`;
  if (value === 'Blocked') return `<span class="badge blocker">${esc(value)}</span>`;
  return `<span class="badge active">${esc(value)}</span>`;
}

function getActiveProject() {
  const projects = getRecentProjects();
  const activeDest = localStorage.getItem('programstartActiveProjectDest');
  return projects.find((item) => item.dest === activeDest) || projects[0] || null;
}

function addRecentProject(project) {
  const existing = getRecentProjects().filter((item) => item.dest !== project.dest);
  const next = [project, ...existing].slice(0, 8);
  setRecentProjects(next);
  localStorage.setItem('programstartActiveProjectDest', project.dest);
}

// ── State loading ──────────────────────────────────────────────────
async function loadAll() {
  try {
    const r = await fetch('/api/state');
    const data = await r.json();
    if (data.error) { console.error(data.error); return; }
    _cachedState = data;
    renderSystem('pb', data.programbuild);
    renderSystem('uj', data.userjourney);
    renderControlDocs(data.catalog, data.programbuild);
    renderSubagents(data.catalog, data.programbuild);
    renderKickoffHandoff(data.catalog, data.programbuild);
    renderUserJourneyExecution(data.catalog);
    renderDriftDashboard(data.catalog);
    // Status bar
    document.getElementById('sb-pb').textContent = data.programbuild.active;
    document.getElementById('sb-uj').textContent = data.userjourney.attached ? data.userjourney.active : 'not attached';
    const oq = data.userjourney.attached ? (data.userjourney.open_questions || 0) : 0;
    const blockerEl = document.getElementById('sb-blockers');
    const ujBlockerBadge = document.getElementById('uj-blockers');
    if (!data.userjourney.attached) {
      blockerEl.innerHTML = `<span class="dot yellow"></span> USERJOURNEY optional and not attached`;
      ujBlockerBadge.style.display = 'none';
    } else if (oq > 0) {
      blockerEl.innerHTML = `<span class="dot red"></span> ${oq} external decision${oq>1?'s':''} unresolved`;
      ujBlockerBadge.textContent = `${oq} blocked decisions`;
      ujBlockerBadge.style.display = '';
    } else {
      blockerEl.innerHTML = `<span class="dot green"></span> No blockers`;
      ujBlockerBadge.style.display = 'none';
    }
    const now = new Date().toLocaleTimeString();
    document.getElementById('lastUpdated').textContent = now;
    document.getElementById('sb-updated').textContent = `Updated ${now}`;
    // Update status dots
    updateDot('dot-pb', data.programbuild);
    updateDot('dot-uj', data.userjourney);
  } catch (e) { console.error('loadAll failed', e); }
}

function updateDot(id, sys) {
  const el = document.getElementById(id);
  if (sys.completed === sys.total) el.className = 'dot green';
  else if (sys.blocked > 0) el.className = 'dot red';
  else el.className = 'dot yellow';
}

function renderSystem(prefix, sys) {
  const isPB = prefix === 'pb';
  if (!sys.attached && !isPB) {
    document.getElementById(`${prefix}-active`).textContent = 'Optional attachment not present';
    document.getElementById(`${prefix}-bar`).style.width = '0%';
    document.getElementById(`${prefix}-progress-label`).textContent = 'optional';
    document.getElementById(`${prefix}-steps`).innerHTML = '<div class="meta">Attach USERJOURNEY only for projects that need interactive onboarding, consent, activation, or first-run routing.</div>';
    return;
  }
  document.getElementById(`${prefix}-active`).textContent =
    (isPB ? 'Stage: ' : 'Phase: ') + sys.active;
  const pct = sys.total > 0 ? Math.round((sys.completed / sys.total) * 100) : 0;
  document.getElementById(`${prefix}-bar`).style.width = pct + '%';
  document.getElementById(`${prefix}-progress-label`).textContent =
    `${sys.completed}/${sys.total} (${pct}%)`;
  if (isPB && sys.variant) {
    document.getElementById('pb-variant').textContent = sys.variant;
  }
  const container = document.getElementById(`${prefix}-steps`);
  container.innerHTML = '';
  for (const step of sys.steps) {
    const entry = sys.entries[step] || {};
    const status = entry.status || 'planned';
    const isActive = step === sys.active;
    const signoff = entry.signoff || {};
    const desc = (sys.descriptions || {})[step] || '';
    const div = document.createElement('div');
    div.className = `step${isActive ? ' active' : ''}`;
    const dot = `<span class="step-dot ${status}"></span>`;
    let nameHtml = `<span class="step-name${isActive ? ' active' : ''}">${step}</span>`;
    if (desc) nameHtml += `<div class="step-desc">${esc(desc)}</div>`;
    let sig = '';
    if (signoff.decision && signoff.date) {
      sig = `<span class="step-signoff">${signoff.decision} · ${signoff.date}</span>`;
    }
    div.innerHTML = `${dot}<div class="step-body">${nameHtml}</div>${sig}`;
    container.appendChild(div);
  }
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function vscodeHref(absPath) {
  return `vscode://file/${encodeURIComponent(absPath.replace(/\\/g, '/'))}`;
}

function workspaceAbsPath(relativePath) {
  return ROOT.replace(/\\/g, '/') + '/' + relativePath;
}

function renderControlDocs(catalog, programbuild) {
  const list = document.getElementById('control-docs-list');
  const meta = document.getElementById('control-meta');
  const docs = catalog?.control_docs || [];
  meta.textContent = `${docs.length} recognized control docs. The current variant is ${programbuild.variant || 'product'}.`;
  list.innerHTML = '';
  for (const doc of docs) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    const isVariant = programbuild.variant && doc.name === `PROGRAMBUILD_${programbuild.variant.toUpperCase()}.md`;
    div.innerHTML = `
      <h3>${esc(doc.name)} ${isVariant ? '<span class="badge variant">active variant</span>' : ''}</h3>
      <p>${esc(doc.purpose || 'No purpose recorded.')}</p>
      <div class="catalog-meta">Canonical for: ${esc(doc.canonical_for || 'n/a')} · ${esc(doc.type || 'n/a')} · ${esc(doc.status || 'n/a')}</div>
      <div class="link-row">
        <button class="btn ghost" onclick="openDocPreview(${JSON.stringify(doc.file)})">Preview</button>
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath(doc.file))}">Open</a>
      </div>`;
    list.appendChild(div);
  }
}

function renderSubagents(catalog, programbuild) {
  const summary = document.getElementById('subagent-summary');
  const req = document.getElementById('subagent-report-req');
  const cards = document.getElementById('subagent-cards');
  const badge = document.getElementById('subagent-variant-badge');
  const subagents = catalog?.subagents || [];
  const variant = (programbuild.variant || 'product').toLowerCase();
  const stageRecs = catalog?.stage_subagents?.[programbuild.active] || [];
  const variantRecs = catalog?.variant_subagents?.[variant] || [];
  const variantOnly = catalog?.variant_only_subagents?.[variant] || [];
  const gate = catalog?.variant_gate_model?.[variant] || null;

  _subagentMap = Object.fromEntries(subagents.map((item) => [item.name, item]));
  badge.style.display = '';
  badge.textContent = `${variant} mode`;
  summary.textContent = gate
    ? `Current stage: ${programbuild.active}. ${variant} gates use ${gate.gate_style}. Evidence expectation: ${gate.evidence_expectation}`
    : `Current stage: ${programbuild.active}.`;

  req.innerHTML = '';
  for (const item of (catalog?.subagent_report_requirements || [])) {
    req.innerHTML += `<span class="pill dim">${esc(item)}</span>`;
  }

  cards.innerHTML = '';
  for (const agent of subagents) {
    const tags = [];
    if (stageRecs.includes(agent.name)) tags.push('<span class="pill rec">stage recommended</span>');
    if (variantRecs.includes(agent.name)) tags.push('<span class="pill variant">variant recommended</span>');
    const useItems = (agent.use_for || []).map((item) => `<li>${esc(item)}</li>`).join('');
    const div = document.createElement('div');
    div.className = 'subagent-card';
    div.innerHTML = `
      <h3>${esc(agent.name)}</h3>
      <div class="pill-row">${tags.join('')}</div>
      <p>${agent.use_for?.length ? 'Use for:' : 'No use-cases listed.'}</p>
      <ul class="catalog-meta" style="margin:6px 0 0 16px">${useItems}</ul>
      <details class="subagent-details">
        <summary>Show prompt</summary>
        <div class="terminal" style="max-height:160px;margin-top:8px">${esc(agent.prompt || 'No canonical prompt available.')}</div>
      </details>
      <div class="link-row">
        <button class="btn ghost" onclick='copySubagentPrompt(${JSON.stringify(agent.name)})'>Copy Prompt</button>
        <button class="btn ghost" onclick="openDocPreview('PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md')">Preview Catalog</button>
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath('PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md'))}">Open Catalog</a>
      </div>`;
    cards.appendChild(div);
  }

  for (const name of variantOnly) {
    const div = document.createElement('div');
    div.className = 'subagent-card';
    div.innerHTML = `
      <h3>${esc(name)}</h3>
      <div class="pill-row"><span class="pill variant">variant-only role</span></div>
      <p>This role is recommended by the ${esc(variant)} playbook, but there is no canonical prompt for it yet in PROGRAMBUILD_SUBAGENTS.md.</p>
      <div class="link-row">
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath(`PROGRAMBUILD/PROGRAMBUILD_${variant.toUpperCase()}.md`))}">Open Variant Playbook</a>
      </div>`;
    cards.appendChild(div);
  }
}

function kickoffProjectLinks(dest, variant) {
  const links = [
    { label: 'Canonical', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` },
    { label: 'File Index', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` },
    { label: 'Kickoff Packet', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md` },
    { label: 'Variant Playbook', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_${variant.toUpperCase()}.md` },
    { label: 'Feasibility', path: `${dest}/PROGRAMBUILD/FEASIBILITY.md` },
    { label: 'Decision Log', path: `${dest}/PROGRAMBUILD/DECISION_LOG.md` },
  ];
  return links;
}

function kickoffStartCommands(dest) {
  const safe = dest.replaceAll('"', '');
  return `cd "${safe}"\n.\\scripts\\pb.ps1 next\n.\\scripts\\pb.ps1 validate`;
}

function renderKickoffHandoff(catalog, programbuild) {
  const summary = document.getElementById('kickoff-summary');
  const files = document.getElementById('kickoff-files');
  const checklist = document.getElementById('kickoff-checklist');
  const lastProject = document.getElementById('kickoff-last-project');
  const activeProject = getActiveProject();
  const lastBootstrap = activeProject || JSON.parse(localStorage.getItem('programstartLastBootstrap') || 'null');
  const variant = (lastBootstrap?.variant || programbuild.variant || 'product').toLowerCase();
  const gate = catalog?.variant_gate_model?.[variant];
  const recentProjects = getRecentProjects();
  const recentEl = document.getElementById('recent-projects');

  summary.textContent = gate
    ? `After bootstrap, lock product shape, USERJOURNEY need, and variant first. Then start with canonical + file index + ${variant} playbook. ${variant} gates use ${gate.gate_style}.`
    : 'After bootstrap, lock product shape, USERJOURNEY need, and your chosen playbook before stage work.';

  files.innerHTML = '';
  for (const item of (catalog?.kickoff?.files || [])) {
    const div = document.createElement('div');
    div.className = 'handoff-card';
    const target = lastBootstrap ? `${lastBootstrap.dest}/PROGRAMBUILD/${item.replace(/\\/g, '/')}` : workspaceAbsPath(`PROGRAMBUILD/${item}`);
    div.innerHTML = `<h3>${esc(item)}</h3><div class="link-row"><button class="btn ghost" onclick="openDocPreview('PROGRAMBUILD/${item}')">Preview</button><a class="btn ghost" href="${vscodeHref(target)}">Open</a></div>`;
    files.appendChild(div);
  }

  checklist.innerHTML = '';
  const decisionRows = catalog?.kickoff?.decision_matrix || [];
  if (decisionRows.length) {
    const matrixRows = decisionRows.map((row) => `
      <tr>
        <td>${esc(row.Decision || '')}</td>
        <td>${esc(row['Choose this when'] || '')}</td>
        <td>${esc(row['Primary effect'] || '')}</td>
      </tr>`).join('');
    const matrixCard = document.createElement('div');
    matrixCard.className = 'handoff-card';
    matrixCard.innerHTML = `
      <h3>Kickoff Decision Matrix</h3>
      <details class="kickoff-details" open>
        <summary>Show decision matrix</summary>
        <div style="overflow:auto;margin-top:8px">
          <table class="data-table">
            <thead>
              <tr><th>Decision</th><th>Choose this when</th><th>Primary effect</th></tr>
            </thead>
            <tbody>${matrixRows}</tbody>
          </table>
        </div>
      </details>`;
    checklist.appendChild(matrixCard);
  }
  for (const section of (catalog?.kickoff?.startup_sections || [])) {
    const div = document.createElement('div');
    div.className = 'handoff-card';
    const items = (section.items || []).map((item) => `<li>${esc(item)}</li>`).join('');
    div.innerHTML = `
      <h3>${esc(section.title)}</h3>
      <details class="kickoff-details" open>
        <summary>Show checklist</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${items}</ul>
      </details>`;
    checklist.appendChild(div);
  }

  if (!lastBootstrap) {
    const preflight = (catalog?.kickoff?.preflight || []).map((item) => `<li>${esc(item)}</li>`).join('');
    lastProject.innerHTML = `
      <h3>No recent bootstrap in this browser</h3>
      <p>Use <span class="inline-code">+ New Project</span>, then come back here for the first documents and startup checklist.</p>
      <details class="kickoff-details" open>
        <summary>Pre-bootstrap requirements</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${preflight}</ul>
      </details>`;
    recentEl.innerHTML = '<span class="meta">No recent projects yet.</span>';
    return;
  }

  const links = kickoffProjectLinks(lastBootstrap.dest.replace(/\\/g, '/'), lastBootstrap.variant)
    .map((item) => `<a class="btn ghost" href="${vscodeHref(item.path)}">${esc(item.label)}</a>`)
    .join('');
  const startCommands = kickoffStartCommands(lastBootstrap.dest);
  lastProject.innerHTML = `
    <h3>Last Bootstrap: ${esc(lastBootstrap.project_name)}</h3>
    <p>Destination: <span class="inline-code">${esc(lastBootstrap.dest)}</span></p>
    <div class="pill-row">
      <span class="pill variant">${esc(lastBootstrap.variant)}</span>
      <span class="pill dim">USERJOURNEY attach separately if needed</span>
      <span class="pill dim">${esc(new Date(lastBootstrap.created_at).toLocaleString())}</span>
    </div>
    <div class="link-row">
      <a class="btn primary" href="${vscodeHref(lastBootstrap.dest.replace(/\\/g, '/'))}">Open Project Folder</a>
      <button class="btn ghost" onclick='copyText(${JSON.stringify(startCommands)}, "Starter commands copied")'>Copy Starter Commands</button>
      <button class="btn ghost" onclick='showStarterCommands(${JSON.stringify(startCommands)})'>Show Starter Commands</button>
    </div>
    <div class="link-row">${links}</div>
    <div class="launcher-grid">
      <div class="launcher-card">
        <h4>Start Here</h4>
        <p>Open Canonical, File Index, Kickoff Packet, and your variant playbook first. Then run <span class="inline-code">pb next</span> inside the new project.</p>
      </div>
      <div class="launcher-card">
        <h4>First Commands</h4>
        <div class="terminal" style="max-height:100px">${esc(startCommands)}</div>
      </div>
    </div>`;

  recentEl.innerHTML = '';
  for (const project of recentProjects) {
    const active = project.dest === lastBootstrap.dest;
    const div = document.createElement('div');
    div.className = 'recent-project';
    div.innerHTML = `
      <div class="title">${esc(project.project_name)} ${active ? '<span class="badge active">active</span>' : ''}</div>
      <div class="path">${esc(project.dest)}</div>
      <button class="btn ghost" onclick='selectRecentProject(${JSON.stringify(project.dest)})'>Select</button>
      <a class="btn ghost" href="${vscodeHref(project.dest.replace(/\\/g, '/'))}">Open</a>
      <button class="btn ghost" onclick='removeRecentProject(${JSON.stringify(project.dest)})'>Remove</button>`;
    recentEl.appendChild(div);
  }
}

function renderUserJourneyExecution(catalog) {
  const summary = document.getElementById('uj-exec-summary');
  const phaseOverview = document.getElementById('uj-phase-overview');
  const sliceFocus = document.getElementById('uj-slice-focus');
  const fileReview = document.getElementById('uj-file-review');
  const risks = document.getElementById('uj-risks');
  const phaseSelect = document.getElementById('uj-phase-select');
  const phaseStatus = document.getElementById('uj-phase-status');
  const phaseBlockers = document.getElementById('uj-phase-blockers');
  const sliceSelect = document.getElementById('uj-slice-select');
  const sliceStatus = document.getElementById('uj-slice-status');
  const sliceNote = document.getElementById('uj-slice-note');
  const exec = catalog?.userjourney_execution || {};
  if (!exec.attached) {
    summary.textContent = 'USERJOURNEY is not attached. This workspace is operating in PROGRAMBUILD-only mode.';
    phaseOverview.innerHTML = '<div class="catalog-item"><p>No USERJOURNEY execution data. Attach it only for interactive end-user products.</p></div>';
    sliceFocus.innerHTML = '';
    fileReview.innerHTML = '';
    risks.innerHTML = '';
    phaseSelect.innerHTML = '';
    sliceSelect.innerHTML = '';
    phaseStatus.value = 'Planned';
    phaseBlockers.value = '';
    sliceStatus.value = 'Pending';
    sliceNote.value = '';
    return;
  }
  const phases = exec.phase_overview || [];
  const sliceReadiness = exec.slice_readiness || [];
  const slices = exec.slice_sections || [];
  const mappings = exec.slice_mapping || [];
  const files = exec.file_sections || [];
  const phase0 = phases.find((row) => String(row.Phase || '').trim() === '0') || phases[0];
  const currentSliceRow = sliceReadiness.find((row) => ['Selected', 'Ready', 'Blocked'].includes(String(row.Status || '').trim())) || sliceReadiness[0];
  const currentSliceName = String(currentSliceRow?.Slice || 'Slice 1');
  const slice1 = slices.find((row) => row.title.startsWith(`${currentSliceName}:`)) || slices[0];
  const map1 = mappings.find((row) => String(row.Slice || '').trim() === currentSliceName) || mappings[0];

  summary.textContent = phase0
    ? `Current planning phase: ${phase0.Phase} (${phase0.Status}). Current slice: ${currentSliceName} (${String(currentSliceRow?.Status || 'Pending')}).`
    : 'Execution data loaded.';

  phaseSelect.innerHTML = phases.map((row) => `<option value="${esc(String(row.Phase || ''))}">Phase ${esc(String(row.Phase || ''))}</option>`).join('');
  if (phase0) {
    phaseSelect.value = String(phase0.Phase || '0');
    phaseStatus.value = String(phase0.Status || 'Planned');
    phaseBlockers.value = String(phase0.Blockers || '');
  }
  const sliceOptions = sliceReadiness.length
    ? sliceReadiness.map((row) => String(row.Slice || ''))
    : slices.map((row) => row.title.split(':')[0]);
  sliceSelect.innerHTML = sliceOptions.map((name) => `<option value="${esc(name)}">${esc(name)}</option>`).join('');
  sliceSelect.value = currentSliceName;
  sliceStatus.value = String(currentSliceRow?.Status || 'Pending');
  sliceNote.value = String(currentSliceRow?.Notes || '');

  phaseOverview.innerHTML = '';
  for (const row of phases.slice(0, 5)) {
    const div = document.createElement('div');
    div.className = 'table-row phase';
    div.innerHTML = `
      <div><div class="label">Phase</div><div class="value">${esc(String(row.Phase || ''))}</div></div>
      <div><div class="label">Status</div><div class="value">${esc(String(row.Status || ''))}</div></div>
      <div><div class="label">Goal</div><div class="value">${esc(String(row.Goal || ''))}</div></div>
      <div><div class="label">Exit Gate</div><div class="value">${esc(String(row['Exit Gate'] || ''))}</div></div>`;
    phaseOverview.appendChild(div);
  }

  sliceFocus.innerHTML = '';
  if (slice1) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(slice1.title)} ${sliceStatusBadge(currentSliceRow?.Status || 'Pending')}</h3>
      <p>${esc(slice1.outcome || '')}</p>
      <div class="catalog-meta">Primary risk: ${esc(slice1.risk || 'n/a')}</div>
      <div class="catalog-meta">Readiness gate: ${esc(String(currentSliceRow?.['Readiness Gate'] || 'n/a'))}</div>
      <div class="catalog-meta">Notes: ${esc(String(currentSliceRow?.Notes || '')) || 'none'}</div>
      <details class="doc-details" open>
        <summary>Show scope and tests</summary>
        <div class="pill-row">${(slice1.scope || []).map((item) => `<span class="pill">${esc(item)}</span>`).join('')}</div>
        <div class="pill-row">${(slice1.test_scope || []).map((item) => `<span class="pill dim">${esc(item)}</span>`).join('')}</div>
      </details>
    `;
    sliceFocus.appendChild(div);
  }
  if (map1) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>First File Review Path</h3>
      <p>${esc(String(map1['Primary Files To Review First'] || ''))}</p>
      <div class="link-row">
        <button class="btn ghost" onclick="openDocPreview('USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md')">Preview Checklist</button>
        <button class="btn ghost" onclick="openDocPreview('USERJOURNEY/EXECUTION_SLICES.md')">Preview Slices</button>
      </div>`;
    sliceFocus.appendChild(div);
  }

  fileReview.innerHTML = '';
  for (const section of files.slice(0, 4)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(section.file)}</h3>
      <div class="catalog-meta">${esc(section.status || 'Status unknown')}</div>
      <details class="doc-details">
        <summary>Show checks</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${(section.items || []).map((item) => `<li>${esc(item)}</li>`).join('')}</ul>
      </details>`;
    fileReview.appendChild(div);
  }

  risks.innerHTML = '';
  for (const row of (exec.critical_risks || []).slice(0, 4)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(String(row.Risk || 'Risk'))}</h3>
      <div class="catalog-meta">Severity: ${esc(String(row.Severity || 'n/a'))}</div>
      <p>${esc(String(row['Why It Matters'] || ''))}</p>
      <details class="doc-details"><summary>Mitigation</summary><div class="catalog-meta">${esc(String(row.Mitigation || ''))}</div></details>`;
    risks.appendChild(div);
  }
}

function renderDriftDashboard(catalog) {
  const summary = document.getElementById('drift-summary');
  const violationsEl = document.getElementById('drift-violations');
  const filesEl = document.getElementById('drift-files');
  const rulesEl = document.getElementById('drift-rules');
  const drift = catalog?.drift || { violations: [], notes: [], changed_files: [], sync_rules: [], status: 'passed' };

  summary.textContent = drift.status === 'failed'
    ? `${drift.violations.length} drift violation(s) detected across ${drift.changed_files.length} changed file(s).`
    : `Drift check currently passes. ${drift.changed_files.length} changed file(s) in the workspace.`;

  violationsEl.innerHTML = '';
  for (const item of [...(drift.violations || []), ...(drift.notes || [])]) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `<p>${esc(item)}</p>`;
    violationsEl.appendChild(div);
  }
  if (!violationsEl.innerHTML) {
    violationsEl.innerHTML = '<div class="catalog-item"><p>No sync notes or violations right now.</p></div>';
  }

  filesEl.innerHTML = '';
  for (const file of (drift.changed_files || [])) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `<h3>${esc(file)}</h3><div class="link-row"><button class="btn ghost" onclick="openDocPreview(${JSON.stringify(file)})">Preview</button><a class="btn ghost" href="${vscodeHref(workspaceAbsPath(file))}">Open</a></div>`;
    filesEl.appendChild(div);
  }
  if (!filesEl.innerHTML) {
    filesEl.innerHTML = '<div class="catalog-item"><p>No changed files detected.</p></div>';
  }

  rulesEl.innerHTML = '';
  for (const rule of (drift.sync_rules || []).slice(0, 6)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(rule.name)}</h3>
      <div class="catalog-meta">system: ${esc(rule.system || 'n/a')}</div>
      <div class="pill-row">
        ${(rule.touched_authority || []).map((item) => `<span class="pill">authority: ${esc(item)}</span>`).join('')}
        ${(rule.touched_dependents || []).map((item) => `<span class="pill dim">dependent: ${esc(item)}</span>`).join('')}
      </div>`;
    rulesEl.appendChild(div);
  }
  if (!rulesEl.innerHTML) {
    rulesEl.innerHTML = '<div class="catalog-item"><p>No sync rules recorded.</p></div>';
  }
}

async function updateUserJourneyPhase() {
  const phase = document.getElementById('uj-phase-select').value;
  const status = document.getElementById('uj-phase-status').value;
  const blockers = document.getElementById('uj-phase-blockers').value;
  const r = await fetch('/api/uj-phase', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({phase, status, blockers}),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  document.getElementById('cmd-label').textContent = result.exit_code === 0 ? 'USERJOURNEY phase updated' : 'USERJOURNEY phase update failed';
  if (result.exit_code === 0) await loadAll();
}

async function updateUserJourneySlice() {
  const slice = document.getElementById('uj-slice-select').value;
  const status = document.getElementById('uj-slice-status').value;
  const notes = document.getElementById('uj-slice-note').value;
  const r = await fetch('/api/uj-slice', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({slice, status, notes}),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  document.getElementById('cmd-label').textContent = result.exit_code === 0 ? 'USERJOURNEY slice updated' : 'USERJOURNEY slice update failed';
  if (result.exit_code === 0) await loadAll();
}

async function postWorkflowAction(path, body, successLabel, failureLabel) {
  const r = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  document.getElementById('cmd-label').textContent = result.exit_code === 0 ? successLabel : failureLabel;
  if (result.exit_code === 0 && !body.dry_run) {
    await loadAll();
    await _runCmdImpl('guide.programbuild');
    await _runCmdImpl('guide.userjourney');
  }
  return result;
}

function selectRecentProject(dest) {
  localStorage.setItem('programstartActiveProjectDest', dest);
  if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
}

function removeRecentProject(dest) {
  const next = getRecentProjects().filter((item) => item.dest !== dest);
  setRecentProjects(next);
  if (localStorage.getItem('programstartActiveProjectDest') === dest) {
    localStorage.setItem('programstartActiveProjectDest', next[0]?.dest || '');
  }
  if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
}

async function copySubagentPrompt(name) {
  const prompt = _subagentMap[name]?.prompt || '';
  if (!prompt) return;
  await copyText(prompt, `${name} prompt copied`, `Clipboard blocked for ${name}`);
}

async function copyText(text, okLabel, failLabel = 'Clipboard blocked') {
  try {
    await navigator.clipboard.writeText(text);
    document.getElementById('cmd-label').textContent = okLabel;
  } catch {
    document.getElementById('cmd-label').textContent = failLabel;
  }
}

function showStarterCommands(text) {
  const out = document.getElementById('output');
  out.className = 'terminal success';
  out.textContent = text;
  document.getElementById('cmd-label').textContent = 'Starter commands';
}

async function openDocPreview(relativePath) {
  const panel = document.getElementById('doc-preview');
  const title = document.getElementById('doc-preview-title');
  const meta = document.getElementById('doc-preview-meta');
  const body = document.getElementById('doc-preview-body');
  const openBtn = document.getElementById('doc-preview-open');
  _docPreviewPath = relativePath;
  panel.className = 'doc-preview';
  title.textContent = relativePath;
  meta.textContent = 'Loading preview...';
  body.textContent = '';
  openBtn.onclick = () => window.open(vscodeHref(workspaceAbsPath(relativePath)), '_self');
  const r = await fetch(`/api/doc?path=${encodeURIComponent(relativePath)}`);
  const result = await r.json();
  if (result.error) {
    meta.textContent = result.error;
    body.textContent = '';
    return;
  }
  meta.textContent = `${result.line_count} lines${result.truncated ? ' · preview truncated to first 220 lines' : ''}`;
  body.textContent = result.content || '(empty file)';
}

function closeDocPreview() {
  document.getElementById('doc-preview').className = 'doc-preview hidden';
  _docPreviewPath = null;
}

// ── Command execution (serialised) ─────────────────────────────────
function runCmd(key, extraArgs) {
  _cmdQueue = _cmdQueue.then(() => _runCmdImpl(key, extraArgs));
  return _cmdQueue;
}

async function _runCmdImpl(key, extraArgs) {
  const label = document.getElementById('cmd-label');
  const spinner = document.getElementById('cmd-spinner');
  const out = document.getElementById('output');
  label.textContent = `Running: ${key}`;
  spinner.className = 'spinner active';
  out.className = 'terminal';
  out.textContent = '';
  const body = {command: key};
  if (extraArgs) body.args = extraArgs;
  try {
    const r = await fetch('/api/run', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    const result = await r.json();
    spinner.className = 'spinner';
    const ok = result.exit_code === 0;
    label.textContent = `${key} — ${ok ? 'OK' : 'FAILED (exit ' + result.exit_code + ')'}`;
    out.textContent = result.output || '(no output)';
    out.className = `terminal ${ok ? 'success' : 'error'}`;
    out.scrollTop = out.scrollHeight;

    // Parse guide output into guide panels
    if (key === 'guide.programbuild') renderGuide('pb', result.output);
    if (key === 'guide.userjourney') renderGuide('uj', result.output);

    // After a real advance: refresh state + guides + regenerate dashboard
    if (key.startsWith('advance.') && !key.endsWith('.dry') && ok) {
      await loadAll();
      await _runCmdImpl('guide.programbuild');
      await _runCmdImpl('guide.userjourney');
      // Fire dashboard regen silently
      fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:'dashboard'})});
    }
    return result;
  } catch (e) {
    spinner.className = 'spinner';
    label.textContent = `${key} — ERROR`;
    out.textContent = 'Network error: ' + e.message;
    out.className = 'terminal error';
    return {output: e.message, exit_code: -1};
  }
}

function renderGuide(prefix, raw) {
  const titleEl = document.getElementById(`guide-${prefix}-title`);
  const descEl = document.getElementById(`guide-${prefix}-desc`);
  const contentEl = document.getElementById(`guide-${prefix}-content`);
  const lines = (raw || '').split('\n');

  // First line is the title (e.g., "PROGRAMBUILD Stage: inputs_and_mode_selection")
  titleEl.textContent = lines[0] || (prefix === 'pb' ? 'PROGRAMBUILD' : 'USERJOURNEY');

  // Look up description from cached state
  const sys = prefix === 'pb' ? 'programbuild' : 'userjourney';
  if (_cachedState && _cachedState[sys]) {
    const d = (_cachedState[sys].descriptions || {})[_cachedState[sys].active] || '';
    if (d) { descEl.textContent = d; descEl.style.display = ''; }
    else { descEl.style.display = 'none'; }
  }

  let html = '';
  let inSection = false;
  for (const line of lines.slice(1)) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.endsWith(':') && !trimmed.startsWith('-')) {
      if (inSection) html += '</div>';
      const sectionName = trimmed.slice(0, -1);
      html += `<div class="guide-label">${esc(sectionName)}</div><div class="guide-items">`;
      inSection = true;
    } else if (trimmed.startsWith('- ') && inSection) {
      const val = trimmed.slice(2);
      let display = val;
      // Make file paths clickable vscode:// links
      if (val.match(/\.(md|json|py|ps1|yml|yaml|txt)$/i)) {
        const absPath = ROOT.replace(/\\/g, '/') + '/' + val;
        display = `<a href="vscode://file/${encodeURIComponent(absPath)}" title="Open in VS Code">${esc(val)}</a>`;
      } else {
        display = esc(val);
      }
      html += `<div class="guide-item">${display}</div>`;
    }
  }
  if (inSection) html += '</div>';
  contentEl.innerHTML = html || `<span class="meta">No guide data</span>`;
}

// ── Pre-flight check (validate + drift + state-check) ─────────────
async function preflightCheck() {
  const out = document.getElementById('output');
  const label = document.getElementById('cmd-label');
  const spinner = document.getElementById('cmd-spinner');
  out.className = 'terminal';
  out.textContent = '';
  label.textContent = 'Pre-flight: validate → state-check → drift...';
  spinner.className = 'spinner active';

  let allOutput = '';
  let allOk = true;
  for (const cmd of ['validate', 'validate.workflow-state', 'drift']) {
    const body = {command: cmd};
    const r = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
    const result = await r.json();
    const ok = result.exit_code === 0;
    allOutput += `━━━ ${cmd} ${ok ? '✓' : '✗'} ━━━\n${result.output}\n\n`;
    if (!ok) allOk = false;
  }
  spinner.className = 'spinner';
  label.textContent = allOk ? 'Pre-flight: ALL PASSED' : 'Pre-flight: ISSUES FOUND';
  out.textContent = allOutput.trim();
  out.className = `terminal ${allOk ? 'success' : 'error'}`;
  out.scrollTop = out.scrollHeight;
}

// ── Advance modal ──────────────────────────────────────────────────
function openAdvanceModal(system, mode = 'advance') {
  _advanceSystem = system;
  _advanceMode = mode;
  const label = system === 'programbuild' ? 'Stage' : 'Phase';
  const current = currentStepEntry(system);
  const signoff = current?.entry?.signoff || {};
  document.getElementById('modal-title').textContent = mode === 'advance'
    ? `Advance ${system.toUpperCase()} ${label}`
    : `Save ${system.toUpperCase()} ${label} Signoff`;
  document.getElementById('modal-desc').textContent = mode === 'advance'
    ? 'This will mark the active step as completed and move the next step to in_progress.'
    : 'This will save signoff metadata for the active step without advancing the workflow.';
  document.getElementById('modal-decision').value = signoff.decision || 'approved';
  document.getElementById('modal-date').value = signoff.date || new Date().toISOString().slice(0, 10);
  document.getElementById('modal-notes').value = signoff.notes || '';
  // Populate signoff history
  const history = current?.entry?.signoff_history || [];
  const histSection = document.getElementById('modal-history-section');
  const histDiv = document.getElementById('modal-history');
  if (history.length > 0) {
    histDiv.innerHTML = history.slice().reverse().map((h) => {
      const decision = esc(h.decision || '\u2014');
      const dt = esc(h.date || '\u2014');
      const saved = esc(h.saved_at || '');
      const noteHtml = h.notes ? `<div style="font-size:10px;margin-top:2px;white-space:pre-wrap">${esc(h.notes)}</div>` : '';
      return `<div style="padding:3px 0;border-bottom:1px solid var(--border)">
        <span style="color:var(--text);font-weight:500">${decision}</span>
        &middot; <span>${dt}</span>
        ${saved ? `<span style="color:var(--dim)"> (saved ${saved})</span>` : ''}
        ${noteHtml}</div>`;
    }).join('');
    histSection.style.display = '';
  } else {
    histSection.style.display = 'none';
  }
  document.getElementById('modal-preflight').innerHTML = '';
  document.getElementById('advance-modal').className = 'modal-overlay';
  document.getElementById('modal-dry-btn').style.display = mode === 'advance' ? '' : 'none';
  document.getElementById('modal-confirm-btn').textContent = mode === 'advance' ? 'Advance' : 'Save Signoff';

  (async () => {
    const pf = document.getElementById('modal-preflight');
    if (mode !== 'advance') {
      pf.innerHTML = current ? `Active ${label.toLowerCase()}: ${esc(current.step)}` : 'No cached workflow state loaded yet.';
      document.getElementById('modal-confirm-btn').disabled = false;
      return;
    }
    pf.innerHTML = '<span style="color:var(--dim)">Running pre-flight (validate + state check)...</span>';
    let checks = [];
    for (const cmd of ['validate.workflow-state', `advance.${system}.dry`]) {
      const r = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:cmd})});
      const result = await r.json();
      const ok = result.exit_code === 0;
      checks.push({cmd, ok, output: result.output});
    }
    const allOk = checks.every(c => c.ok);
    let html = '';
    for (const c of checks) {
      const icon = c.ok ? `<span style="color:var(--green)">✓</span>` : `<span style="color:var(--red)">✗</span>`;
      html += `<div>${icon} ${esc(c.cmd)}: ${esc(c.output.split('\n')[0])}</div>`;
    }
    if (!allOk) html += `<div style="color:var(--red);margin-top:4px">Fix issues before advancing.</div>`;
    pf.innerHTML = html;
    document.getElementById('modal-confirm-btn').disabled = !allOk;
  })();
}

function closeAdvanceModal() {
  document.getElementById('advance-modal').className = 'modal-overlay hidden';
  _advanceSystem = null;
}

async function dryRunFromModal() {
  if (!_advanceSystem) return;
  const system = _advanceSystem;
  const decision = document.getElementById('modal-decision').value;
  const dateValue = document.getElementById('modal-date').value;
  const notes = document.getElementById('modal-notes').value;
  closeAdvanceModal();
  await postWorkflowAction(
    '/api/workflow-advance',
    {system, decision, date: dateValue, notes, dry_run: true},
    `${system} advance dry-run complete`,
    `${system} advance dry-run failed`,
  );
}

async function confirmAdvanceFromModal() {
  if (!_advanceSystem) return;
  const system = _advanceSystem;
  const decision = document.getElementById('modal-decision').value;
  const dateValue = document.getElementById('modal-date').value;
  const notes = document.getElementById('modal-notes').value;
  closeAdvanceModal();
  if (_advanceMode === 'signoff') {
    await postWorkflowAction(
      '/api/workflow-signoff',
      {system, decision, date: dateValue, notes},
      `${system} signoff saved`,
      `${system} signoff failed`,
    );
    return;
  }
  await postWorkflowAction(
    '/api/workflow-advance',
    {system, decision, date: dateValue, notes},
    `${system} advanced`,
    `${system} advance failed`,
  );
}

// ── Bootstrap / New Project modal ─────────────────────────────────
function openBootstrapModal() {
  document.getElementById('bs-name').value = '';
  const destEl = document.getElementById('bs-dest');
  destEl.value = '';
  delete destEl.dataset.manual;
  document.getElementById('bs-preview-wrap').style.display = 'none';
  document.getElementById('bs-create-btn').disabled = true;
  document.querySelector('input[name="bsVariant"][value="product"]').checked = true;
  document.getElementById('bootstrap-modal').className = 'modal-overlay';
  setTimeout(() => document.getElementById('bs-name').focus(), 50);
}

function bsNameChanged(input) {
  const name = input.value.trim();
  const dest = document.getElementById('bs-dest');
  if (!dest.dataset.manual && name) dest.value = `C:\\Projects\\${name}`;
  document.getElementById('bs-create-btn').disabled = true;
}

function closeBootstrapModal() {
  document.getElementById('bootstrap-modal').className = 'modal-overlay hidden';
}

function _getBootstrapParams(dryRun) {
  return {
    dest: document.getElementById('bs-dest').value.trim(),
    project_name: document.getElementById('bs-name').value.trim(),
    variant: document.querySelector('input[name="bsVariant"]:checked')?.value || 'product',
    dry_run: !!dryRun,
  };
}

async function previewBootstrap() {
  const wrap = document.getElementById('bs-preview-wrap');
  const out = document.getElementById('bs-preview-out');
  const createBtn = document.getElementById('bs-create-btn');
  wrap.style.display = '';
  out.textContent = 'Running dry-run...';
  out.className = 'terminal';
  createBtn.disabled = true;
  const r = await fetch('/api/bootstrap', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(_getBootstrapParams(true)),
  });
  const result = await r.json();
  out.textContent = result.output || '(no output)';
  const ok = result.exit_code === 0;
  out.className = `terminal ${ok ? 'success' : 'error'}`;
  createBtn.disabled = !ok;
}

async function createProject() {
  const params = _getBootstrapParams(false);
  closeBootstrapModal();
  const label = document.getElementById('cmd-label');
  const spinner = document.getElementById('cmd-spinner');
  const out = document.getElementById('output');
  label.textContent = `Creating: ${params.project_name}...`;
  spinner.className = 'spinner active';
  out.className = 'terminal';
  out.textContent = '';
  const r = await fetch('/api/bootstrap', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params),
  });
  const result = await r.json();
  spinner.className = 'spinner';
  const ok = result.exit_code === 0;
  label.textContent = ok ? `Project created: ${params.project_name}` : `Bootstrap failed (exit ${result.exit_code})`;
  out.textContent = result.output || '(no output)';
  if (ok) {
    const created = { ...params, created_at: new Date().toISOString() };
    localStorage.setItem('programstartLastBootstrap', JSON.stringify(created));
    addRecentProject(created);
    if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
    out.textContent += `\n\n─────\nDone! Open your new project in VS Code:\n  code "${params.dest}"\nThen start with Canonical, File Index, Kickoff Packet, and your chosen variant playbook.`;
  }
  out.className = `terminal ${ok ? 'success' : 'error'}`;
  out.scrollTop = out.scrollHeight;
}

function clearOutput() {
  const out = document.getElementById('output');
  out.className = 'terminal hidden';
  out.textContent = '';
  document.getElementById('cmd-label').textContent = 'Ready';
}

// ── Init ───────────────────────────────────────────────────────────
(async () => {
  await loadAll();
  // Load both guides sequentially (avoid racing for the output panel)
  await runCmd('guide.programbuild');
  await runCmd('guide.userjourney');
})();

// Auto-refresh state every 30s
setInterval(loadAll, 30000);
</script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the PROGRAMSTART dashboard."""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        code = args[1] if len(args) > 1 else "?"
        print(f"  {self.command} {self.path}  ->  {code}")

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str) -> None:
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            html = HTML.replace("'__ROOT__'", json.dumps(str(ROOT)))
            self._send_html(html)
        elif parsed.path == "/api/state":
            self._send_json(get_state_json())
        elif parsed.path == "/api/doc":
            query = parse_qs(parsed.query)
            path = query.get("path", [""])[0]
            data = get_doc_preview(path)
            self._send_json(data, 200 if "error" not in data else 400)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/uj-phase":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, Exception):
                self._send_json({"error": "invalid JSON body"}, 400)
                return
            result = update_implementation_tracker_phase(
                phase=str(body.get("phase", "")),
                status=str(body.get("status", "")),
                blockers=str(body.get("blockers", "")),
            )
            self._send_json(result, 200 if result.get("exit_code") == 0 else 400)
            return
        if parsed.path == "/api/uj-slice":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, Exception):
                self._send_json({"error": "invalid JSON body"}, 400)
                return
            result = update_implementation_tracker_slice(
                slice_name=str(body.get("slice", "")),
                status=str(body.get("status", "")),
                notes=str(body.get("notes", "")),
            )
            self._send_json(result, 200 if result.get("exit_code") == 0 else 400)
            return
        if parsed.path == "/api/workflow-signoff":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, Exception):
                self._send_json({"error": "invalid JSON body"}, 400)
                return
            result = save_workflow_signoff(
                system=str(body.get("system", "")),
                decision=str(body.get("decision", "")),
                signoff_date=str(body.get("date", "")),
                notes=str(body.get("notes", "")),
            )
            self._send_json(result, 200 if result.get("exit_code") == 0 else 400)
            return
        if parsed.path == "/api/workflow-advance":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, Exception):
                self._send_json({"error": "invalid JSON body"}, 400)
                return
            result = advance_workflow_with_signoff(
                system=str(body.get("system", "")),
                decision=str(body.get("decision", "")),
                signoff_date=str(body.get("date", "")),
                notes=str(body.get("notes", "")),
                dry_run=bool(body.get("dry_run", False)),
            )
            self._send_json(result, 200 if result.get("exit_code") == 0 else 400)
            return
        if parsed.path == "/api/bootstrap":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, Exception):
                self._send_json({"error": "invalid JSON body"}, 400)
                return
            result = run_bootstrap(
                dest=str(body.get("dest", "")),
                project_name=str(body.get("project_name", "")),
                variant=str(body.get("variant", "product")),
                dry_run=bool(body.get("dry_run", False)),
            )
            self._send_json(result)
            return
        if parsed.path != "/api/run":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length))
        except (ValueError, Exception):
            self._send_json({"error": "invalid JSON body"}, 400)
            return
        command_key = str(body.get("command", ""))
        raw_args = body.get("args")
        if isinstance(raw_args, list):
            normalized_args: list[str] = []
            for item in cast(list[Any], raw_args):
                if isinstance(item, str | int | float | bool):
                    normalized_args.append(str(item))
            extra_args = normalized_args
        else:
            extra_args = None
        result = run_command(command_key, extra_args)
        self._send_json(result)


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the PROGRAMSTART local web dashboard.")
    parser.add_argument("--port", type=int, default=7771, help="Port to listen on (default 7771).")
    parser.add_argument("--no-open", action="store_true", help="Don't automatically open a browser tab.")
    args = parser.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), DashboardHandler)
    url = f"http://127.0.0.1:{args.port}"
    print("\n  PROGRAMSTART Dashboard")
    print("  ---------------------")
    print(f"  Listening on  {url}")
    print(f"  Workspace     {ROOT}")
    print("\n  Press Ctrl+C to stop.\n")

    if not args.no_open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Dashboard stopped.")
    return 0


if __name__ == "__main__":
    try:
        from .programstart_common import warn_direct_script_invocation  # noqa: PLC0415
    except ImportError:  # pragma: no cover - standalone script execution fallback
        from programstart_common import warn_direct_script_invocation  # noqa: PLC0415

    warn_direct_script_invocation("'uv run programstart serve' or 'pb serve'")
    raise SystemExit(main())
