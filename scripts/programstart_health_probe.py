"""Read-only health probe for PROGRAMSTART-structured repositories.

Runs status, validation, drift, and checklist checks against a target repo
(local or the current workspace) and returns a structured JSON report.
Designed for non-intrusive assessment of in-progress projects — never writes
to the target repo.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .programstart_common import (
        ROOT,
        load_registry_from_path,
        warn_direct_script_invocation,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        ROOT,
        load_registry_from_path,
        warn_direct_script_invocation,
    )

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

CHECKBOX_RE = re.compile(r"^- \[(?P<mark>[ xX])\]\s+")


@dataclass
class SystemHealthReport:
    """Health report for a single system (programbuild or userjourney)."""

    system: str = ""
    present: bool = False
    active_step: str = ""
    variant: str = ""
    total_control_files: int = 0
    present_control_files: int = 0
    total_output_files: int = 0
    present_output_files: int = 0
    missing_files: list[str] = field(default_factory=list)
    checklist_checked: int = 0
    checklist_total: int = 0
    checklist_pct: float = 0.0
    validation_problems: list[str] = field(default_factory=list)
    drift_violations: list[str] = field(default_factory=list)
    drift_notes: list[str] = field(default_factory=list)
    days_since_last_signoff: int | None = None
    last_signoff_date: str = ""
    last_signoff_decision: str = ""
    last_signoff_commit_hash: str = ""
    files_changed_since_signoff: int | None = None
    completed_steps: list[str] = field(default_factory=list)
    blocked_steps: list[str] = field(default_factory=list)


@dataclass
class HealthProbeReport:
    """Aggregated health report for one or more PROGRAMSTART-structured repos."""

    target: str = ""
    probe_time: str = ""
    registry_version: str = ""
    repo_role: str = ""
    systems: list[SystemHealthReport] = field(default_factory=list)
    structural_problems: list[str] = field(default_factory=list)
    overall_health: str = ""  # healthy, warnings, degraded, critical
    summary: str = ""


# ---------------------------------------------------------------------------
# Helpers — operate against an arbitrary root, never write
# ---------------------------------------------------------------------------


def _target_path(target_root: Path, relative: str) -> Path:
    return target_root / relative


def _load_json_from(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_target_registry(target_root: Path) -> dict[str, Any]:
    registry_path = target_root / "config" / "process-registry.json"
    if not registry_path.exists():
        return {}
    return load_registry_from_path(registry_path)


def _load_target_state(target_root: Path, registry: dict, system: str) -> dict[str, Any]:
    state_cfg = registry.get("workflow_state", {}).get(system, {})
    state_file = state_cfg.get("file", "")
    if not state_file:
        fallback = "PROGRAMBUILD/PROGRAMBUILD_STATE.json" if system == "programbuild" else "USERJOURNEY/USERJOURNEY_STATE.json"
        state_file = fallback
    return _load_json_from(target_root / state_file)


def _active_step(registry: dict, system: str, state: dict) -> str:
    config = registry.get("workflow_state", {}).get(system, {})
    active_key = config.get("active_key", "active_stage" if system == "programbuild" else "active_phase")
    return str(state.get(active_key, "unknown"))


def _step_order(registry: dict, system: str) -> list[str]:
    config = registry.get("workflow_state", {}).get(system, {})
    return [s["name"] if isinstance(s, dict) else str(s) for s in config.get("step_order", [])]


def _entry_key(system: str) -> str:
    return "stages" if system == "programbuild" else "phases"


def _git_changed_files(target_root: Path) -> list[str]:
    commands = [
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
    ]
    changed: list[str] = []
    for cmd in commands:
        try:
            result = subprocess.run(
                cmd,
                cwd=str(target_root),
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            stripped = line.strip().replace("\\", "/")
            if stripped and stripped not in changed:
                changed.append(stripped)
    return changed


# ---------------------------------------------------------------------------
# Core checks
# ---------------------------------------------------------------------------


def _check_required_files(target_root: Path, registry: dict, system: str) -> tuple[list[str], int, int, int, int]:
    """Returns (missing_files, ctrl_present, ctrl_total, out_present, out_total)."""
    sys_cfg = registry.get("systems", {}).get(system, {})
    missing: list[str] = []
    ctrl_files = sys_cfg.get("control_files", [])
    out_files = sys_cfg.get("output_files", sys_cfg.get("core_files", []))
    for f in ctrl_files:
        if not _target_path(target_root, f).exists():
            missing.append(f)
    for f in out_files:
        if not _target_path(target_root, f).exists():
            missing.append(f)
    ctrl_present = len(ctrl_files) - sum(1 for f in ctrl_files if f in missing)
    out_present = len(out_files) - sum(1 for f in out_files if f in missing)
    return missing, ctrl_present, len(ctrl_files), out_present, len(out_files)


def _check_metadata(target_root: Path, registry: dict, system: str) -> list[str]:
    """Check that metadata-required files have standard metadata headers."""
    problems: list[str] = []
    sys_cfg = registry.get("systems", {}).get(system, {})
    required_meta_files = sys_cfg.get("metadata_required", [])
    standard_prefixes = ["Purpose:", "Owner:", "Authority:"]
    for rel in required_meta_files:
        path = _target_path(target_root, rel)
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            problems.append(f"Cannot read {rel}")
            continue
        found = 0
        for line in text.splitlines()[:20]:
            stripped = line.strip()
            if stripped == "---":
                break
            for prefix in standard_prefixes:
                if stripped.startswith(prefix):
                    found += 1
        if found == 0:
            problems.append(f"Missing metadata header in {rel}")
    return problems


def _check_authority_sync(
    target_root: Path, registry: dict, changed_files: list[str], system: str | None = None
) -> tuple[list[str], list[str]]:
    """Evaluate sync rule violations for given changed files."""
    violations: list[str] = []
    notes: list[str] = []
    changed_set = set(changed_files)
    for rule in registry.get("sync_rules", []):
        if system and rule.get("system", "") not in (system, "cross"):
            continue
        authority = set(rule["authority_files"])
        dependents = set(rule["dependent_files"])
        touched_auth = sorted(changed_set & authority)
        touched_dep = sorted(changed_set & dependents)
        if touched_dep and not touched_auth and rule.get("require_authority_when_dependents_change", False):
            violations.append(f"{rule['name']}: dependents changed without authority: {', '.join(touched_dep)}")
        elif touched_auth and not touched_dep:
            notes.append(f"{rule['name']}: authority changed without dependents: {', '.join(touched_auth)}")
    return violations, notes


def _check_step_order(target_root: Path, registry: dict, system: str, state: dict, changed_files: list[str]) -> list[str]:
    """Detect files edited before their owning step is active."""
    violations: list[str] = []
    is_template = registry.get("workspace", {}).get("repo_role") == "template_repo"
    if is_template:
        return violations
    config = registry.get("workflow_state", {}).get(system, {})
    steps = _step_order(registry, system)
    active = _active_step(registry, system, state)
    if active not in steps:
        return violations
    active_idx = steps.index(active)
    step_files = config.get("step_files", {})
    for cf in changed_files:
        owning = next((s for s in steps if cf in step_files.get(s, [])), None)
        if not owning:
            continue
        owning_idx = steps.index(owning)
        if owning_idx > active_idx:
            violations.append(f"{cf} belongs to future step '{owning}' (active: '{active}')")
    return violations


def _check_workflow_state(target_root: Path, registry: dict, system: str) -> list[str]:
    """Validate workflow state structural integrity."""
    problems: list[str] = []
    state = _load_target_state(target_root, registry, system)
    if not state:
        problems.append(f"No workflow state file for {system}")
        return problems
    config = registry.get("workflow_state", {}).get(system, {})
    active_key = config.get("active_key", "active_stage" if system == "programbuild" else "active_phase")
    if active_key not in state:
        problems.append(f"Missing '{active_key}' in {system} state")
    entry_key = _entry_key(system)
    entries = state.get(entry_key, {})
    steps = _step_order(registry, system)
    for step in steps:
        if step not in entries:
            problems.append(f"Step '{step}' missing from {system} state entries")
    return problems


def _checklist_progress(target_root: Path, system: str) -> tuple[int, int]:
    """Return (checked, total) for the system's checklist if it exists."""
    if system == "programbuild":
        path = target_root / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md"
    else:
        return 0, 0
    if not path.exists():
        return 0, 0
    text = path.read_text(encoding="utf-8")
    checked = total = 0
    for line in text.splitlines():
        match = CHECKBOX_RE.match(line.strip())
        if not match:
            continue
        total += 1
        if match.group("mark").lower() == "x":
            checked += 1
    return checked, total


def _signoff_info(state: dict, system: str) -> tuple[str, str, str, int | None, list[str], list[str]]:
    """Extract latest signoff, completed steps, blocked steps.

    Returns: (last_date, last_decision, last_commit_hash, days_since, completed, blocked)
    """
    entry_key = _entry_key(system)
    entries = state.get(entry_key, {})
    last_date = ""
    last_decision = ""
    last_commit_hash = ""
    completed: list[str] = []
    blocked: list[str] = []
    for step_name, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        status = entry.get("status", "")
        if status == "completed":
            completed.append(step_name)
        if status == "blocked":
            blocked.append(step_name)
        signoff = entry.get("signoff", {})
        if isinstance(signoff, dict):
            d = signoff.get("date", "")
            if d and d > last_date:
                last_date = d
                last_decision = signoff.get("decision", "")
                last_commit_hash = signoff.get("commit_hash", "")
    days_since = None
    if last_date:
        try:
            last_dt = datetime.strptime(last_date, "%Y-%m-%d").replace(tzinfo=UTC)
            days_since = (datetime.now(UTC) - last_dt).days
        except ValueError:
            pass
    return last_date, last_decision, last_commit_hash, days_since, completed, blocked


def _files_changed_since_commit(target_root: Path, commit_hash: str) -> int | None:
    """Return the number of files changed since the given commit hash.

    Returns None if git is unavailable or the hash cannot be resolved.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{commit_hash}..HEAD"],
            cwd=str(target_root),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        if result.returncode != 0:
            return None
        lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
        return len(lines)
    except (OSError, subprocess.TimeoutExpired):
        return None


# ---------------------------------------------------------------------------
# Build report for a single system
# ---------------------------------------------------------------------------


def probe_system(target_root: Path, registry: dict, system: str, changed_files: list[str]) -> SystemHealthReport | None:
    """Run all read-only checks against one system in the target repo."""
    sys_cfg = registry.get("systems", {}).get(system)
    if not sys_cfg:
        return None
    sys_root = sys_cfg.get("root", "")
    is_optional = sys_cfg.get("optional", False)
    if is_optional and not _target_path(target_root, sys_root).exists():
        return None

    state = _load_target_state(target_root, registry, system)
    report = SystemHealthReport(system=system, present=True)

    # Active step and variant
    report.active_step = _active_step(registry, system, state)
    report.variant = state.get("variant", "")

    # File presence
    missing, cp, ct, op, ot = _check_required_files(target_root, registry, system)
    report.missing_files = missing
    report.present_control_files = cp
    report.total_control_files = ct
    report.present_output_files = op
    report.total_output_files = ot

    # Metadata
    report.validation_problems.extend(_check_metadata(target_root, registry, system))

    # Workflow state structure
    report.validation_problems.extend(_check_workflow_state(target_root, registry, system))

    # Sync rule drift
    violations, notes = _check_authority_sync(target_root, registry, changed_files, system)
    report.drift_violations.extend(violations)
    report.drift_notes.extend(notes)

    # Step-order drift
    step_violations = _check_step_order(target_root, registry, system, state, changed_files)
    report.drift_violations.extend(step_violations)

    # Checklist progress
    checked, total = _checklist_progress(target_root, system)
    report.checklist_checked = checked
    report.checklist_total = total
    report.checklist_pct = round(checked / total * 100, 1) if total else 0.0

    # Signoff info
    last_date, last_decision, last_commit_hash, days, completed, blocked = _signoff_info(state, system)
    report.last_signoff_date = last_date
    report.last_signoff_decision = last_decision
    report.last_signoff_commit_hash = last_commit_hash
    report.days_since_last_signoff = days
    report.completed_steps = completed
    report.blocked_steps = blocked

    # Commit hash staleness
    if last_commit_hash:
        report.files_changed_since_signoff = _files_changed_since_commit(target_root, last_commit_hash)

    return report


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------


def _classify_health(report: HealthProbeReport) -> tuple[str, str]:
    """Return (overall_health, summary) based on all systems."""
    total_violations = sum(len(s.drift_violations) for s in report.systems)
    total_problems = sum(len(s.validation_problems) for s in report.systems) + len(report.structural_problems)
    total_missing = sum(len(s.missing_files) for s in report.systems)
    any_blocked = any(s.blocked_steps for s in report.systems)
    stale = any((s.days_since_last_signoff or 0) > 30 for s in report.systems if s.last_signoff_date)
    signoff_drift = any((s.files_changed_since_signoff or 0) > 0 for s in report.systems if s.last_signoff_commit_hash)

    if total_violations > 0 or total_problems > 3 or any_blocked:
        health = "critical"
    elif total_missing > 3 or total_problems > 0 or stale:
        health = "degraded"
    elif total_missing > 0 or total_violations > 0 or signoff_drift:
        health = "warnings"
    else:
        health = "healthy"

    parts: list[str] = []
    for s in report.systems:
        step_info = f"stage={s.active_step}" if s.system == "programbuild" else f"phase={s.active_step}"
        files_info = f"files={s.present_control_files + s.present_output_files}/{s.total_control_files + s.total_output_files}"
        checklist_info = f"checklist={s.checklist_pct}%" if s.checklist_total else ""
        staleness = f"last_signoff={s.days_since_last_signoff}d_ago" if s.days_since_last_signoff is not None else "no_signoffs"
        drift_hint = f"changed_since_signoff={s.files_changed_since_signoff}" if s.files_changed_since_signoff else ""
        issues = len(s.drift_violations) + len(s.validation_problems) + len(s.missing_files)
        row = f"{s.system}: {step_info}, {files_info}, {checklist_info}, {staleness}"
        if drift_hint:
            row += f", {drift_hint}"
        row += f", issues={issues}"
        parts.append(row.replace(", ,", ","))

    summary = f"health={health}; " + "; ".join(parts)
    return health, summary


def probe_target(target_root: Path) -> HealthProbeReport:
    """Run the full read-only health probe against a target repo."""
    report = HealthProbeReport(
        target=str(target_root),
        probe_time=datetime.now(UTC).isoformat(timespec="seconds"),
    )

    registry = _load_target_registry(target_root)
    if not registry:
        report.structural_problems.append("No config/process-registry.json found — not a PROGRAMSTART-structured repo")
        report.overall_health = "critical"
        report.summary = "Cannot assess: missing process-registry.json"
        return report

    report.registry_version = registry.get("version", "unknown")
    report.repo_role = registry.get("workspace", {}).get("repo_role", "unknown")

    changed_files = _git_changed_files(target_root)

    for system_name in registry.get("systems", {}):
        sys_report = probe_system(target_root, registry, system_name, changed_files)
        if sys_report:
            report.systems.append(sys_report)

    if not report.systems:
        report.structural_problems.append("No active systems found in registry")

    report.overall_health, report.summary = _classify_health(report)
    return report


# ---------------------------------------------------------------------------
# Multi-repo scan
# ---------------------------------------------------------------------------


def probe_multiple(targets: list[Path]) -> list[HealthProbeReport]:
    """Probe multiple repos and return a list of reports."""
    return [probe_target(t) for t in targets]


def print_multi_summary(reports: list[HealthProbeReport]) -> None:
    """Print a concise summary table across multiple repos."""
    print()
    print(f"  {'Repo':<40} {'Health':<10} {'Systems':<12} {'Issues':<8} {'Last Signoff':<14}")
    print(f"  {'─' * 40} {'─' * 10} {'─' * 12} {'─' * 8} {'─' * 14}")
    for r in reports:
        name = Path(r.target).name
        systems = ", ".join(s.system[:4] for s in r.systems) or "none"
        issues = sum(len(s.drift_violations) + len(s.validation_problems) + len(s.missing_files) for s in r.systems) + len(
            r.structural_problems
        )
        last_signoff = "none"
        for s in r.systems:
            if s.last_signoff_date:
                last_signoff = s.last_signoff_date
        print(f"  {name:<40} {r.overall_health:<10} {systems:<12} {issues:<8} {last_signoff:<14}")
    print()


# ---------------------------------------------------------------------------
# Text report
# ---------------------------------------------------------------------------


def print_report(report: HealthProbeReport) -> None:
    """Print a human-readable health report."""
    print()
    print("  PROGRAMSTART Health Probe")
    print(f"  Target:   {report.target}")
    print(f"  Time:     {report.probe_time}")
    print(f"  Registry: {report.registry_version}")
    print(f"  Role:     {report.repo_role}")
    print(f"  Health:   {report.overall_health.upper()}")
    print()

    if report.structural_problems:
        print("  Structural Problems:")
        for p in report.structural_problems:
            print(f"    - {p}")
        print()

    for sys_report in report.systems:
        label = sys_report.system.upper()
        print(f"  {label}")
        print(f"    Active step:       {sys_report.active_step}")
        if sys_report.variant:
            print(f"    Variant:           {sys_report.variant}")
        print(f"    Control files:     {sys_report.present_control_files}/{sys_report.total_control_files}")
        print(f"    Output files:      {sys_report.present_output_files}/{sys_report.total_output_files}")
        if sys_report.checklist_total:
            print(
                "    Checklist:         "
                f"{sys_report.checklist_checked}/{sys_report.checklist_total} "
                f"({sys_report.checklist_pct}%)"
            )
        print(f"    Completed steps:   {', '.join(sys_report.completed_steps) or 'none'}")
        if sys_report.blocked_steps:
            print(f"    Blocked steps:     {', '.join(sys_report.blocked_steps)}")
        if sys_report.last_signoff_date:
            print(
                "    Last signoff:      "
                f"{sys_report.last_signoff_date} "
                f"({sys_report.last_signoff_decision}) - "
                f"{sys_report.days_since_last_signoff}d ago"
            )
        else:
            print("    Last signoff:      none")

        if sys_report.missing_files:
            print(f"    Missing files ({len(sys_report.missing_files)}):")
            for f in sys_report.missing_files:
                print(f"      - {f}")
        if sys_report.validation_problems:
            print(f"    Validation problems ({len(sys_report.validation_problems)}):")
            for p in sys_report.validation_problems:
                print(f"      - {p}")
        if sys_report.drift_violations:
            print(f"    Drift violations ({len(sys_report.drift_violations)}):")
            for v in sys_report.drift_violations:
                print(f"      - {v}")
        if sys_report.drift_notes:
            print(f"    Drift notes ({len(sys_report.drift_notes)}):")
            for n in sys_report.drift_notes:
                print(f"      - {n}")
        print()

    print(f"  Summary: {report.summary}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only health probe for PROGRAMSTART-structured repositories.",
    )
    parser.add_argument(
        "--target",
        action="append",
        help="Path to a PROGRAMSTART-structured repo to probe. Repeatable. Defaults to current workspace.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args(argv)

    targets = [Path(t).resolve() for t in args.target] if args.target else [ROOT]

    if len(targets) == 1:
        report = probe_target(targets[0])
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print_report(report)
        return 1 if report.overall_health == "critical" else 0

    reports = probe_multiple(targets)
    if args.json:
        print(json.dumps([asdict(r) for r in reports], indent=2))
    else:
        print_multi_summary(reports)
    return 1 if any(r.overall_health == "critical" for r in reports) else 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart health' or 'pb health'")
    raise SystemExit(main())
