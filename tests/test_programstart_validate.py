from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_bootstrap as bootstrap
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
    assert validate.validate_authority_sync(load_json(ROOT / "config" / "process-registry.json")) == []


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
    assert validate.validate_workflow_state(registry, "userjourney") == []


def test_bootstrap_programbuild_dry_run_and_main_refuses_non_empty(tmp_path: Path, monkeypatch, capsys) -> None:
    registry = load_json(ROOT / "config" / "process-registry.json")
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
    registry = load_json(ROOT / "config" / "process-registry.json")
    destination = tmp_path / "dest"
    bootstrap.bootstrap_programbuild(destination, registry, "enterprise", dry_run=False)
    state_path = destination / registry["workflow_state"]["programbuild"]["state_file"]
    state = load_json(state_path)
    assert state["variant"] == "enterprise"
