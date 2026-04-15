from __future__ import annotations

import argparse
import datetime
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
        system_is_optional_and_absent,
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
        system_is_optional_and_absent,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_state_path,
        workflow_steps,
        workspace_path,
    )


def _check_decision_log_entries(stage_name: str) -> list[str]:
    """Check DECISION_LOG.md has at least one entry referencing a stage.

    Returns a list of warning-level problems (empty = pass).
    """
    log_path = workspace_path("PROGRAMBUILD/DECISION_LOG.md")
    if not log_path.exists():
        return [f"DECISION_LOG.md does not exist (expected for {stage_name})"]
    text = log_path.read_text(encoding="utf-8")

    rows = parse_markdown_table(text, "Decision Register")
    if not rows:
        return [f"DECISION_LOG.md: no entries in Decision Register (expected for {stage_name})"]

    stage_refs = [r for r in rows if stage_name.lower() in r.get("Stage", "").lower()]
    if not stage_refs:
        return [f"DECISION_LOG.md: no entries reference stage '{stage_name}'"]
    return []


# ---------------------------------------------------------------------------
# Content quality helper (W-1)
# ---------------------------------------------------------------------------

_PLACEHOLDER_PATTERNS = re.compile(
    r"\bTBD\b|\bTODO\b|\[FILL IN\]|\bPLACEHOLDER\b|Lorem ipsum",
)


def check_content_quality(filepath: Path) -> list[str]:
    """Detect placeholder content in *filepath*. Returns warnings (non-blocking)."""
    if not filepath.exists():
        return []
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    warnings: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        match = _PLACEHOLDER_PATTERNS.search(line)
        if match:
            warnings.append(f"{filepath.name}:{lineno}: placeholder '{match.group()}' detected")
    return warnings


def _relative_workspace_path(path: Path) -> str:
    try:
        return path.relative_to(workspace_path(".")).as_posix()
    except ValueError:
        return path.as_posix()


def placeholder_content_targets(registry: dict) -> dict[str, tuple[str, str]]:
    """Return repo placeholder-scan targets mapped to (severity, role)."""
    targets: dict[str, tuple[str, str]] = {}

    def register(paths: list[str] | set[str], severity: str, role: str) -> None:
        for relative_path in sorted({path.replace("\\", "/") for path in paths}):
            if not relative_path.endswith(".md"):
                continue
            targets.setdefault(relative_path, (severity, role))

    systems = cast(dict[str, Any], registry.get("systems", {}))
    programbuild = cast(dict[str, Any], systems.get("programbuild", {}))
    register(cast(list[str], programbuild.get("output_files", [])), "problem", "programbuild-output")

    userjourney = cast(dict[str, Any], systems.get("userjourney", {}))
    userjourney_root = str(userjourney.get("root", "USERJOURNEY")).strip() or "USERJOURNEY"
    userjourney_absent = bool(userjourney.get("optional")) and not workspace_path(userjourney_root).exists()
    if userjourney and not userjourney_absent:
        workflow_state = cast(dict[str, Any], registry.get("workflow_state", {}))
        userjourney_state = cast(dict[str, Any], workflow_state.get("userjourney", {}))
        userjourney_step_files = cast(dict[str, list[str]], userjourney_state.get("step_files", {}))
        userjourney_outputs: set[str] = set()
        for step_files in userjourney_step_files.values():
            userjourney_outputs.update(step_files)
        register(userjourney_outputs, "problem", "userjourney-output")

    decisions_dir = workspace_path("docs/decisions")
    if decisions_dir.exists():
        adr_files = {_relative_workspace_path(path) for path in decisions_dir.glob("*.md") if path.name != "README.md"}
        register(adr_files, "problem", "adr")

    repo_docs = {"README.md", "QUICKSTART.md", "CONTRIBUTING.md", "SECURITY.md"}
    docs_dir = workspace_path("docs")
    if docs_dir.exists():
        repo_docs.update(_relative_workspace_path(path) for path in docs_dir.glob("*.md") if path.parent == docs_dir)
    register(repo_docs.difference(targets), "warning", "repo-doc")

    return targets


def validate_placeholder_content(registry: dict) -> tuple[list[str], list[str]]:
    """Scan repo planning/documentation surfaces for unresolved placeholder content."""
    problems: list[str] = []
    warnings: list[str] = []

    for relative_path, (severity, role) in placeholder_content_targets(registry).items():
        findings = check_content_quality(workspace_path(relative_path))
        for finding in findings:
            message = f"{role}: {relative_path}: {finding}"
            if severity == "problem":
                problems.append(message)
            else:
                warnings.append(message)

    return problems, warnings


def stage_content_quality_warnings(step: str) -> list[str]:
    """Return non-blocking placeholder warnings for *step*'s key documents."""
    _step_files: dict[str, list[str]] = {
        "feasibility": ["PROGRAMBUILD/FEASIBILITY.md"],
        "research": ["PROGRAMBUILD/RESEARCH_SUMMARY.md"],
        "requirements_and_ux": ["PROGRAMBUILD/REQUIREMENTS.md", "PROGRAMBUILD/USER_FLOWS.md"],
        "architecture_and_risk_spikes": ["PROGRAMBUILD/ARCHITECTURE.md", "PROGRAMBUILD/RISK_SPIKES.md"],
        "test_strategy": ["PROGRAMBUILD/TEST_STRATEGY.md"],
        "release_readiness": ["PROGRAMBUILD/RELEASE_READINESS.md"],
        "audit_and_drift_control": ["PROGRAMBUILD/AUDIT_REPORT.md"],
        "post_launch_review": ["PROGRAMBUILD/POST_LAUNCH_REVIEW.md"],
    }
    files = _step_files.get(step, [])
    warnings: list[str] = []
    for rel in files:
        warnings.extend(check_content_quality(workspace_path(rel)))
    return warnings


def run_stage_gate_check(registry: dict, check_name: str) -> list[str]:
    """Dispatch a stage-gate content check by name.

    Called from preflight_problems() during 'advance'. Each check validates
    that a stage's outputs meet structural quality requirements before the
    workflow advances to the next stage.
    """
    dispatch: dict[str, Any] = {
        "intake-complete": validate_intake_complete,
        "feasibility-criteria": validate_feasibility_criteria,
        "research-complete": validate_research_complete,
        "requirements-complete": validate_requirements_complete,
        "architecture-contracts": validate_architecture_contracts,
        "risk-spikes": validate_risk_spikes,
        "risk-spikes-resolved": validate_risk_spike_resolution,
        "test-strategy-complete": validate_test_strategy_complete,
        "scaffold-complete": validate_scaffold_complete,
        "implementation-entry": validate_implementation_entry_criteria,
        "release-ready": validate_release_ready,
        "audit-complete": validate_audit_complete,
        "engineering-ready": validate_engineering_ready,
    }
    fn = dispatch.get(check_name)
    if fn is None:
        return []
    return fn(registry)


def validate_intake_complete(_registry: dict) -> list[str]:
    """Check that KICKOFF_PACKET fields and IDEA_INTAKE questions are filled."""
    problems: list[str] = []

    # 1. Check KICKOFF_PACKET required fields
    kickoff_path = workspace_path("PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md")
    if not kickoff_path.exists():
        problems.append("PROGRAMBUILD_KICKOFF_PACKET.md does not exist (See: shape-idea.prompt.md)")
        return problems
    kickoff_text = kickoff_path.read_text(encoding="utf-8")

    required_fields = [
        "PROJECT_NAME",
        "ONE_LINE_DESCRIPTION",
        "PRIMARY_USER",
        "CORE_PROBLEM",
        "SUCCESS_METRIC",
        "PRODUCT_SHAPE",
    ]
    for field in required_fields:
        match = re.search(rf"^{field}:[ \t]*(.*)$", kickoff_text, re.MULTILINE)
        if not match:
            problems.append(f"PROGRAMBUILD_KICKOFF_PACKET.md: {field} field not found")
        else:
            value = match.group(1).strip()
            # Strip the hint text for PRODUCT_SHAPE
            if field == "PRODUCT_SHAPE":
                value = re.sub(r"\[.*\]", "", value).strip()
            if not value:
                problems.append(f"PROGRAMBUILD_KICKOFF_PACKET.md: {field} is empty")
            elif field == "PRODUCT_SHAPE":
                VALID_PRODUCT_SHAPES = frozenset(
                    {
                        "web-app",
                        "mobile-app",
                        "api-service",
                        "cli-tool",
                        "data-pipeline",
                        "browser-extension",
                        "desktop-app",
                        "library/sdk",
                        "platform/marketplace",
                        "ai-agent/assistant",
                    }
                )
                if value.lower().replace(" ", "-") not in VALID_PRODUCT_SHAPES:
                    problems.append(
                        f"PROGRAMBUILD_KICKOFF_PACKET.md: PRODUCT_SHAPE '{value}' is not a recognized shape. "
                        "Valid shapes: web-app, mobile-app, API-service, CLI-tool, data-pipeline, "
                        "browser-extension, desktop-app, library/SDK, platform/marketplace, AI-agent/assistant"
                    )

    # 2. Check IDEA_INTAKE code block fields
    intake_path = workspace_path("PROGRAMBUILD/PROGRAMBUILD_IDEA_INTAKE.md")
    if not intake_path.exists():
        problems.append("PROGRAMBUILD_IDEA_INTAKE.md does not exist")
        return problems
    intake_text = intake_path.read_text(encoding="utf-8")

    required_blocks = [
        "PROBLEM_RAW",
        "WHO_HAS_THIS_PROBLEM",
        "CURRENT_SOLUTION",
        "SUCCESS_OUTCOME",
        "CHEAPEST_VALIDATION",
    ]
    for block in required_blocks:
        match = re.search(rf"^{block}:[ \t]*(.*)$", intake_text, re.MULTILINE)
        if not match or not match.group(1).strip():
            problems.append(f"PROGRAMBUILD_IDEA_INTAKE.md: {block} is empty")

    # 3. Check minimum exclusions (NOT_BUILDING_1 through NOT_BUILDING_3+)
    not_building = re.findall(r"^NOT_BUILDING_\d+:[ \t]*(.+)$", intake_text, re.MULTILINE)
    filled = [n for n in not_building if n.strip()]
    if len(filled) < 3:
        problems.append(f"PROGRAMBUILD_IDEA_INTAKE.md: {len(filled)} NOT_BUILDING entries filled, need at least 3")

    # 4. Check minimum kill signals (KILL_SIGNAL_1 through KILL_SIGNAL_3+)
    kill_signals = re.findall(r"^KILL_SIGNAL_\d+:[ \t]*(.+)$", intake_text, re.MULTILINE)
    filled_kills = [k for k in kill_signals if k.strip()]
    if len(filled_kills) < 3:
        problems.append(f"PROGRAMBUILD_IDEA_INTAKE.md: {len(filled_kills)} KILL_SIGNAL entries filled, need at least 3")

    problems.extend(_check_decision_log_entries("inputs_and_mode_selection"))

    return problems


def validate_feasibility_criteria(_registry: dict) -> list[str]:
    """Check kill criteria structure and go/no-go decision in FEASIBILITY.md."""
    problems: list[str] = []
    feas_path = workspace_path("PROGRAMBUILD/FEASIBILITY.md")
    if not feas_path.exists():
        problems.append("FEASIBILITY.md does not exist (See: shape-feasibility.prompt.md)")
        return problems
    text = feas_path.read_text(encoding="utf-8")

    # Extract Kill Criteria section (between ## Kill Criteria and next ##)
    kill_match = re.search(
        r"^## Kill Criteria\s*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not kill_match:
        problems.append("FEASIBILITY.md: no '## Kill Criteria' section found")
        return problems

    kill_section = kill_match.group(1)
    # Extract bullet items (- criterion)
    bullets = re.findall(r"^- (.+)$", kill_section, re.MULTILINE)
    # Filter out template placeholders
    real_criteria = [b.strip() for b in bullets if b.strip() and b.strip() != "criterion"]

    if len(real_criteria) < 3:
        problems.append(f"FEASIBILITY.md: {len(real_criteria)} kill criteria found, need at least 3")

    # Check each criterion follows "If/When [condition], then [action]" format
    if_then_pattern = re.compile(
        r"(?i)^(if|when)\s+.+,\s+(then\s+)?"
        r"(stop|kill|abort|pivot|project is killed|redirect|pause|no.go)"
    )
    for i, criterion in enumerate(real_criteria, 1):
        if not if_then_pattern.search(criterion):
            display = f"'{criterion[:60]}...'" if len(criterion) > 60 else f"'{criterion}'"
            problems.append(f"FEASIBILITY.md: kill criterion {i} is not in 'If [condition], then [action]' format: {display}")

    # Check Recommendation section has a decision
    rec_match = re.search(
        r"^## Recommendation\s*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if rec_match:
        rec_text = rec_match.group(1)
        if re.search(r"go\s*/\s*limited spike\s*/\s*no.go", rec_text, re.IGNORECASE):
            problems.append(
                "FEASIBILITY.md: Recommendation still contains the template option list — "
                "replace 'go / limited spike / no-go' with a single decision"
            )
        elif not re.search(r"(?i)\b(go|no.go|limited spike|stop|investigate)\b", rec_text):
            problems.append("FEASIBILITY.md: Recommendation section has no go/no-go decision")
    else:
        problems.append("FEASIBILITY.md: no '## Recommendation' section found")

    problems.extend(_check_decision_log_entries("feasibility_and_kill_criteria"))

    return problems


def validate_research_complete(_registry: dict) -> list[str]:
    """Check RESEARCH_SUMMARY.md exists and has at least one ## section heading."""
    problems: list[str] = []
    research_path = workspace_path("PROGRAMBUILD/RESEARCH_SUMMARY.md")
    if not research_path.exists():
        problems.append("RESEARCH_SUMMARY.md: file does not exist (See: shape-research.prompt.md)")
        return problems
    content = research_path.read_text(encoding="utf-8")
    if not re.search(r"^## ", content, re.MULTILINE):
        problems.append(
            "RESEARCH_SUMMARY.md: no ## section headings found (expected structured research output with at least one section)"
        )
    return problems


def validate_requirements_complete(_registry: dict) -> list[str]:
    """Check requirements have IDs, priorities, acceptance criteria, and flow references."""
    problems: list[str] = []

    req_path = workspace_path("PROGRAMBUILD/REQUIREMENTS.md")
    if not req_path.exists():
        problems.append("REQUIREMENTS.md does not exist (See: shape-requirements.prompt.md)")
        return problems
    req_text = req_path.read_text(encoding="utf-8")

    # Parse the Functional Requirements table
    req_rows = parse_markdown_table(req_text, "Functional Requirements")
    # Filter out template placeholder rows (empty Requirement column)
    real_rows = [r for r in req_rows if r.get("Requirement", "").strip()]

    if not real_rows:
        problems.append("REQUIREMENTS.md: no functional requirements defined")
        return problems

    # Validate each requirement row
    for row in real_rows:
        req_id = row.get("ID", "").strip()
        priority = row.get("Priority", "").strip()

        if not req_id:
            problems.append("REQUIREMENTS.md: requirement row has no ID")
            continue
        if not priority:
            problems.append(f"REQUIREMENTS.md: {req_id} has no priority")
        elif priority not in ("P0", "P1", "P2"):
            problems.append(f"REQUIREMENTS.md: {req_id} has invalid priority '{priority}'")

    # Check user stories have acceptance criteria
    stories = re.findall(r"### Story \d+.*?(?=### Story |^## |\Z)", req_text, re.DOTALL | re.MULTILINE)
    for i, story in enumerate(stories, 1):
        if "Acceptance criteria:" in story:
            criteria_text = story.split("Acceptance criteria:")[1]
            criteria_text = re.split(r"\n##", criteria_text)[0]
            real_criteria = [
                line.strip() for line in criteria_text.splitlines() if line.strip().startswith("-") and line.strip() != "-"
            ]
            if not real_criteria:
                problems.append(f"REQUIREMENTS.md: Story {i} has empty acceptance criteria")

    # Check cross-reference to USER_FLOWS.md
    flow_path = workspace_path("PROGRAMBUILD/USER_FLOWS.md")
    if flow_path.exists():
        flow_text = flow_path.read_text(encoding="utf-8")
        if not re.search(r"^#{2,3} .+", flow_text, re.MULTILINE):
            problems.append("USER_FLOWS.md: no ## or ### section headings found (expected at least one flow definition section)")
        for row in real_rows:
            req_id = row.get("ID", "").strip()
            if req_id and not re.search(r"\b" + re.escape(req_id) + r"\b", flow_text):
                problems.append(f"USER_FLOWS.md: no reference to requirement {req_id}")
    else:
        problems.append("USER_FLOWS.md does not exist")

    return problems


def validate_architecture_contracts(_registry: dict) -> list[str]:
    """Check ARCHITECTURE.md has required sections and real content."""
    problems: list[str] = []

    arch_path = workspace_path("PROGRAMBUILD/ARCHITECTURE.md")
    if not arch_path.exists():
        problems.append("ARCHITECTURE.md does not exist (See: shape-architecture.prompt.md)")
        return problems
    text = arch_path.read_text(encoding="utf-8")

    # Check for Data Model section (various naming conventions)
    has_data_model = bool(
        re.search(
            r"^## .*(Data Model|Data.*Ownership|Entity|Schema)",
            text,
            re.MULTILINE | re.IGNORECASE,
        )
    )
    if not has_data_model:
        problems.append("ARCHITECTURE.md: no data model section found")

    # Check for contracts/surface section (product-shape dependent)
    has_contracts = bool(
        re.search(
            r"^## .*(Contract|Command Surface|System Boundar|API|Endpoint|Interface)",
            text,
            re.MULTILINE | re.IGNORECASE,
        )
    )
    if not has_contracts:
        problems.append("ARCHITECTURE.md: no contracts, command surface, or system boundaries section found")

    # Check Technology Decision Table has real entries
    tech_rows = parse_markdown_table(text, "Technology Decision Table")
    real_tech = [r for r in tech_rows if r.get("Choice", "").strip()]
    if not real_tech:
        problems.append("ARCHITECTURE.md: Technology Decision Table has no entries")

    # Check System Topology section is not just the template placeholder
    topo_match = re.search(
        r"^## System Topology\s*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if topo_match:
        topo_text = topo_match.group(1).strip()
        if not topo_text:
            problems.append("ARCHITECTURE.md: System Topology section is empty")
    else:
        problems.append("ARCHITECTURE.md: no System Topology section found")

    problems.extend(_check_decision_log_entries("architecture_and_contracts"))

    return problems


def validate_risk_spikes(_registry: dict) -> list[str]:
    """Check RISK_SPIKES.md has at least one real spike entry with required fields."""
    problems: list[str] = []

    spikes_path = workspace_path("PROGRAMBUILD/RISK_SPIKES.md")
    if not spikes_path.exists():
        problems.append("RISK_SPIKES.md does not exist (See: shape-architecture.prompt.md, PROGRAMBUILD.md §11)")
        return problems

    text = spikes_path.read_text(encoding="utf-8")
    if not text.strip():
        problems.append("RISK_SPIKES.md is empty")
        return problems

    rows = parse_markdown_table(text, "Spike Register")
    real_rows = [r for r in rows if r.get("Spike", "").strip() and r.get("Spike", "").strip() not in ("", "spike")]

    if not real_rows:
        problems.append("RISK_SPIKES.md: Spike Register has no entries")
        return problems

    for row in real_rows:
        spike_id = row.get("Spike", "").strip()
        if not row.get("Pass criteria", "").strip():
            problems.append(f"RISK_SPIKES.md: spike '{spike_id}' has no pass criteria (acceptance criteria)")
        if not row.get("Method", "").strip():
            problems.append(f"RISK_SPIKES.md: spike '{spike_id}' has no method (time-box/approach)")

    return problems


def validate_risk_spike_resolution(_registry: dict) -> list[str]:
    """Check all RISK_SPIKES.md rows have a resolved/deferred/accepted status."""
    problems: list[str] = []
    spikes_path = workspace_path("PROGRAMBUILD/RISK_SPIKES.md")
    if not spikes_path.exists():
        return problems  # file-existence is checked by validate_risk_spikes; no duplication
    rows = parse_markdown_table(spikes_path.read_text(encoding="utf-8"), "Spike Register")
    real_rows = [r for r in rows if r.get("Spike", "").strip() and r.get("Spike", "").strip() not in ("", "spike")]
    if not real_rows:
        return problems  # empty table handled by validate_risk_spikes
    RESOLVED_VALUES = {"resolved", "deferred", "accepted", "pass", "done", "closed"}
    for row in real_rows:
        # Use or-chaining: Result column exists but may be empty; fall through to Decision/Status
        result = (row.get("Result") or row.get("Decision") or row.get("Status", "")).strip().lower()
        if not result or (result not in RESOLVED_VALUES and not any(v in result for v in RESOLVED_VALUES)):
            spike_id = row.get("Spike", "unknown").strip()
            problems.append(
                f"RISK_SPIKES.md: spike '{spike_id}' has unresolved status '{result or 'empty'}' "
                "(expected one of: resolved, deferred, accepted, or equivalent)"
            )
    return problems


def validate_test_strategy_complete(_registry: dict) -> list[str]:
    """Check TEST_STRATEGY.md exists and has at least one test category and requirement reference."""
    problems: list[str] = []

    ts_path = workspace_path("PROGRAMBUILD/TEST_STRATEGY.md")
    if not ts_path.exists():
        problems.append("TEST_STRATEGY.md does not exist (See: shape-test-strategy.prompt.md)")
        return problems

    text = ts_path.read_text(encoding="utf-8")

    # Check for at least one test category/layer definition (table row with real content)
    rows = parse_markdown_table(text, "Test Pyramid Targets")
    real_rows = [r for r in rows if r.get("Layer", "").strip()]
    if not real_rows:
        problems.append("TEST_STRATEGY.md: Test Pyramid Targets has no test categories defined")

    # Check for at least one requirement ID reference (FR-NNN or NFR-NNN)
    if not re.search(r"\b(FR|NFR)-\d+\b", text):
        problems.append("TEST_STRATEGY.md: no requirement IDs (FR-NNN or NFR-NNN) referenced")

    return problems


def validate_scaffold_complete(_registry: dict) -> list[str]:
    """Check scaffold outputs: project config file and CI directory present."""
    problems: list[str] = []

    # Check for a project configuration file (pyproject.toml, package.json, or Cargo.toml)
    config_candidates = [
        workspace_path("pyproject.toml"),
        workspace_path("package.json"),
        workspace_path("Cargo.toml"),
        workspace_path("go.mod"),
    ]
    has_project_config = any(p.exists() for p in config_candidates)
    if not has_project_config:
        problems.append(
            "Scaffold: no project configuration file found (expected pyproject.toml, package.json, Cargo.toml, or go.mod)"
        )

    # Check for CI configuration
    ci_candidates = [
        workspace_path(".github/workflows"),
        workspace_path(".circleci"),
        workspace_path(".gitlab-ci.yml"),
        workspace_path("Jenkinsfile"),
    ]
    has_ci = any(p.exists() for p in ci_candidates)
    if not has_ci:
        problems.append(
            "Scaffold: no CI configuration found (expected .github/workflows/, .circleci/, .gitlab-ci.yml, or Jenkinsfile)"
        )

    return problems


def validate_implementation_entry_criteria(registry: dict) -> list[str]:
    """Check that all Stage 7 prerequisites are satisfied."""
    problems: list[str] = []
    problems.extend(validate_architecture_contracts(registry))
    problems.extend(validate_test_strategy_complete(registry))
    problems.extend(validate_risk_spikes(registry))
    problems.extend(validate_risk_spike_resolution(registry))
    return problems


def validate_release_ready(_registry: dict) -> list[str]:
    """Check RELEASE_READINESS.md exists and has a go/no-go decision."""
    problems: list[str] = []

    rr_path = workspace_path("PROGRAMBUILD/RELEASE_READINESS.md")
    if not rr_path.exists():
        problems.append("RELEASE_READINESS.md does not exist (See: shape-release-readiness.prompt.md)")
        return problems

    text = rr_path.read_text(encoding="utf-8")

    # Check Go / No-Go Decision section has a real decision
    decision_match = re.search(
        r"^## Go / No-Go Decision\s*\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not decision_match:
        problems.append("RELEASE_READINESS.md: no '## Go / No-Go Decision' section found")
    else:
        decision_text = decision_match.group(1).strip()
        if not decision_text or decision_text.lower() == "decision:":
            problems.append(
                "RELEASE_READINESS.md: Go / No-Go Decision section is empty — replace 'Decision:' with the actual decision"
            )
        elif not re.search(r"(?i)\b(go|no.go|hold|approved|blocked)\b", decision_text):
            problems.append(
                "RELEASE_READINESS.md: Go / No-Go Decision has no clear decision keyword "
                "(expected: go, no-go, hold, approved, or blocked)"
            )

    return problems


def validate_audit_complete(_registry: dict) -> list[str]:
    """Check AUDIT_REPORT.md exists and has a findings list."""
    problems: list[str] = []

    audit_path = workspace_path("PROGRAMBUILD/AUDIT_REPORT.md")
    if not audit_path.exists():
        problems.append("AUDIT_REPORT.md does not exist (See: PROGRAMBUILD.md §16)")
        return problems

    text = audit_path.read_text(encoding="utf-8")

    rows = parse_markdown_table(text, "Findings")
    real_rows = [r for r in rows if r.get("Finding", "").strip()]

    if not real_rows:
        problems.append("AUDIT_REPORT.md: Findings table has no entries — complete the audit before marking Stage 9 done")

    return problems


def validate_post_launch_review(_registry: dict) -> list[str]:
    """Check POST_LAUNCH_REVIEW.md exists and has meaningful content."""
    problems: list[str] = []
    plr_path = workspace_path("PROGRAMBUILD/POST_LAUNCH_REVIEW.md")
    if not plr_path.exists():
        problems.append("POST_LAUNCH_REVIEW.md does not exist (required for Stage 10)")
        return problems
    text = plr_path.read_text(encoding="utf-8")
    # Require at least one non-blank, non-heading, non-metadata line of real content
    content_lines = [
        ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#") and not ln.strip().startswith("---")
    ]
    if len(content_lines) < 3:
        problems.append("POST_LAUNCH_REVIEW.md appears to be a stub — add review content before Stage 10 advance")
    return problems


def validate_registry(registry: dict) -> list[str]:
    problems: list[str] = []
    if "systems" not in registry or "sync_rules" not in registry:
        problems.append("config/process-registry.json is missing top-level systems or sync_rules keys")
    policy = cast(dict[str, Any], registry.get("repo_boundary_policy", {}))
    if policy.get("enabled"):
        docs = cast(list[dict[str, Any]], policy.get("docs", []))
        if not docs:
            problems.append("config/process-registry.json repo_boundary_policy must declare docs when enabled")
        for index, rule in enumerate(docs, start=1):
            if not rule.get("path"):
                problems.append(f"config/process-registry.json repo_boundary_policy docs[{index}] is missing path")
            must_contain = cast(list[str], rule.get("must_contain", []))
            if not must_contain:
                problems.append(
                    f"config/process-registry.json repo_boundary_policy docs[{index}] must declare at least one required phrase"
                )
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
        raw = clean_md(row.get("Canonical file", ""))
        if not raw:
            continue
        if "/" in raw:
            # Cross-system or docs/ path — validate it exists rather than checking set membership
            if not workspace_path(raw).exists():
                problems.append(f"PROGRAMBUILD_CANONICAL.md authority map references missing file: {raw}")
        else:
            target = Path(raw).name
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


def enforce_engineering_ready_in_all(registry: dict, system_filter: str | None = None) -> bool:
    if system_filter == "programbuild":
        return False
    validation = cast(dict[str, Any], registry.get("validation", {}))
    return bool(validation.get("enforce_engineering_ready_in_all", False))


def expected_bootstrap_assets() -> set[str]:
    root = workspace_path(".")
    expected: set[str] = {
        ".secrets.baseline",
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".gitlint",
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
        "dashboard/*",
        "docs/*.md",
        "docs/decisions/*.md",
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
    workspace = registry.get("workspace", {})
    assets = set(cast(list[str], workspace.get("bootstrap_assets", [])))
    uj_assets = set(cast(list[str], workspace.get("userjourney_bootstrap_assets", [])))
    uj_absent = system_is_optional_and_absent(registry, "userjourney")
    all_assets = assets | uj_assets
    missing = sorted(expected_bootstrap_assets() - all_assets)
    if missing:
        problems.append("bootstrap_assets is missing current workspace files: " + ", ".join(missing))
    for asset in sorted(all_assets):
        if uj_absent and asset in uj_assets:
            continue
        if not workspace_path(asset).exists():
            problems.append(f"bootstrap_assets references missing workspace file: {asset}")
    return problems


def validate_repo_boundary_policy(registry: dict) -> list[str]:
    policy = cast(dict[str, Any], registry.get("repo_boundary_policy", {}))
    if not policy.get("enabled"):
        return []

    problems: list[str] = []
    for rule in cast(list[dict[str, Any]], policy.get("docs", [])):
        relative_path = str(rule.get("path", ""))
        path = workspace_path(relative_path)
        if not path.exists():
            problems.append(f"repo boundary policy references missing file: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for required_phrase in cast(list[str], rule.get("must_contain", [])):
            if required_phrase not in text:
                problems.append(f"repo boundary policy phrase missing from {relative_path}: {required_phrase}")
    return problems


def validate_prompt_registry_completeness(registry: dict) -> list[str]:
    problems: list[str] = []
    prompt_registry = cast(dict[str, Any], registry.get("prompt_registry", {}))
    class_keys = ("workflow_prompt_files", "operator_prompt_files", "internal_prompt_files")
    seen_classes: dict[str, list[str]] = {}
    registered_paths: set[str] = set()

    for class_key in class_keys:
        for raw_path in cast(list[str], prompt_registry.get(class_key, [])):
            relative_path = raw_path.replace("\\", "/")
            seen_classes.setdefault(relative_path, []).append(class_key)

            if not relative_path.startswith(".github/prompts/"):
                problems.append(f"prompt_registry contains non-prompt path in {class_key}: {relative_path}")
                continue
            if not relative_path.endswith(".prompt.md"):
                problems.append(f"prompt_registry contains non-.prompt.md entry in {class_key}: {relative_path}")
            if class_key == "internal_prompt_files" and not relative_path.startswith(".github/prompts/internal/"):
                problems.append(f"prompt_registry internal prompt is outside .github/prompts/internal/: {relative_path}")
            if class_key != "internal_prompt_files" and relative_path.startswith(".github/prompts/internal/"):
                problems.append(f"prompt_registry public prompt class contains internal prompt: {relative_path}")
            if not workspace_path(relative_path).exists():
                problems.append(f"prompt_registry references missing prompt file: {relative_path}")

            registered_paths.add(relative_path)

    for relative_path, class_names in sorted(seen_classes.items()):
        if len(class_names) > 1:
            problems.append(
                f"prompt_registry duplicates prompt file across classes: {relative_path} ({', '.join(sorted(class_names))})"
            )

    prompts_root = workspace_path(".github/prompts")
    on_disk_prompt_files: set[str] = set()
    if prompts_root.exists():
        on_disk_prompt_files.update(f".github/prompts/{path.name}" for path in prompts_root.glob("*.prompt.md"))
        internal_root = prompts_root / "internal"
        if internal_root.exists():
            on_disk_prompt_files.update(
                f".github/prompts/internal/{path.relative_to(internal_root).as_posix()}"
                for path in internal_root.rglob("*.prompt.md")
            )

    missing_from_registry = sorted(on_disk_prompt_files - registered_paths)
    for relative_path in missing_from_registry:
        problems.append(f"prompt_registry missing on-disk prompt file: {relative_path}")

    return problems


def _markdown_section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def validate_prompt_authority_metadata(registry: dict) -> list[str]:
    problems: list[str] = []
    prompt_registry = cast(dict[str, Any], registry.get("prompt_registry", {}))
    public_prompts = set(cast(list[str], prompt_registry.get("workflow_prompt_files", []))) | set(
        cast(list[str], prompt_registry.get("operator_prompt_files", []))
    )
    prompt_authority = cast(dict[str, Any], registry.get("prompt_authority", {}))

    for prompt_path, payload in sorted(prompt_authority.items()):
        if prompt_path not in public_prompts:
            problems.append(f"prompt_authority references prompt outside public prompt_registry: {prompt_path}")
            continue

        path = workspace_path(prompt_path)
        if not path.exists():
            problems.append(f"prompt_authority references missing prompt file: {prompt_path}")
            continue

        authority_files = cast(list[str], cast(dict[str, Any], payload).get("authority_files", []))
        if not authority_files:
            problems.append(f"prompt_authority entry has no authority_files: {prompt_path}")
            continue
        if len(authority_files) != len(set(authority_files)):
            problems.append(f"prompt_authority entry contains duplicate authority_files: {prompt_path}")

        text = path.read_text(encoding="utf-8")
        section = _markdown_section(text, "Authority Loading")
        if not section:
            problems.append(f"prompt_authority entry points at prompt without '## Authority Loading' section: {prompt_path}")
            continue

        for authority_path in authority_files:
            if not workspace_path(authority_path).exists():
                problems.append(f"prompt_authority references missing authority file for {prompt_path}: {authority_path}")
            if authority_path not in section:
                problems.append(
                    f"prompt_authority expects '{authority_path}' in Authority "
                    f"Loading for {prompt_path}, but prompt text is missing it"
                )

    for prompt_path in sorted(public_prompts):
        path = workspace_path(prompt_path)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        section = _markdown_section(text, "Authority Loading")
        if section and prompt_path not in prompt_authority:
            problems.append(f"prompt_authority missing metadata for prompt with '## Authority Loading': {prompt_path}")

    return problems


def validate_prompt_generation_boundary(registry: dict) -> list[str]:
    """Validate which prompt families are generated artifacts versus manual prompt surfaces."""
    problems: list[str] = []
    prompt_generation = cast(dict[str, Any], registry.get("prompt_generation", {}))
    if not prompt_generation:
        return problems

    artifact_root = str(prompt_generation.get("artifact_root", "")).strip().replace("\\", "/")
    managed_stage_prompts = cast(list[dict[str, Any]], prompt_generation.get("managed_stage_prompts", []))
    prompt_registry = cast(dict[str, Any], registry.get("prompt_registry", {}))
    public_prompt_files = set(cast(list[str], prompt_registry.get("workflow_prompt_files", []))) | set(
        cast(list[str], prompt_registry.get("operator_prompt_files", []))
    )
    internal_prompt_files = set(cast(list[str], prompt_registry.get("internal_prompt_files", [])))
    registered_prompt_files = public_prompt_files | internal_prompt_files

    for prompt_path in sorted(public_prompt_files):
        path = workspace_path(prompt_path)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if text.startswith("# AUTO-GENERATED by programstart prompt-build"):
            problems.append(f"public prompt must be manually maintained, not prompt-build generated: {prompt_path}")

    try:
        from .programstart_prompt_build import build_prompt
    except ImportError:  # pragma: no cover - standalone script execution fallback
        from programstart_prompt_build import build_prompt

    seen_paths: set[str] = set()
    seen_stages: set[str] = set()
    for entry in managed_stage_prompts:
        stage = str(entry.get("stage", "")).strip()
        prompt_path = str(entry.get("path", "")).strip().replace("\\", "/")
        if not stage or not prompt_path:
            problems.append("prompt_generation managed_stage_prompts entries must include non-empty stage and path")
            continue
        if stage in seen_stages:
            problems.append(f"prompt_generation duplicates managed stage entry: {stage}")
        seen_stages.add(stage)
        if prompt_path in seen_paths:
            problems.append(f"prompt_generation duplicates managed prompt path: {prompt_path}")
        seen_paths.add(prompt_path)
        if artifact_root and not prompt_path.startswith(f"{artifact_root}/"):
            problems.append(f"prompt_generation managed prompt path is outside artifact_root: {prompt_path}")
        if prompt_path in registered_prompt_files:
            problems.append(f"prompt_generation managed prompt path must not appear in prompt_registry: {prompt_path}")

        path = workspace_path(prompt_path)
        if not path.exists():
            problems.append(f"prompt_generation managed prompt is missing on disk: {prompt_path}")
            continue
        expected = build_prompt(stage, registry=registry)
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            problems.append(
                f"prompt_generation managed prompt is out of date for stage "
                f"'{stage}': {prompt_path}; run 'uv run programstart "
                "prompt-build --sync-managed'"
            )

    return problems


def validate_rule_enforcement(registry: dict) -> list[str]:
    """Verify that structural rules from the authority model are enforced.

    Checks:
    1. Every authority file referenced in sync_rules exists.
    2. Every system has a canonical authority doc and a file index.
    3. Agent definitions reference valid systems.
    4. Health probe, assessment prompts, and enforcement scripts exist.
    5. All CLI commands in registry are covered by the dispatch.
    """
    problems: list[str] = []
    repo_role = cast(dict[str, Any], registry.get("workspace", {})).get("repo_role", "template_repo")

    # 1. Sync rule files exist (skip rules for optional absent systems)
    for rule in registry.get("sync_rules", []):
        rule_system = rule.get("system", "")
        if rule_system and rule_system in registry.get("systems", {}) and system_is_optional_and_absent(registry, rule_system):
            continue
        for f in rule.get("authority_files", []):
            if not workspace_path(f).exists():
                problems.append(f"sync_rules[{rule['name']}]: authority file missing: {f}")
        for f in rule.get("dependent_files", []):
            if not workspace_path(f).exists():
                problems.append(f"sync_rules[{rule['name']}]: dependent file missing: {f}")

    # 2. Every system has canonical + index
    for system_name, sys_cfg in registry.get("systems", {}).items():
        root = sys_cfg.get("root", "")
        if system_is_optional_and_absent(registry, system_name):
            continue
        if system_name == "programbuild":
            canonical = workspace_path(f"{root}/PROGRAMBUILD_CANONICAL.md")
            file_index = workspace_path(f"{root}/PROGRAMBUILD_FILE_INDEX.md")
            if not canonical.exists():
                problems.append(f"{system_name}: missing PROGRAMBUILD_CANONICAL.md")
            if not file_index.exists():
                problems.append(f"{system_name}: missing PROGRAMBUILD_FILE_INDEX.md")

    # 3. Required assessment infrastructure
    required_infra = [
        "scripts/programstart_health_probe.py",
        "scripts/programstart_validate.py",
        "scripts/programstart_drift_check.py",
        "scripts/programstart_status.py",
        "scripts/programstart_workflow_state.py",
        "scripts/check_commit_msg.py",
        ".github/prompts/programstart-cross-stage-validation.prompt.md",
        ".github/prompts/programstart-stage-transition.prompt.md",
        ".github/prompts/programstart-what-next.prompt.md",
        ".github/prompts/propagate-canonical-change.prompt.md",
        ".github/instructions/source-of-truth.instructions.md",
        ".github/instructions/conventional-commits.instructions.md",
        ".github/agents/architecture-security.agent.md",
        ".github/agents/discovery-scoping.agent.md",
        ".github/agents/quality-release.agent.md",
        "docs/decisions/README.md",
    ]
    if repo_role == "template_repo":
        required_infra.append(".github/prompts/audit-process-drift.prompt.md")
    for path in required_infra:
        if not workspace_path(path).exists():
            problems.append(f"missing required assessment infrastructure: {path}")

    problems.extend(validate_prompt_registry_completeness(registry))
    problems.extend(validate_prompt_authority_metadata(registry))

    # 4. Instruction files exist and reference valid patterns
    instruction_files = [
        ".github/instructions/programbuild.instructions.md",
        ".github/instructions/userjourney.instructions.md",
    ]
    for path in instruction_files:
        if not workspace_path(path).exists():
            problems.append(f"missing instruction file: {path}")

    # 6. bootstrap_assets coverage: any new instruction file, decision record, or
    #    enforcement script (check_*.py) in bootstrap_assets must appear in either
    #    required_infra or a sync_rule. This catches new governance files added to
    #    bootstrap without being wired into enforcement.
    bootstrap_assets = set(cast(list[str], registry.get("workspace", {}).get("bootstrap_assets", [])))
    all_synced_files: set[str] = set()
    for rule in registry.get("sync_rules", []):
        all_synced_files.update(rule.get("authority_files", []))
        all_synced_files.update(rule.get("dependent_files", []))
    required_infra_set = set(required_infra)
    known_instruction_files = set(instruction_files)
    covered = required_infra_set | all_synced_files | known_instruction_files

    def _should_cover(asset: str) -> bool:
        """Return True if this asset type requires enforcement coverage."""
        if asset.startswith(".github/instructions/") and asset.endswith(".md"):
            return True
        if asset.startswith("docs/decisions/") and asset.endswith(".md"):
            return True
        name = Path(asset).name
        if asset.startswith("scripts/") and name.startswith("check_") and name.endswith(".py"):
            return True
        return False

    for asset in sorted(bootstrap_assets):
        if not _should_cover(asset):
            continue
        if asset not in covered:
            problems.append(
                f"bootstrap_assets governance file not covered by required_infra, instruction_files, or any sync_rule: {asset}"
            )

    # 7. ADR number sequencing — docs/decisions/NNNN-title.md must be sequential with no gaps
    decisions_dir = workspace_path("docs/decisions")
    if decisions_dir.exists():
        adr_numbers: list[int] = []
        for adr_path in sorted(decisions_dir.glob("*.md")):
            if adr_path.name == "README.md":
                continue
            m = re.match(r"^(\d{4})-", adr_path.name)
            if m:
                adr_numbers.append(int(m.group(1)))
            else:
                problems.append(f"docs/decisions file does not follow NNNN-title.md naming: {adr_path.name}")
        for expected, actual in enumerate(sorted(adr_numbers), start=1):
            if actual != expected:
                problems.append(f"docs/decisions ADR sequence gap: expected {expected:04d} but found {actual:04d}")
                break

    # 5. copilot-instructions.md references key rules
    copilot_path = workspace_path(".github/copilot-instructions.md")
    if copilot_path.exists():
        text = copilot_path.read_text(encoding="utf-8")
        required_phrases = [
            "Repository boundary is explicit",
            "process-registry.json",
            "scripts/programstart_status.py",
            "scripts/programstart_validate.py",
            "scripts/programstart_drift_check.py",
            "Conventional Commits",
            "docs/decisions",
            "RFC 2119",
        ]
        for phrase in required_phrases:
            if phrase not in text:
                problems.append(f"copilot-instructions.md missing rule reference: {phrase}")

    return problems


def validate_adr_coverage(registry: dict) -> list[str]:
    """Warn about DECISION_LOG.md entries that have no corresponding ADR in docs/decisions/."""
    warnings: list[str] = []
    decision_log = workspace_path("PROGRAMBUILD/DECISION_LOG.md")
    if not decision_log.exists():
        return warnings
    text = decision_log.read_text(encoding="utf-8")
    rows = parse_markdown_table(text, "Decision Register")
    if not rows:
        return warnings

    decisions_dir = workspace_path("docs/decisions")
    adr_texts: dict[str, str] = {}
    if decisions_dir.exists():
        for adr_path in decisions_dir.glob("*.md"):
            if adr_path.name == "README.md":
                continue
            adr_texts[adr_path.name] = adr_path.read_text(encoding="utf-8")

    for row in rows:
        dec_id = row.get("ID", "").strip()
        status = row.get("Status", "").strip().upper()
        if status not in ("ACTIVE", "ACCEPTED", "REVERSED"):
            continue
        if not dec_id:
            continue
        # Check if any ADR references this decision ID
        found = any(dec_id in content for content in adr_texts.values())
        if not found:
            decision_text = row.get("Decision", "").strip()
            warnings.append(f"{dec_id} ({decision_text[:60]}) is {status} but has no corresponding ADR in docs/decisions/")
    return warnings


def _parse_markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    frontmatter: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def _adr_title(text: str) -> str:
    match = re.search(r"^#\s+\d{4}\.\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _normalize_adr_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().casefold()


def _adr_decision_link(text: str) -> str:
    match = re.search(r"<!--\s*(DEC-\d{3})\s*-->", text)
    return match.group(1) if match else ""


def _adr_readme_entries(readme_text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    for row in parse_markdown_table(readme_text, "Index"):
        raw_id = row.get("ID", "").strip()
        link_match = re.match(r"\[(\d{4})\]\(([^)]+)\)", raw_id)
        if not link_match:
            continue
        adr_id, target = link_match.groups()
        entries[adr_id] = {
            "target": target.strip(),
            "title": row.get("Title", "").strip(),
            "status": row.get("Status", "").strip(),
            "date": row.get("Date", "").strip(),
        }
    return entries


def _legacy_pre_register_adr_ids(registry: dict) -> set[str]:
    policy = cast(dict[str, Any], registry.get("adr_policy", {}))
    return {
        str(item).strip()
        for item in cast(list[str], policy.get("legacy_pre_register_adrs", []))
        if re.fullmatch(r"\d{4}", str(item).strip())
    }


def validate_adr_coherence(registry: dict) -> list[str]:
    """Validate ADR frontmatter, README index, and DECISION_LOG linkage coherence."""
    problems: list[str] = []
    decisions_dir = workspace_path("docs/decisions")
    readme_path = decisions_dir / "README.md"
    decision_log_path = workspace_path("PROGRAMBUILD/DECISION_LOG.md")
    legacy_pre_register_ids = _legacy_pre_register_adr_ids(registry)
    repo_role = cast(dict[str, Any], registry.get("workspace", {})).get("repo_role", "template_repo")

    if not decisions_dir.exists() or not readme_path.exists() or not decision_log_path.exists():
        return problems

    readme_entries = _adr_readme_entries(readme_path.read_text(encoding="utf-8"))
    decision_rows = parse_markdown_table(decision_log_path.read_text(encoding="utf-8"), "Decision Register")
    decision_row_by_id = {row.get("ID", "").strip(): row for row in decision_rows if row.get("ID", "").strip()}
    adr_status_by_name: dict[str, str] = {}
    decision_row_by_adr_name: dict[str, dict[str, str]] = {}

    for row in decision_rows:
        related_file = row.get("Related file", "").strip()
        match = re.search(r"docs/decisions/(\d{4}-[^\s|,]+\.md)", related_file)
        if match:
            decision_row_by_adr_name[match.group(1)] = row

    for legacy_id in sorted(legacy_pre_register_ids):
        if not any(path.name.startswith(f"{legacy_id}-") for path in decisions_dir.glob("*.md")):
            problems.append(f"adr_policy legacy_pre_register_adrs references missing ADR file: {legacy_id}")

    for adr_path in sorted(decisions_dir.glob("*.md")):
        if adr_path.name == "README.md":
            continue

        adr_text = adr_path.read_text(encoding="utf-8")
        frontmatter = _parse_markdown_frontmatter(adr_text)
        adr_id_match = re.match(r"^(\d{4})-", adr_path.name)
        adr_id = adr_id_match.group(1) if adr_id_match else ""
        title = _adr_title(adr_text)
        dec_id = _adr_decision_link(adr_text)
        status = frontmatter.get("status", "")
        date = frontmatter.get("date", "")
        is_legacy_pre_register = adr_id in legacy_pre_register_ids
        adr_status_by_name[adr_path.name] = status

        if not frontmatter:
            problems.append(f"ADR missing YAML frontmatter: {adr_path.name}")
        if not title:
            problems.append(f"ADR missing MADR title heading: {adr_path.name}")
        if is_legacy_pre_register and dec_id:
            problems.append(f"legacy pre-register ADR should not declare a DECISION_LOG linkage comment: {adr_path.name}")
        if not is_legacy_pre_register and not dec_id:
            problems.append(f"ADR missing decision-log linkage comment <!-- DEC-xxx -->: {adr_path.name}")
        elif (
            not is_legacy_pre_register
            and dec_id not in decision_row_by_id
            and not (repo_role == "project_repo" and adr_path.name not in decision_row_by_adr_name)
        ):
            if dec_id:
                problems.append(f"ADR references unknown DECISION_LOG entry {dec_id}: {adr_path.name}")
        if is_legacy_pre_register and adr_path.name in decision_row_by_adr_name:
            problems.append(
                "legacy pre-register ADR is referenced by "
                f"PROGRAMBUILD/DECISION_LOG.md and must not remain legacy-classified: {adr_path.name}"
            )

        readme_entry = readme_entries.get(adr_id)
        if not readme_entry:
            problems.append(f"ADR missing from docs/decisions/README.md index: {adr_path.name}")
        else:
            if readme_entry["target"] != adr_path.name:
                problems.append(
                    f"ADR README target mismatch for {adr_id}: expected {adr_path.name} but found {readme_entry['target']}"
                )
            if title and _normalize_adr_title(readme_entry["title"]) != _normalize_adr_title(title):
                problems.append(
                    f"ADR README title mismatch for {adr_path.name}: expected '{title}' but found '{readme_entry['title']}'"
                )
            if status and readme_entry["status"] != status:
                problems.append(
                    f"ADR README status mismatch for {adr_path.name}: expected '{status}' but found '{readme_entry['status']}'"
                )
            if date and readme_entry["date"] != date:
                problems.append(
                    f"ADR README date mismatch for {adr_path.name}: expected '{date}' but found '{readme_entry['date']}'"
                )

        superseded_match = re.fullmatch(r"superseded by ADR-(\d{4})", status)
        if superseded_match:
            superseding_name_prefix = superseded_match.group(1)
            has_target = any(path.name.startswith(f"{superseding_name_prefix}-") for path in decisions_dir.glob("*.md"))
            if not has_target:
                problems.append(
                    f"ADR {adr_path.name} is superseded by ADR-{superseding_name_prefix} but that ADR file does not exist"
                )

    for readme_entry in readme_entries.values():
        target_path = decisions_dir / readme_entry["target"]
        if not target_path.exists():
            problems.append(f"ADR README index points to missing file: {readme_entry['target']}")

    for row in decision_rows:
        dec_id = row.get("ID", "").strip()
        status = row.get("Status", "").strip().upper()
        if status not in {"ACTIVE", "REVERSED"}:
            continue
        related_file = row.get("Related file", "").strip()
        match = re.search(r"docs/decisions/(\d{4}-[^\s|,]+\.md)", related_file)
        if not match:
            continue
        adr_name = match.group(1)
        adr_id = adr_name[:4]
        if adr_id in legacy_pre_register_ids:
            problems.append(
                f"{dec_id} references legacy pre-register ADR {adr_name}; "
                "remove the legacy classification or point at a post-register ADR"
            )
        adr_status = adr_status_by_name.get(adr_name, "")
        if adr_status.startswith("superseded by ADR-"):
            problems.append(
                f"{dec_id} references superseded ADR {adr_name} in PROGRAMBUILD/DECISION_LOG.md; update it to the current ADR"
            )

    return problems


def validate_decision_log_reversal_invariants(_registry: dict) -> list[str]:
    problems: list[str] = []
    decision_log_path = workspace_path("PROGRAMBUILD/DECISION_LOG.md")
    if not decision_log_path.exists():
        return problems

    rows = parse_markdown_table(decision_log_path.read_text(encoding="utf-8"), "Decision Register")
    if not rows:
        return problems

    rows_by_id = {row.get("ID", "").strip(): row for row in rows if row.get("ID", "").strip()}
    reversed_by_target: dict[str, list[str]] = {}
    superseded_by_target: dict[str, list[str]] = {}

    for row in rows:
        dec_id = row.get("ID", "").strip()
        status = row.get("Status", "").strip().upper()
        replaces = row.get("Replaces", "").strip()
        if status == "REVERSED":
            if not replaces or replaces == "—":
                problems.append(f"{dec_id} is REVERSED but Replaces is empty")
                continue
            if replaces == dec_id:
                problems.append(f"{dec_id} cannot reverse itself")
                continue
            target = rows_by_id.get(replaces)
            if target is None:
                problems.append(f"{dec_id} reverses missing decision {replaces}")
                continue
            reversed_by_target.setdefault(replaces, []).append(dec_id)
            target_status = target.get("Status", "").strip().upper()
            target_replaces = target.get("Replaces", "").strip()
            if target_status != "SUPERSEDED":
                problems.append(
                    f"{dec_id} reverses {replaces}, but {replaces} is {target_status or 'missing a status'} instead of SUPERSEDED"
                )
            if target_replaces != dec_id:
                problems.append(f"{dec_id} reverses {replaces}, but {replaces} must point back via Replaces={dec_id}")
        elif status == "SUPERSEDED":
            if not replaces or replaces == "—":
                problems.append(f"{dec_id} is SUPERSEDED but Replaces is empty")
                continue
            if replaces == dec_id:
                problems.append(f"{dec_id} cannot supersede itself")
                continue
            target = rows_by_id.get(replaces)
            if target is None:
                problems.append(f"{dec_id} is SUPERSEDED by missing decision {replaces}")
                continue
            superseded_by_target.setdefault(replaces, []).append(dec_id)
            target_status = target.get("Status", "").strip().upper()
            target_replaces = target.get("Replaces", "").strip()
            if target_status != "REVERSED":
                problems.append(
                    f"{dec_id} is SUPERSEDED by {replaces}, but {replaces} is "
                    f"{target_status or 'missing a status'} instead of REVERSED"
                )
            if target_replaces != dec_id:
                problems.append(f"{dec_id} is SUPERSEDED by {replaces}, but {replaces} must point back via Replaces={dec_id}")

    for target, dec_ids in reversed_by_target.items():
        if len(dec_ids) > 1:
            problems.append(f"Decision {target} is reversed more than once: {', '.join(sorted(dec_ids))}")
    for target, dec_ids in superseded_by_target.items():
        if len(dec_ids) > 1:
            problems.append(f"Decision {target} supersedes more than one original row: {', '.join(sorted(dec_ids))}")

    return problems


def validate_test_coverage(registry: dict) -> list[str]:
    """Warn about production scripts that have no matching test file."""
    warnings: list[str] = []
    scripts_dir = workspace_path("scripts")
    tests_dir = workspace_path("tests")
    if not scripts_dir.exists():
        return warnings
    EXCLUDED_SUFFIXES = ("_smoke.py", "_smoke_readonly.py")
    EXCLUDED_NAMES = {"__init__.py", "programstart_smoke_helpers.py", "programstart_dashboard_golden.py"}
    for script in sorted(scripts_dir.glob("*.py")):
        if script.name in EXCLUDED_NAMES or any(script.name.endswith(s) for s in EXCLUDED_SUFFIXES):
            continue
        test_file = tests_dir / f"test_{script.name}"
        if not test_file.exists():
            warnings.append(f"no test file for script: scripts/{script.name} (expected tests/test_{script.name})")
    return warnings


def validate_coverage_source_completeness(_registry: dict) -> list[str]:
    """Warn about production scripts not registered in [tool.coverage.run].source."""
    import tomllib

    problems: list[str] = []
    scripts_dir = workspace_path("scripts")
    if not scripts_dir.exists():
        return problems
    pyproject = workspace_path("pyproject.toml")
    if not pyproject.exists():
        return problems
    config = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    source_list = config.get("tool", {}).get("coverage", {}).get("run", {}).get("source", [])
    source_modules = {s.replace("scripts.", "") for s in source_list}
    EXCLUDED_SUFFIXES = ("_smoke.py", "_smoke_readonly.py")
    EXCLUDED_NAMES = {"__init__.py", "programstart_smoke_helpers.py", "programstart_dashboard_golden.py"}
    for script in sorted(scripts_dir.glob("*.py")):
        if script.name in EXCLUDED_NAMES or any(script.name.endswith(s) for s in EXCLUDED_SUFFIXES):
            continue
        module_name = script.stem
        if module_name not in source_modules:
            problems.append(f"scripts/{script.name} is not in [tool.coverage.run].source in pyproject.toml")
    return problems


def validate_kb_freshness(_registry: dict) -> list[str]:
    """Warn about knowledge-base tracks whose last_review_date exceeds freshness_days."""
    warnings: list[str] = []
    kb_path = workspace_path("config/knowledge-base.json")
    if not kb_path.exists():
        return warnings
    kb = json.loads(kb_path.read_text(encoding="utf-8"))
    today = datetime.date.today()
    for track in kb.get("research_ledger", {}).get("tracks", []):
        name = track.get("name", "<unnamed>")
        freshness_days = track.get("freshness_days")
        last_review = track.get("last_review_date")
        if freshness_days is None or last_review is None:
            warnings.append(f"KB track '{name}' missing freshness_days or last_review_date")
            continue
        try:
            review_date = datetime.date.fromisoformat(last_review)
        except ValueError:
            warnings.append(f"KB track '{name}' has invalid last_review_date: {last_review}")
            continue
        age = (today - review_date).days
        if age > freshness_days:
            warnings.append(f"KB track '{name}' is stale: last reviewed {last_review} ({age}d ago, limit {freshness_days}d)")
    return warnings


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
            if status not in {"planned", "in_progress", "completed", "blocked"}:
                problems.append(f"{system} step '{step}' has invalid status value: '{status}'")
            if status == "in_progress":
                in_progress_steps.append(step)
            if index < active_index and status != "completed":
                problems.append(f"{system} step '{step}' must be completed before active step '{active_step}'")
            if index < active_index and decision not in ("approved", "go", "accepted"):
                problems.append(f"{system} step '{step}' is missing approved sign-off before active step '{active_step}'")
            if index < active_index and not signoff_date:
                problems.append(f"{system} step '{step}' is missing sign-off date before active step '{active_step}'")
            if signoff_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", signoff_date):
                problems.append(f"{system} step '{step}' has invalid signoff date format: '{signoff_date}' (expected YYYY-MM-DD)")
            if index > active_index and status == "completed":
                problems.append(f"{system} step '{step}' cannot be completed after the active step '{active_step}'")
        if len(in_progress_steps) != 1:
            problems.append(f"{system} must have exactly one in_progress step; found {len(in_progress_steps)}")
        elif in_progress_steps[0] != active_step:
            problems.append(f"{system} active step '{active_step}' does not match in_progress step '{in_progress_steps[0]}'")
    return problems


ALLOWED_ROOT_MD = {
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "QUICKSTART.md",
    "n8n.md",
}

ALLOWED_ROOT_NON_MD = {
    "CODEOWNERS",
}


def validate_file_hygiene(_registry: dict) -> list[str]:
    """Check that no unexpected .md files sit at the repo root."""
    problems: list[str] = []
    root = workspace_path(".")
    for md in sorted(root.glob("*.md")):
        if md.name not in ALLOWED_ROOT_MD:
            problems.append(f"Unexpected .md file at repo root: {md.name} — should it be in devlog/ or outputs/?")
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
            "repo-boundary",
            "rule-enforcement",
            "test-coverage",
            "template-test-coverage",
            "adr-coverage",
            "adr-coherence",
            "decision-log-coherence",
            "prompt-authority",
            "prompt-generation",
            "placeholder-content",
            "kb-freshness",
            "intake-complete",
            "feasibility-criteria",
            "research-complete",
            "requirements-complete",
            "architecture-contracts",
            "risk-spikes",
            "risk-spikes-resolved",
            "test-strategy-complete",
            "scaffold-complete",
            "implementation-entry",
            "release-ready",
            "audit-complete",
            "post-launch-review",
            "coverage-source",
            "file-hygiene",
        ],
        default="all",
    )
    parser.add_argument(
        "--system",
        choices=["programbuild", "userjourney"],
        help="Only validate this system.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit 1 if any warnings).",
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
        problems.extend(validate_repo_boundary_policy(registry))
        problems.extend(validate_rule_enforcement(registry))
        problems.extend(validate_bootstrap_assets(registry))
        if enforce_engineering_ready_in_all(registry, sf):
            problems.extend(validate_engineering_ready(registry))
        reference_problems, reference_warnings = validate_planning_references(registry)
        problems.extend(reference_problems)
        warnings.extend(metadata_warnings(registry, sf))
        warnings.extend(reference_warnings)
        warnings.extend(validate_test_coverage(registry))
        warnings.extend(validate_coverage_source_completeness(registry))
        warnings.extend(validate_adr_coverage(registry))
        problems.extend(validate_adr_coherence(registry))
        problems.extend(validate_decision_log_reversal_invariants(registry))
        problems.extend(validate_prompt_authority_metadata(registry))
        problems.extend(validate_prompt_generation_boundary(registry))
        placeholder_problems, placeholder_warnings = validate_placeholder_content(registry)
        problems.extend(placeholder_problems)
        warnings.extend(placeholder_warnings)
        warnings.extend(validate_kb_freshness(registry))
        warnings.extend(validate_file_hygiene(registry))
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
    elif args.check == "repo-boundary":
        problems.extend(validate_repo_boundary_policy(registry))
    elif args.check == "bootstrap-assets":
        problems.extend(validate_bootstrap_assets(registry))
    elif args.check == "rule-enforcement":
        problems.extend(validate_rule_enforcement(registry))
    elif args.check == "test-coverage" or args.check == "template-test-coverage":
        warnings.extend(validate_test_coverage(registry))
    elif args.check == "adr-coverage":
        warnings.extend(validate_adr_coverage(registry))
    elif args.check == "adr-coherence":
        problems.extend(validate_adr_coherence(registry))
    elif args.check == "decision-log-coherence":
        problems.extend(validate_decision_log_reversal_invariants(registry))
    elif args.check == "prompt-authority":
        problems.extend(validate_prompt_authority_metadata(registry))
    elif args.check == "prompt-generation":
        problems.extend(validate_prompt_generation_boundary(registry))
    elif args.check == "placeholder-content":
        placeholder_problems, placeholder_warnings = validate_placeholder_content(registry)
        problems.extend(placeholder_problems)
        warnings.extend(placeholder_warnings)
    elif args.check == "kb-freshness":
        warnings.extend(validate_kb_freshness(registry))
    elif args.check == "intake-complete":
        problems.extend(validate_intake_complete(registry))
    elif args.check == "feasibility-criteria":
        problems.extend(validate_feasibility_criteria(registry))
    elif args.check == "research-complete":
        problems.extend(validate_research_complete(registry))
    elif args.check == "requirements-complete":
        problems.extend(validate_requirements_complete(registry))
    elif args.check == "architecture-contracts":
        problems.extend(validate_architecture_contracts(registry))
    elif args.check == "risk-spikes":
        problems.extend(validate_risk_spikes(registry))
    elif args.check == "risk-spikes-resolved":
        problems.extend(validate_risk_spike_resolution(registry))
    elif args.check == "engineering-ready":
        problems.extend(validate_engineering_ready(registry))
    elif args.check == "test-strategy-complete":
        problems.extend(validate_test_strategy_complete(registry))
    elif args.check == "scaffold-complete":
        problems.extend(validate_scaffold_complete(registry))
    elif args.check == "implementation-entry":
        problems.extend(validate_implementation_entry_criteria(registry))
    elif args.check == "release-ready":
        problems.extend(validate_release_ready(registry))
    elif args.check == "audit-complete":
        problems.extend(validate_audit_complete(registry))
    elif args.check == "post-launch-review":
        problems.extend(validate_post_launch_review(registry))
    elif args.check == "coverage-source":
        warnings.extend(validate_coverage_source_completeness(registry))
    elif args.check == "file-hygiene":
        warnings.extend(validate_file_hygiene(registry))
    else:
        problems.extend(validate_engineering_ready(registry))

    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    if args.strict and warnings:
        print("Validation failed (strict mode) — warnings treated as errors:")
        for warning in warnings:
            print(f"- {warning}")
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
