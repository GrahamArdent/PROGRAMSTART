from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_bootstrap as bootstrap
from scripts import programstart_common as common
from scripts import programstart_validate as validate
from scripts.programstart_common import load_json, write_json


def build_registry() -> dict:
    return {
        "systems": {
            "programbuild": {
                "root": "PROGRAMBUILD",
                "control_files": ["PROGRAMBUILD/CONTROL.md"],
                "output_files": ["PROGRAMBUILD/OUTPUT.md"],
                "metadata_required": ["PROGRAMBUILD/OUTPUT.md"],
            },
            "userjourney": {
                "root": "USERJOURNEY",
                "optional": True,
                "core_files": ["USERJOURNEY/USERJOURNEY_STATE.json"],
                "metadata_required": [],
                "engineering_blocker_file": "USERJOURNEY/OPEN_QUESTIONS.md",
            },
        },
        "metadata_rules": {
            "required_prefixes": [
                "Purpose:",
                "Owner:",
                "Last updated:",
                "Depends on:",
                "Authority:",
            ],
            "owner_placeholder": "[ASSIGN]",
        },
        "sync_rules": [],
        "workflow_guidance": {},
        "planning_reference_rules": {
            "docs": [
                "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md",
                "USERJOURNEY/IMPLEMENTATION_PLAN.md",
            ],
            "workspace_prefixes": [
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
            "allowlist_manifest": "USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json",
        },
        "repo_boundary_policy": {
            "enabled": True,
            "docs": [
                {
                    "path": ".github/copilot-instructions.md",
                    "must_contain": ["Repository boundary is explicit"],
                }
            ],
        },
    }


def write_programbuild_authority_docs(tmp_path: Path, control_files: list[str], output_files: list[str]) -> None:
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir(parents=True, exist_ok=True)

    control_lines = "\n".join(f"- `{Path(path).name}`" for path in control_files if path.endswith(".md"))
    output_lines = "\n".join(f"- `{Path(path).name}`" for path in output_files if path.endswith(".md"))
    authority_map_rows = "\n".join(
        f"| concern {index} | `{Path(path).name}` |"
        for index, path in enumerate([*control_files, *output_files], start=1)
        if path.endswith(".md")
    )
    (programbuild / "PROGRAMBUILD_CANONICAL.md").write_text(
        "\n".join(
            [
                "# PROGRAMBUILD_CANONICAL.md",
                "",
                "## 2. Critical Naming Standard",
                "",
                "System control files:",
                control_lines,
                "",
                "Project execution outputs:",
                output_lines,
                "",
                "## 3. Authority Map",
                "",
                "| Concern | Canonical file |",
                "|---|---|",
                authority_map_rows,
                "",
            ]
        ),
        encoding="utf-8",
    )

    control_rows = "\n".join(
        f"| `{Path(path).name}` | control | active | purpose | authority |" for path in control_files if path.endswith(".md")
    )
    output_rows = "\n".join(
        f"| `{Path(path).name}` | output | active | purpose | authority |" for path in output_files if path.endswith(".md")
    )
    (programbuild / "PROGRAMBUILD_FILE_INDEX.md").write_text(
        "\n".join(
            [
                "# PROGRAMBUILD_FILE_INDEX.md",
                "",
                "## 1. Control Files",
                "",
                "| File | Type | Status | Purpose | Canonical for |",
                "|---|---|---|---|---|",
                control_rows,
                "",
                "## 2. Project Output Files",
                "",
                "| File | Type | Status | Purpose | Canonical for |",
                "|---|---|---|---|---|",
                output_rows,
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_validate_registry_reports_missing_sections() -> None:
    assert validate.validate_registry({})


def test_validate_registry_reports_invalid_repo_boundary_policy() -> None:
    problems = validate.validate_registry({"systems": {}, "sync_rules": [], "repo_boundary_policy": {"enabled": True}})
    assert any("repo_boundary_policy must declare docs" in item for item in problems)


def test_extract_bullets_after_marker_stops_at_next_marker() -> None:
    text = "\n".join(
        [
            "System control files:",
            "- `PROGRAMBUILD_CANONICAL.md`",
            "Project execution outputs:",
            "- `OUTPUT.md`",
        ]
    )

    items = validate.extract_bullets_after_marker(text, "System control files:")

    assert items == ["PROGRAMBUILD_CANONICAL.md"]


def test_extract_bullets_after_marker_returns_empty_when_marker_missing() -> None:
    assert validate.extract_bullets_after_marker("- `PROGRAMBUILD_CANONICAL.md`", "System control files:") == []


def test_validate_authority_sync_passes_on_current_repo() -> None:
    assert validate.validate_authority_sync(common.load_registry()) == []


def test_validate_authority_sync_reports_guidance_and_sync_rule_drift(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "systems": {
            "programbuild": {
                "root": "PROGRAMBUILD",
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md"],
                "output_files": ["PROGRAMBUILD/OUTPUT.md"],
                "metadata_required": [],
            },
            "userjourney": {
                "root": "USERJOURNEY",
                "optional": True,
                "core_files": ["USERJOURNEY/README.md"],
                "metadata_required": [],
                "engineering_blocker_file": "USERJOURNEY/OPEN_QUESTIONS.md",
            },
        },
        "sync_rules": [
            {
                "name": "bad_rule",
                "system": "programbuild",
                "authority_files": ["PROGRAMBUILD/MISSING.md"],
                "dependent_files": [],
            }
        ],
        "workflow_guidance": {
            "kickoff": {
                "files": ["PROGRAMBUILD/MISSING_GUIDE.md"],
                "scripts": [],
                "prompts": [],
            }
        },
    }
    write_programbuild_authority_docs(
        tmp_path,
        registry["systems"]["programbuild"]["control_files"],
        registry["systems"]["programbuild"]["output_files"],
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_authority_sync(registry)

    assert any("sync rule 'bad_rule' references undeclared" in item for item in problems)
    assert any("workflow guidance 'kickoff' references missing file" in item for item in problems)


def test_validate_authority_sync_reports_inventory_and_authority_map_drift(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "systems": {
            "programbuild": {
                "root": "PROGRAMBUILD",
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md"],
                "output_files": ["PROGRAMBUILD/OUTPUT.md"],
                "metadata_required": [],
            },
            "userjourney": {
                "root": "USERJOURNEY",
                "optional": True,
                "core_files": [],
                "metadata_required": [],
                "engineering_blocker_file": "USERJOURNEY/OPEN_QUESTIONS.md",
            },
        },
    }
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir(parents=True, exist_ok=True)
    (programbuild / "PROGRAMBUILD_CANONICAL.md").write_text(
        "\n".join(
            [
                "# PROGRAMBUILD_CANONICAL.md",
                "",
                "## 2. Critical Naming Standard",
                "",
                "System control files:",
                "- `PROGRAMBUILD_CANONICAL.md`",
                "",
                "Project execution outputs:",
                "- `WRONG_OUTPUT.md`",
                "",
                "## 3. Authority Map",
                "",
                "| Concern | Canonical file |",
                "|---|---|",
                "| concern | `UNKNOWN.md` |",
            ]
        ),
        encoding="utf-8",
    )
    (programbuild / "PROGRAMBUILD_FILE_INDEX.md").write_text(
        "\n".join(
            [
                "# PROGRAMBUILD_FILE_INDEX.md",
                "",
                "## 1. Control Files",
                "",
                "| File | Type | Status | Purpose | Canonical for |",
                "|---|---|---|---|---|",
                "| `PROGRAMBUILD_CANONICAL.md` | control | active | purpose | authority |",
                "",
                "## 2. Project Output Files",
                "",
                "| File | Type | Status | Purpose | Canonical for |",
                "|---|---|---|---|---|",
                "| `WRONG_OUTPUT.md` | output | active | purpose | authority |",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_authority_sync(registry)

    assert any("system control file list is out of sync" in item for item in problems)
    assert any("project execution output list is out of sync" in item for item in problems)
    assert any("control file table is out of sync" in item for item in problems)
    assert any("project output table is out of sync" in item for item in problems)
    assert any("authority map references unknown file" in item for item in problems)


def test_validate_authority_sync_reports_declared_missing_workspace_file(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "systems": {
            "programbuild": {
                "root": "PROGRAMBUILD",
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md"],
                "output_files": ["PROGRAMBUILD/OUTPUT.md"],
                "metadata_required": [],
            },
            "userjourney": {
                "root": "USERJOURNEY",
                "optional": False,
                "core_files": ["USERJOURNEY/README.md"],
                "metadata_required": [],
                "engineering_blocker_file": "USERJOURNEY/OPEN_QUESTIONS.md",
            },
        },
        "sync_rules": [
            {
                "name": "missing_declared",
                "system": "userjourney",
                "authority_files": ["USERJOURNEY/README.md"],
                "dependent_files": [],
            }
        ],
    }
    write_programbuild_authority_docs(
        tmp_path,
        registry["systems"]["programbuild"]["control_files"],
        registry["systems"]["programbuild"]["output_files"],
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_authority_sync(registry)

    assert problems == ["sync rule 'missing_declared' references missing workspace file: USERJOURNEY/README.md"]


def test_validate_authority_sync_skips_optional_absent_userjourney(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "systems": {
            "programbuild": {
                "root": "PROGRAMBUILD",
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md"],
                "output_files": ["PROGRAMBUILD/OUTPUT.md"],
                "metadata_required": [],
            },
            "userjourney": {
                "root": "USERJOURNEY",
                "optional": True,
                "core_files": ["USERJOURNEY/README.md"],
                "metadata_required": [],
                "engineering_blocker_file": "USERJOURNEY/OPEN_QUESTIONS.md",
            },
        },
        "sync_rules": [
            {
                "name": "skip_optional",
                "system": "userjourney",
                "authority_files": ["USERJOURNEY/README.md"],
                "dependent_files": ["USERJOURNEY/OPEN_QUESTIONS.md"],
            }
        ],
        "workflow_guidance": {
            "userjourney": {
                "phase_0": {
                    "files": ["USERJOURNEY/README.md"],
                    "scripts": [],
                    "prompts": [".github/prompts/userjourney-next-slice.prompt.md"],
                }
            }
        },
    }
    write_programbuild_authority_docs(
        tmp_path,
        registry["systems"]["programbuild"]["control_files"],
        registry["systems"]["programbuild"]["output_files"],
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(common, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_authority_sync(registry)

    assert problems == []


def test_validate_planning_references_detects_missing_workspace_and_external_refs(tmp_path: Path, monkeypatch) -> None:
    delivery = tmp_path / "USERJOURNEY" / "DELIVERY_GAMEPLAN.md"
    delivery.parent.mkdir(parents=True, exist_ok=True)
    delivery.write_text(
        "\n".join(
            [
                "See `USERJOURNEY/MISSING.md` for local details.",
                "Review `v6_clean_repo_candidate/app/page.tsx` before coding.",
            ]
        ),
        encoding="utf-8",
    )
    for relative in ("USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md", "USERJOURNEY/IMPLEMENTATION_PLAN.md"):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("No paths here.", encoding="utf-8")
    (tmp_path / "USERJOURNEY" / "USERJOURNEY_INTEGRITY_REFERENCE.json").write_text(
        '{"allowed_external_paths": ["frontend/app/auth/login/page.tsx"]}',
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems, warnings = validate.validate_planning_references(build_registry())

    assert problems == [
        "USERJOURNEY/DELIVERY_GAMEPLAN.md references missing workspace path: USERJOURNEY/MISSING.md",
        (
            "USERJOURNEY/DELIVERY_GAMEPLAN.md references non-allowlisted external implementation path: "
            "v6_clean_repo_candidate/app/page.tsx"
        ),
    ]
    assert warnings == []


def test_validate_planning_references_allows_manifested_external_paths(tmp_path: Path, monkeypatch) -> None:
    delivery = tmp_path / "USERJOURNEY" / "DELIVERY_GAMEPLAN.md"
    delivery.parent.mkdir(parents=True, exist_ok=True)
    delivery.write_text("Review `frontend/app/auth/login/page.tsx` before coding.", encoding="utf-8")
    for relative in ("USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md", "USERJOURNEY/IMPLEMENTATION_PLAN.md"):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("No paths here.", encoding="utf-8")
    (tmp_path / "USERJOURNEY" / "USERJOURNEY_INTEGRITY_REFERENCE.json").write_text(
        '{"allowed_external_paths": ["frontend/app/auth/login/page.tsx"]}',
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems, warnings = validate.validate_planning_references(build_registry())

    assert problems == []
    assert warnings == []


def test_validate_planning_references_skips_missing_docs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems, warnings = validate.validate_planning_references(build_registry())

    assert problems == []
    assert warnings == []


def test_validate_required_files_reports_missing_file(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    problems = validate.validate_required_files(registry, "programbuild")
    assert any("Missing required file" in item for item in problems)


def test_validate_metadata_and_warnings(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    output_path = tmp_path / "PROGRAMBUILD" / "OUTPUT.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "Purpose: Example",
                "Owner: [ASSIGN]",
                "Last updated: 2026-03-27",
                "Depends on: None",
                "Authority: template",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    assert validate.validate_metadata(registry, "programbuild") == []
    warnings = validate.metadata_warnings(registry, "programbuild")
    assert any("Owner not assigned" in item for item in warnings)


def test_validate_engineering_ready_detects_open_questions(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    open_questions = tmp_path / "USERJOURNEY" / "OPEN_QUESTIONS.md"
    open_questions.parent.mkdir(parents=True, exist_ok=True)
    open_questions.write_text(
        "## Remaining Operational And Legal Decisions\n1. Need legal signoff\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(validate, "validate_required_files", lambda registry: [])
    problems = validate.validate_engineering_ready(registry)
    assert any("not engineering-ready" in item for item in problems)


def test_enforce_engineering_ready_in_all_uses_validation_policy() -> None:
    registry = build_registry() | {"validation": {"enforce_engineering_ready_in_all": True}}
    assert validate.enforce_engineering_ready_in_all(registry) is True
    assert validate.enforce_engineering_ready_in_all(registry, "programbuild") is False


def test_validate_workflow_state_handles_valid_and_invalid_states(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility"],
            }
        }
    }
    state_path = tmp_path / "PROGRAMBUILD_STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "feasibility",
            "stages": {
                "inputs_and_mode_selection": {
                    "status": "completed",
                    "signoff": {"decision": "approved", "date": "2026-03-27", "notes": "ok"},
                },
                "feasibility": {
                    "status": "in_progress",
                    "signoff": {"decision": "", "date": "", "notes": ""},
                },
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda registry, system: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda registry, system: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda registry, system: ["inputs_and_mode_selection", "feasibility"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda registry, system, state=None: "feasibility")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda system: "stages")
    assert validate.validate_workflow_state(registry, "programbuild") == []

    write_json(
        state_path,
        {
            "active_stage": "feasibility",
            "stages": {
                "inputs_and_mode_selection": {
                    "status": "planned",
                    "signoff": {"decision": "", "date": "", "notes": ""},
                },
                "feasibility": {
                    "status": "planned",
                    "signoff": {"decision": "", "date": "", "notes": ""},
                },
            },
        },
    )
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert problems


def test_bootstrap_helpers_support_dry_run_and_main(tmp_path: Path, monkeypatch, capsys) -> None:
    target_file = tmp_path / "README.md"
    bootstrap.write_file(target_file, "hello", dry_run=True)
    bootstrap.copy_file(Path(__file__), tmp_path / "copy.txt", dry_run=True)
    dry_run_output = capsys.readouterr().out
    assert "CREATE" in dry_run_output
    assert "COPY" in dry_run_output

    destination = tmp_path / "main-bootstrap"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "programstart_bootstrap.py",
            "--dest",
            str(destination),
            "--project-name",
            "MainBootstrap",
            "--variant",
            "product",
        ],
    )
    assert bootstrap.main() == 0
    assert (destination / "README.md").exists()


def test_validate_main_all_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "all"])
    result = validate.main()
    out = capsys.readouterr().out
    assert "Validation passed" in out
    assert result == 0


def test_validate_main_all_runs_engineering_ready_when_policy_enabled(capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        validate,
        "load_registry",
        lambda: {
            "validation": {"enforce_engineering_ready_in_all": True},
            "systems": {},
            "sync_rules": [],
            "metadata_rules": {"required_prefixes": [], "owner_placeholder": "[ASSIGN]"},
        },
    )
    monkeypatch.setattr(validate, "validate_registry", lambda _registry: [])
    monkeypatch.setattr(validate, "validate_required_files", lambda _registry, _sf=None: [])
    monkeypatch.setattr(validate, "validate_metadata", lambda _registry, _sf=None: [])
    monkeypatch.setattr(validate, "validate_workflow_state", lambda _registry, _sf=None: [])
    monkeypatch.setattr(validate, "validate_authority_sync", lambda _registry: [])
    monkeypatch.setattr(validate, "validate_repo_boundary_policy", lambda _registry: [])
    monkeypatch.setattr(validate, "validate_bootstrap_assets", lambda _registry: [])
    monkeypatch.setattr(validate, "validate_test_coverage", lambda _registry: [])
    monkeypatch.setattr(validate, "validate_planning_references", lambda _registry: ([], []))
    monkeypatch.setattr(validate, "metadata_warnings", lambda _registry, _sf=None: [])
    monkeypatch.setattr(validate, "validate_engineering_ready", lambda _registry: ["engineering blocked"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "all"])

    result = validate.main()
    out = capsys.readouterr().out

    assert result == 1
    assert "engineering blocked" in out


def test_validate_main_required_files(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "required-files"])
    result = validate.main()
    out = capsys.readouterr().out
    assert "Validation passed" in out
    assert result == 0


def test_validate_main_metadata(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "metadata"])
    result = validate.main()
    out = capsys.readouterr().out
    assert "Validation passed" in out
    assert result == 0


def test_validate_main_workflow_state(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "workflow-state"])
    result = validate.main()
    out = capsys.readouterr().out
    assert "Validation passed" in out
    assert result == 0


def test_validate_main_with_system_filter(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "all", "--system", "programbuild"])
    result = validate.main()
    out = capsys.readouterr().out
    assert "Validation passed" in out
    assert result == 0


def test_validate_metadata_reports_missing_prefixes(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    output_path = tmp_path / "PROGRAMBUILD" / "OUTPUT.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("Purpose: Example\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    problems = validate.validate_metadata(registry, "programbuild")
    assert any("Metadata incomplete" in item for item in problems)


def test_validate_required_files_skips_optional_absent(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(common, "workspace_path", lambda relative: tmp_path / relative)
    problems = validate.validate_required_files(registry, "userjourney")
    assert problems == []


def test_validate_workflow_state_reports_missing_file(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility"],
            }
        }
    }
    missing = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    monkeypatch.setattr(validate, "workflow_state_path", lambda _registry, _system: missing)
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert any("Missing workflow state file" in item for item in problems)


def test_validate_workflow_state_reports_invalid_active_step(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility"],
            }
        }
    }
    state_path = tmp_path / "PROGRAMBUILD_STATE.json"
    write_json(state_path, {"active_stage": "unknown", "stages": {}})
    monkeypatch.setattr(validate, "workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _registry, _system: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda _registry, _system, _state=None: "unknown")
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert any("Invalid active step" in item for item in problems)


def test_validate_workflow_state_reports_entry_and_progress_problems(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility", "architecture"],
            }
        }
    }
    state_path = tmp_path / "PROGRAMBUILD_STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "feasibility",
            "stages": {
                "inputs_and_mode_selection": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
                "feasibility": {"status": "completed", "signoff": {"decision": "", "date": "", "notes": ""}},
                "architecture": {"status": "completed", "signoff": {"decision": "approved", "date": "2026-03-27", "notes": ""}},
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _registry, _system: load_json(state_path))
    monkeypatch.setattr(
        validate, "workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection", "feasibility", "architecture"]
    )
    monkeypatch.setattr(validate, "workflow_active_step", lambda _registry, _system, _state=None: "feasibility")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda _system: "stages")
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert any("must be completed before active step" in item for item in problems)
    assert any("missing approved sign-off" in item for item in problems)
    assert any("missing sign-off date" in item for item in problems)
    assert any("cannot be completed after the active step" in item for item in problems)
    assert any("exactly one in_progress" in item for item in problems)


def test_validate_main_engineering_ready_failure(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_engineering_ready", lambda _registry: ["blocked"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "engineering-ready"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 1
    assert "Validation failed" in out


def test_validate_main_metadata_warnings(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_metadata", lambda _registry, _sf=None: [])
    monkeypatch.setattr(validate, "metadata_warnings", lambda _registry, _sf=None: ["warn owner"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "metadata"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Warnings:" in out


def test_validate_main_planning_references_warnings(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_planning_references", lambda _registry: ([], ["warn path"]))
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "planning-references"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "warn path" in out


def test_validate_main_authority_sync_failure(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_authority_sync", lambda _registry: ["authority mismatch"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "authority-sync"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 1
    assert "authority mismatch" in out


def test_validate_repo_boundary_policy_detects_missing_phrase(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    policy_file = tmp_path / ".github" / "copilot-instructions.md"
    policy_file.parent.mkdir(parents=True, exist_ok=True)
    policy_file.write_text("missing required text\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_repo_boundary_policy(registry)

    assert any("repo boundary policy phrase missing" in item for item in problems)


def test_validate_main_repo_boundary_failure(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_repo_boundary_policy", lambda _registry: ["repo boundary drift"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "repo-boundary"])

    result = validate.main()
    out = capsys.readouterr().out

    assert result == 1
    assert "repo boundary drift" in out


def test_metadata_warnings_ignores_assigned_owner(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    output_path = tmp_path / "PROGRAMBUILD" / "OUTPUT.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "Purpose: Example",
                "Owner: Alice",
                "Last updated: 2026-03-27",
                "Depends on: None",
                "Authority: template",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    assert validate.metadata_warnings(registry, "programbuild") == []


def test_validate_engineering_ready_optional_absent(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(common, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(validate, "validate_required_files", lambda _registry: ["missing base"])
    problems = validate.validate_engineering_ready(registry)
    assert problems == ["missing base"]


def test_validate_workflow_state_reports_missing_entry(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility"],
            }
        }
    }
    state_path = tmp_path / "PROGRAMBUILD_STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "inputs_and_mode_selection",
            "stages": {
                "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}}
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _registry, _system: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda _registry, _system, _state=None: "inputs_and_mode_selection")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda _system: "stages")
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert any("Missing state entry 'feasibility'" in item for item in problems)


def test_validate_workflow_state_reports_active_step_mismatch(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility"],
            }
        }
    }
    state_path = tmp_path / "PROGRAMBUILD_STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "feasibility",
            "stages": {
                "inputs_and_mode_selection": {
                    "status": "in_progress",
                    "signoff": {"decision": "approved", "date": "2026-03-27", "notes": ""},
                },
                "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _registry, _system: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda _registry, _system, _state=None: "feasibility")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda _system: "stages")
    problems = validate.validate_workflow_state(registry, "programbuild")
    assert any("does not match in_progress step" in item for item in problems)


def test_validate_engineering_ready_passes_when_open_items_empty(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    open_questions = tmp_path / "USERJOURNEY" / "OPEN_QUESTIONS.md"
    open_questions.parent.mkdir(parents=True, exist_ok=True)
    open_questions.write_text("## Remaining Operational And Legal Decisions\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(validate, "validate_required_files", lambda _registry: [])
    assert validate.validate_engineering_ready(registry) == []


def test_validate_metadata_skips_missing_files_and_optional_absent(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry()
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    assert validate.validate_metadata(registry) == []
    assert validate.metadata_warnings(registry) == []


def test_validate_workflow_state_skips_optional_absent(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "userjourney": {
                "state_file": "USERJOURNEY/USERJOURNEY_STATE.json",
                "active_key": "active_phase",
                "initial_step": "phase_0",
                "step_order": ["phase_0"],
            }
        }
    }
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(common, "workspace_path", lambda relative: tmp_path / relative)
    assert validate.validate_workflow_state(registry, "userjourney") == []


def test_bootstrap_programbuild_dry_run_and_main_refuses_non_empty(tmp_path: Path, monkeypatch, capsys) -> None:
    registry = common.load_registry()
    destination = tmp_path / "dest"
    destination.mkdir()
    (destination / "existing.txt").write_text("x", encoding="utf-8")
    bootstrap.bootstrap_programbuild(destination, registry, "enterprise", dry_run=True)
    dry_run_output = capsys.readouterr().out
    assert "CREATE" in dry_run_output

    monkeypatch.setattr(
        sys,
        "argv",
        ["programstart_bootstrap.py", "--dest", str(destination), "--project-name", "Blocked", "--variant", "product"],
    )
    assert bootstrap.main() == 1


def test_bootstrap_programbuild_writes_variant(tmp_path: Path) -> None:
    registry = common.load_registry()
    destination = tmp_path / "dest"
    bootstrap.bootstrap_programbuild(destination, registry, "enterprise", dry_run=False)
    state_path = destination / registry["workflow_state"]["programbuild"]["state_file"]
    state = load_json(state_path)
    assert state["variant"] == "enterprise"


def test_validate_workflow_state_rejects_invalid_status(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "step_a",
                "step_order": ["step_a"],
            }
        }
    }
    state_path = tmp_path / "STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "step_a",
            "stages": {
                "step_a": {"status": "running", "signoff": {"decision": "", "date": "", "notes": ""}},
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda _r, _s: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _r, _s: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda _r, _s: ["step_a"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda _r, _s, _st=None: "step_a")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda _s: "stages")

    problems = validate.validate_workflow_state(registry, "programbuild")

    assert any("invalid status value" in p and "running" in p for p in problems)


def test_validate_workflow_state_rejects_bad_date_format(tmp_path: Path, monkeypatch) -> None:
    registry = build_registry() | {
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "step_a",
                "step_order": ["step_a", "step_b"],
            }
        }
    }
    state_path = tmp_path / "STATE.json"
    write_json(
        state_path,
        {
            "active_stage": "step_b",
            "stages": {
                "step_a": {
                    "status": "completed",
                    "signoff": {"decision": "approved", "date": "March 2026", "notes": ""},
                },
                "step_b": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            },
        },
    )
    monkeypatch.setattr(validate, "workflow_state_path", lambda _r, _s: state_path)
    monkeypatch.setattr(validate, "load_workflow_state", lambda _r, _s: load_json(state_path))
    monkeypatch.setattr(validate, "workflow_steps", lambda _r, _s: ["step_a", "step_b"])
    monkeypatch.setattr(validate, "workflow_active_step", lambda _r, _s, _st=None: "step_b")
    monkeypatch.setattr(validate, "workflow_entry_key", lambda _s: "stages")

    problems = validate.validate_workflow_state(registry, "programbuild")

    assert any("invalid signoff date format" in p and "March 2026" in p for p in problems)


def test_validate_rule_enforcement_adr_sequence_gap(tmp_path: Path, monkeypatch) -> None:
    decisions_dir = tmp_path / "docs" / "decisions"
    decisions_dir.mkdir(parents=True)
    (decisions_dir / "README.md").write_text("# ADRs", encoding="utf-8")
    (decisions_dir / "0001-first.md").write_text("# ADR 1", encoding="utf-8")
    (decisions_dir / "0003-third.md").write_text("# ADR 3", encoding="utf-8")  # gap at 0002
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    registry = build_registry() | {"workspace": {"bootstrap_assets": []}}
    problems = validate.validate_rule_enforcement(registry)

    assert any("ADR sequence gap" in p and "0002" in p for p in problems)


def test_validate_rule_enforcement_adr_bad_naming(tmp_path: Path, monkeypatch) -> None:
    decisions_dir = tmp_path / "docs" / "decisions"
    decisions_dir.mkdir(parents=True)
    (decisions_dir / "README.md").write_text("# ADRs", encoding="utf-8")
    (decisions_dir / "my-decision.md").write_text("# bad name", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    registry = build_registry() | {"workspace": {"bootstrap_assets": []}}
    problems = validate.validate_rule_enforcement(registry)

    assert any("does not follow NNNN-title.md naming" in p for p in problems)


def test_validate_rule_enforcement_project_repo_does_not_require_template_operator_prompt(monkeypatch) -> None:
    real_workspace_path = validate.workspace_path

    def fake_workspace_path(relative: str) -> Path:
        if relative == ".github/prompts/audit-process-drift.prompt.md":
            return Path("C:/definitely-missing/audit-process-drift.prompt.md")
        return real_workspace_path(relative)

    monkeypatch.setattr(validate, "workspace_path", fake_workspace_path)
    monkeypatch.setattr(validate, "validate_prompt_registry_completeness", lambda _registry: [])
    registry = common.load_registry()
    workspace = dict(registry.get("workspace", {}))
    workspace["repo_role"] = "project_repo"
    registry["workspace"] = workspace

    problems = validate.validate_rule_enforcement(registry)

    assert not any("audit-process-drift.prompt.md" in p for p in problems)


def test_validate_prompt_registry_completeness_flags_unregistered_prompt_file(tmp_path: Path, monkeypatch) -> None:
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "orphan.prompt.md").write_text("---\nname: orphan\ndescription: orphan\nagent: agent\n---\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_prompt_registry_completeness(
        {
            "prompt_registry": {
                "workflow_prompt_files": [],
                "operator_prompt_files": [],
                "internal_prompt_files": [],
            }
        }
    )

    assert any("prompt_registry missing on-disk prompt file: .github/prompts/orphan.prompt.md" in p for p in problems)


def test_validate_prompt_registry_completeness_flags_missing_registered_prompt_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_prompt_registry_completeness(
        {
            "prompt_registry": {
                "workflow_prompt_files": [".github/prompts/missing.prompt.md"],
                "operator_prompt_files": [],
                "internal_prompt_files": [],
            }
        }
    )

    assert any("prompt_registry references missing prompt file: .github/prompts/missing.prompt.md" in p for p in problems)


def test_validate_prompt_authority_metadata_flags_missing_metadata_for_prompt_with_section(tmp_path: Path, monkeypatch) -> None:
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "shape.prompt.md").write_text(
        "## Authority Loading\n\n- `PROGRAMBUILD/PROGRAMBUILD.md`\n",
        encoding="utf-8",
    )
    (tmp_path / "PROGRAMBUILD").mkdir(parents=True)
    (tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD.md").write_text("# stub\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_prompt_authority_metadata(
        {
            "prompt_registry": {
                "workflow_prompt_files": [".github/prompts/shape.prompt.md"],
                "operator_prompt_files": [],
                "internal_prompt_files": [],
            },
            "prompt_authority": {},
        }
    )

    assert any("prompt_authority missing metadata for prompt with '## Authority Loading'" in p for p in problems)


def test_validate_prompt_authority_metadata_flags_prompt_text_mismatch(tmp_path: Path, monkeypatch) -> None:
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "shape.prompt.md").write_text(
        "## Authority Loading\n\n- `PROGRAMBUILD/PROGRAMBUILD.md`\n",
        encoding="utf-8",
    )
    (tmp_path / "PROGRAMBUILD").mkdir(parents=True)
    (tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "PROGRAMBUILD" / "REQUIREMENTS.md").write_text("# stub\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    problems = validate.validate_prompt_authority_metadata(
        {
            "prompt_registry": {
                "workflow_prompt_files": [".github/prompts/shape.prompt.md"],
                "operator_prompt_files": [],
                "internal_prompt_files": [],
            },
            "prompt_authority": {
                ".github/prompts/shape.prompt.md": {
                    "authority_files": ["PROGRAMBUILD/PROGRAMBUILD.md", "PROGRAMBUILD/REQUIREMENTS.md"]
                }
            },
        }
    )

    assert any("PROGRAMBUILD/REQUIREMENTS.md" in p and "prompt text is missing it" in p for p in problems)


def test_validate_main_prompt_authority_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "prompt-authority"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


def test_validate_rule_enforcement_includes_prompt_registry_completeness(monkeypatch, tmp_path: Path) -> None:
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "orphan.prompt.md").write_text("---\nname: orphan\ndescription: orphan\nagent: agent\n---\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    registry = build_registry() | {
        "workspace": {"bootstrap_assets": []},
        "prompt_registry": {
            "workflow_prompt_files": [],
            "operator_prompt_files": [],
            "internal_prompt_files": [],
        },
    }
    problems = validate.validate_rule_enforcement(registry)

    assert any("prompt_registry missing on-disk prompt file: .github/prompts/orphan.prompt.md" in p for p in problems)


def test_validate_test_coverage_warns_on_missing_test_file(tmp_path: Path, monkeypatch) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (scripts_dir / "programstart_foo.py").write_text("", encoding="utf-8")
    (scripts_dir / "programstart_bar.py").write_text("", encoding="utf-8")
    (scripts_dir / "programstart_baz_smoke.py").write_text("", encoding="utf-8")  # excluded
    (tests_dir / "test_programstart_foo.py").write_text("", encoding="utf-8")  # exists
    monkeypatch.setattr(validate, "workspace_path", lambda relative: tmp_path / relative)

    warnings = validate.validate_test_coverage({})

    assert any("programstart_bar.py" in w for w in warnings)
    assert not any("programstart_foo.py" in w for w in warnings)
    assert not any("programstart_baz_smoke.py" in w for w in warnings)


def test_validate_main_test_coverage_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "template-test-coverage"])
    result = validate.main()
    out = capsys.readouterr().out
    # Should pass (warnings are not errors)
    assert result == 0
    assert "Validation passed" in out


def test_validate_main_all_includes_bootstrap_assets(capsys, monkeypatch) -> None:
    monkeypatch.setattr(validate, "validate_bootstrap_assets", lambda _registry: ["bootstrap gap"])
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "all"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 1
    assert "bootstrap gap" in out


# ---------- ADR coverage ----------


_DECISION_LOG_TEMPLATE = """\
# DECISION_LOG.md

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
{rows}

## Decision Details
"""


def write_adr(
    decisions_dir: Path,
    filename: str,
    *,
    status: str,
    date: str,
    title: str,
    decision_id: str | None = "DEC-001",
) -> None:
    decision_link = [f"<!-- {decision_id} -->", ""] if decision_id else []
    (decisions_dir / filename).write_text(
        "\n".join(
            [
                "---",
                f"status: {status}",
                f"date: {date}",
                "deciders: [Solo operator]",
                "consulted: []",
                "informed: []",
                "---",
                "",
                f"# {filename[:4]}. {title}",
                "",
                *decision_link,
                "## Context and Problem Statement",
                "",
                "Context.",
            ]
        ),
        encoding="utf-8",
    )


def write_adr_readme(decisions_dir: Path, rows: list[str]) -> None:
    (decisions_dir / "README.md").write_text(
        "\n".join(
            [
                "# Decision Records",
                "",
                "## Index",
                "",
                "| ID | Title | Status | Date |",
                "|---|---|---|---|",
                *rows,
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_adr_coverage_no_warning_when_adr_references_decision(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="| DEC-001 | 2026-01-01 | inputs | Adopt foo | ACTIVE | — | Solo | foo.py |")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    (decisions / "0001-adopt-foo.md").write_text("Relates to DEC-001\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_adr_coverage({})
    assert warnings == []


def test_adr_coverage_warning_when_no_matching_adr(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="| DEC-002 | 2026-01-01 | inputs | Use bar | ACTIVE | — | Solo | bar.py |")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    # ADR exists but references a different decision
    (decisions / "0001-something-else.md").write_text("Unrelated content\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_adr_coverage({})
    assert len(warnings) == 1
    assert "DEC-002" in warnings[0]
    assert "ACTIVE" in warnings[0]


def test_adr_coverage_warns_for_reversed_decision_without_matching_adr(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-004 | 2026-01-01 | inputs | Replace foo | REVERSED | DEC-001 | Solo | bar.py |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    (decisions / "README.md").write_text("# ADRs", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_adr_coverage({})
    assert len(warnings) == 1
    assert "DEC-004" in warnings[0]
    assert "REVERSED" in warnings[0]


def test_adr_coverage_ignores_superseded_decisions(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="| DEC-003 | 2026-01-01 | inputs | Old choice | SUPERSEDED | — | Solo | old.py |")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_adr_coverage({})
    assert warnings == []


def test_adr_coverage_no_warning_when_no_decisions(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_adr_coverage({})
    assert warnings == []


def test_adr_coverage_no_warning_when_decision_log_missing(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
    warnings = validate.validate_adr_coverage({})
    assert warnings == []


def test_validate_main_adr_coverage_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "adr-coverage"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


def test_validate_adr_coherence_passes_for_consistent_records(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | ACTIVE | — | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0001-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo")
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    assert validate.validate_adr_coherence({}) == []


def test_validate_adr_coherence_flags_readme_status_mismatch(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | ACTIVE | — | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0001-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo")
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | superseded by ADR-0002 | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({})
    assert any("README status mismatch" in problem for problem in problems)


def test_validate_adr_coherence_flags_missing_superseding_adr(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | SUPERSEDED | DEC-002 | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(
        decisions,
        "0001-adopt-foo.md",
        status="superseded by ADR-0002",
        date="2026-04-15",
        title="Adopt foo",
    )
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | superseded by ADR-0002 | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({})
    assert any("ADR-0002" in problem and "does not exist" in problem for problem in problems)


def test_validate_adr_coherence_flags_missing_decision_link(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | ACTIVE | — | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    (decisions / "0001-adopt-foo.md").write_text(
        "\n".join(
            [
                "---",
                "status: accepted",
                "date: 2026-04-15",
                "deciders: [Solo operator]",
                "consulted: []",
                "informed: []",
                "---",
                "",
                "# 0001. Adopt foo",
            ]
        ),
        encoding="utf-8",
    )
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({})
    assert any("missing decision-log linkage comment" in problem for problem in problems)


def test_validate_adr_coherence_allows_listed_legacy_pre_register_adr_without_decision_link(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0001-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo", decision_id=None)
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    assert validate.validate_adr_coherence({"adr_policy": {"legacy_pre_register_adrs": ["0001"]}}) == []


def test_validate_adr_coherence_flags_unlisted_legacy_style_adr_without_decision_link(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0001-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo", decision_id=None)
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({})
    assert any("missing decision-log linkage comment" in problem for problem in problems)


def test_validate_adr_coherence_allows_inherited_template_adr_links_in_project_repo(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0004-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo", decision_id="DEC-001")
    write_adr_readme(decisions, ["| [0004](0004-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    assert validate.validate_adr_coherence({"workspace": {"repo_role": "project_repo"}}) == []


def test_validate_adr_coherence_flags_missing_legacy_pre_register_adr_from_policy(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(rows="")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr_readme(decisions, [])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({"adr_policy": {"legacy_pre_register_adrs": ["0001"]}})
    assert any("legacy_pre_register_adrs references missing ADR file: 0001" in problem for problem in problems)


def test_validate_adr_coherence_flags_decision_log_reference_to_legacy_pre_register_adr(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | ACTIVE | — | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(decisions, "0001-adopt-foo.md", status="accepted", date="2026-04-15", title="Adopt foo")
    write_adr_readme(decisions, ["| [0001](0001-adopt-foo.md) | Adopt foo | accepted | 2026-04-15 |"])
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({"adr_policy": {"legacy_pre_register_adrs": ["0001"]}})
    assert any("references legacy pre-register ADR 0001-adopt-foo.md" in problem for problem in problems)


def test_validate_adr_coherence_flags_active_decision_pointing_to_superseded_adr(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | ACTIVE | — | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    decisions = tmp_path / "docs" / "decisions"
    decisions.mkdir(parents=True)
    write_adr(
        decisions,
        "0001-adopt-foo.md",
        status="superseded by ADR-0002",
        date="2026-04-15",
        title="Adopt foo",
    )
    write_adr(decisions, "0002-adopt-bar.md", status="accepted", date="2026-04-15", title="Adopt bar", decision_id="DEC-002")
    write_adr_readme(
        decisions,
        [
            "| [0001](0001-adopt-foo.md) | Adopt foo | superseded by ADR-0002 | 2026-04-15 |",
            "| [0002](0002-adopt-bar.md) | Adopt bar | accepted | 2026-04-15 |",
        ],
    )
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_adr_coherence({})
    assert any("references superseded ADR 0001-adopt-foo.md" in problem for problem in problems)


def test_validate_main_adr_coherence_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "adr-coherence"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


def test_validate_decision_log_reversal_invariants_passes_for_reciprocal_pair(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="\n".join(
            [
                "| DEC-001 | 2026-04-15 | inputs | Adopt foo | SUPERSEDED | DEC-002 | Solo | docs/decisions/0001-adopt-foo.md |",
                "| DEC-002 | 2026-04-15 | inputs | Adopt bar | REVERSED | DEC-001 | Solo | docs/decisions/0002-adopt-bar.md |",
            ]
        )
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    assert validate.validate_decision_log_reversal_invariants({}) == []


def test_validate_decision_log_reversal_invariants_flags_missing_reversed_target(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="| DEC-001 | 2026-04-15 | inputs | Adopt foo | SUPERSEDED | DEC-099 | Solo | docs/decisions/0001-adopt-foo.md |"
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_decision_log_reversal_invariants({})
    assert any("missing decision DEC-099" in problem for problem in problems)


def test_validate_decision_log_reversal_invariants_flags_non_reciprocal_pair(tmp_path, monkeypatch) -> None:
    log = _DECISION_LOG_TEMPLATE.format(
        rows="\n".join(
            [
                "| DEC-001 | 2026-04-15 | inputs | Adopt foo | SUPERSEDED | DEC-002 | Solo | docs/decisions/0001-adopt-foo.md |",
                "| DEC-002 | 2026-04-15 | inputs | Adopt bar | REVERSED | DEC-003 | Solo | docs/decisions/0002-adopt-bar.md |",
            ]
        )
    )
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "DECISION_LOG.md").write_text(log, encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_decision_log_reversal_invariants({})
    assert any("must point back via Replaces=DEC-001" in problem for problem in problems)


def test_validate_main_decision_log_coherence_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "decision-log-coherence"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


# ---------- KB freshness ----------


def test_kb_freshness_no_warning_when_fresh(tmp_path, monkeypatch) -> None:
    import datetime

    today = datetime.date.today().isoformat()
    kb = {"research_ledger": {"tracks": [{"name": "Test track", "freshness_days": 7, "last_review_date": today}]}}
    kb_path = tmp_path / "config" / "knowledge-base.json"
    kb_path.parent.mkdir(parents=True)
    kb_path.write_text(json.dumps(kb), encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_kb_freshness({})
    assert warnings == []


def test_kb_freshness_warns_when_stale(tmp_path, monkeypatch) -> None:
    import datetime

    stale_date = (datetime.date.today() - datetime.timedelta(days=15)).isoformat()
    kb = {"research_ledger": {"tracks": [{"name": "Stale track", "freshness_days": 7, "last_review_date": stale_date}]}}
    kb_path = tmp_path / "config" / "knowledge-base.json"
    kb_path.parent.mkdir(parents=True)
    kb_path.write_text(json.dumps(kb), encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_kb_freshness({})
    assert len(warnings) == 1
    assert "Stale track" in warnings[0]
    assert "stale" in warnings[0]


# ---------------------------------------------------------------------------
# Phase B: coverage push — previously uncovered branches in validate.py
# ---------------------------------------------------------------------------


def test_check_content_quality_returns_empty_on_read_error(tmp_path: Path, monkeypatch) -> None:
    """Lines 83-84: OSError when reading file → returns empty list."""
    f = tmp_path / "unreadable.md"
    f.write_text("content", encoding="utf-8")

    def _raise(self, **kwargs):  # noqa: ANN001
        raise OSError("simulated disk error")

    monkeypatch.setattr(Path, "read_text", _raise)
    result = validate.check_content_quality(f)
    assert result == []


def test_run_stage_gate_check_unknown_name_returns_empty() -> None:
    """Line 410: unknown check_name in run_stage_gate_check → empty list."""
    result = validate.run_stage_gate_check({}, "nonexistent-check-XYZ-phase-b")
    assert result == []


def test_validate_implementation_entry_criteria_covers_all_subchecks(
    monkeypatch,
) -> None:
    """Lines 530-535: validate_implementation_entry_criteria calls all four sub-checks."""
    monkeypatch.setattr(validate, "validate_architecture_contracts", lambda _r: [])
    monkeypatch.setattr(validate, "validate_test_strategy_complete", lambda _r: [])
    monkeypatch.setattr(validate, "validate_risk_spikes", lambda _r: [])
    monkeypatch.setattr(validate, "validate_risk_spike_resolution", lambda _r: [])
    result = validate.validate_implementation_entry_criteria({})
    assert result == []


def test_validate_feasibility_criteria_template_recommendation_flagged(tmp_path: Path, monkeypatch) -> None:
    """Lines 235-236: Recommendation section with 'go / limited spike / no-go' template text."""
    feas = tmp_path / "PROGRAMBUILD" / "FEASIBILITY.md"
    feas.parent.mkdir(parents=True, exist_ok=True)
    feas.write_text(
        "## Kill Criteria\n"
        "- If performance < 100ms, then stop\n"
        "- If user retention < 10%, then kill\n"
        "- If infra cost > $50k, then abort\n\n"
        "## Recommendation\n"
        "go / limited spike / no-go\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
    problems = validate.validate_feasibility_criteria({})
    assert any("still contains the template option list" in p for p in problems)


def test_validate_feasibility_criteria_missing_recommendation_section(tmp_path: Path, monkeypatch) -> None:
    """Line 273: FEASIBILITY.md without ## Recommendation section → appropriate problem."""
    feas = tmp_path / "PROGRAMBUILD" / "FEASIBILITY.md"
    feas.parent.mkdir(parents=True, exist_ok=True)
    feas.write_text(
        "## Kill Criteria\n"
        "- If performance < 100ms, then stop\n"
        "- If user retention < 10%, then kill\n"
        "- If infra cost > $50k, then abort\n\n"
        "## Other Section\n"
        "No recommendation here.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
    problems = validate.validate_feasibility_criteria({})
    assert any("no '## Recommendation' section found" in p for p in problems)


def test_validate_registry_policy_doc_missing_must_contain() -> None:
    """Lines 622/625: policy doc with path but no must_contain → problem reported."""
    problems = validate.validate_registry(
        {
            "systems": {},
            "sync_rules": [],
            "repo_boundary_policy": {
                "enabled": True,
                "docs": [{"path": "CONTRIBUTING.md"}],
            },
        }
    )
    assert any("must declare at least one required phrase" in p for p in problems)


def test_kb_freshness_warns_when_fields_missing(tmp_path, monkeypatch) -> None:
    kb = {"research_ledger": {"tracks": [{"name": "Incomplete track"}]}}
    kb_path = tmp_path / "config" / "knowledge-base.json"
    kb_path.parent.mkdir(parents=True)
    kb_path.write_text(json.dumps(kb), encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_kb_freshness({})
    assert len(warnings) == 1
    assert "missing" in warnings[0]


def test_kb_freshness_warns_on_bad_date(tmp_path, monkeypatch) -> None:
    kb = {"research_ledger": {"tracks": [{"name": "Bad date", "freshness_days": 7, "last_review_date": "not-a-date"}]}}
    kb_path = tmp_path / "config" / "knowledge-base.json"
    kb_path.parent.mkdir(parents=True)
    kb_path.write_text(json.dumps(kb), encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    warnings = validate.validate_kb_freshness({})
    assert len(warnings) == 1
    assert "invalid" in warnings[0]


def test_kb_freshness_returns_empty_when_no_kb_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
    warnings = validate.validate_kb_freshness({})
    assert warnings == []


def test_validate_main_kb_freshness_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "kb-freshness"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


# ---------------------------------------------------------------------------
# Phase K tests
# ---------------------------------------------------------------------------


class TestStrictModeValidate:
    def test_strict_exits_1_on_warnings(self, capsys, monkeypatch) -> None:
        monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "test-coverage", "--strict"])
        monkeypatch.setattr(validate, "validate_test_coverage", lambda _reg: ["fake warning"])
        result = validate.main()
        out = capsys.readouterr().out
        assert result == 1
        assert "strict mode" in out

    def test_strict_exits_0_when_no_warnings(self, capsys, monkeypatch) -> None:
        monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "test-coverage", "--strict"])
        monkeypatch.setattr(validate, "validate_test_coverage", lambda _reg: [])
        result = validate.main()
        assert result == 0


class TestCoverageSourceCompleteness:
    def test_detects_unregistered_module(self, tmp_path, monkeypatch) -> None:
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "programstart_new.py").write_text("# new", encoding="utf-8")
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.coverage.run]\nsource = ["scripts.programstart_old"]', encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.validate_coverage_source_completeness({})
        assert any("programstart_new.py" in w for w in warnings)

    def test_passes_when_all_registered(self, tmp_path, monkeypatch) -> None:
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "programstart_foo.py").write_text("# foo", encoding="utf-8")
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.coverage.run]\nsource = ["scripts.programstart_foo"]', encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.validate_coverage_source_completeness({})
        assert warnings == []

    def test_excludes_smoke_scripts(self, tmp_path, monkeypatch) -> None:
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "programstart_something_smoke.py").write_text("# smoke", encoding="utf-8")
        (scripts_dir / "__init__.py").write_text("", encoding="utf-8")
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.coverage.run]\nsource = []", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.validate_coverage_source_completeness({})
        assert warnings == []


class TestPostLaunchReview:
    def test_missing_file_fails(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        problems = validate.validate_post_launch_review({})
        assert any("does not exist" in p for p in problems)

    def test_stub_file_fails(self, tmp_path, monkeypatch) -> None:
        plr = tmp_path / "PROGRAMBUILD" / "POST_LAUNCH_REVIEW.md"
        plr.parent.mkdir(parents=True)
        plr.write_text("# Post Launch Review\n---\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        problems = validate.validate_post_launch_review({})
        assert any("stub" in p for p in problems)

    def test_real_content_passes(self, tmp_path, monkeypatch) -> None:
        plr = tmp_path / "PROGRAMBUILD" / "POST_LAUNCH_REVIEW.md"
        plr.parent.mkdir(parents=True)
        plr.write_text(
            "# Post Launch Review\n\nFinding 1: all tests green.\nOutcome: stable.\nVerdict: ship it.\nExtra: yes.\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        problems = validate.validate_post_launch_review({})
        assert problems == []


class TestBroadenedTestCoverage:
    def test_check_commit_msg_flagged_when_no_test(self, tmp_path, monkeypatch) -> None:
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "check_commit_msg.py").write_text("# commit msg", encoding="utf-8")
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.validate_test_coverage({})
        assert any("check_commit_msg.py" in w for w in warnings)


# ---------------------------------------------------------------------------
# Content quality detection (H-2 / W-1)
# ---------------------------------------------------------------------------


class TestCheckContentQuality:
    def test_detects_tbd(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("# Title\nSome content TBD here\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 1
        assert "TBD" in warnings[0]
        assert "DOC.md:2" in warnings[0]

    def test_detects_todo(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("line 1\nTODO: fix later\nline 3\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 1
        assert "TODO" in warnings[0]

    def test_detects_fill_in(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("[FILL IN] your name\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 1
        assert "[FILL IN]" in warnings[0]

    def test_detects_placeholder(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("This is a PLACEHOLDER value\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 1
        assert "PLACEHOLDER" in warnings[0]

    def test_detects_lorem_ipsum(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("Lorem ipsum dolor sit amet\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 1
        assert "Lorem ipsum" in warnings[0]

    def test_clean_file_returns_empty(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("# Architecture\nReal content here.\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert warnings == []

    def test_missing_file_returns_empty(self, tmp_path) -> None:
        warnings = validate.check_content_quality(tmp_path / "MISSING.md")
        assert warnings == []

    def test_multiple_placeholders(self, tmp_path) -> None:
        f = tmp_path / "DOC.md"
        f.write_text("TBD\nReal line\nTODO: later\n", encoding="utf-8")
        warnings = validate.check_content_quality(f)
        assert len(warnings) == 2


class TestStageContentQualityWarnings:
    def test_known_step_with_placeholders(self, tmp_path, monkeypatch) -> None:
        feas = tmp_path / "PROGRAMBUILD" / "FEASIBILITY.md"
        feas.parent.mkdir(parents=True)
        feas.write_text("# Feasibility\nTBD\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.stage_content_quality_warnings("feasibility")
        assert len(warnings) == 1
        assert "TBD" in warnings[0]

    def test_known_step_clean(self, tmp_path, monkeypatch) -> None:
        feas = tmp_path / "PROGRAMBUILD" / "FEASIBILITY.md"
        feas.parent.mkdir(parents=True)
        feas.write_text("# Feasibility\nReal analysis.\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.stage_content_quality_warnings("feasibility")
        assert warnings == []

    def test_unknown_step_returns_empty(self) -> None:
        warnings = validate.stage_content_quality_warnings("inputs_and_mode_selection")
        assert warnings == []

    def test_multi_file_step(self, tmp_path, monkeypatch) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir(parents=True)
        (pb / "REQUIREMENTS.md").write_text("TODO: write reqs\n", encoding="utf-8")
        (pb / "USER_FLOWS.md").write_text("Clean content.\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)
        warnings = validate.stage_content_quality_warnings("requirements_and_ux")
        assert len(warnings) == 1
        assert "REQUIREMENTS.md" in warnings[0]


class TestRepoWidePlaceholderContent:
    def test_placeholder_content_targets_assign_role_based_severity(self, tmp_path, monkeypatch) -> None:
        docs_decisions = tmp_path / "docs" / "decisions"
        docs_decisions.mkdir(parents=True)
        (docs_decisions / "0001-test.md").write_text("# ADR\n", encoding="utf-8")
        (tmp_path / "README.md").write_text("# Readme\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

        registry = {
            "systems": {
                "programbuild": {"output_files": ["PROGRAMBUILD/FEASIBILITY.md"]},
                "userjourney": {"optional": True, "root": "_missing"},
            },
            "workflow_state": {
                "userjourney": {"step_files": {}},
            },
        }

        targets = validate.placeholder_content_targets(registry)

        assert targets["PROGRAMBUILD/FEASIBILITY.md"] == ("problem", "programbuild-output")
        assert targets["docs/decisions/0001-test.md"] == ("problem", "adr")
        assert targets["README.md"] == ("warning", "repo-doc")

    def test_validate_placeholder_content_flags_programbuild_outputs_as_problems(self, tmp_path, monkeypatch) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir(parents=True)
        (pb / "FEASIBILITY.md").write_text("TBD\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

        problems, warnings = validate.validate_placeholder_content(
            {
                "systems": {
                    "programbuild": {"output_files": ["PROGRAMBUILD/FEASIBILITY.md"]},
                    "userjourney": {"optional": True, "root": "_missing"},
                },
                "workflow_state": {"userjourney": {"step_files": {}}},
            }
        )

        assert warnings == []
        assert len(problems) == 1
        assert "programbuild-output" in problems[0]
        assert "TBD" in problems[0]

    def test_validate_placeholder_content_flags_repo_docs_as_warnings(self, tmp_path, monkeypatch) -> None:
        (tmp_path / "README.md").write_text("TODO: finish summary\n", encoding="utf-8")
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

        problems, warnings = validate.validate_placeholder_content(
            {
                "systems": {
                    "programbuild": {"output_files": []},
                    "userjourney": {"optional": True, "root": "_missing"},
                },
                "workflow_state": {"userjourney": {"step_files": {}}},
            }
        )

        assert problems == []
        assert len(warnings) == 1
        assert "repo-doc" in warnings[0]
        assert "README.md" in warnings[0]

    def test_validate_placeholder_content_skips_optional_userjourney_when_absent(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

        targets = validate.placeholder_content_targets(
            {
                "systems": {
                    "programbuild": {"output_files": []},
                    "userjourney": {"optional": True, "root": "USERJOURNEY"},
                },
                "workflow_state": {
                    "userjourney": {
                        "step_files": {"phase_0": ["USERJOURNEY/OPEN_QUESTIONS.md"]}
                    }
                },
            }
        )

        assert "USERJOURNEY/OPEN_QUESTIONS.md" not in targets


def test_validate_main_placeholder_content_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "placeholder-content"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out


def test_validate_prompt_generation_boundary_flags_public_auto_generated_prompt(tmp_path: Path, monkeypatch) -> None:
    prompt = tmp_path / ".github" / "prompts" / "bad.prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("# AUTO-GENERATED by programstart prompt-build — do not hand-edit\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_prompt_generation_boundary(
        {
            "prompt_generation": {"artifact_root": "outputs/generated-prompts", "managed_stage_prompts": []},
            "prompt_registry": {
                "workflow_prompt_files": [".github/prompts/bad.prompt.md"],
                "operator_prompt_files": [],
                "internal_prompt_files": [],
            },
        }
    )

    assert any("public prompt must be manually maintained" in problem for problem in problems)


def test_validate_prompt_generation_boundary_flags_outdated_managed_prompt(tmp_path: Path, monkeypatch) -> None:
    generated = tmp_path / "outputs" / "generated-prompts" / "feasibility.prompt.md"
    generated.parent.mkdir(parents=True)
    generated.write_text("stale\n", encoding="utf-8")
    monkeypatch.setattr(validate, "workspace_path", lambda rel: tmp_path / rel)

    problems = validate.validate_prompt_generation_boundary(
        common.load_registry() | {
            "prompt_generation": {
                "artifact_root": "outputs/generated-prompts",
                "managed_stage_prompts": [
                    {"stage": "feasibility", "path": "outputs/generated-prompts/feasibility.prompt.md"}
                ],
            }
        }
    )

    assert any("run 'uv run programstart prompt-build --sync-managed'" in problem for problem in problems)


def test_validate_main_prompt_generation_passes(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_validate.py", "--check", "prompt-generation"])
    result = validate.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Validation passed" in out
