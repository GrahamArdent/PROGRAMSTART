from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import (
    _ensure_scripts_importable,
    _use_color,
    clr_bold,
    clr_cyan,
    clr_dim,
    clr_green,
    clr_red,
    clr_yellow,
    collect_registry_integrity_files,
    create_default_workflow_state,
    detect_workspace_root,
    display_workspace_path,
    extract_numbered_items,
    generated_outputs_root,
    git_changed_files,
    has_required_metadata,
    load_registry,
    load_workflow_state,
    metadata_prefixes,
    metadata_value,
    parse_markdown_table,
    save_workflow_state,
    status_color,
    to_posix,
    validate_state_against_schema,
    warn_direct_script_invocation,
    workflow_active_step,
    workflow_entry_key,
    workflow_step_files,
    workflow_steps,
    write_json,
)


def test_parse_markdown_table_extracts_rows() -> None:
    text = """
## Example

| Name | Value |
|---|---|
| alpha | one |
| beta | two |
"""
    rows = parse_markdown_table(text, "Example")
    assert rows == [{"Name": "alpha", "Value": "one"}, {"Name": "beta", "Value": "two"}]


def test_extract_numbered_items_reads_section() -> None:
    text = """
## Remaining Operational And Legal Decisions
1. First item
2. Second item

## Another Section
1. Ignored item
"""
    assert extract_numbered_items(text, "Remaining Operational And Legal Decisions") == [
        "First item",
        "Second item",
    ]


def test_create_default_workflow_state_sets_active_step() -> None:
    registry = load_registry()
    state = create_default_workflow_state(registry, "programbuild")
    assert state["system"] == "programbuild"
    assert state["active_stage"] == "inputs_and_mode_selection"
    assert state["stages"]["inputs_and_mode_selection"]["status"] == "in_progress"


def test_has_required_metadata_flags_missing_prefixes() -> None:
    registry = load_registry()
    prefixes = metadata_prefixes(registry)
    text = """
Purpose: Example
Owner: [ASSIGN]
Last updated: 2026-03-27
"""
    missing = has_required_metadata(text, prefixes)
    assert "Depends on:" in missing
    assert "Authority:" in missing


def test_create_default_workflow_state_userjourney_has_no_variant() -> None:
    registry = load_registry()
    state = create_default_workflow_state(registry, "userjourney")
    assert state["system"] == "userjourney"
    assert state["active_phase"] == "phase_0"
    assert "variant" not in state


def test_git_changed_files_returns_list() -> None:
    changed = git_changed_files()
    assert isinstance(changed, list)


def test_terminal_color_helpers(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert _use_color()
    assert "\u001b[33m" in clr_yellow("warn")
    assert "\u001b[31m" in clr_red("stop")
    assert "\u001b[1m" in clr_bold("bold")
    assert "\u001b[2m" in clr_dim("dim")
    assert "completed" in status_color("completed")
    assert "in_progress" in status_color("in_progress")
    assert "blocked" in status_color("blocked")
    assert "planned" in status_color("planned")


def test_terminal_color_helpers_disable_color(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert not _use_color()
    assert clr_yellow("warn") == "warn"


def test_color_helpers_non_tty_disables_color(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    assert not _use_color()
    assert clr_green("ok") == "ok"
    assert clr_cyan("info") == "info"
    assert clr_red("err") == "err"
    assert clr_bold("b") == "b"
    assert clr_dim("d") == "d"


def test_color_helpers_all_codes_with_color(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert "\u001b[32m" in clr_green("pass")
    assert "\u001b[36m" in clr_cyan("note")
    assert clr_green("pass").endswith("\u001b[0m")
    assert clr_cyan("note").endswith("\u001b[0m")


def test_status_color_returns_original_text(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    for status in ("completed", "in_progress", "blocked", "planned", "unknown"):
        result = status_color(status)
        assert status in result


def test_workflow_helpers_round_trip(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    state_path = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    monkeypatch.setattr("scripts.programstart_common.workflow_state_path", lambda _registry, _system: state_path)
    created = load_workflow_state(registry, "programbuild")
    assert created["active_stage"] == "inputs_and_mode_selection"
    created["variant"] = "enterprise"
    save_workflow_state(registry, "programbuild", created)
    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert saved["variant"] == "enterprise"


def test_write_json_writes_expected_payload(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "state.json"
    write_json(target, {"alpha": 1, "beta": ["two"]})

    assert json.loads(target.read_text(encoding="utf-8")) == {"alpha": 1, "beta": ["two"]}


def test_workflow_metadata_helpers() -> None:
    registry = load_registry()
    assert workflow_entry_key("programbuild") == "stages"
    assert workflow_entry_key("userjourney") == "phases"
    assert workflow_steps(registry, "programbuild")
    assert workflow_step_files(registry, "programbuild", "inputs_and_mode_selection")
    state = create_default_workflow_state(registry, "programbuild")
    assert workflow_active_step(registry, "programbuild", state) == "inputs_and_mode_selection"


def test_metadata_value_stops_at_rule_break() -> None:
    text = "---\nPurpose: Example\n---\nOwner: Hidden\n"
    assert metadata_value(text, "Owner:") is None


def test_metadata_value_returns_none_when_prefix_never_appears() -> None:
    text = "Purpose: Example\nLast updated: 2026-03-27\n"
    assert metadata_value(text, "Owner:") is None


def test_parse_markdown_table_skips_malformed_rows() -> None:
    text = """
## Example

| Name | Value |
|---|---|
| alpha | one |
| malformed |
| beta | two |
"""
    rows = parse_markdown_table(text, "Example")
    assert rows == [{"Name": "alpha", "Value": "one"}, {"Name": "beta", "Value": "two"}]


def test_parse_markdown_table_returns_empty_when_section_has_no_table() -> None:
    assert parse_markdown_table("## Example\ntext only\n", "Example") == []


def test_git_changed_files_handles_oserror_and_deduplicates(monkeypatch) -> None:
    calls = iter(
        [
            OSError("git missing"),
            SimpleNamespace(returncode=0, stdout="README.md\nREADME.md\nPROGRAMBUILD\\FEASIBILITY.md\n"),
            SimpleNamespace(returncode=0, stdout=""),  # ls-files --others
        ]
    )

    def fake_run(*_args, **_kwargs):
        result = next(calls)
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert git_changed_files() == ["README.md", "PROGRAMBUILD/FEASIBILITY.md"]


def test_collect_registry_integrity_files_uses_registry_scope(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_common.ROOT", tmp_path)
    (tmp_path / "README.md").write_text("root", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("docs", encoding="utf-8")
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD.md").write_text("pb", encoding="utf-8")
    (tmp_path / "USERJOURNEY").mkdir()
    (tmp_path / "USERJOURNEY" / "README.md").write_text("uj", encoding="utf-8")
    (tmp_path / "USERJOURNEY" / "USERJOURNEY_INTEGRITY_REFERENCE.json").write_text("{}", encoding="utf-8")
    (tmp_path / "BACKUPS" / "snapshot").mkdir(parents=True)
    (tmp_path / "BACKUPS" / "snapshot" / "PROGRAMBUILD.md").write_text("backup", encoding="utf-8")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "ignored.txt").write_text("ignored", encoding="utf-8")
    (tmp_path / "MANIFEST_2099-01-01.txt").write_text("ignored", encoding="utf-8")

    registry = {
        "workspace": {
            "root_readme": "README.md",
            "bootstrap_assets": ["docs/index.md"],
        },
        "systems": {
            "programbuild": {
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD.md"],
            },
            "userjourney": {
                "core_files": [
                    "USERJOURNEY/README.md",
                    "USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json",
                ],
            },
        },
        "integrity": {
            "manifest_collection": {
                "include_workspace_readme": True,
                "include_bootstrap_assets": True,
                "include_system_file_groups": ["control_files", "core_files"],
                "include_baseline_roots": True,
                "exclude_prefixes": [".venv"],
                "exclude_globs": ["MANIFEST_*.txt"],
            },
            "baselines": [
                {
                    "name": "snapshot",
                    "root": "BACKUPS/snapshot",
                },
                {
                    "name": "attachment",
                    "manifest": "USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json",
                },
            ],
        },
    }

    files = collect_registry_integrity_files(registry)

    assert {path.relative_to(tmp_path).as_posix() for path in files} == {
        "BACKUPS/snapshot/PROGRAMBUILD.md",
        "PROGRAMBUILD/PROGRAMBUILD.md",
        "README.md",
        "USERJOURNEY/README.md",
        "USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json",
        "docs/index.md",
    }


def test_to_posix_returns_relative_workspace_path() -> None:
    assert to_posix(ROOT / "README.md") == "README.md"


def test_generated_outputs_root_uses_registry_workspace_setting(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_common.ROOT", tmp_path)
    registry = {"workspace": {"generated_outputs_root": "artifacts"}}

    assert generated_outputs_root(registry) == tmp_path / "artifacts"


def test_display_workspace_path_falls_back_for_external_paths(tmp_path: Path) -> None:
    assert display_workspace_path(tmp_path / "outside.txt") == str(tmp_path / "outside.txt")


def test_detect_workspace_root_prefers_current_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    nested = workspace / "nested" / "child"
    (workspace / "config").mkdir(parents=True)
    (workspace / "config" / "process-registry.json").write_text("{}", encoding="utf-8")
    nested.mkdir(parents=True)

    assert detect_workspace_root(nested) == workspace


def test_detect_workspace_root_prefers_environment_override(tmp_path: Path, monkeypatch) -> None:
    workspace = tmp_path / "override-root"
    workspace.mkdir(parents=True)
    monkeypatch.setenv("PROGRAMSTART_ROOT", str(workspace))

    assert detect_workspace_root(ROOT) == workspace.resolve()


def test_detect_workspace_root_falls_back_to_package_root(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("PROGRAMSTART_ROOT", raising=False)

    assert detect_workspace_root(tmp_path) == ROOT


def test_warn_direct_script_invocation_emits_warning(monkeypatch, caplog) -> None:
    import logging

    monkeypatch.setattr(sys, "argv", ["scripts/programstart_validate.py", "--check", "all"])

    with caplog.at_level(logging.WARNING, logger="scripts.programstart_common"):
        warn_direct_script_invocation("'uv run programstart validate' or 'pb validate'")

    assert any("deprecated" in r.message for r in caplog.records)
    assert any("uv run programstart validate" in r.message for r in caplog.records)


def test_warn_direct_script_invocation_skips_console_script(monkeypatch, caplog) -> None:
    import logging

    monkeypatch.setattr(sys, "argv", ["programstart", "status"])

    with caplog.at_level(logging.WARNING, logger="scripts.programstart_common"):
        warn_direct_script_invocation("'uv run programstart status' or 'pb status'")

    assert not any("deprecated" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Phase A: coverage push — common.py uncovered branches
# ---------------------------------------------------------------------------


def test_ensure_scripts_importable_adds_path_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """_ensure_scripts_importable should insert scripts dir when it is not on sys.path."""
    scripts_dir = str(ROOT / "scripts")
    original_path = sys.path.copy()
    try:
        monkeypatch.setattr(sys, "path", [p for p in sys.path if p != scripts_dir])
        assert scripts_dir not in sys.path
        _ensure_scripts_importable()
        assert scripts_dir in sys.path
    finally:
        sys.path[:] = original_path


def test_write_json_retries_on_transient_permission_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """write_json should retry after a single PermissionError and succeed."""
    import time

    call_count = {"n": 0}
    original_replace = Path.replace

    def flaky_replace(self: Path, target: Path) -> None:  # type: ignore[return]
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise PermissionError("file locked")
        original_replace(self, target)

    monkeypatch.setattr(Path, "replace", flaky_replace)
    monkeypatch.setattr(time, "sleep", lambda _: None)
    dest = tmp_path / "out.json"
    write_json(dest, {"key": "value"})
    assert json.loads(dest.read_text()) == {"key": "value"}
    assert call_count["n"] == 2


def test_write_json_raises_after_all_retries_exhausted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """write_json should re-raise PermissionError after three failed attempts."""
    import time

    monkeypatch.setattr(Path, "replace", lambda self, target: (_ for _ in ()).throw(PermissionError("locked")))
    monkeypatch.setattr(time, "sleep", lambda _: None)
    with pytest.raises(PermissionError):
        write_json(tmp_path / "out.json", {"key": "value"})


def test_validate_state_against_schema_unknown_system_is_noop() -> None:
    """Unknown system name should return early without raising."""
    validate_state_against_schema({"active_stage": "x", "stages": {}}, "unknown_system")
