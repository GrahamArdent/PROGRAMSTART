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
import logging
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

from filelock import FileLock

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SCRIPTS = Path(__file__).resolve().parent
logger = logging.getLogger(__name__)
READONLY_MODE = os.environ.get("PROGRAMSTART_READONLY", "").strip().lower() in ("1", "true", "yes")

try:
    from .programstart_command_registry import dashboard_allowed_commands
    from .programstart_common import (
        challenge_gate_record_from_log,
        extract_numbered_items,
        git_changed_files,
        load_registry,
        load_workflow_state,
        parse_markdown_table,
        pyproject_dependency_sync_required,
        save_workflow_state,
        system_is_attached,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_config,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )
    from .programstart_health_probe import probe_target as _probe_target
    from .programstart_markdown_parsers import (
        clean_md,
        extract_bullets,
        extract_bullets_after_marker,
        extract_file_checklist_sections,
        extract_slice_sections,
        extract_startup_sections,
        extract_subagents,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_command_registry import dashboard_allowed_commands
    from programstart_health_probe import probe_target as _probe_target
    from programstart_markdown_parsers import (
        clean_md,
        extract_bullets,
        extract_bullets_after_marker,
        extract_file_checklist_sections,
        extract_slice_sections,
        extract_startup_sections,
        extract_subagents,
    )

    from programstart_common import (
        challenge_gate_record_from_log,
        extract_numbered_items,
        git_changed_files,
        load_registry,
        load_workflow_state,
        parse_markdown_table,
        pyproject_dependency_sync_required,
        save_workflow_state,
        system_is_attached,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_config,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )

# ---------------------------------------------------------------------------
# Allowed commands — strict whitelist, no shell interpolation possible
# ---------------------------------------------------------------------------
ALLOWED_COMMANDS: dict[str, list[str]] = dashboard_allowed_commands(PYTHON, SCRIPTS)

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")
_ALLOWED_EXTRA_ARGS: frozenset[str] = frozenset({"--decision", "--notes", "--date", "--system", "approved", "hold", "blocked"})
_MAX_EXTRA_ARGS = 8
_MAX_EXTRA_ARG_LENGTH = 2000
MAX_SIGNOFF_HISTORY = 100


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def run_command(command_key: str, extra_args: list[str] | None = None) -> dict[str, Any]:
    """Run an allowed command and return {output, exit_code}."""
    if command_key not in ALLOWED_COMMANDS:
        return {"output": f"Error: unknown command '{command_key}'", "exit_code": 1}
    cmd = ALLOWED_COMMANDS[command_key][:]
    if extra_args:
        if len(extra_args) > _MAX_EXTRA_ARGS:
            return {"output": f"Error: too many extra args (max {_MAX_EXTRA_ARGS})", "exit_code": 1}
        for arg in extra_args:
            if len(arg) > _MAX_EXTRA_ARG_LENGTH:
                return {"output": f"Error: extra arg exceeds {_MAX_EXTRA_ARG_LENGTH} char limit", "exit_code": 1}
            if arg not in _ALLOWED_EXTRA_ARGS:
                return {"output": f"Error: extra arg '{arg}' not permitted", "exit_code": 1}
        cmd.extend(extra_args)
    env = {**os.environ, "NO_COLOR": "1"}
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, env=env, timeout=60)
    except subprocess.TimeoutExpired:
        return {"output": "Error: command timed out after 60 seconds", "exit_code": 1}
    output = result.stdout + (f"\nSTDERR:\n{result.stderr}" if result.stderr.strip() else "")
    return {"output": strip_ansi(output.strip()), "exit_code": result.returncode}


_SAFE_PATH_RE = re.compile(
    r"^[A-Za-z]:[/\\][A-Za-z0-9 /\\._-]{1,259}$"  # Windows
    r"|^/[A-Za-z0-9 /._-]{1,259}$"  # Unix
)
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
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, env=env, timeout=60)
    except subprocess.TimeoutExpired:
        return {"output": "Error: bootstrap timed out after 60 seconds", "exit_code": 1}
    output = result.stdout + (f"\nSTDERR:\n{result.stderr}" if result.stderr.strip() else "")
    return {"output": strip_ansi(output.strip()), "exit_code": result.returncode}


def get_state_json() -> dict[str, Any]:
    """Return both workflow states as JSON-serialisable dicts plus guidance metadata."""
    try:
        registry = load_registry()

        guidance = registry.get("workflow_guidance", {})
        result: dict[str, Any] = {}
        for system in ("programbuild", "userjourney"):
            system_cfg = registry.get("systems", {}).get(system, {})
            attached = system_is_attached(registry, system)
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
                except (FileNotFoundError, KeyError, ValueError):
                    sys_data["open_questions"] = 0
            result[system] = sys_data

        file_index_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md").read_text(encoding="utf-8")
        kickoff_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md").read_text(encoding="utf-8")
        subagents_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md").read_text(encoding="utf-8")
        playbook_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD.md").read_text(encoding="utf-8")
        lite_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_LITE.md").read_text(encoding="utf-8")
        product_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_PRODUCT.md").read_text(encoding="utf-8")
        enterprise_text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_ENTERPRISE.md").read_text(encoding="utf-8")
        userjourney_attached = system_is_attached(registry, "userjourney")
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

        stage_subagents = dict(registry.get("workflow_guidance", {}).get("programbuild", {}).get("stage_subagents", {}))

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
        logging.getLogger(__name__).exception("Unexpected error in get_state_json")
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
    if not target.is_relative_to(ROOT.resolve()):
        return {"error": "path escapes workspace"}
    if not target.exists() or not target.is_file():
        return {"error": "file not found"}
    if target.suffix.lower() not in {".md", ".txt", ".json", ".py", ".ps1", ".yml", ".yaml"}:
        return {"error": "file type not previewable"}
    try:
        size = target.stat().st_size
    except OSError:
        return {"error": "unable to stat file"}
    if size > 65536:
        return {"error": "file too large for preview (>64 KB)"}
    text = target.read_text(encoding="utf-8")
    lines = text.splitlines()
    return {
        "path": normalized,
        "line_count": len(lines),
        "truncated": len(lines) > 220,
        "content": "\n".join(lines[:220]),
    }


def sanitize_markdown_table_cell(value: str) -> str:
    """Keep user-entered text from corrupting markdown table structure."""
    sanitized = value.replace("\r", " ").replace("\n", " ").replace("|", "¦")
    return " ".join(sanitized.split())


def update_implementation_tracker_phase(phase: str, status: str, blockers: str) -> dict[str, Any]:
    """Update the USERJOURNEY implementation tracker phase overview row."""
    if not (ROOT / "USERJOURNEY").exists():
        return {"output": "Error: USERJOURNEY is not attached in this repository.", "exit_code": 1}
    valid_statuses = {"Planned", "In Progress", "Blocked", "Completed"}
    phase = phase.strip()
    status = status.strip()
    blockers = sanitize_markdown_table_cell(blockers.strip())
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
    notes = sanitize_markdown_table_cell(notes.strip())
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

    registry = load_registry()
    state_path = workflow_state_path(registry, system)
    lock = FileLock(str(state_path) + ".lock", timeout=10)
    with lock:
        state = load_workflow_state(registry, system)
        active_step = workflow_active_step(registry, system, state)
        entry_key = workflow_entry_key(system)
        entries = cast(dict[str, Any], state[entry_key])
        entry = cast(dict[str, Any], entries[active_step])
        signoff_record = {
            "decision": decision.strip(),
            "date": signoff_date.strip(),
            "notes": sanitize_markdown_table_cell(notes.strip()),
            "saved_at": date.today().isoformat(),
        }
        entry["signoff"] = signoff_record
        history = entry.setdefault("signoff_history", [])
        history.append(signoff_record)
        if len(history) > MAX_SIGNOFF_HISTORY:
            logger.warning(
                "signoff_history for %s %s exceeded %d entries; oldest trimmed",
                system,
                active_step,
                MAX_SIGNOFF_HISTORY,
            )
            entry["signoff_history"] = history[-MAX_SIGNOFF_HISTORY:]
        save_workflow_state(registry, system, state, acquire_lock=False)
    return {"output": f"Saved signoff metadata for {system} {active_step}", "exit_code": 0}


def advance_workflow_with_signoff(
    system: str,
    decision: str,
    signoff_date: str,
    notes: str,
    dry_run: bool,
    gate_result: str = "",
    gate_date: str = "",
    gate_notes: str = "",
) -> dict[str, Any]:
    """Advance a workflow while recording explicit signoff metadata."""
    if system not in {"programbuild", "userjourney"}:
        return {"output": "Error: unknown system.", "exit_code": 1}

    registry = load_registry()

    # Dry-run path does not modify state — no lock needed.
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
    notes_value = sanitize_markdown_table_cell(notes.strip())
    current_index = steps.index(active_step)
    next_step = steps[current_index + 1] if current_index + 1 < len(steps) else None
    gate_date_value = gate_date.strip() or date.today().isoformat()
    gate_notes_value = sanitize_markdown_table_cell(gate_notes.strip())
    gate_record: dict[str, Any] | None = None
    if system == "programbuild":
        if gate_result:
            proceed_map = {"clear": "yes", "warning": "conditional", "blocked": "no"}
            gate_record = {
                "source": "dashboard_api",
                "from_stage": active_step,
                "to_stage": next_step or "",
                "date": gate_date_value,
                "proceed": proceed_map.get(gate_result, ""),
                "result": gate_result,
                "notes": gate_notes_value,
                "checks": {},
            }
        else:
            gate_record = challenge_gate_record_from_log(active_step)
        if gate_record is None:
            return {
                "output": (
                    f"Error: no Challenge Gate evidence found for stage '{active_step}'. "
                    "Record the gate in PROGRAMBUILD_CHALLENGE_GATE.md or provide gate_result in the API payload."
                ),
                "exit_code": 1,
            }
        if gate_record.get("result") == "blocked":
            return {
                "output": f"Error: Challenge Gate for stage '{active_step}' is blocking. Resolve it before advancing.",
                "exit_code": 1,
            }
    if dry_run:
        if next_step:
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

    # Mutating path — acquire lock for the full read-modify-write cycle.
    state_path = workflow_state_path(registry, system)
    lock = FileLock(str(state_path) + ".lock", timeout=10)
    with lock:
        # Re-read state under lock to avoid lost-update races.
        state = load_workflow_state(registry, system)
        active_step = workflow_active_step(registry, system, state)
        entries = cast(dict[str, Any], state[entry_key])
        current_entry = cast(dict[str, Any], entries[active_step])

        advance_record = {
            "decision": decision_value,
            "date": date_value,
            "notes": notes_value,
            "saved_at": date.today().isoformat(),
        }
        current_entry["status"] = "completed"
        current_entry["signoff"] = advance_record
        history = current_entry.setdefault("signoff_history", [])
        history.append(advance_record)
        if len(history) > MAX_SIGNOFF_HISTORY:
            logger.warning(
                "signoff_history for %s %s exceeded %d entries; oldest trimmed",
                system,
                active_step,
                MAX_SIGNOFF_HISTORY,
            )
            current_entry["signoff_history"] = history[-MAX_SIGNOFF_HISTORY:]
        if gate_record:
            current_entry["challenge_gate"] = gate_record
        if next_step:
            next_entry = cast(dict[str, Any], entries[next_step])
            if str(next_entry.get("status", "planned")) == "planned":
                next_entry["status"] = "in_progress"
            state["active_stage" if system == "programbuild" else "active_phase"] = next_step
            output = f"Advanced {system} from {active_step} to {next_step}"
        else:
            output = f"Completed final {system} step {active_step}"

        save_workflow_state(registry, system, state, acquire_lock=False)
    return {"output": output, "exit_code": 0}


def build_drift_summary() -> dict[str, Any]:
    """Return a dashboard-friendly drift summary based on current changed files and sync rules."""
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
            if rule.get("name") == "pyproject_requirements_sync" and not pyproject_dependency_sync_required():
                continue
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
# Dashboard static files
# ---------------------------------------------------------------------------
DASHBOARD_DIR = ROOT / "dashboard"


def _load_dashboard_html() -> str:
    """Load and cache the dashboard HTML template."""
    html_path = DASHBOARD_DIR / "index.html"
    if not html_path.is_file():
        return "<h1>Dashboard files not found</h1><p>Expected: dashboard/index.html</p>"
    return html_path.read_text(encoding="utf-8")


_STATIC_CONTENT_TYPES: dict[str, str] = {
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}
_CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"


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
        self.send_header("Content-Security-Policy", _CSP)
        self.end_headers()
        self.wfile.write(body)

    def _discard_request_body(self) -> None:
        """Drain any request body before returning early from a POST handler."""
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            self.rfile.read(length)

    def _serve_static(self, filename: str) -> None:
        """Serve a file from the dashboard/ directory with path traversal protection."""
        safe = Path(filename).name  # strip any directory components
        fpath = DASHBOARD_DIR / safe
        if not fpath.is_file():
            self.send_response(404)
            self.end_headers()
            return
        # Ensure resolved path is within DASHBOARD_DIR
        try:
            fpath.resolve().relative_to(DASHBOARD_DIR.resolve())
        except ValueError:
            self.send_response(403)
            self.end_headers()
            return
        content_type = _STATIC_CONTENT_TYPES.get(fpath.suffix, "application/octet-stream")
        body = fpath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            html = _load_dashboard_html().replace('"__ROOT__"', json.dumps(str(ROOT)))
            self._send_html(html)
        elif parsed.path == "/api/state":
            self._send_json(get_state_json())
        elif parsed.path == "/api/doc":
            query = parse_qs(parsed.query)
            path = query.get("path", [""])[0]
            data = get_doc_preview(path)
            self._send_json(data, 200 if "error" not in data else 400)
        elif parsed.path == "/api/health":
            from dataclasses import asdict as _asdict

            report = _probe_target(ROOT)
            self._send_json(_asdict(report))
        elif parsed.path.startswith("/static/"):
            self._serve_static(parsed.path[len("/static/") :])
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        if READONLY_MODE:
            self._discard_request_body()
            self._send_json({"error": "server is in read-only mode"}, 405)
            return
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
                gate_result=str(body.get("gate_result", "")),
                gate_date=str(body.get("gate_date", "")),
                gate_notes=str(body.get("gate_notes", "")),
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
            self._discard_request_body()
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
