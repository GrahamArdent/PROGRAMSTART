from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.programstart_bootstrap import bootstrap_repository, write_project_agent_entry
from scripts.programstart_bootstrap_methodology import bootstrap_methodology_repository

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("project", "variant"),
    [("Small local tool", "lite"), ("Interactive stateful program", "product"), ("Async service", "enterprise")],
)
def test_real_lean_bootstrap_has_usable_project_orientation(tmp_path: Path, project: str, variant: str) -> None:
    """PT-FR-002-001: materialize, resolve authority and use real target control."""
    target = tmp_path / "project"
    bootstrap_methodology_repository(target, project_name=project, variant=variant)
    entry = (target / "AGENTS.md").read_text()
    assert json.dumps(project) in entry
    for ref in re.findall(r"PROGRAMBUILD/[A-Z_]+\.(?:md|json)", entry):
        assert (target / ref).is_file(), ref
    assert "programstart target --repo . status" in entry
    assert "application run/test commands are not selected" in entry
    assert not any((target / x).exists() for x in ["scripts", "tests", "dashboard", "USERJOURNEY", "pyproject.toml"])
    manifest = json.loads((target / ".programstart-manifest.json").read_text())
    assert re.fullmatch(r"[a-f0-9]{40}", manifest["source_commit"])
    assert manifest["source_commit"] in entry
    assert "AGENTS.md" not in manifest["files"]  # project-owned, not template-managed
    for command in [["status"], ["guide", "--system", "programbuild"]]:
        result = subprocess.run(
            [sys.executable, "-m", "scripts.programstart_cli", "target", "--repo", str(target), *command],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr + result.stdout
        assert "inputs_and_mode_selection" in result.stdout
    protocol = (target / "PROGRAMBUILD/PROGRAMBUILD_IDEA_INTAKE.md").read_text()
    assert "Outcome and information foundation" in protocol
    assert "Schema/field presence checks cannot answer" in protocol
    assert "model suggestion is not a fact" in protocol
    with pytest.raises(FileExistsError):
        bootstrap_methodology_repository(target, project_name=project, variant=variant)
    before = (target / "AGENTS.md").read_bytes()
    write_project_agent_entry(target, project_name="another name", variant="lite", external_runtime=True, dry_run=False)
    assert (target / "AGENTS.md").read_bytes() == before


def test_full_bootstrap_uses_its_local_runtime_mode(tmp_path: Path) -> None:
    target = tmp_path / "full"
    bootstrap_repository(target, project_name="Full project", variant="lite")
    entry = (target / "AGENTS.md").read_text()
    assert "uv run programstart status" in entry
    assert "programstart target --repo ." not in entry
    assert (target / "scripts/programstart_cli.py").is_file()


@pytest.mark.parametrize("symlink", [False, True])
def test_local_agent_instructions_are_preserved(tmp_path: Path, symlink: bool) -> None:
    original = "# Accepted local rules\n"
    if symlink:
        owner = tmp_path / "owner.md"
        owner.write_text(original)
        (tmp_path / "AGENTS.md").symlink_to(owner)
    else:
        (tmp_path / "AGENTS.md").write_text(original)
    write_project_agent_entry(tmp_path, project_name="New", variant="product", external_runtime=True, dry_run=False)
    assert (tmp_path / "AGENTS.md").read_text() == original
    assert (tmp_path / "AGENTS.md").is_symlink() == symlink


def test_dry_run_and_unverified_source_are_honest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "new"
    write_project_agent_entry(target, project_name="New", variant="lite", external_runtime=True, dry_run=True)
    assert not target.exists()

    def missing_git(*args: object, **kwargs: object) -> str:
        raise FileNotFoundError("git")

    monkeypatch.setattr(subprocess, "run", missing_git)
    write_project_agent_entry(target, project_name="New", variant="lite", external_runtime=True, dry_run=False)
    assert "UNKNOWN (resolve before relying on template provenance)" in (target / "AGENTS.md").read_text()


def test_dirty_source_cannot_claim_exact_commit_provenance(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def source_state(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        value = "a" * 40 if "rev-parse" in command else " M scripts/programstart_bootstrap.py"
        return subprocess.CompletedProcess(command, 0, stdout=value)

    monkeypatch.setattr(subprocess, "run", source_state)
    write_project_agent_entry(tmp_path, project_name="New", variant="lite", external_runtime=True, dry_run=False)
    assert "HEAD alone does not identify these source bytes" in (tmp_path / "AGENTS.md").read_text()


@pytest.mark.parametrize("defect", ["none", "missing_source", "wrong_unit", "wrong_identity", "stale", "suggestion"])
def test_composed_information_fixture(tmp_path: Path, defect: str) -> None:
    """P3/P4/P11: real fresh processes; fixed oracle rejects broken information.

    This demonstrates a test contract only, not automatic product generation or
    semantic adequacy of PROGRAMSTART's future discovery outputs.
    """
    fixture = ROOT / "tests/fixtures/foundation"
    contract = json.loads((fixture / "expected.json").read_text())
    state = tmp_path / "record.json"

    def invoke(action: str, payload: dict | None = None) -> subprocess.CompletedProcess[str]:
        args = [sys.executable, str(fixture / "workflow.py"), action, str(state)]
        if payload is not None:
            args.append(json.dumps(payload))
        return subprocess.run(args, text=True, capture_output=True, check=False)

    assert invoke("import", contract["input"]).returncode == 0
    original = state.read_bytes()
    correction = contract["correction"].copy()
    if defect == "missing_source":
        correction.pop("source")
    elif defect == "wrong_unit":
        correction["unit"] = "boxes"
    elif defect == "wrong_identity":
        correction["id"] = "record-2"
    elif defect == "stale":
        correction["version"] = 1
    elif defect == "suggestion":
        correction["kind"] = "model_suggestion"
    result = invoke("correct", correction)
    if defect != "none":
        assert result.returncode != 0
        assert state.read_bytes() == original
        return
    assert result.returncode == 0
    assert invoke("correct", correction).returncode == 0  # repeat is same effect
    report = json.loads(invoke("report").stdout)
    assert report == contract["expected_report"]
    assert contract["input"] != contract["expected_report"]  # stale-output negative control
    # A broken handoff that consumes the original import cannot satisfy this oracle.
    with pytest.raises(AssertionError):
        assert contract["input"] == contract["expected_report"]
