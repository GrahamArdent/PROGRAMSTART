from __future__ import annotations

import json
from pathlib import Path

from scripts import (
    programstart_attach,
    programstart_impact,
    programstart_init,
    programstart_recommend,
    programstart_research_delta,
    programstart_workflow_state,
)
from scripts.programstart_common import load_registry
from scripts.programstart_validate import validate_bootstrap_assets

ROOT = Path(__file__).resolve().parents[1]


def test_validate_bootstrap_assets_passes_current_repo() -> None:
    assert validate_bootstrap_assets(load_registry()) == []


def test_recommend_cli_json_for_cli_tool(capsys) -> None:
    result = programstart_recommend.main(["--product-shape", "CLI tool", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert payload["product_shape"] == "cli tool"
    assert payload["variant"] in {"lite", "product", "enterprise"}
    assert "uv" in [name.lower() for name in payload["stack_names"]]


def test_impact_cli_returns_json(capsys) -> None:
    result = programstart_impact.main(["workflow", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "relations" in payload
    assert "decision_rules" in payload
    assert "comparisons" in payload


def test_research_cli_writes_delta_template(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "delta.md"
    result = programstart_research_delta.main(
        [
            "--track",
            "Python runtime and packaging",
            "--date",
            "2026-03-29",
            "--output",
            str(output_path),
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    assert "Wrote research delta template" in out
    text = output_path.read_text(encoding="utf-8")
    assert "# Research Delta - Python runtime and packaging" in text
    assert "Outcome: changed | unchanged | blocked pending evidence" in text


def test_attach_userjourney_copies_from_source(tmp_path: Path) -> None:
    destination = tmp_path / "repo"
    destination.mkdir()
    source = ROOT / "USERJOURNEY"

    programstart_attach.attach_userjourney(destination, source)

    assert (destination / "USERJOURNEY" / "README.md").exists()
    assert (destination / "USERJOURNEY" / "USERJOURNEY_STATE.json").exists()


def test_init_stamps_kickoff_packet_and_readme(tmp_path: Path) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmePlanner",
            "--product-shape",
            "CLI tool",
            "--one-line-description",
            "A planning CLI",
            "--owner",
            "Acme Owner",
        ]
    )
    assert result == 0
    kickoff_text = (destination / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md").read_text(encoding="utf-8")
    readme_text = (destination / "README.md").read_text(encoding="utf-8")
    assert "PROJECT_NAME: AcmePlanner" in kickoff_text
    assert "PRODUCT_SHAPE: CLI tool" in kickoff_text
    assert "# AcmePlanner" in readme_text
    assert "A planning CLI" in readme_text


def test_init_can_attach_userjourney(tmp_path: Path) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmeJourney",
            "--product-shape",
            "web app",
            "--attach-userjourney",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
        ]
    )
    assert result == 0
    assert (destination / "USERJOURNEY" / "README.md").exists()


def test_impact_cli_handles_programbuild_only_repo(tmp_path: Path, monkeypatch, capsys) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmePlanner",
            "--product-shape",
            "CLI tool",
        ]
    )

    assert result == 0
    capsys.readouterr()

    monkeypatch.chdir(destination)
    result = programstart_impact.main(["workflow", "--json"])

    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "relations" in payload


def test_advance_preflight_blocks_when_problems(capsys, monkeypatch) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.preflight_problems",
        lambda _registry, _system: ["metadata incomplete"],
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild"])

    result = programstart_workflow_state.main()
    out = capsys.readouterr().out
    assert result == 1
    assert "Advance preflight failed" in out


def test_advance_skip_preflight_allows_progress(capsys, monkeypatch) -> None:
    saved: dict[str, object] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _registry, _system: ["bad"])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state",
        lambda _registry, _system, value: saved.update(value),
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild", "--skip-preflight"])

    result = programstart_workflow_state.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Advanced programbuild" in out
    assert saved["active_stage"] == "feasibility"
